import individual_editions_stats as instats

df = instats.load_year('Sydney 2000')

instats.make_ranking(df)
instats.make_medals_bar_chart(df)
instats.make_medals_pie_chart(df)