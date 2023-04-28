import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

################### Declarations ################
st.set_page_config(page_title="Search by name",layout="wide")


#Auto-generate dataframe filtering
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df
# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)

def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

dfData = load_data(st.secrets["Oval3DataSource"])
cols = ['Name','Att.Position','Att.Competition','Att.Club', 'Att.Rarity','lastSale.CurrentUSDPrice','lastSale.price', 'blockchain', 'lastSale.date' ,'tokenId', 'Att.Serial_number', 'lastSale.buyer']
df = dfData[cols]

# Remove nan values
#df = df.dropna(subset = ["lastSale.CurrentUSDPrice"]) 
# Replace ',' by '.' in price colums
#df['lastSale.price'] = df['lastSale.price'].apply(lambda x: float(x.split()[0].replace(',', '.')))
#df['lastSale.CurrentUSDPrice'] = df['lastSale.CurrentUSDPrice'].apply(lambda x: float(x.split()[0].replace(',', '.')))
#Set tokenId as index
#df.set_index('Name', inplace=True)
################### Visualisation ###################

st.markdown("# Search by name")
st.sidebar.header("Search by name")

#namelist = df.index.values.tolist()
namelist = df['Name']
option  = st.selectbox('Choose a name', namelist)
#st.write('You selected:', option)
dfname = df[df["Name"] == option]
st.dataframe(dfname)
#st.dataframe(filter_dataframe(dfname))
