
import pandas as pd
import streamlit as st

################### Declarations ################

################### Functions ###################

st.write("Welcome to Oval3 Analytics")


# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

# Print results.
#st.write(df)

st.write("Top 30 Sell")
cols = ['blockchain','lastSale.price', 'lastSale.CurrentUSDPrice', 'lastSale.date' ,'tokenId', 'Name', 'Att.Rarity', 'Att.Club', 'Att.Competition', 'Att.Position', 'Att.Serial_number', 'lastSale.buyer']
dfcols = df[cols]
top30_Sell = (dfcols.sort_values(by=['lastSale.CurrentUSDPrice'],ascending=False)).head(30)

st.write(top30_Sell)