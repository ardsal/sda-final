import streamlit as st
import pandas as pd
import plotly.express as px



def filter_one(df, select):
    return df[df["hotel"]==select]


def filter_two(df,year):
    if not year:
        return df
    else:
        return df[df["arrival_date_year"].isin(year)]


st.header("Exploratory Data Analysis")

df = pd.read_csv(r"data/hotel_booking_demand.csv",encoding="utf-8")
df=df[df["is_canceled"]==0]
df["arrival_date_year"]=df["arrival_date_year"].astype(int)
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

df["book_window"]=df["lead_time"].apply(bookings_category)

    

select_box = st.sidebar.selectbox(label="Choose the hotel", options=["City Hotel","Resort Hotel"],placeholder="Choose the hotel")
filtered_data = filter_one(df,select_box)
year = st.sidebar.multiselect("Select Year",options=filtered_data["arrival_date_year"].unique().tolist())
data2 = filter_two(filtered_data,year)

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


avg_los = data2.groupby(by=["arrival_date_year","arrival_date_month"])["length_of_stay"].mean().reset_index(name="average_LoS")
avg_los["arrival_date_year"] = avg_los["arrival_date_year"].astype(str)
avg_los["arrival_date_month"] = pd.Categorical(
    avg_los["arrival_date_month"], categories=month_order, ordered=True
)


booking_by_channel =data2.groupby(by=["arrival_date_year","market_segment"]).size().reset_index(name="count")
booking_by_channel["arrival_date_year"] = booking_by_channel["arrival_date_year"].astype(str)





col1,col2 = st.columns([1,1],vertical_alignment="top")
with col1:
    st.markdown("**Average Length of Stay**")
    fig=px.bar(data_frame=avg_los,x="arrival_date_month",
               y="average_LoS",barmode ="group",color="arrival_date_year",
               category_orders={"arrival_date_month": month_order},facet_col="arrival_date_year",
               labels={"arrival_date_month":"Month",
                       "arrival_date_year":"Year",
                       "average_adr":"Average Length of Stay"
                       })
    st.plotly_chart(fig,use_container_width=True)
    fig.update_layout(xaxis=dict(categoryorder="array", categoryarray=month_order))


with col2:
    st.markdown("**Bookings By Channel**")
    fig2=px.pie(data_frame=booking_by_channel,names="market_segment",values="count")
    fig2.update_layout(xaxis=dict(categoryorder="array", categoryarray=month_order))
    st.plotly_chart(fig2,use_container_width=True)

col3,col4 = st.columns([1,1],vertical_alignment="top")

booking_window = data2.groupby(by=["arrival_date_year","arrival_date_month","book_window"]).size().reset_index(name="book_wind_count")
booking_window["arrival_date_year"] = booking_window["arrival_date_year"].astype(str)

top_countries = data2.groupby(by=["arrival_date_year","arrival_date_month","countries"]).size().reset_index(name="countries_count")
top_countries["arrival_date_year"] = top_countries["arrival_date_year"].astype(str)

with col3:
    st.markdown("**Booking Window**")
    fig3=px.bar(data_frame=booking_window,x="arrival_date_month",
               y="book_wind_count",barmode ="stack",color_discrete_map =
                {"Super Early Booking":"green",
                 "Early Booking":"dark blue",
                 "Last Minute":"light red",
                 "Super Last Minute":"dark red",
                 "Moderate":"light blue"},
               category_orders={"arrival_date_month": month_order},facet_col="arrival_date_year",
               labels={"arrival_date_month":"Month",
                       "arrival_date_year":"Year",
                       "book_wind_count":"Booking Window"
                       })
    st.plotly_chart(fig3,use_container_width=True)
    fig3.update_layout(xaxis=dict(categoryorder="array", categoryarray=month_order))


with col4:
    st.markdown("**Top 10 Countries**")
    fig4=px.pie(data_frame=top_countries,names="countries",values="countries_count")
    st.plotly_chart(fig4,use_container_width=True)


col5=st.columns(1)[0]
with col5:
    st.markdown("**ADR by month**")
    fig5=px.box(data2,x="arrival_date_month",y="adr",category_orders={"arrival_date_month": month_order},color="arrival_date_year")
    st.plotly_chart(fig5,use_container_width=True)
col6=st.columns(1)[0]
with col6:
    st.markdown("**ADR by Room Type**")
    fig6=px.box(data2,x="assigned_room_type",y="adr",color="arrival_date_year")
    st.plotly_chart(fig6,use_container_width=True)
