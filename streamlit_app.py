import altair as alt
import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap


# Show the page title and description.
st.set_page_config(page_title="Our Anthropogenic Shorelines")
st.title("Our Anthropogenic Shorelines")
st.write(
    """
    Explore the impact of human activities on the coastal environment.
    """
)
# interactions 
interactions = st.container(border=False)
# data views
viewer = st.container(border=False)
##setting up tab layout
tab1, tab2, tab3 = viewer.tabs(["Table", "Timeline","Map"])


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/reclaimed_Islands_gt_bg.csv") 
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
types = interactions.multiselect(
    "Type",
    df.Type.unique(),
    default=["Extension"],
)

# Show a slider widget with the years using `st.slider`.
years = interactions.slider("Date", 2010, 2024, (2010, 2024))

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["Type"].isin(types)) & (df["Date"].between(years[0], years[1]))]
df_filtered = df_filtered.sort_values(by="Date", ascending=False)


# Display the data as a table using `st.dataframe`.
tab1.dataframe(
    df_filtered,
    use_container_width=True,
    column_config={"Date": st.column_config.TextColumn("Date")},
)

# see the extent of projects by year
df_chart = df_filtered.groupby(["Area_sqm", "Date"], as_index=False).sum()
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("Date:N", title="Year"),
        y=alt.Y("Area_sqm:Q", title="Total Area (sqm)"),
        color="Type:N",
    )
    .properties(height=320)
)
tab2.altair_chart(chart, use_container_width=True)


with tab3:
    islands = df_filtered#pd.read_csv("data/island_latlong.csv")

    #get the average value of the lat and long
    ave_lat = islands["Latitude"].mean()
    ave_long = islands["Longitude"].mean()

    m = leafmap.Map(center=[ave_lat, ave_long], zoom=6)

    m.add_points_from_xy(islands, x="Longitude", y="Latitude")
    m.to_streamlit(height=500)