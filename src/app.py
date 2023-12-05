# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
#st.balloons()

# Page configuration (optional)
# st.set_page_config(page_title="TITLE TITLE TILE", # page title, displayed on the window/tab bar
#                    page_icon="apple", # favicon: icon that shows on the window/tab bar 
#                    layout="wide", # use full width of the page
#                    menu_items={
#                        'About': "WRITE WHAT YOUR PAGE IS ABOUT"
#                    })

# Data loading
@st.cache_data
def load_csv(path):
    df = pd.read_csv(path)
    return df

@st.cache_data
def load_json(path):
    with open(path) as response:
        json_object = json.load(response)
        return json_object

# Data from: https://data.open-power-system-data.org/renewable_power_plants/
df_raw = load_csv(path="./data/raw/renewable_power_plants_CH.csv")
df = deepcopy(df_raw)

# Coordinates of the Cantons from: https://data.opendatasoft.com/explore/dataset/georef-switzerland-kanton%40public/export/?disjunctive.kan_code&disjunctive.kan_name&sort=year&location=8,46.82242,8.22403&basemap=jawg.streets&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6Imdlb3JlZi1zd2l0emVybGFuZC1rYW50b25AcHVibGljIiwib3B0aW9ucyI6eyJkaXNqdW5jdGl2ZS5rYW5fY29kZSI6dHJ1ZSwiZGlzanVuY3RpdmUua2FuX25hbWUiOnRydWUsInNvcnQiOiJ5ZWFyIn19LCJjaGFydHMiOlt7ImFsaWduTW9udGgiOnRydWUsInR5cGUiOiJsaW5lIiwiZnVuYyI6IkNPVU5UIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzE0MkU3QiJ9XSwieEF4aXMiOiJ5ZWFyIiwibWF4cG9pbnRzIjoiIiwidGltZXNjYWxlIjoieWVhciIsInNvcnQiOiIifV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9
cantons_raw = load_json("./data/raw/georef-switzerland-kanton.geojson")
cantons = deepcopy(cantons_raw)

# Match the canton code from the df with the canton name in the json
cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais', 
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich', 
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève', 
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz', 
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}
df["canton_name"] = df["canton"].map(cantons_dict)

# Count number of a specific energy source per canton
def number_energy_source_per_cantoon(df, energy_source):
    energy_sources_level_1 = list(df.energy_source_level_1.unique())
    energy_sources_level_2 = list(df.energy_source_level_2.unique())
    energy_sources_level_3 = list(df.energy_source_level_3.dropna().unique())
    column = ""
    if energy_source in energy_sources_level_1:
        sources_per_canton = df[df["energy_source_level_1"]==energy_source].groupby("canton_name").size().reset_index(name="count")
    elif energy_source in energy_sources_level_2:
        sources_per_canton = df[df["energy_source_level_2"]==energy_source].groupby("canton_name").size().reset_index(name="count")
    elif energy_source in energy_sources_level_3:
        sources_per_canton = df[df["energy_source_level_3"]==energy_source].groupby("canton_name").size().reset_index(name="count")
    else:
        sources_per_canton = df.groupby("canton_name").size().reset_index(name="count")
    return sources_per_canton

# Plotting function
def color_cantons_by_data(data, label, title="Number of Clean Energy Sources per Canton"):
    fig = px.choropleth_mapbox(
        data, 
        color="count",
        geojson=cantons, 
        locations="canton_name", 
        featureidkey="properties.kan_name",
        center={"lat": 46.8, "lon": 8.3},
        mapbox_style="open-street-map", 
        zoom=6.3,
        opacity=0.8,
        width=900,
        height=500,
        labels={"canton_name":"Canton",
            "count":label},
        title=f"<b>{title}</b>",
        color_continuous_scale="Viridis",
    )
    fig.update_layout(margin={"r":0,"t":35,"l":0,"b":0},
                    font={"family":"Sans",
                        "color":"maroon"},
                    hoverlabel={"bgcolor":"white",
                                "font_color":"black", 
                                "font_size":12,
                                "font_family":"Sans"},
                    title={"font_size":20,
                            "xanchor":"left", "x":0.01,
                            "yanchor":"bottom", "y":0.95}
                    )
    return fig

# Add title and header
# Using html to make your title colorful 
# your can change the type of header, here it's h1/h2 and color: purple/green
st.markdown("<h1 style='text-align: center; color: purple;'>My First Dashboard with Streamlit</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: green;'>Renewable Power Plants in Switzerland Data Exploration</h2>", unsafe_allow_html=True)



# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=df)

# Widgets: selectbox
energy_sources_level_1 = list(df.energy_source_level_1.unique())
energy_sources_level_2 = list(df.energy_source_level_2.unique())
energy_sources_level_3 = list(df.energy_source_level_3.dropna().unique())
all_energy_sources = ["All"] + sorted(energy_sources_level_1 + energy_sources_level_2 + energy_sources_level_3)
energy_source = st.selectbox("Choose an energy source", all_energy_sources)

# Count number of the selected sources per canton
sources_per_canton = number_energy_source_per_cantoon(df, energy_source)

# Add a map plot
st.header("Maps")

# Choropleth mapbox using Plotly GO
st.subheader("Plotly Map")

plotly_map = color_cantons_by_data(
    data=sources_per_canton,
    label=f"Number of {energy_source} Sources"
)
st.plotly_chart(plotly_map)
