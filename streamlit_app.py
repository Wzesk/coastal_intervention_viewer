import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Anthropogenic Coasts", page_icon="🎬")
st.title("Anthropogenic Coasts")
st.write(
    """
    Anthropogenic Coastal Impact Explorer allows you to explore the impact of human activities on the coastal environment.
    """
)

## setting up test layout
col1, col2 = st.columns(2)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/reclaimed_Islands_gt.csv") 
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
types = col1.multiselect(
    "Type",
    df.Type.unique(),
    default=["Airport Development", "Extension"],
)

# Show a slider widget with the years using `st.slider`.
years = st.slider("Date", 2010, 2024, (2010, 2024))

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["Type"].isin(types))] #& (df["Date"].between(years[0], years[1]))]
df_reshaped = df_filtered.pivot_table(
    index="Date", columns="Type", values="Area_sqm", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="Date", ascending=False)


# Display the data as a table using `st.dataframe`.
col1.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"Date": st.column_config.TextColumn("Date")},
)

# # Display the data as an Altair chart using `st.altair_chart`.
# df_chart = pd.melt(
#     df_reshaped.reset_index(), id_vars="Date", var_name="Type", value_name="Area_sqm"
# )
# chart = (
#     alt.Chart(df_chart)
#     .mark_line()
#     .encode(
#         x=alt.X("Date:N", title="Year"),
#         y=alt.Y("Area_sqm:Q", title="Gross earnings ($)"),
#         color="Type:N",
#     )
#     .properties(height=320)
# )
# col2.altair_chart(chart, use_container_width=True)
