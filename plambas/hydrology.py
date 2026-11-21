"""Monthly climate methods used by SRCLET. All stored water depths are in millimetres."""
import math
import calendar
from datetime import date
from statistics import NormalDist, mean

from plambas.formulas import legacy_expression
from plambas.monthly_data import number, period_values


FAO = {
    "id": "fao56", "name": "FAO-56 Penman–Monteith", "unit": "mm/month", "output": "ET0",
    "parameters": {"wind_height": 2., "as": .25, "bs": .5},
    "version": 1, "source": "Allen et al. (1998), FAO-56, equations 6, 43, 46",
    "latex": (r"d\cdot\frac{0.408\cdot\mathrm{slope}\cdot(\mathrm{Rn}-G)"
              r"+\mathrm{gamma}\cdot\frac{900}{T+273}\cdot\mathrm{u2}\cdot(\mathrm{es}-\mathrm{ea})}"
              r"{\mathrm{slope}+\mathrm{gamma}\cdot(1+0.34\cdot\mathrm{u2})}"),
    "expression": legacy_expression(
        "d*(0.408*slope*(Rn-G)+gamma*900/(T+273)*u2*(es-ea))/(slope+gamma*(1+0.34*u2))"),
}
BALANCE = {
    "id": "mccabe2007", "name": "McCabe–Markstrom (2007)", "output": "Deficit", "unit": "mm/month",
    "version": 1, "source": "USGS OFR 2007-1088; Čadro (2019), §5.1.6",
    "inputs": ["Year", "Month", "ET0", "Tmean", "PRCP"], "latex": "Deficit = ET₀ − AET",
    "parameters": {"capacity": 100., "initial": 100., "direct": .076, "runoff": .75,
                   "snow_temp": -10., "rain_temp": 3.3, "melt": .5},
}
FREQUENCY = {
    "id": "weibull_normal", "name": "Weibull · normal", "unit": "mm/month",
    "version": 1, "source": "Čadro (2019), §5.1.2.3, §5.1.6, equation 32",
    "inputs": ["Year", "Month", "Deficit"], "latex": "P = r / (n + 1)",
    "parameters": {"month": 8, "years": 10},
}
PARAMETER_LABELS = {
    "wind_height": "Wind measurement height (m)", "as": "Ångström aₛ", "bs": "Ångström bₛ",
    "capacity": "Soil capacity (mm)", "initial": "Initial soil water (mm)",
    "direct": "Direct runoff fraction", "runoff": "Surplus runoff fraction",
    "snow_temp": "Snow temperature (°C)", "rain_temp": "Rain temperature (°C)",
    "melt": "Maximum melt fraction", "month": "Critical month", "years": "Return period (years)",
}


def scalar(row, key):
    return number(row.get(key), ",")


def mean_temperature(row):
    value = scalar(row, "Tmean")
    if value is None:
        hi, lo = scalar(row, "Tmax"), scalar(row, "Tmin")
        if hi is not None and lo is not None:
            value = (hi + lo) / 2
    return value


def vapour_pressure(t):
    return .6108 * math.exp(17.27 * t / (t + 237.3))


def radiation(y, m, lat, z, tmin, tmax, ea, rs, sunshine, p):
    if None in (lat, z, tmin, tmax, ea) or (rs is None and sunshine is None):
        return None
    if not -90 <= lat <= 90 or ea < 0:
        raise ValueError("Latitude / vapour pressure out of range.")
    j = date(y, m, 15).timetuple().tm_yday
    angle = 2 * math.pi * j / 365
    phi, decl = math.radians(lat), .409 * math.sin(angle - 1.39)
    sunset = math.acos(max(-1, min(1, -math.tan(phi) * math.tan(decl))))
    ra = (24 * 60 / math.pi) * .0820 * (1 + .033 * math.cos(angle)) * (
        sunset * math.sin(phi) * math.sin(decl) + math.cos(phi) * math.cos(decl) * math.sin(sunset))
    rso = (.75 + .00002 * z) * ra
    if rso <= 0 or sunset <= 0:
        return None
    if rs is None:
        day_length = 24 * sunset / math.pi
        if not 0 <= sunshine <= day_length + .1:
            raise ValueError("Sunshine hours outside daylight period.")
        rs = (p["as"] + p["bs"] * min(1, sunshine / day_length)) * ra
    ratio = min(1, rs / rso)
    longwave = (4.903e-9 * ((tmax + 273.16)**4 + (tmin + 273.16)**4) / 2
                * (.34 - .14 * math.sqrt(ea)) * (1.35 * ratio - .35))
    return .77 * rs - longwave


