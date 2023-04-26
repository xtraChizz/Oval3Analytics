
import pandas as pd
import streamlit as st

################### Declarations ################



# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)


################### Visualisation ###################
st.write("Welcome to Oval3 Analytics")


dfData = load_data(st.secrets["Oval3DataSource"])

# Print results.
#st.write(df)

st.write("Top 30 Sell")
cols = ['Name', 'Att.Rarity', 'blockchain', 'lastSale.price', 'lastSale.CurrentUSDPrice', 'lastSale.date','tokenId', 'Att.Club', 'Att.Competition', 'Att.Position', 'Att.Serial_number', 'lastSale.buyer']
df = dfData[cols]
top30_Sell = df.sort_values(by=['lastSale.CurrentUSDPrice'],ascending=False)
st.write(top30_Sell)