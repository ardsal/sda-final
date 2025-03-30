import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.header("Cancelation Flow")
def filter_one(df, select):
    return df[df["hotel"]==select]

def bookings_category(x):
    if 0 < x <= 3:
        return "Super Last Minute"
    elif 3 < x <= 7:
        return "Last Minute"
    elif 7 < x <= 14:
        return "Moderate"
    elif 14 < x <= 31:
        return "Early Booking"
    else:
        return "Super Early Booking"



df = pd.read_csv(r"sda-final/data/hotel_booking_demand.csv",encoding="utf-8")

df["book_window"]=df["lead_time"].apply(bookings_category)

select_box = st.sidebar.selectbox(label="Choose the hotel", options=["City Hotel","Resort Hotel"],placeholder="Choose the hotel")
data1 = filter_one(df, select_box)
option_box = st.sidebar.selectbox(label="Choose the column", 
                                  options=["distribution_channel","assigned_room_type","deposit_type","book_window"],
                                  placeholder="Choose the column")

def group_by_filter(df,option_box):
    grouped_df = df.groupby(["arrival_date_year",option_box,"is_canceled"]).size().reset_index(name="Count")
    years = grouped_df["arrival_date_year"].unique().tolist()
    option = grouped_df[option_box].unique().tolist()
    canceled = grouped_df["is_canceled"].unique().tolist()
    node= [year for year in years] + option + canceled
    node_indice = {label:i for i,label in enumerate(node)}
    links=[]
    for index,row in grouped_df.iterrows():
        links.append({
        "source":node_indice[row["arrival_date_year"]],
        "target":node_indice[row[option_box]],
        "values":row["Count"]
    })
    for index,row in grouped_df.iterrows():
        links.append({
        "source":node_indice[row[option_box]],
        "target":node_indice[row["is_canceled"]],
        "values":row["Count"]
    })
        
    return node_indice,links
node_indice={}
links = []
node_indice,links = group_by_filter(data1,option_box)

fig = go.Figure(go.Sankey(
    arrangement="freeform",
    node=dict(
        pad=20,
        thickness=12,
        label=list(node_indice.keys()),
        color="skyblue", 
        hovertemplate="%{label}<br>Count: %{value}<extra></extra>" 
    ),
    link=dict(
        source=[link["source"] for link in links],  
        target=[link["target"] for link in links],  
        value=[link["values"] for link in links],   
        color="rgba(255, 165, 0, 0.6)",  
        hovertemplate="%{label}<br>Count: %{value}<extra></extra>"
    )
))

fig.update_layout(title_text="Sankey Diagram", font_size=10)
        
st.plotly_chart(fig,use_container_width=True)
