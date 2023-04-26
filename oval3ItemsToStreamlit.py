
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


dfData = dfData.dropna(subset = ["lastSale.CurrentUSDPrice"]) 
dfData['lastSale.CurrentUSDPrice'] = dfData['lastSale.CurrentUSDPrice'].apply(lambda x: float(x.split()[0].replace(',', '.')))

order_byDate = dfData.sort_values(by=['lastSale.date'],ascending=False)
top10_Sell = dfData.sort_values(by=['lastSale.CurrentUSDPrice'],ascending=False).head(30)
ById = dfData.sort_values(by=['tokenId']).head(40)
st.write(top10_Sell)