#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import gcsfs


#######################
# Page configuration
st.set_page_config(
    page_title="BPM Community Breakdown",
    # page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# Load data

### Local
    ### TO-DO   --> add correct data
# df_reshaped = pd.read_csv('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/cleaned_data_for_ml.csv')
# df_analytics = pd.read_csv('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/data_for_analytics.csv')


### GCS
bucket_name = 'taxifare_d-hodal'
file_path_analytics = 'data_for_analytics.csv'
file_path_ml = "cleaned_data_for_ml.csv"
file_path_cg = "Community Growth.xlsx"

# Create a file system object using gcsfs
fs = gcsfs.GCSFileSystem()

with fs.open(f'{bucket_name}/{file_path_analytics}') as f:
    df_gcs_an = pd.read_csv(f)

with fs.open(f'{bucket_name}/{file_path_ml}') as g:
    df_gcs_ml = pd.read_csv(g)

with fs.open(f'{bucket_name}/{file_path_cg}') as h:
    df_gcs_cg = pd.read_excel(h)

df_analytics = df_gcs_an
df_reshaped = df_gcs_ml
df_line = df_gcs_cg
######################
# Colors
color_bpm_logo = '#c'


#######################
# Sidebar
with st.sidebar:
    st.title('BPM')





    event_list = sorted(list(df_analytics.Event.unique()))

    selected_event = st.selectbox('Select an event', event_list)

    # with.st.sidebar.beta_container()
    with st.expander('About', expanded=False):
        st.write('''
            Made with 🖤 from Berlin,\n
Shubhi Jain, Dominic Hodal, Yulia Vilensky
            ''')


# (https://www.linkedin.com/in/email-shubhi-jain/)
# (https://www.linkedin.com/in/yulia-vilensky/)

# Contents of ~/my_app/main_page.py


st.markdown('<span style="font-size: 50px; color: #00FF00;">BPM Community Dashboard</span>', unsafe_allow_html=True)
#st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)
 # text-align: center;
st.sidebar.markdown("# BPM Community Dashboard")


#    df_selected_event = df_reshaped[df_reshaped.event == selected_event]
#    df_selected_event_sorted = df_selected_event.sort_values(by="population", ascending=False) # <-- to be changed

    #color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    # selected_color_theme = st.selectbox('Select a color theme', color_theme_list)




#######################
# Dashboard Main Panel
col = st.columns((2, 4, 2), gap='medium')

with col[0]:
    st.markdown('#### Event Attendance')
     #st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)
           
    
    event_mask = df_analytics["Event"] == selected_event
    df_event_masked = df_analytics[event_mask]
    df_event_status = df_event_masked["Attendee Status"].value_counts()
    attended  = df_event_status["Checked In"]
    signed_up = df_event_masked["Attendee Status"].value_counts().sum()
    venue_size = df_line['Venues management '].iloc[selected_event - 1]

    at_percent_ = (attended / venue_size)*100
    at_percent = round(at_percent_, 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("$\large Attendance$", f"{attended}")
    col2.metric("$\large Venue Size$", f"{venue_size}")
    col3.metric("$\large Conversion$", f"{at_percent}%")



with col[0]:
    st.markdown('#### Attendee Breakdown')

    mask = df_analytics["Event"] == selected_event
    df_analytics_masked = df_analytics[mask]
    df_job_position = pd.DataFrame(df_analytics_masked["Your Job Position"].value_counts().reset_index())
    
    pie_colors = ["#0000db","#FF3A06","#5E57FF", "#F23CA6", "#FF9535", "#4BFF36", "#02FEE4"] #  "#1c0159","#22016d","#b697ff","#d3c0ff","#9362ff","#a881ff"
    
    fig_pie = px.pie(df_job_position, values='count', names='Your Job Position', ) # 
    fig_pie.update_layout(showlegend=False, )
    fig_pie.update_traces(hoverinfo='label+percent',
                  marker=dict(colors=pie_colors, ))
  
    st.plotly_chart(fig_pie, use_container_width=True,sharing="streamlit", )



with col[1]:
    st.markdown('#### Community Growth')

    # df_line = pd.read_excel("/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/Community Growth.xlsx")
    headers = df_line.iloc[0]
    df_line_renamed  = pd.DataFrame(df_line.values[1:], columns=headers)
    df_line_renamed['Newsletter'] = df_line_renamed['Newsletter'].fillna(0)
    months = ["August", "September", "October", "November", "December", "January", "February", "March"]
    # number
    list_l = list(df_line_renamed['LinkedIn'].iloc[:(selected_event+ 2)])
    list_2 = list(df_line_renamed['Newsletter'].iloc[:(selected_event+ 2)])
    list_3 = list(df_line_renamed['Instagram'].iloc[:(selected_event+ 2)])
    list_4 = months[:(selected_event + 2)]
    # list_l = [25, 50, 135, 230, 670, 950]
    # list_2 = [0, 0, 0, 350, 550, 800]
    # list_3 = [4, 12, 25, 30, 50, 50]
    # list_4 = [1, 2, 3, 4, 5, 6]
    
    dict_growth = {
        "LinkedIn": list_l,
        "Mailing list": list_2,
        "Instagram": list_3,
        "Month": list_4
    }
    df_com_growth = pd.DataFrame(dict_growth)
    
    fig_line = go.Figure(data=go.Line(x=df_com_growth["Month"], y=df_com_growth["LinkedIn"], name="LinkedIn", line_color="#FF0000"))
    fig_line.add_scatter(x=df_com_growth["Month"], y=df_com_growth["Mailing list"], name="Mailing list", line_color="#0000FF")
    fig_line.add_scatter(x=df_com_growth["Month"], y=df_com_growth["Instagram"], name="Instagram", line_color="#00FF00")

# Update layout to change x-axis labels
    fig_line.update_layout(xaxis=dict(
        tickvals=[0, 1, 2, 3, 4, 5, 6, 7],  # Positions of the ticks on the axis
        ticktext=months  # Labels for the ticks
))
  
    st.plotly_chart(fig_line, use_container_width=True,)
    
#     st.line_chart(
#    df_com_growth, x="Month", y=["LinkedIn", "M", "Instagram"], color=["#FF0000", "#0000FF", "#00FF00"]  # Optional
# )
    


with col[1]:
    st.markdown('#### Registration Flow')
     
    # event_mask = df_analytics["Event"] == selected_event
    # df_event_masked = df_analytics[event_mask]
    df_event_status = df_event_masked["Attendee Status"].value_counts()
    attended  = df_event_status["Attending"]
    signed_up = df_event_status["Checked In"]
    registered = attended + signed_up
    cancelled = df_event_status["Not Attending"]

    	
    san_registered = cancelled + signed_up
    san_ticketed = attended + cancelled
    san_wait_list = san_registered - san_ticketed
    cancelled = cancelled
    confirmed = signed_up
    admitted = attended
    no_show = confirmed - admitted
    
    label = ["Registered", "Ticket", "Wait list", "Confirmed", "Cancelled", "Admitted", "No show"]
    source = [0, 0, 1, 1, 2, 3, 3]
    target = [1, 2, 3, 4, 3, 5, 6]
    value = [san_registered, san_ticketed, san_wait_list, cancelled, confirmed, admitted, no_show]
   # value = [204, 91, 113, 90, 48, 71, 18] 
    
    link= dict(source = source, target = target, value = value,)
    node = dict(label = label, pad = 35, thickness = 10)
    data = go.Sankey(link = link, node = node)

    fig_san = go.Figure(data)
    fig_san.update_layout(
    hovermode = "x",
    title = "Event ticket breakdown",
)

    st.plotly_chart(fig_san, use_container_width=True, sharing="streamlit",)


    

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
