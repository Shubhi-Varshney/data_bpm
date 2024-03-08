#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go



st.markdown("# Prediction")
st.sidebar.markdown("# Prediction")



# raw_data = 


st.header("Make Prediction")

# if st.button("Predict"):
    


# ml_data = pd.read_csv('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/ml_data_clusters.csv')

fig_scatter = px.scatter_3d(ml_data,
                    x = 'jobTitle',
                    y = 'jobTitle2',
                    z = 'jobDuration',
                    opacity=0.7, width=500, height=500
           )

st.plotly_chart(fig_scatter, use_container_width=True, )