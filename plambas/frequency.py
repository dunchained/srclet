import calendar
import math
from statistics import mean
from plambas.formulas import walk
from plambas.monthly_data import number, period_values

DISTRIBUTIONS = {
    "normal": "Normal",
    "lognormal": "Log-normal",
    "weibull": "Weibull",
    "gamma": "Gamma",
    "gumbel": "Gumbel",
    "exponential": "Exponential",
}


def frequency_result(method, rows):
    from scipy import optimize, stats
    import numpy as np

    p = method["parameters"]
    m, years = int(p["month"]), p["years"]
    field = method.get("series", "Deficit")
    if not 1 <= m <= 12 or years < 2:
        raise ValueError("Invalid month or return period.")
    samples = {}
    for row in rows:
        y, month, _ = period_values(row)
        x = number(row.get(field), ",")
        if month == m and x is not None:
            if y in samples:
                raise ValueError("Duplicate month.")
            samples[y] = x
    if len(samples) < years:
        raise ValueError(f"{len(samples)} / {years:g} " + "years")
    values = sorted(samples.values(), reverse=True)
    dist = method.get("distribution", "normal")
    signed = values[-1] < 0
    if signed and dist not in ("normal", "gumbel"):
        raise ValueError("This distribution requires non-negative data.")
    data = values if signed else [v for v in values if v > 0]
    n = len(data)
    prob = lambda r, total: walk(method["expression"], {"r": r, "n": total})
    ranks = [[v, float(prob(i, len(values)))] for i, v in enumerate(values, 1)]
    if any(not 0 <= q <= 1 for _, q in ranks):
        raise ValueError("Invalid probability.")
    zero = 1 - n / len(values)
    target = 1 - 1 / years
    fit_error = 0.0
    if not data or target <= zero:
        estimate = 0.0
    elif data[0] == data[-1]:
        estimate = data[0]
    else:
        target = (target - zero) / (1 - zero)
        pairs = [
            (x, 1 - prob(i, n)) for i, x in enumerate(data, 1) if 0 < prob(i, n) < 1
        ]
        if len(pairs) < 2:
            raise ValueError("Too few interior plotting positions.")
        x, probs = map(np.asarray, zip(*pairs))
        if dist in ("normal", "gumbel", "lognormal"):
            rv = stats.gumbel_r if dist == "gumbel" else stats.norm
            z = rv.ppf(probs)
            observed = np.log(x) if dist == "lognormal" else x
            slope, intercept = np.polyfit(z, observed, 1)
            fitted = intercept + slope * z
            estimate = intercept + slope * rv.ppf(target)
            if dist == "lognormal":
                estimate, fitted = np.exp(estimate), np.exp(fitted)
        elif dist == "exponential":
            z = stats.expon.ppf(probs)
            scale = (z @ x) / (z @ z)
            estimate, fitted = scale * stats.expon.ppf(target), scale * z
        else:
            rv = {"weibull": stats.weibull_min, "gamma": stats.gamma}[dist]

            def residual(theta):
                shape, scale = np.exp(theta)
                return scale * rv.ppf(probs, shape) - x

            fitted_params = optimize.least_squares(
                residual, [0, math.log(mean(data))], bounds=([-7, -50], [9, 50])
            )
            shape, scale = np.exp(fitted_params.x)
            fitted = scale * rv.ppf(probs, shape)
            estimate = scale * rv.ppf(target, shape)
        fit_error = float(np.sqrt(np.mean((x - fitted) ** 2)))
    if not math.isfinite(estimate):
        raise ValueError("Non-finite result.")
    estimate = float(estimate if signed else max(0, estimate))
    extra = {"RMSE": fit_error}
    if field == "Deficit":
        for days in (28, 29) if m == 2 else (calendar.monthrange(2001, m)[1],):
            extra[f"q24 ({days} d, L/s/ha)"] = 10000 * estimate / (86400 * days)
    return [
        {
            "year": None,
            "month": m,
            "value": estimate,
            "missing": [],
            "inputs": {"n": len(values), "period": years},
            "outputs": extra,
            "series": sorted(samples.items()),
            "plotting_positions": ranks,
        }
    ]
