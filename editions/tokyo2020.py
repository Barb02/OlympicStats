import individual_editions_stats as instats
import streamlit as st

df = instats.load_year('Tokyo 2020')

st.write("**Note:** Although the Tokyo games took place in 2021 due the Covid-19 pandemic, the name 'Tokyo 2020' was still adopted by the committee.")

instats.make_ranking(df)
instats.make_medals_bar_chart(df)
instats.make_medals_pie_chart(df)