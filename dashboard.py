import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")

@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df['language'] = df['language'].fillna('Unknown')  
        return df
    except FileNotFoundError:
        st.error("The dataset could not be found. Please check the file path.")
        return pd.DataFrame() 
    except pd.errors.EmptyDataError:
        st.error("The dataset is empty. Please provide a valid CSV file.")
        return pd.DataFrame()


df = load_data("github_dataset.csv")  

if not df.empty:

    st.title("GitHub Repository Dashboard")


    st.sidebar.header("Filters")
    languages = df['language'].unique().tolist()
    selected_language = st.sidebar.multiselect("Select Programming Language", options=languages, default=languages)


    filtered_df = df[df['language'].isin(selected_language)]

   
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stars Count by Language")
        fig_horizontal_stars = px.bar(filtered_df, y='language', x='stars_count', orientation='h')
        st.plotly_chart(fig_horizontal_stars)


    with col2:
        st.subheader("Pull Requests vs. Stars")
        fig_scatter = px.scatter(filtered_df, x='stars_count', y='pull_requests', color='language',
                                  title='Pull Requests vs. Stars by Language', labels={'stars_count': 'Stars', 'pull_requests': 'Pull Requests'})
        st.plotly_chart(fig_scatter)

    col3, col4 = st.columns(2)


    with col3:
        st.subheader("Distribution of Stars Count")
        fig_histogram = px.histogram(filtered_df, x='stars_count', nbins=30)
        st.plotly_chart(fig_histogram)

 
    with col4:
        st.subheader("Forks Count Distribution by Language")
        fig_box = px.box(filtered_df, x='language', y='forks_count')
        st.plotly_chart(fig_box)

  
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at']) 
        stars_over_time = df.groupby(['created_at', 'language']).agg({'stars_count': 'sum'}).reset_index()
        stars_heatmap = stars_over_time.pivot("created_at", "language", "stars_count")
        st.subheader("Heatmap of Stars Count by Language and Time")
        fig_heatmap = px.imshow(stars_heatmap, color_continuous_scale='Viridis')
        st.plotly_chart(fig_heatmap)


    if 'created_at' in df.columns:
        stars_over_time = df.groupby(['created_at', 'language']).agg({'stars_count': 'sum'}).reset_index()
        
        st.subheader("Stars Count and Forks Count by Language Over Time")
        
       
        col5, col6 = st.columns(2)

       
        with col5:
            fig_area_stars = px.area(stars_over_time, x='created_at', y='stars_count', color='language', 
                                    labels={'stars_count': 'Stars Count'})
            st.plotly_chart(fig_area_stars)

        
        forks_over_time = df.groupby(['created_at', 'language']).agg({'forks_count': 'sum'}).reset_index()
        with col6:
            fig_area_forks = px.area(forks_over_time, x='created_at', y='forks_count', color='language', 
                                       labels={'forks_count': 'Forks Count'})
            st.plotly_chart(fig_area_forks)

    col7, col8 = st.columns(2)


    with col7:
        st.subheader("Stars Distribution by Language")
        stars_distribution = filtered_df.groupby('language')['stars_count'].sum().reset_index()
        fig_stars_pie = px.pie(stars_distribution, values='stars_count', names='language')
        st.plotly_chart(fig_stars_pie)

    with col8:
        st.subheader("Forks Distribution by Language")
        forks_distribution = filtered_df.groupby('language')['forks_count'].sum().reset_index()
        fig_forks_pie = px.pie(forks_distribution, values='forks_count', names='language')
        st.plotly_chart(fig_forks_pie)


    if 'created_at' in df.columns:
        stars_over_time = df.groupby(df['created_at'].dt.to_period('M')).agg({'stars_count': 'sum'}).reset_index()
        stars_over_time['created_at'] = stars_over_time['created_at'].dt.to_timestamp()

        st.subheader("Trend of Stars Over Time")
        fig_trend_stars = px.line(stars_over_time, x='created_at', y='stars_count', title='Stars Over Time', markers=True)
        st.plotly_chart(fig_trend_stars)

else:
    st.warning("No data available to display.")
