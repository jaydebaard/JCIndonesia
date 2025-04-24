from io import BytesIO
import pandas as pd

# Simulasi semua nilai untuk preview kode generate_excel
total_days = 10
hours_per_day = 8
total_hours = total_days * hours_per_day
cost_per_hour = 16.69
total_cost_usd = total_hours * cost_per_hour
kurs_usd_to_idr = 16000
total_cost_idr = total_cost_usd * kurs_usd_to_idr
flight_cost = 1600000
hotel_cost = 3000000
meal_cost = 1000000
total_cost_with_extras = total_cost_idr + flight_cost + hotel_cost + meal_cost
margin_percent = 20.0
final_price_idr = total_cost_with_extras * (1 + margin_percent / 100)
gross_margin_percent = ((final_price_idr - total_cost_with_extras) / final_price_idr) * 100
currency = "IDR (Rupiah)"  # or "USD (Dollar)"

def generate_excel(currency: str):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Perhitungan')
        writer.sheets['Perhitungan'] = worksheet

        worksheet.write('A1', 'Deskripsi')
        worksheet.write('B1', 'Nilai')

        if currency == "USD (Dollar)":
            rate = kurs_usd_to_idr
            worksheet.write('A2', 'Total Hari Kerja')
            worksheet.write('B2', total_days)

            worksheet.write('A3', 'Jam Kerja per Hari')
            worksheet.write('B3', hours_per_day)

            worksheet.write('A4', 'Total Jam Kerja')
            worksheet.write_formula('B4', '=B2*B3')

            worksheet.write('A5', 'Biaya per Jam (USD)')
            worksheet.write('B5', cost_per_hour)

            worksheet.write('A6', 'Total Biaya Kerja (USD)')
            worksheet.write_formula('B6', '=B4*B5')

            worksheet.write('A7', 'Tiket Pesawat (USD)')
            worksheet.write('B7', flight_cost / rate)

            worksheet.write('A8', 'Hotel (USD)')
            worksheet.write('B8', hotel_cost / rate)

            worksheet.write('A9', 'Meal (USD)')
            worksheet.write('B9', meal_cost / rate)

            worksheet.write('A10', 'Total Biaya (USD)')
            worksheet.write_formula('B10', '=B6+B7+B8+B9')

            worksheet.write('A11', 'Margin (%)')
            worksheet.write('B11', margin_percent / 100)

            worksheet.write('A12', 'Final Price (USD)')
            worksheet.write_formula('B12', '=B10*(1+B11)')

            worksheet.write('A13', 'Gross Margin (%)')
            worksheet.write_formula('B13', '=(B12-B10)/B12')

            usd_fmt = workbook.add_format({'num_format': '$#,##0.00'})
            percent_fmt = workbook.add_format({'num_format': '0.00%'})
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 20, usd_fmt)
            worksheet.set_row(12, None, percent_fmt)
            worksheet.set_row(13, None, percent_fmt)

        else:
            worksheet.write('A2', 'Total Hari Kerja')
            worksheet.write('B2', total_days)

            worksheet.write('A3', 'Jam Kerja per Hari')
            worksheet.write('B3', hours_per_day)

            worksheet.write('A4', 'Total Jam Kerja')
            worksheet.write_formula('B4', '=B2*B3')

            worksheet.write('A5', 'Biaya per Jam (USD)')
            worksheet.write('B5', cost_per_hour)

            worksheet.write('A6', 'Kurs ke IDR')
            worksheet.write('B6', kurs_usd_to_idr)

            worksheet.write('A7', 'Total Biaya Kerja (IDR)')
            worksheet.write_formula('B7', '=B4*B5*B6')

            worksheet.write('A8', 'Tiket Pesawat (IDR)')
            worksheet.write('B8', flight_cost)

            worksheet.write('A9', 'Hotel (IDR)')
            worksheet.write('B9', hotel_cost)

            worksheet.write('A10', 'Meal (IDR)')
            worksheet.write('B10', meal_cost)

            worksheet.write('A11', 'Total Biaya (IDR)')
            worksheet.write_formula('B11', '=B7+B8+B9+B10')

            worksheet.write('A12', 'Margin (%)')
            worksheet.write('B12', margin_percent / 100)

            worksheet.write('A13', 'Final Price (IDR)')
            worksheet.write_formula('B13', '=B11*(1+B12)')

            worksheet.write('A14', 'Gross Margin (%)')
            worksheet.write_formula('B14', '=(B13-B11)/B13')

            idr_fmt = workbook.add_format({'num_format': '#,##0'})
            percent_fmt = workbook.add_format({'num_format': '0.00%'})
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 20, idr_fmt)
            worksheet.set_row(13, None, percent_fmt)
            worksheet.set_row(14, None, percent_fmt)

    output.seek(0)
    return output

excel_output = generate_excel(currency)
excel_output.getvalue()[:100]  # Show beginning bytes as preview
