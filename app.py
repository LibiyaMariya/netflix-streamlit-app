import streamlit as st
import pandas as pd

# Title
st.title("🎬 Netflix Data Explorer")

# Load the dataset
df = pd.read_csv("netflix_titles.csv")

# Show full dataset
st.write("Here's the raw Netflix dataset:")
st.dataframe(df)

# Show counts of Movies and TV Shows
st.subheader("📊 Content Type Breakdown")
st.bar_chart(df['type'].value_counts())
# Sidebar Filters
st.sidebar.header("Filter Options")

# Filter by country
countries = df['country'].dropna().unique()
selected_country = st.sidebar.selectbox("Select Country", sorted(countries), key="country_select")


# Filter by content type
types = df['type'].unique()
selected_type = st.sidebar.multiselect("Select Type", types, default=types, key="type_select")

# Filter by release year
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
selected_year = st.sidebar.slider("Select Release Year", min_year, max_year, (min_year, max_year), key="year_slider")
# Search by title
search_term = st.sidebar.text_input("Search by Title", key="title_search")
if search_term:
    df = df[df['title'].str.contains(search_term, case=False, na=False)]

# Apply filters
filtered_df = df[
    (df['country'] == selected_country) &
    (df['type'].isin(selected_type)) &
    (df['release_year'].between(*selected_year))
]

# Display filtered dataset
st.subheader("🎯 Filtered Netflix Titles")
st.dataframe(filtered_df)
# Download filtered data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", data=csv, file_name="filtered_netflix.csv", mime="text/csv")
