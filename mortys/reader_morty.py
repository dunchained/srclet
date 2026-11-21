from mortys.font_morty import read_input_font_size, read_menu_font_size, read_text_font_size
from mortys.language_morty import tr
from variables import var

FONT_SIZES = {"large": var.font_size_large, "medium": var.font_size_medium, "small": var.font_size_small}


def read_font_size_text():
    return [tr(key.capitalize()) for key in FONT_SIZES]


def read_font_size_key(font_size_text):
    return next(key for key in FONT_SIZES if tr(key.capitalize()) == font_size_text)


def load_json_data_and_check(font_size):
    return next((tr(key.capitalize()) for key, value in FONT_SIZES.items() if value == font_size),
                tr("Medium"))


def read_menu_font_size_current_text():
    return load_json_data_and_check(read_menu_font_size())


def read_text_font_size_current_text():
    return load_json_data_and_check(read_text_font_size())


def read_input_font_size_current_text():
    return load_json_data_and_check(read_input_font_size())
