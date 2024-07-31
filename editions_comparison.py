import streamlit as st
import pandas as pd
import altair as alt

st.title("Medals Count Evolution through the Years")

country_colors = [
    "#3a87f2",
    "#050396", "#f00a0a", "#fac8c8", "#32d426", "#9733a6",
    "#FFDD44", "#FF69B4", "#00CED1", "#FFD700", "#8A2BE2",
    "#7FFF00", "#DC143C", "#FF8C00", "#ADFF2F" 
]

years = range(2000, 2021, 4)

complete_df = pd.DataFrame()

for year in years:
    df = pd.read_csv("medals" + str(year) + ".csv")
    df['Year'] = year
    complete_df = pd.concat([complete_df, df])

all_countries = complete_df['Country'].unique()
# sort by year and rank
default = all_countries[:5]

countries = st.multiselect(
    "Pick 2 to 10 countries to compare",
    all_countries.tolist(),
    default.tolist(),
    max_selections=10
)

df_countries = complete_df[complete_df['Country'].isin(countries)]
country_codes = df_countries['Country Code'].unique()
all_combinations = pd.MultiIndex.from_product([years, country_codes], names=['Year', 'Country Code']).to_frame(index=False)

df_total = df_countries[['Year', 'Country Code', 'Total']]
# ...

df_total = pd.merge(all_combinations, df_total, on=['Year', 'Country Code'], how='left')
df_total['Total'] = df_total['Total'].fillna(0)

chart_colors = alt.Scale(domain=df_total['Country Code'].unique(), range=country_colors[1:len(countries)+1])

line = alt.Chart(df_total).mark_line().encode(
    x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Total', title='Total Medals'),
    color=alt.Color('Country Code:N', scale=chart_colors, legend=alt.Legend(title='Country'))
).properties(
    width=800,
    height=400,
    title='Total Medals Over Years by Country'
)

points = alt.Chart(df_total).mark_point().encode(
    x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Total', title='Total Medals'),
    color='Country Code'
)

chart = line + points

st.altair_chart(chart)
