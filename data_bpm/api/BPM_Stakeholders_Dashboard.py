#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

#######################
# Page configuration
st.set_page_config(
    page_title="BPM Stakeholders Dashboard",
    # page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# Load data
    ### TO-DO   --> add correct data
df_reshaped = pd.read_csv('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/cleaned_data_for_ml.csv')
df_analytics = pd.read_csv('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/data_for_analytics.csv')



#######################
# Sidebar
with st.sidebar:
    st.title('BPM')
    
    


    
    event_list = sorted(list(df_analytics.Event.unique()))
    
    selected_event = st.selectbox('Select an event', event_list)
    
    # with.st.sidebar.beta_container()
    with st.expander('About', expanded=False):
        st.write('''
            Made with 🖤 from Berlin,
Shubhi Jain (https://www.linkedin.com/in/email-shubhi-jain/),
Dominic Hodal (email),
Yulia Vilensky (https://www.linkedin.com/in/yulia-vilensky/)
            ''')


# Contents of ~/my_app/main_page.py

st.markdown("# BPM Stakeholders Dashboard")
st.sidebar.markdown("# BPM Stakeholders Dashboard")


#    df_selected_event = df_reshaped[df_reshaped.event == selected_event]
#    df_selected_event_sorted = df_selected_event.sort_values(by="population", ascending=False) # <-- to be changed

    # color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    # selected_color_theme = st.selectbox('Select a color theme', color_theme_list)



# Donut chart
# def make_donut(input_response, input_text, input_color):
#   if input_color == 'blue':
#       chart_color = ['#29b5e8', '#155F7A']
#   if input_color == 'green':
#       chart_color = ['#27AE60', '#12783D']
#   if input_color == 'orange':
#       chart_color = ['#F39C12', '#875A12']
#   if input_color == 'red':
#       chart_color = ['#E74C3C', '#781F16']
    
#   source = pd.DataFrame({
#       "Topic": ['', input_text],
#       "% value": [100-input_response, input_response]
#   })
#   source_bg = pd.DataFrame({
#       "Topic": ['', input_text],
#       "% value": [100, 0]
#   })
    
#   plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
#       theta="% value",
#       color= alt.Color("Topic:N",
#                       scale=alt.Scale(
#                           #domain=['A', 'B'],
#                           domain=[input_text, ''],
#                           # range=['#29b5e8', '#155F7A']),  # 31333F
#                           range=chart_color),
#                       legend=None),
#   ).properties(width=130, height=130)
    
#   text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
#   plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
#       theta="% value",
#       color= alt.Color("Topic:N",
#                       scale=alt.Scale(
#                           # domain=['A', 'B'],
#                           domain=[input_text, ''],
#                           range=chart_color),  # 31333F
#                       legend=None),
#   ).properties(width=130, height=130)
#   return plot_bg + plot + text




#######################
# Dashboard Main Panel
col = st.columns((2, 4, 2), gap='medium')

with col[0]:
    st.markdown('#### Event Attendance'
                
    """
<style>
[data-testid="stMetricLabel"] {
    font-size: 100px;
}
</style>
""",
    unsafe_allow_html=True,
)
    
    event_mask = df_analytics["Event"] == selected_event
    df_event_masked = df_analytics[event_mask]
    df_event_status = df_event_masked["Attendee Status"].value_counts()
    attended  = df_event_status["Checked In"]
    signed_up = df_event_masked["Attendee Status"].value_counts().sum()


    at_percent_ = (attended / signed_up)*100
    at_percent = round(at_percent_, 1)
    
    col1, col2, col3 = st.columns(3)   
    col1.metric("$\large Attendance$", f"{attended}")
    col2.metric("$\large Registered$", f"{signed_up}")
    col3.metric("$\large Conversion$", f"{at_percent}%")



with col[0]:
    st.markdown('#### Attendee Breakdown')
    
    mask = df_analytics["Event"] == selected_event
    df_analytics_masked = df_analytics[mask]
    df_job_position = pd.DataFrame(df_analytics_masked["Your Job Position"].value_counts().reset_index())
    
    fig_pie = px.pie(df_job_position, values='count', names='Your Job Position')
    
  
    st.plotly_chart(fig_pie, use_container_width=True,sharing="streamlit", )
    
    

with col[1]:
    st.markdown('#### Community Growth')

    list_l = [25, 50, 235, 230, 670, 950, 1800]
    list_2 = [0, 0, 0, 350, 550, 800, 1000]
    list_3 = [4, 12, 25, 30, 50, 70, 80]
    list_4 = [0, 1, 2, 3, 4, 5, 6]
    dict_growth = {
        "LinkedIn": list_l,
        "M": list_2,
        "Instagram": list_3,
        "Month": list_4
    }
    df_com_growth = pd.DataFrame(dict_growth)
    
    st.line_chart(
   df_com_growth, x="Month", y=["LinkedIn", "M", "Instagram"], color=["#FF0000", "#0000FF", "#00FF00"]  # Optional
)
    


with col[1]:
    st.markdown('#### Registration Flow')
    
    label = ["Registered", "Ticket", "Wait list", "Confirmed", "Cancelled", "Admitted", "No show"]
    source = [0, 0, 1, 1, 2, 3, 3]
    target = [1, 2, 3, 4, 3, 5, 6]
    value = [204, 91, 113, 90, 48, 71, 18]
    link= dict(source = source, target = target, value = value,)
    node = dict(label = label, pad = 35, thickness = 10)
    data = go.Sankey(link = link, node = node)
    
    fig_san = go.Figure(data)
    fig_san.update_layout(
    hovermode = "x",
    title = "Event ticket breakdown",
)
    
    st.plotly_chart(fig_san, use_container_width=True, sharing="streamlit",)

    
    # choropleth = make_choropleth(df_selected_year, 'states_code', 'population', selected_color_theme)
    # st.plotly_chart(choropleth, use_container_width=True)
    
    # heatmap = make_heatmap(df_reshaped, 'year', 'states', 'population', selected_color_theme)
    # st.altair_chart(heatmap, use_container_width=True)
    

with col[2]:
    df_attendees = pd.DataFrame(df_reshaped["company"].value_counts().reset_index())
    st.markdown('#### Top Companies')

    st.dataframe(df_attendees,
                 column_order=("company", "count"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "company": st.column_config.TextColumn(
                        "Companies",
                    ),
                    "count": st.column_config.ProgressColumn(
                        "Attendees",
                        format="%f",
                        min_value=0,
                        max_value=max(df_attendees["count"]),
                     )}
                 )
    
    
    
    
