def generate_excel():
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Perhitungan')
        writer.sheets['Perhitungan'] = worksheet

        # Judul kolom
        worksheet.write('A1', 'Deskripsi')
        worksheet.write('B1', 'Nilai')

        # Data statis
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

        worksheet.write('A7', 'Kurs ke IDR')
        worksheet.write('B7', kurs_usd_to_idr)

        worksheet.write('A8', 'Total Biaya Kerja (IDR)')
        worksheet.write_formula('B8', '=B6*B7')

        worksheet.write('A9', 'Tiket Pesawat (IDR)')
        worksheet.write('B9', flight_cost)

        worksheet.write('A10', 'Hotel (IDR)')
        worksheet.write('B10', hotel_cost)

        worksheet.write('A11', 'Meal (IDR)')
        worksheet.write('B11', meal_cost)

        worksheet.write('A12', 'Total Biaya (IDR)')
        worksheet.write_formula('B12', '=B8+B9+B10+B11')

        worksheet.write('A13', 'Margin (%)')
        worksheet.write('B13', margin_percent / 100)

        worksheet.write('A14', 'Final Price (IDR)')
        worksheet.write_formula('B14', '=B12*(1+B13)')

        worksheet.write('A15', 'Gross Margin (%)')
        worksheet.write_formula('B15', '=(B14-B12)/B14')

        # Format persentase dan ribuan
        percent_fmt = workbook.add_format({'num_format': '0.00%'})
        rupiah_fmt = workbook.add_format({'num_format': '#,##0'})

        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 20, rupiah_fmt)
        worksheet.set_row(14, None, percent_fmt)
        worksheet.set_row(12, None, percent_fmt)

    output.seek(0)
    return output.getvalue()
