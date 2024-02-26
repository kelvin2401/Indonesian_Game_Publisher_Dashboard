import streamlit as st
import pandas as pd
import altair as alt
import geopandas as gpd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')

df = pd.read_pickle('steam_games.pkl')

st.title("Indonesian Game Publisher Analysis")

st.markdown("On January 26, 2024, detikcom, among other news outlets, published a news article about how Indonesia's Ministry of Communication and Information Technology or Kominfo will be blocking video games that are not published by an Indonesian legal body. Kris Antoni, who is the founder of Toge Productions, an Indonesian game developer and publisher company, has tweeted that this regulation is prone to corruption and abuse as well as hinder the Indonesain video game industry. This data dashboard aims to explore the implications of this regulation.")

mx_games, mx_developers, mx_publishers = st.columns(3)

with mx_games:
    st.metric("Indonesian Steam Games", value=df['title'].nunique())

with mx_developers:
    st.metric("Indonesian Developers", value=df['developer'].nunique())

with mx_publishers:
    st.metric("Indonesian and Global Publishers", value=df['publisher'].nunique())

    
st.header("Number of Games by Publisher Category and Developer")

st.markdown("Information about Indonesian video games from a popular gaming platform, Steam, are collected, mostly by getting a list of Indonesian game developers from the Indonesian Games Association (AGI) website. Publishers are then categorized into whether they are an Indonesian company or not and whether the Indonesian company is a legal entity or not. A legal entity here means that the company is a Limited Liability Company or PT in Indonesian. From 46 Steam games, 17 of them or 37% would be blocked by Kominfo if they are not republished by an Indonesian legal entity in 2024. These are Indonesian games that are developed by Indonesian game developers.")

games_count = df['category'].value_counts().reset_index()
games_count.columns = ['category', 'number_of_games']
games_count_dev = df['developer'].value_counts().reset_index()
games_count_dev.columns = ['developer', 'number_of_games']

chart1 = alt.Chart(games_count).mark_bar().encode(
    y=alt.Y('category', axis=alt.Axis(labelLimit=200), title='Category'),
    x='number_of_games',
    color=alt.Color('category', legend=None),
    tooltip=['category', 'number_of_games']
).properties(
    title='Number of Games by Publisher Category',
    height=298
)

chart2 = alt.Chart(games_count_dev).mark_bar().encode(
    y=alt.Y('developer', axis=alt.Axis(labelLimit=200), title='Developer'),
    x='number_of_games',
    color=alt.Color('developer', legend=None),
    tooltip=['developer', 'number_of_games']
).properties(
    title='Number of Games by Developer'
)

combined_chart = (chart1 | chart2).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_legend(
    title=None,
    labelFontSize=12
)

st.altair_chart(combined_chart, use_container_width=True)

option = st.selectbox(
    'Filter by:',
    ('Developer', 'Publisher')
)

filter_text = st.text_input(f'Enter {option} name:')

df2 = df[['title','developer','publisher']]
df2.rename(columns = {'title':'Title', 'developer':'Developer', 'publisher':'Publisher'}, inplace = True)

if option == 'Developer':
    filtered_df = df2[df2['Developer'].str.contains(filter_text, case=False)]
elif option == 'Publisher':
    filtered_df = df2[df2['Publisher'].str.contains(filter_text, case=False)]

st.dataframe(filtered_df, use_container_width=True, column_config={"_index": None})

st.markdown("In addition, video game publishing regulations from countries all over the world are explored and visualized in a map. This shows that only China and Indonesia require publishers to do extra steps in order to have their games for all ages published. On the other hand, South Korea and countries in the European Union require publishers to have a license to publish video games that contain mature elements.")

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

world = world[world['name'] != 'Antarctica']

eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
                'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
                'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands',
                'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']

countries_orange = world[world.name.isin(eu_countries) | (world.name == 'South Korea')]

countries_red = world[(world.name == 'Indonesia') | (world.name == 'China')]

fig, ax = plt.subplots(figsize=(8, 6))

world.plot(ax=ax, color='#555555')

countries_orange.plot(ax=ax, color='orange', edgecolor='black', label='Countries that require license for mature games')

countries_red.plot(ax=ax, color='red', edgecolor='black', label='Countries that require license for all games')

ax.set_title('Map of Countries with Video Game Publishing Regulations', color='white')  
ax.axis('off')

orange_legend = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=5, label='Countries that require license for mature games')
red_legend = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=5, label='Countries that require license for all games')

ax.legend(handles=[orange_legend, red_legend], loc='lower left', fontsize=8, facecolor='black', edgecolor='white', labelcolor='white')

fig.patch.set_facecolor('black')

st.pyplot(fig, use_container_width=False)

st.markdown("The action taken by Kominfo shows that the government wants more control over the gaming industry. However, this decision has made people worry about how it might affect creativity, new ideas, and the overall growth of the gaming sector in Indonesia. The discussion about this rule will probably keep going as people involved look at how it affects things and push for changes to make sure the gaming world in Indonesia can grow well and include everyone.")
