import individual_editions_stats as instats

df = instats.load_year('London 2012')

instats.make_ranking(df)
instats.make_medals_bar_chart(df)
instats.make_medals_pie_chart(df)