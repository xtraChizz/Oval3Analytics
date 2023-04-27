import pandas as pd
import streamlit as st

################### Declarations ################

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

dfData = load_data(st.secrets["Oval3DataSource"])

cols = ['Name','Att.Rarity','blockchain','lastSale.price', 'lastSale.CurrentUSDPrice', 'lastSale.date' ,'tokenId',   'Att.Club', 'Att.Competition', 'Att.Position', 'Att.Serial_number', 'lastSale.buyer']
df = dfData[cols]

# Remove nan values
df = df.dropna(subset = ["lastSale.CurrentUSDPrice"]) 
################### Visualisation ###################

st.write("Welcome to Oval3 Analytics")

# Replace ',' by '.' in price colums
df['lastSale.price'] = df['lastSale.price'].apply(lambda x: float(x.split()[0].replace(',', '.')))
df['lastSale.CurrentUSDPrice'] = df['lastSale.CurrentUSDPrice'].apply(lambda x: float(x.split()[0].replace(',', '.')))

#Set tokenId as index
df.set_index('tokenId', inplace=True)

#Filters
order_byDate = df.sort_values(by=['lastSale.date'],ascending=False)
top10_Sell = df.sort_values(by=['lastSale.CurrentUSDPrice'],ascending=False).head(10)
ById = df.sort_values(by=['tokenId']).head(40)

# Show top 10 sell
st.write("Top10 Sell")
st.write(top10_Sell.style.format(thousands=" "), use_container_width=True)