def fao_inputs(rows, meta, p=None):
    p = p or FAO["parameters"]
    if p["wind_height"] < .1 or not 0 <= p["as"] <= 1 or not 0 <= p["bs"] <= 1-p["as"]:
        raise ValueError("Invalid wind height or Ångström coefficients.")
    temperatures = {}
    for row in rows:
        y, m, _ = period_values(row)
        index = y * 12 + m
        if index in temperatures:
            raise ValueError(f"Duplicate month: {y}-{m:02}")
        temperatures[index] = mean_temperature(row)
    output = []
    for row in rows:
        y, m, days = period_values(row)
        index = y * 12 + m
        t = temperatures[index]
        tmax, tmin = scalar(row, "Tmax"), scalar(row, "Tmin")
        if tmin is not None and tmax is not None and tmin > tmax:
            raise ValueError(f"{y}-{m:02}: Tmin > Tmax")
        z = scalar(row, "z")
        if z is None:
            z = scalar(meta, "weather_station_elevation")
        lat = scalar(row, "Φ")
        if lat is None:
            lat = scalar(meta, "weather_station_latitude")
        es = ea = None
        if tmax is not None and tmin is not None:
            high, low = vapour_pressure(tmax), vapour_pressure(tmin)
            es = (high + low) / 2
            rhmax, rhmin, rh = (scalar(row, k) for k in ("RHmax", "RHmin", "RHmean"))
            if any(v is not None and not 0 <= v <= 100 for v in (rhmax, rhmin, rh)):
                raise ValueError(f"{y}-{m:02}: RH (0–100%)")
            if rhmax is not None and rhmin is not None:
                ea = (low * rhmax + high * rhmin) / 200
            elif rh is not None:
                ea = es * rh / 100
        if scalar(row, "ea") is not None:
            ea = scalar(row, "ea")
        elif scalar(row, "Tdew") is not None:
            ea = vapour_pressure(scalar(row, "Tdew"))
        rn = scalar(row, "Rn")
        if rn is None:
            rn = radiation(y, m, lat, z, tmin, tmax, ea, scalar(row, "Rs"), scalar(row, "n"), p)
        heat = scalar(row, "G")
        prev, nxt = temperatures.get(index - 1), temperatures.get(index + 1)
        if heat is None and prev is not None:
            if nxt is not None:
                heat = .07 * (nxt - prev)
            elif t is not None:
                heat = .14 * (t - prev)
        wind = scalar(row, "u2")
        if wind is None and scalar(row, "uz") is not None:
            wind = scalar(row, "uz") * 4.87 / math.log(67.8 * p["wind_height"] - 5.42)
        if wind is not None and wind < 0:
            raise ValueError(f"{y}-{m:02}: u2 < 0")
        if z is not None and not -500 <= z <= 9000:
            raise ValueError(f"{y}-{m:02}: elevation")
        gamma = None if z is None else .000665 * 101.3 * ((293 - .0065*z) / 293)**5.26
        output.append({**row, "Year": y, "Month": m, "d": days, "T": t,
                       "slope": None if t is None else 4098 * vapour_pressure(t) / (t+237.3)**2,
                       "gamma": gamma, "Rn": rn, "G": heat, "u2": wind,
                       "es": es, "ea": ea})
    return output


