from openpyxl.chart import LineChart, Reference, ScatterChart, Series
from openpyxl.styles import Font, PatternFill


def add_result_charts(book, result, tr):
    method = result["method"]
    rows = result["rows"]
    sheet = book.create_sheet(tr("Charts")[:31])
    name = tr(method["name"])
    unit = tr(method["unit"])
    monthly = any(r["year"] is not None for r in rows)
    if monthly:
        others = [
            key
            for key in ("AET", "RO", "ST", "PACK")
            if any(key in r.get("outputs", {}) for r in rows)
        ]
        sheet.append([tr("Month"), name, *others])
        for r in sorted(rows, key=lambda x: (x["year"], x["month"])):
            sheet.append(
                [
                    f"{r['year']:04}-{r['month']:02}",
                    r["value"],
                    *(r.get("outputs", {}).get(k) for k in others),
                ]
            )
        chart = LineChart()
        chart.title = name
        chart.y_axis.title = unit
        chart.x_axis.title = tr("Month")
        chart.add_data(
            Reference(
                sheet,
                min_col=2,
                max_col=2 + len(others),
                min_row=1,
                max_row=sheet.max_row,
            ),
            titles_from_data=True,
        )
        chart.set_categories(
            Reference(sheet, min_col=1, min_row=2, max_row=sheet.max_row)
        )
        for series in chart.series:
            series.marker.symbol = "circle"
            series.marker.size = 4
        if not others:
            chart.legend = None
    else:
        points = rows[0].get("plotting_positions", [])
        if not points:
            sheet.append([tr("Method"), tr("Result")])
            sheet.append([name, rows[0]["value"]])
            from openpyxl.chart import BarChart

            chart = BarChart()
            chart.add_data(
                Reference(sheet, min_col=2, min_row=1, max_row=2), titles_from_data=True
            )
            chart.set_categories(Reference(sheet, min_col=1, min_row=2, max_row=2))
        else:
            sheet.append(
                [
                    tr("Exceedance probability (%)"),
                    method.get("series", "Deficit") + " (" + unit + ")",
                ]
            )
            for value, probability in sorted(points, key=lambda pair: pair[1]):
                sheet.append([100 * probability, value])
            chart = ScatterChart()
            chart.x_axis.title = tr("Exceedance probability (%)")
            chart.y_axis.title = unit
            curve = Series(
                Reference(sheet, min_col=2, min_row=2, max_row=sheet.max_row),
                Reference(sheet, min_col=1, min_row=2, max_row=sheet.max_row),
                title=name,
            )
            curve.marker.symbol = "circle"
            curve.marker.size = 5
            chart.series.append(curve)
        chart.title = name
    chart.width = 23
    chart.height = 13
    chart.style = 13
    sheet.add_chart(chart, "H2")
    for ws in (book.active, sheet):
        ws.freeze_panes = "B2"
        ws.auto_filter.ref = ws.dimensions
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="274C60")
            ws.column_dimensions[cell.column_letter].width = min(
                45, max(14, len(str(cell.value)) + 2)
            )
        for row in ws.iter_rows():
            for cell in row:
                if cell.data_type == "f":
                    cell.data_type = "s"
