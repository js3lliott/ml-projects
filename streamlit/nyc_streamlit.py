import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache
def get_data():
    return pd.read_csv("http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv")

df = get_data()

st.title("Streamlit 101: An In-depth Introduction")
st.markdown("Welcome to this in-depth introduction to [Streamlit](www.streamlit.io). for this exercise we're going to use an Airbnb [dataset](http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv) containing NYC listings,")

st.header("Airbnb NYC listings: data at a glance")
st.markdown("The first five records of the Airbnb data we downloaded.")
st.dataframe(df.head())
st.header("Caching our data")
st.markdown("Streamlit has a handy decorator [`st.cache`](https://streamlit.io/docs/api.html#optimize-performance) to enable data caching")
st.code("""
    @st.cache
    def get_data():
        url = "http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv"
        return pd.read_csv(url)
""", language="python")
st.markdown("_To display a code block, pass in the string to display as code to [`st.code`](https://streamlit.io/docs/api.html#streamlit.code)_.")
with st.echo():
    st.markdown("Alternatively, use [`st.echo`](https://streamlit.io/docs/api.html#streamlit.echo).")

st.header("Where are the most expensive properties located?")
st.subheader("On a map")
st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")
st.map(df.query("price>=800")[["latitude", "longitude"]].dropna(how='any'))
st.subheader("In a table")
st.markdown("Following are the top five most expensive properties.")
st.write(df.query("price>=800").sort_values("price", ascending=False).head())

st.subheader("Selecting a subset of columns")
st.write(f"Out of the {df.shape[1]} columns, you might want to view only a subset. Streamlit has a [multiselect](https://streamlit.io/docs/api.html#streamlit.multiselect) widget for this.")
defaultcols = ["name", "host_name", "neighbourhood", "room_type", "price"]
cols = st.multiselect("Columns", df.columns.tolist(), default=defaultcols)
st.dataframe(df[cols].head(10))

st.header("Average price by room type")
st.write("You can also display static tables. As opposed to a dataframe, with a static table you cannot sort by clicking the column header.")
st.table(df.groupby("room_type").price.mean().reset_index()\
    .round(2).sort_values("price", ascending=False)\
    .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))

st.header("Which host has the most properties listed?")
listingcounts = df.host_id.value_counts()
top_host_1 = df.query('host_id == @listingcounts.index[0]')
top_host_2 = df.query('host_id == @listingcounts.index[1]')
st.write(f"""**{top_host_1.iloc[0].host_name}** is at the top with {listingcounts.iloc[0]} property listings.
**{top_host_2.iloc[1].host_name}** is second with {listingcounts.iloc[1]} listings. Following are randomly chosen
listings from the two displayed as JSON using [`st.json`](https://streamlit.io/docs/api.html#streamlit.json)""")

st.json({top_host_1.iloc[0].host_name: top_host_1\
    [["name", "neighbourhood", "room_type", "minimum_nights", "price"]]\
        .sample(2, random_state=4).to_dict(orient="records"),
        top_host_2.iloc[0].host_name: top_host_2\
            [["name", "neighbourhood", "room_type", "minimum_nights", "price"]]\
                .sample(2, random_state=4).to_dict(orient="records")})

