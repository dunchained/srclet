import unittest

from plambas.hydrology import BALANCE, FAO, FREQUENCY
from plambas.monthly_results import calculate


class HydrologyTest(unittest.TestCase):
    def test_fao56_monthly_example_17_bangkok(self):
        rows = [{"Year": 2001, "Month": 3, "Tmean": 29.2},
                {"Year": 2001, "Month": 4, "Tmax": 34.8, "Tmin": 25.6, "n": 8.5, "ea": 2.85, "u2": 2.0}]
        record = calculate(FAO, rows, {"weather_station_elevation": 2, "weather_station_latitude": 13+44/60})
        april = record["rows"][1]
        self.assertAlmostEqual(april["inputs"]["Rn"], 14.33, delta=.02)
        self.assertAlmostEqual(april["inputs"]["G"], .14)
        self.assertAlmostEqual(april["value"]/30, 5.72, delta=.02)
        self.assertIsNone(record["rows"][0]["value"])

    def test_balance_mass_conservation_and_new_year(self):
        data = [(2023, 12, -12, 60, 5), (2024, 1, -1, 80, 10), (2024, 2, 8, 200, 25), (2024, 3, 12, 0, 80)]
        rows = [{"Year": y, "Month": m, "Tmean": t, "PRCP": p, "ET0": et} for y, m, t, p, et in data]
        result = calculate(BALANCE, rows)["rows"]
        storage = BALANCE["parameters"]["initial"]
        for row, rec in zip(rows, result):
            out = rec["outputs"]
            next_storage = out["ST"] + out["PACK"] + out["CARRY"]
            self.assertAlmostEqual(storage + row["PRCP"], next_storage + out["AET"] + out["RO"])
            self.assertAlmostEqual(rec["value"], row["ET0"] - out["AET"])
            storage = next_storage
        self.assertEqual(result[0]["outputs"]["PACK"], 60)
        self.assertGreater(result[1]["outputs"]["MELT"], 0.)
        with self.assertRaisesRegex(ValueError, "consecutive"):
            calculate(BALANCE, [rows[0], rows[2]])

    def test_frequency_constant_zero_and_record_length(self):
        rows = [{"Year": y, "Month": 8, "Deficit": 34.} for y in range(2000, 2010)]
        output = calculate(FREQUENCY, rows)["rows"][0]
        self.assertEqual(output["value"], 34)
        self.assertAlmostEqual(output["outputs"]["q24 (31 d, L/s/ha)"], .1269414576)
        with self.assertRaises(ValueError):
            calculate(FREQUENCY, rows[1:])
        for row in rows:
            row["Deficit"] = 0
        self.assertEqual(calculate(FREQUENCY, rows)["rows"][0]["value"], 0)

