import streamlit as st
import pandas as pd
import altair as alt

st.title("Medal Count Evolution Through the Years")

country_colors = [
    "#3a87f2",
    "#050396", "#f00a0a", "#fac8c8", "#32d426", "#9733a6",
    "#FFDD44", "#FF69B4", "#00CED1", "#FFD700", "#8A2BE2",
    "#7FFF00", "#DC143C", "#FF8C00", "#ADFF2F" 
]

years = range(2000, 2025, 4)

complete_df = pd.DataFrame()

for year in years:
    df = pd.read_csv("data/medals" + str(year) + ".csv")
    df['Year'] = year
    complete_df = pd.concat([complete_df, df])

all_countries = complete_df.sort_values(by=['Year', 'Rank'], ascending=[False, True])['Country'].unique()
default = all_countries[:4]

countries = st.multiselect(
    "Pick 2 to 10 countries to compare",
    all_countries.tolist(),
    default.tolist(),
    max_selections=10
)

df_countries = complete_df[complete_df['Country'].isin(countries)]
country_codes = df_countries['Country Code'].unique()
all_combinations = pd.MultiIndex.from_product([years, country_codes], names=['Year', 'Country Code']).to_frame(index=False)
chart_colors = alt.Scale(domain=country_codes, range=country_colors[1:len(countries)+1])

df_rank = df_countries[['Year', 'Country Code', 'Rank']]

line = alt.Chart(df_rank).mark_line(interpolate='monotone').encode(
    x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Rank:Q', scale=alt.Scale(reverse=True, domainMin=1), axis=alt.Axis(tickCount=10, title='Rank')),
    color=alt.Color('Country Code:N', scale=chart_colors, legend=alt.Legend(title='Country'))
).properties(title='Country Rankings Over the Years', width=800, height=400)

points = alt.Chart(df_rank).mark_point().encode(
    x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Rank:Q', scale=alt.Scale(reverse=True)),
    color=alt.Color('Country Code:N', scale=chart_colors, legend=alt.Legend(title='Country'))
)

chart = line + points

st.altair_chart(chart)

st.write("**Note:** The graph above uses the gold medal count as the rank criterion, with the number of silver and bronze medals serving as tiebrakers, in this order. This is one of the most common ways of ranking countries, though it's not official. An interesting fact is how USA media normally uses total medal count as the ranking criterion, which results in their team being ranked first in the 2008 Beijing Olympics. This can be seen in the chart below:")
st.write("")
st.write("")

def make_line_chart(column_name):

    df = df_countries[['Year', 'Country Code', column_name]]
    df = pd.merge(all_combinations, df, on=['Year', 'Country Code'], how='left')
    df[column_name] = df[column_name].fillna(0)

    line = alt.Chart(df).mark_line().encode(
        x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y(column_name, title= column_name + ' Medals'),
        color=alt.Color('Country Code:N', scale=chart_colors, legend=alt.Legend(title='Country'))
    ).properties(
        width=800,
        height=400,
        title= column_name + ' Medals by Country Over the Years'
    )

    points = alt.Chart(df).mark_point().encode(
        x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y(column_name, title= column_name + ' Medals'),
        color='Country Code'
    )

    chart = line + points
    st.altair_chart(chart)


make_line_chart('Total')
make_line_chart('Gold')
make_line_chart('Silver')
make_line_chart('Bronze')


st.write("")
st.write("")
st.write("Looking at the total medal chart, an interesting analysis would be to check if there is a relationship between the rise in the number of medals and the country hosting the Games.")
st.write("These are the total medal counts for the edition each of these countries hosted and the corresponding previous edition:")

st.write("")
st.write("**Total Medal Count Before and on Hosting Year**")
st.write("")

st.write("🇬🇷 Greece")
col1 , col2 = st.columns(2)
col1.metric("Sydney 2000", "13 medals")
col2.metric("Athens 2004", "16 medals", f"{(16/13 - 1) * 100:.2f}" + "%")

st.write("🇨🇳 China")
col1, col2 = st.columns(2)
col1.metric("Athens 2004", "63 medals")
col2.metric("Beijing 2008", "100 medals", f"{(100/63 - 1) * 100:.2f}" + "%")

st.write("🇬🇧 Great Britain")
col1, col2 = st.columns(2)
col1.metric("Beijing 2008", "51 medals")
col2.metric("London 2012", "65 medals", f"{(65/51 - 1) * 100:.2f}" + "%")

st.write("🇧🇷 Brazil")
col1, col2 = st.columns(2)
col1.metric("London 2012", "17 medals")
col2.metric("Rio 2016", "19 medals", f"{(19/17 - 1) * 100:.2f}" + "%")

st.write("🇯🇵 Japan")
col1, col2 = st.columns(2)
col1.metric("Rio 2016", "41 medals")
col2.metric("Tokyo 2020 (2021)", "58 medals", f"{(58/41 - 1)*100:.2f}" + "%")

st.write("🇫🇷 France")
col1, col2 = st.columns(2)
col1.metric("Tokyo 2020 (2021)", "33 medals")
col2.metric("France 2024", "64 medals", f"{(64/33 - 1)*100:.2f}" + "%")

st.write("")
st.write("As it can be seen, in every edition the host country improved its total mdeal count, which is expected due to hometown support, athletes own will to win at home, increased investment on sports by the hosting country and potential favoritism given by the referees (unfortunately may happen!).")  
st.write("However, not all countries improved at the same rate. The largest increases were achieved by Japan, China and France, the last with an impressive number of ~94\% rise. Meanwhile, the smallest increases were seen in Greece and Brazil, with only 3 and 2 additional medals, respectively.") 
st.write("There are some factors that could explain these differences:")
st.write("* Number of athletes representing the country")
st.write("* Amount of monetary investment in sports")
st.write("* Level of importance given to the Olympic Games performance (e.g., political reasons, such as USA x USSR rivalry during the Cold War)")
st.write("* Amount of hometown attendance, and therefore, crowd support")
