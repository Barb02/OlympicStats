import streamlit as st
import pandas as pd
import altair as alt

st.title('Olympic Games Data Analysis')

st.header('Tokyo 2020')

df = pd.read_csv('medals.csv')

st.write('**Ranking**')
st.dataframe(df)

df_chart = df.drop(['Country', 'Rank', 'Total'], axis=1).head(5)
df_long = df_chart.melt(id_vars='Country Code', var_name='Medal', value_name='Count')

country_colors = alt.Scale(domain=df_long['Country Code'].unique(), range=['#050396', '#f00a0a', '#fac8c8', '#32d426', '#9733a6'])

chart = alt.Chart(df_long).mark_bar().encode(
    x=alt.X('Country Code:N', title=None, axis=None, sort=None),
    y=alt.Y('Count:Q', title='Number of Medals'),
    color=alt.Color('Country Code:N', scale=country_colors, legend=alt.Legend(title='Country', orient='left')),
    column=alt.Column('Medal:N', title=None, sort=['Gold', 'Silver', 'Bronze'])
).properties(
    title='Medal Counts by Country',
    width=200 
).configure_axis(
    labelAngle=0
)

st.altair_chart(chart)