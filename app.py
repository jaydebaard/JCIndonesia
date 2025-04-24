def generate_excel():
    df = pd.DataFrame({
        "Deskripsi": [
            "Total Hari Kerja",
            "Jam Kerja per Hari",
            "Total Jam Kerja",
            "Biaya per Jam (USD)",
            "Total Biaya Kerja (USD)",
            "Kurs ke IDR",
            "Total Biaya Kerja (IDR)",
            "Tiket Pesawat (IDR)",
            "Hotel (IDR)",
            "Meal (IDR)",
            "Total Biaya (IDR)",
            "Margin (%)",
            "Final Price (IDR)",
            "Gross Margin (%)"
        ],
        "Nilai": [
            total_days,
            hours_per_day,
            total_hours,
            cost_per_hour,
            total_cost_usd,
            kurs_usd_to_idr,
            total_cost_idr,
            flight_cost,
            hotel_cost,
            meal_cost,
            total_cost_with_extras,
            margin_percent,
            final_price_idr,
            gross_margin_percent
        ]
    })

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Perhitungan')
    output.seek(0)
    return output
