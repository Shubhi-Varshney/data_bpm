#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import requests
import data_bpm.api.bpm 

st.markdown("# Prediction")
st.sidebar.markdown("# Prediction")


# Function to call predict API
def call_predict_api(payload):
    url = "http://localhost:8000/predict"  # Update URL as needed
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Prediction failed with status code {response.status_code}")
        return None



    


st.header("Make Prediction")

if st.button("Predict"):
    st.header("Upload CSV file")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Check if required columns are present
        if set(COLUMN_NAMES_RAW).issubset(df.columns):
            # Display uploaded data
            st.write("Uploaded Data:")
            st.write(df)

            # Predict button
            if st.button("Predict"):
                # Call predict API for each row
                st.write("Predictions:")
                for _, row in df.iterrows():
                    payload = row[COLUMN_NAMES_RAW].to_dict()
                    prediction = call_predict_api(payload)
                    if prediction is not None:
                        st.write(prediction)
        else:
            st.error("CSV file does not contain all required columns.")
    





ml_data = pd.read_csv('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/ml_data_clusters.csv')

fig_scatter = px.scatter_3d(ml_data,
                    x = 'jobTitle',
                    y = 'jobTitle2',
                    z = 'jobDuration',
                    opacity=0.7, width=500, height=500,
                    color='dbscan_cluster',
           )

st.plotly_chart(fig_scatter, use_container_width=True, )