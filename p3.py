import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import folium
import plotly.figure_factory as ff
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static
import plotly.graph_objects as go
from PIL import Image

# Set page config to wide layout
st.set_page_config(page_title="Población de carros eléctricos en Washington", layout="wide", page_icon="https://cdn-icons-png.flaticon.com/512/1996/1996729.png")

col1, col2, col3 = st.columns(3)
col1.metric("Clean source", "70 %", "-30%")
col2.metric("Tesla population", "50%", "-5%")
col3.metric("King County", "50%", "2.4%")

bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA1L3BmLXMxMjQtYWstMjY4MV8yLmpwZw.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    color: black;
}
</style>
'''
st.markdown(bg_img, unsafe_allow_html=True)

image = Image.open('UK.png')

# Importing Google Fonts
st.markdown(
    """
    <link href='https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap' rel='stylesheet'>
    <style>
        .st-cc h1 {
            color: black;
            font-family: 'Roboto', sans-serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Mostrar el título in a more professional font
st.markdown('<h1 style="color: black; font-family: \'Buffalo\';">Población de carros eléctricos en Washington</h1>', unsafe_allow_html=True)


# Contenido del sidebar
selected2 = option_menu(None, ["Home", "Map", "KPIs", 'References'],
                        icons=['house', 'map', "chart-pie", 'book'],
                        menu_icon="cast", default_index=0, orientation="horizontal")
selected2

# Load data and perform preprocessing
#mapa
df = pd.read_csv('Electric_Vehicle_Population_Data.csv')
fips_df = pd.read_csv('FIP.csv')

df = df.dropna()
df.rename(columns={"Electric Vehicle Type": "elec", "Clean Alternative Fuel Vehicle (CAFV) Eligibility": "clean"}, inplace=True)
df.replace({'Plug-in Hybrid Electric Vehicle (PHEV)': 'PHEV', 'Battery Electric Vehicle (BEV)': 'BEV',
            'Clean Alternative Fuel Vehicle Eligible': 'Clean Alt Fuel', 'Eligibility unknown as battery range has not been researched': 'Unknown'
            , 'Not eligible due to low battery range': 'Not Clean'}, inplace=True)
county_counts = df['County'].value_counts().to_dict()
df['Count'] = df['County'].map(county_counts)
df3 = pd.merge(df,fips_df, on='County')

state_geo = requests.get("https://raw.githubusercontent.com/python-visualization/folium/master/tests/us-counties.json").json()
excel_url = "https://github.com/SVterry2023/al/raw/main/df3.xlsx"
state_data = pd.read_excel(excel_url, engine="openpyxl")

m = folium.Map(location=[0, 0], zoom_start=1)

#Frecuencias absolutas
tfa = pd.value_counts(df['clean'])
tt= pd.DataFrame(tfa)

#Tabla de frecuencias relativas
t = df['clean'].shape[0]
tfr = tfa/t
tf = pd.DataFrame(tfr)
tf['name'] = tf.index

#Frecuencias absolutas
tfm = pd.value_counts(df['Make'])
tm= pd.DataFrame(tfm)
#Tabla de frecuencias relativas
tm = df['Make'].shape[0]
tfrm = tfm/tm
tfm = pd.DataFrame(tfrm)
tfm['name'] = tfm.index
top_5_values = tfm.head(5)

#Frecuencias absolutas
tfz = pd.value_counts(df['County'])
tz= pd.DataFrame(tfz)
#Tabla de frecuencias relativas
tz = df['County'].shape[0]
tfrz = tfz/tz
tfz = pd.DataFrame(tfrz)
tfz['name'] = tfz.index
top_5 = tfz.head(5)



if selected2 == "Home":
  heading_text = '<h2 style="color: black;"> La situación actual</h2>'
  st.markdown(heading_text, unsafe_allow_html=True)
  st.markdown('<p style="font-family: \'Times New Roman\'; font-size: 18px; color: black;"> La producción de carros eléctricos ha aumentado, pero esto no necesariamente representa una mejora para el medio ambiente .</p>', unsafe_allow_html=True)
  st.image("UK.png")

  @st.cache_data
  def compute_Sankey_chart():
      # Extract unique values
      elec_values = df['elec'].unique()
      clean_values = df['clean'].unique()

      # Create a list of unique labels
      unique_labels = list(elec_values) + list(clean_values)

      # Map labels to indices
      label_indices = {label: idx for idx, label in enumerate(unique_labels)}

      node_colors = ["rgba(0, 128, 255, 0.8)", "rgba(0, 255, 0, 0.8)", "rgba(255, 0, 0, 0.8)", "rgba(169, 169, 169, 0.8)"]

      # Create Sankey diagram data
      source_indices = [label_indices[elec] for elec in df['elec']]
      target_indices = [label_indices[clean] for clean in df['clean']]

      link_values = [1] * len(df)

      # Create Sankey diagram
      fig = go.Figure(data=[go.Sankey(
          valueformat=".0f",
          valuesuffix="TWh",
          node=dict(
              pad=15,
              thickness=15,
              line=dict(color="black", width=0.5),
              label=unique_labels,
              color=node_colors
          ),
          link=dict(
              source=source_indices,
              target=target_indices,
              value=link_values,
              color="rgba(173, 216, 230, 0.5)"
          ))])
      fig.update_layout({
      'plot_bgcolor': 'rgba(0, 0, 0, 0)',
      'paper_bgcolor': 'rgba(0, 0, 0, 0)',
      'margin': dict(l=0, r=0, b=0, t=0, pad=0),
      'height': 500,  # Adjust the height as needed
      'width': 800,   # Adjust the width as needed
      })
      return fig

  fig4 = compute_Sankey_chart()
  heading_text11 = '<h3 style="color: black;"> Diagrama diluvial</h3>'
  st.markdown(heading_text11, unsafe_allow_html=True)
  st.plotly_chart(fig4, use_container_width=True)

if selected2== 'References':
  heading_text1 = '<h2 style="color: black;">Referencias</h2>'
  st.markdown(heading_text1, unsafe_allow_html=True)
  st.markdown('<p style="font-family: \'Times New Roman\'; font-size: 18px; color: black;"> Gupta, S. (2021). Electric Vehicle Population Data. Kaggle. https://www.kaggle.com/code/shubhamgupta012/electric-vehicle-population-data .</p>', unsafe_allow_html=True)
  st.markdown('<p style="font-family: \'Times New Roman\'; font-size: 18px; color: black;"> Tabuchi, H. (2021, March 2). Electric Vehicles Are Better for the Environment. The New York Times. https://www.nytimes.com/2021/03/02/climate/electric-vehicles-environment.html .</p>', unsafe_allow_html=True)


if selected2 == "Map":
  folium.Choropleth(
      geo_data=state_geo,
      name="choropleth",
      data=state_data,
      columns=["FIP", "Count"],
      key_on="feature.id",
      fill_color="YlGn",
      fill_opacity=0.7,
      line_opacity=0.2,
      legend_name="Cantidad de carros eléctricos",
  ).add_to(m)

  folium.LayerControl().add_to(m)
  heading_text2 = '<h2 style="color: black;"> Mapa de condados en Estados Unidos </h2>'
  st.markdown(heading_text2, unsafe_allow_html=True)
  folium_static(m)

  st.markdown('<p style="font-family: \'Times New Roman\'; font-size: 18px; color: black;"> Análisis de los condados de Estados Unidos .</p>', unsafe_allow_html=True)



# Sunburst chart centered on the webpage
if selected2 == "KPIs":
    opcion = st.sidebar.selectbox('Escoge la sección', ['¿La fuente es sustentable?', 'Distribucion de marcas y modelos', 'Distribución de condados'])
    if opcion == "¿La fuente es sustentable?":
        @st.cache_data
        def compute_sunburst():
            fig = px.sunburst(df3, path=['elec', 'clean', 'Make'], color='clean', color_discrete_sequence=px.colors.qualitative.Set1)
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'margin': dict(l=0, r=0, b=0, t=0, pad=0),
            'height': 500,  # Adjust the height as needed
            'width': 800,   # Adjust the width as needed
            })
            return fig

        @st.cache_data
        def compute_p2():
          fig = px.pie(tf, values='clean', names='name', color_discrete_sequence=px.colors.sequential.Blugrn)
          fig.update_layout({
          'plot_bgcolor': 'rgba(0, 0, 0, 0)',
          'paper_bgcolor': 'rgba(0, 0, 0, 0)',
          'margin': dict(l=0, r=0, b=0, t=0, pad=0),
          'height': 500,  # Adjust the height as needed
          'width': 800,   # Adjust the width as needed
          })
          return fig

        figv = compute_p2()
        fig3 = compute_sunburst()
        heading_text20 = '<h2 style="color: black;"> ¿La fuente es sustentable? </h2>'
        st.markdown(heading_text20, unsafe_allow_html=True)
        heading_text3 = '<h3 style="color: black;"> Sunburst</h3>'
        st.markdown(heading_text3, unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown('<p style="font-family: \'Times New Roman\'; font-size: 18px; color: black;"> En las siguientes gráficas se puede observar la proporción de vehículos con energía limpia .</p>', unsafe_allow_html=True)
        heading_text4 = '<h3 style="color: black;"> Proporcion de carros sustentables</h3>'
        st.markdown(heading_text4, unsafe_allow_html=True)
        st.plotly_chart(figv, use_container_width=True)


    if opcion == "Distribucion de marcas y modelos":
        @st.cache_data
        def compute_Treemap():
            fig = px.treemap(df, path=[px.Constant("Car model proportions"), 'Model Year', 'Make', 'Model'], color='Model', color_discrete_sequence=px.colors.diverging.Portland)
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'margin': dict(l=0, r=0, b=0, t=0, pad=0),
            'height': 500,  # Adjust the height as needed
            'width': 800,   # Adjust the width as needed
            })
            return fig

        @st.cache_data
        def compute_p1():
          fig = px.pie(top_5_values, values='Make', names='name', color_discrete_sequence=px.colors.sequential.RdBu)
          fig.update_layout({
              'plot_bgcolor': 'rgba(0, 0, 0, 0)',
              'paper_bgcolor': 'rgba(0, 0, 0, 0)',
              'margin': dict(l=0, r=0, b=0, t=0, pad=0),
              'height': 500,  # Adjust the height as needed
              'width': 800,   # Adjust the width as needed
              })
          return fig

        figr = compute_p1()
        fig7 = compute_Treemap()
        heading_text21 = '<h2 style="color: black;"> Distribucion de marcas y modelos </h2>'
        st.markdown(heading_text21, unsafe_allow_html=True)
        heading_text5 = '<h3 style="color: black;"> Treemap</h3>'
        st.markdown(heading_text5, unsafe_allow_html=True)
        st.plotly_chart(fig7, use_container_width=True)
        heading_text6 = '<h3 style="color: black;"> Marcas </h3>'
        st.markdown(heading_text6, unsafe_allow_html=True)
        st.plotly_chart(figr, use_container_width=True)

    if opcion == "Distribución de condados":
        @st.cache_data
        def compute_p3():
          fig = px.pie(top_5, values='County', names='name', color_discrete_sequence=px.colors.sequential.Burgyl)
          fig.update_layout({
          'plot_bgcolor': 'rgba(0, 0, 0, 0)',
          'paper_bgcolor': 'rgba(0, 0, 0, 0)',
          'margin': dict(l=0, r=0, b=0, t=0, pad=0),
          'height': 500,  # Adjust the height as needed
          'width': 800,   # Adjust the width as needed
          })
          return fig

        figk = compute_p3()
        heading_text22 = '<h2 style="color: black;"> Distribución de condados </h2>'
        st.markdown(heading_text22, unsafe_allow_html=True)
        heading_text15 = '<h3 style="color: black;"> Condados </h3>'
        st.markdown(heading_text15, unsafe_allow_html=True)
        st.plotly_chart(figk, use_container_width=True)

