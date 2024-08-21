import mysql.connector
import streamlit as st
import pandas as pd

mydb = mysql.connector.connect(
    user='root',
    password='Bavankumar@123',
    database='redbus'
)

db = mydb.cursor()

sql = 'select * from new_table'
db.execute(sql)
results = db.fetchall()

# Convert results to a Pandas DataFrame
df = pd.DataFrame(results, columns=[desc[0] for desc in db.description])

def main():
    st.sidebar.image("logo1.png", caption="")
    # st.sidebar.title("RedBus Application")

    # Initialize filtered_df with the full DataFrame
    filtered_df = df.copy()

    Start_filter = st.sidebar.multiselect('Select From', df['Starting Point'].unique())
    if Start_filter:
        filtered_df = filtered_df[filtered_df['Starting Point'].isin(Start_filter)]

    Ending_filter = st.sidebar.multiselect('Select End', df['Ending Point'].unique())
    if Ending_filter:
        filtered_df = filtered_df[filtered_df['Ending Point'].isin(Ending_filter)]

    # Seat type filter
    Bus_type_filter = st.sidebar.multiselect('Select Seat Type', df['Bus Type'].unique())
    if Bus_type_filter:
        filtered_df = filtered_df[filtered_df['Bus Type'].isin(Bus_type_filter)]

    # AC type filter
    ac_type_filter = st.sidebar.multiselect('Select AC Type', df['Bus Type (Categorized)'].unique())
    if ac_type_filter:
        filtered_df = filtered_df[filtered_df['Bus Type (Categorized)'].isin(ac_type_filter)]

    # Fare range filter
    price_range = st.sidebar.slider('Price Range', float(df['Price'].min()), float(df['Price'].max()), (float(df['Price'].min()), float(df['Price'].max())))
    if price_range:
        filtered_df = filtered_df[(filtered_df['Price'] >= price_range[0]) & (filtered_df['Price'] <= price_range[1])]

    # Rating range filter
    star_rating_range = st.sidebar.slider('Star Rating Range', float(df['Star Rating'].min()), float(df['Star Rating'].max()), (float(df['Star Rating'].min()), float(df['Star Rating'].max())))
    if star_rating_range:
        filtered_df = filtered_df[(filtered_df['Star Rating'] >= star_rating_range[0]) & (filtered_df['Star Rating'] <= star_rating_range[1])]

    # Sort by filter
    sort_by = st.sidebar.selectbox('Sort By', options=['Price', 'Duration', 'Star Rating', 'Departing Time'], index=0)
    filtered_df = filtered_df.sort_values(by=sort_by)

    # Display the data
    st.title('Bus Application Data')
    st.dataframe(filtered_df[['Starting Point', 'Ending Point', 'Bus Name', 'Departing Time', 'Reaching Time', 'Duration', 'Price', 'Seat Availability', 'Star Rating']], use_container_width=True)
    filtered_df = filtered_df.head(50)

if __name__ == "__main__":
    main()
