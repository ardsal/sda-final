import streamlit as st  
import pandas as pd

geoMap= st.Page(page="sda-final/src/map.py",
                
            title="Geographical Distribution",
            icon=":material/globe:",
            default=True        
)

generalEDA = st.Page(page="src\eda.py",
                     title="Exploratory Data Analysis",
                     icon=":material/monitoring:"
                     )


canc = st.Page(page="src\canc.py",
               title="Cancelation Flow",
               icon=":material/schema:"
               )

pg = st.navigation({"GeoMap":[geoMap],
                    "EDA":[generalEDA],
                    "Canc":[canc]})
pg.run()
