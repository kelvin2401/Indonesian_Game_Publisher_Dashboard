import streamlit as st
import pandas as pd
import altair as alt
import geopandas as gpd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')

df = pd.read_pickle('steam_games.pkl')

# Streamlit App
st.title("Indonesian Game Publisher Analysis")

st.markdown("On January 26, 2024, detikcom, among other news outlets, published a news article about how Indonesia's Ministry of Communication and Information Technology or Kominfo will be blocking video games that are not published by an Indonesian legal body. Kris Antoni, who is the founder of Toge Productions, an Indonesian game developer and publisher company, has tweeted that this regulation is prone to corruption and abuse as well as hinder the Indonesain video game industry. This data dashboard aims to explore the implications of this regulation.")

mx_games, mx_developers, mx_publishers = st.columns(3)

#st.dataframe(df)

with mx_games:
    st.metric("Indonesian Steam Games", value=df['title'].nunique())

with mx_developers:
    st.metric("Indonesian Developers", value=df['developer'].nunique())

with mx_publishers:
    st.metric("Indonesian and Global Publishers", value=df['publisher'].nunique())

    
st.header("Number of Games by Publisher Category and Developer")

st.markdown("Information about Indonesian video games from a popular gaming platform, Steam, are collected, mostly by getting a list of Indonesian game developers from the Indonesian Games Association (AGI) website. Publishers are then categorized into whether they are an Indonesian company or not and whether the Indonesian company is a legal entity, the company is a Limited Liability Company or PT in Indonesian, or not. From 46 Steam games, 17 of them or 37% would be blocked by Kominfo if they are not republished by an Indonesian legal entity in 2024. These are Indonesian games that are developed by Indonesian game developers.")

# Group by the 'category' column and count the number of games in each category
games_count = df['category'].value_counts().reset_index()
games_count.columns = ['category', 'number_of_games']
games_count_dev = df['developer'].value_counts().reset_index()
games_count_dev.columns = ['developer', 'number_of_games']

# Create chart 1
chart1 = alt.Chart(games_count).mark_bar().encode(
    y=alt.Y('category', axis=alt.Axis(labelLimit=200), title='Category'),
    x='number_of_games',
    color=alt.Color('category', legend=None),
    tooltip=['category', 'number_of_games']
).properties(
    title='Number of Games by Publisher Category',
    height=298
)

# Create chart 2
chart2 = alt.Chart(games_count_dev).mark_bar().encode(
    y=alt.Y('developer', axis=alt.Axis(labelLimit=200), title='Developer'),
    x='number_of_games',
    color=alt.Color('developer', legend=None),
    tooltip=['developer', 'number_of_games']
).properties(
    title='Number of Games by Developer'
)

# Combine the charts and apply configuration settings
combined_chart = (chart1 | chart2).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_legend(
    title=None,
    labelFontSize=12
)

# Display the combined chart using Streamlit
st.altair_chart(combined_chart, use_container_width=True)

# Load the world shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Remove Antarctica from the world GeoDataFrame
world = world[world['name'] != 'Antarctica']

# Define the list of EU countries
eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
                'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
                'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands',
                'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']

# Filter the world shapefile for EU countries
countries_orange = world[world.name.isin(eu_countries) | (world.name == 'South Korea')]

# Filter for Indonesia and China
countries_red = world[(world.name == 'Indonesia') | (world.name == 'China')]

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the world map with a dark background
world.plot(ax=ax, color='#555555')

# Plot selected countries with orange color for mature game license requirement
countries_orange.plot(ax=ax, color='orange', edgecolor='black', label='Countries that require license for mature games')

# Plot selected countries with red color for license requirement for all games
countries_red.plot(ax=ax, color='red', edgecolor='black', label='Countries that require license for all games')

# Set title and turn off axis
ax.set_title('Map of Countries with Video Game Publishing Regulations', color='white')  # Set title color to white
ax.axis('off')

# Add legends
orange_legend = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=5, label='Countries that require license for mature games')
red_legend = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=5, label='Countries that require license for all games')

# Display legends with white text
ax.legend(handles=[orange_legend, red_legend], loc='lower left', fontsize=8, facecolor='black', edgecolor='white', labelcolor='white')

# Set figure face color to black for dark mode
fig.patch.set_facecolor('black')

# Display the plot in Streamlit
st.pyplot(fig, use_container_width=False)

st.markdown("In addition, video game publishing regulations from countries all over the world are explored and visualized in a map. This shows that only China and Indonesia require publishers to do extra steps in order to have their games for all ages published. On the other hand, South Korea and countries in the European Union require publishers to have a license to publish video games that contain mature elements.")