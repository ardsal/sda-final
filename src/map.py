import streamlit as st  
import pandas as pd
import plotly.express as px
st.title("Geographical Distribution of Guests")

df = pd.read_csv(r"data/hotel_booking_demand.csv",encoding="utf-8")
df=df[df["is_canceled"]==0]
countries = df.groupby("country").agg(count=("country", "size")).reset_index()



fig = px.choropleth(
    countries,
    locations="country",  
    locationmode="ISO-3",  
    color="count",  
    hover_name="country", 
    color_continuous_scale=px.colors.sequential.Plasma,  
    title="Reservation Count by Country",
    projection="kavrayskiy7",
)


st.plotly_chart(fig, selection_mode="box",use_container_width=False)
