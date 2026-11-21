#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
python_bin="${SRCLET_PYTHON:-python3}"
install_python() {
    if command -v apt-get >/dev/null; then sudo apt-get install -y python3 python3-venv
    elif command -v dnf >/dev/null; then sudo dnf install -y python3
    elif command -v pacman >/dev/null; then sudo pacman -S --needed python
    else echo "Install Python 3.10+ with venv support and run this launcher again." >&2; return 1
    fi
}
if ! command -v "$python_bin" >/dev/null; then install_python; fi
if [[ ! -x .venv/bin/python ]]; then
    "$python_bin" -m venv .venv || {
        install_python
        "$python_bin" -m venv .venv
    }
fi
py=.venv/bin/python
"$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else "Python 3.10+ required")'
"$py" -m pip install --disable-pip-version-check -r requirements.txt
# On minimal Linux desktops Qt wheels need the operating system's X11/EGL libraries.
if command -v ldd >/dev/null; then
    qt_dir=$("$py" -c 'from PyQt6.QtCore import QLibraryInfo as L; print(L.path(L.LibraryPath.PrefixPath))')
    missing=$(ldd "$qt_dir/plugins/platforms/libqxcb.so" "$qt_dir/libexec/QtWebEngineProcess" | awk '/not found/{print $1}' | sort -u)
    if [[ -n "$missing" ]]; then
        if command -v apt-get >/dev/null; then
            sudo apt-get install -y libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 libxcb-xinerama0 libxcb-image0 libxcb-render-util0 libxkbcommon-x11-0 libegl1 libgl1 libnss3 libxcomposite1 libxdamage1 libxrandr2 libgbm1
        elif command -v dnf >/dev/null; then
            sudo dnf install -y xcb-util-cursor xcb-util-wm xcb-util-keysyms xcb-util-image xcb-util-renderutil libxkbcommon-x11 mesa-libEGL libglvnd-glx nss libXcomposite libXdamage libXrandr mesa-libgbm
        elif command -v pacman >/dev/null; then
            sudo pacman -S --needed xcb-util-cursor xcb-util-wm xcb-util-keysyms xcb-util-image xcb-util-renderutil libxkbcommon-x11 mesa libglvnd nss libxcomposite libxdamage libxrandr
        else
            echo "Missing Qt system libraries: $missing" >&2
            exit 1
        fi
    fi
fi
exec "$py" srclet.py "$@"