def balance_rows(rows, p):
    cap, soil = p["capacity"], p["initial"]
    tt, tr = p["snow_temp"], p["rain_temp"]
    if not (0 < cap and 0 <= soil <= cap and tt < tr and
            all(0 <= p[k] <= 1 for k in ("direct", "runoff", "melt"))):
        raise ValueError("Invalid soil, snow or runoff parameters.")
    snowpack = carry = 0.
    previous = None
    result = []
    for row in sorted(rows, key=lambda r: period_values(r)[:2]):
        y, m, _ = period_values(row)
        index = 12 * y + m
        if previous is not None and index != previous + 1:
            raise ValueError(f"{y}-{m:02}: consecutive months required.")
        previous = index
        t, rain_total, et = (scalar(row, k) for k in ("Tmean", "PRCP", "ET0"))
        if None in (t, rain_total, et) or min(rain_total, et) < 0:
            raise ValueError(f"{y}-{m:02}: Tmean, PRCP, ET0")
        rain_share = min(1., max(0., (t - tt) / (tr - tt)))
        rain = rain_total * rain_share
        snowpack += rain_total - rain
        melt = snowpack * rain_share * p["melt"]
        snowpack -= melt
        direct = rain * p["direct"]
        liquid = rain - direct + melt
        if liquid < et:
            draw = min(soil, (et - liquid) * soil / cap)
            aet = liquid + draw
            soil -= draw
            surplus = 0.
        else:
            aet = et
            total = soil + liquid - et
            soil = min(total, cap)
            surplus = max(0., total - cap)
        carry += surplus
        runoff = carry * p["runoff"]
        carry -= runoff
        result.append({"year": y, "month": m, "inputs": {"Tmean": t, "PRCP": rain_total, "ET0": et},
                       "value": et-aet, "missing": [], "outputs": {"AET": aet, "ST": soil, "PACK": snowpack,
                       "MELT": melt, "SURPLUS": surplus, "DRO": direct, "RO": direct + runoff, "CARRY": carry}})
    return result


def frequency_rows(rows, p):
    month, period = p["month"], p["years"]
    if month not in range(1, 13) or period < 2:
        raise ValueError("Invalid month or return period.")
    series = {}
    for row in rows:
        year, m, _ = period_values(row)
        if m != month:
            continue
        value = scalar(row, "Deficit")
        if value is None:
            continue
        if year in series or value < 0:
            raise ValueError(f"{year}-{m:02}: duplicate or negative deficit.")
        series[year] = value
    if len(series) < period:
        raise ValueError(f"{len(series)} / {int(period)} years")
    normal = NormalDist()
    positive = sorted(x for x in series.values() if x > 0)
    target = 1 - 1 / period
    zero_share = 1 - len(positive) / len(series)
    # Fit a normal quantile line to the nonzero observations at Weibull positions.
    if target <= zero_share or not positive:
        estimate = 0.
    elif positive[0] == positive[-1]:
        estimate = positive[0]
    else:
        scores = [normal.inv_cdf(rank/(len(positive)+1)) for rank in range(1, len(positive)+1)]
        centre = mean(positive)
        slope = sum(z*(x-centre) for z, x in zip(scores, positive)) / sum(z*z for z in scores)
        estimate = max(0., centre + slope * normal.inv_cdf((target-zero_share)/(1-zero_share)))
    lengths = (28, 29) if month == 2 else (calendar.monthrange(2001, int(month))[1],)
    hydromodule = {f"q24 ({days} d, L/s/ha)": 10000 * estimate / (86400 * days) for days in lengths}
    return [{"year": None, "month": int(month), "outputs": hydromodule, "inputs": {"n": len(series), "period": period},
             "value": estimate, "missing": [], "series": sorted(series.items())}]

