import pandas as pd
import streamlit as st

################### Declarations ################

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)


st.set_page_config(page_title="Top 10 Sales",layout="wide")

st.markdown("# Top 10 sales")
st.sidebar.header("Top 10 sales")

dfData = load_data(st.secrets["Oval3DataSource"])

cols = ['Name','Att.Rarity','Score','blockchain','lastSale.price', 'lastSale.CurrentUSDPrice', 'lastSale.date' ,'tokenId',   'Att.Club', 'Att.Competition', 'Att.Position', 'Att.Serial_number', 'lastSale.buyer']
df = dfData[cols]

# Remove nan values
df = df.dropna(subset = ["lastSale.CurrentUSDPrice"]) 
################### Visualisation ###################
tab1, tab2, tab3, tab4, tab5 = st.tabs(["All", "UNIQUE", "SUPER RARE", "RARE", "LIMITED"])


# Replace ',' by '.' in price colums
df['lastSale.price'] = df['lastSale.price'].apply(lambda x: float(x.split()[0].replace(',', '.')))
df['lastSale.CurrentUSDPrice'] = df['lastSale.CurrentUSDPrice'].apply(lambda x: float(x.split()[0].replace(',', '.')))

#Set tokenId as index
df.set_index('tokenId', inplace=True)

#Filters
order_byDate = df.sort_values(by=['lastSale.date'],ascending=False)

ById = df.sort_values(by=['tokenId']).head(40)

# Show top 10 
with tab1:
    top10_Sell = df.sort_values(by=['lastSale.CurrentUSDPrice'],ascending=False).head(10)
    top10_Sell.index = pd.RangeIndex(start=1, stop=11, step=1)
    st.write("Top 10 All rarity")
    st.write(top10_Sell.style.format(thousands=" "), use_container_width=True)

#top 10 UNIQUE  
with tab2:
    dfunique = df[df["Att.Rarity"] == 'UNIQUE']
    top10_Sell_Unique = dfunique.sort_values(by=['lastSale.CurrentUSDPrice'],ascending=False).head(10)
    top10_Sell_Unique.index = pd.RangeIndex(start=1, stop=11, step=1)
    st.write("Top 10 Unique ")
    st.write(top10_Sell_Unique.style.format(thousands=" "), use_container_width=True)

#top 10 SR
with tab3:
    dfSR= df[df["Att.Rarity"] == 'SUPER RARE']
    top10_Sell_SR = dfSR.sort_values(by=['lastSale.CurrentUSDPrice'],ascending=False).head(10)
    top10_Sell_SR.index = pd.RangeIndex(start=1, stop=11, step=1)
    st.write("Top 10 Super Rare ")
    st.write(top10_Sell_SR.style.format(thousands=" "), use_container_width=True)

#top 10 Rare
with tab4:
    dfRare= df[df["Att.Rarity"] == 'RARE']
    top10_Sell_Rare = dfRare.sort_values(by=['lastSale.CurrentUSDPrice'],ascending=False).head(10)
    top10_Sell_Rare.index = pd.RangeIndex(start=1, stop=11, step=1)
    st.write("Top 10 Rare ")
    st.write(top10_Sell_Rare.style.format(thousands=" "), use_container_width=True)


#top 10 Limited
with tab5:
    dfLimited= df[df["Att.Rarity"] == 'LIMITED']
    top10_Sell_Limited = dfLimited.sort_values(by=['lastSale.CurrentUSDPrice'],ascending=False).head(10)
    top10_Sell_Limited.index = pd.RangeIndex(start=1, stop=11, step=1)
    st.write("Top 10 Limited ")
    st.write(top10_Sell_Limited.style.format(thousands=" "), use_container_width=True)

