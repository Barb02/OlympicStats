import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go


country_colors = [
    "#3a87f2",
    "#050396", "#f00a0a", "#fac8c8", "#32d426", "#9733a6",
    "#FFDD44", "#FF69B4", "#00CED1", "#FFD700", "#8A2BE2",
    "#7FFF00", "#DC143C", "#FF8C00", "#ADFF2F" 
]


def load_year(year):

    st.title('Olympic Games Data Through the Years')

    st.header(year)

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    return pd.read_csv('data/medals' + year[-4:] + '.csv')


def make_ranking(df):

    df = df.reset_index(drop=True)

    st.write('**Ranking**')
    st.dataframe(df, hide_index=True)

    st.write("")
    st.write("")
    st.write("")
    st.write("")


def make_medals_bar_chart(df):

    st.write('**Medal Counts by Country**')

    df_chart = df.drop(['Rank', 'Total'], axis=1)

    all_countries = df_chart['Country']
    default = all_countries.head(5)

    countries = st.multiselect(
        "Pick 2 to 10 countries to compare",
        all_countries.tolist(),
        default.tolist(),
        max_selections=10
    )

    df_chart = df_chart[df_chart['Country'].isin(countries)]

    df_chart.drop('Country', axis=1, inplace=True)
    df_long = df_chart.melt(id_vars='Country Code', var_name='Medal', value_name='Count')

    chart_colors = alt.Scale(domain=df_long['Country Code'].unique(), range=country_colors[1:len(countries)+1])

    chart = alt.Chart(df_long).mark_bar().encode(
        x=alt.X('Country Code:N', title=None, axis=None, sort=None),
        y=alt.Y('Count:Q', title='Number of Medals'),
        color=alt.Color('Country Code:N', scale=chart_colors, legend=alt.Legend(title='Country', orient='left')),
        column=alt.Column('Medal:N', title=None, sort=['Gold', 'Silver', 'Bronze'])
    ).properties(
        width=200 
    ).configure_axis(
        labelAngle=0
    )

    st.altair_chart(chart)

    st.write("")


def make_medals_pie_chart(df):

    df_pie = df.drop(['Country', 'Rank'], axis=1)

    total_sum = df_pie['Total'].sum()
    df_pie['Percentage'] = df_pie['Total'] / total_sum * 100

    df_pie['Country Code'] = df_pie.apply(lambda row: 'Other' if row['Percentage'] < 1.80 else row['Country Code'], axis=1)
    df_pie = df_pie.groupby('Country Code').sum().reset_index()
    df_pie = df_pie.sort_values(by='Total', ascending=False).reset_index(drop=True)

    fig = go.Figure(data=[go.Pie(labels=df_pie['Country Code'], values=df_pie['Total'], hole=0.3, marker=dict(colors=country_colors))])
    fig.update_layout(title_text='Medal Distribution', height=600)

    st.plotly_chart(fig, use_container_width=True)