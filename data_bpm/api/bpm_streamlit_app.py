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
    st.title('BPM Stakeholders Dashboard')
    
    event_list = [1, 2, 3, 4, 5, 6]
    
    selected_event = st.selectbox('Select an event', event_list)
#    df_selected_event = df_reshaped[df_reshaped.event == selected_event]
#    df_selected_event_sorted = df_selected_event.sort_values(by="population", ascending=False) # <-- to be changed

    # color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    # selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

# # Choropleth map
# def make_choropleth(input_df, input_id, input_column, input_color_theme):
#     choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
#                                color_continuous_scale=input_color_theme,
#                                range_color=(0, max(df_selected_year.population)),
#                                scope="usa",
#                                labels={'population':'Population'}
#                               )
#     choropleth.update_layout(
#         template='plotly_dark',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         margin=dict(l=0, r=0, t=0, b=0),
#         height=350
#     )
#     return choropleth


# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)

# Calculate number of people attending from each company
def calculate_company_number(input_df):
    
    df_attendees = pd.DataFrame(input_df["company"].value_counts())
    
    return  df_attendees
        

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
    attended  = [0, 56, 81, 64, 32, 108, 140]
    signed_up = [0, 163, 202, 129, 99, 253, 221]
    # df_at_widg = pd.read_csv('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/BPM Events list people.csv')
    
    # at_num = df_at_widg[f"{selected_event}"].sum()
    at_percent_ = (attended[selected_event] / signed_up[selected_event])*100
    at_percent = round(at_percent_, 1)
    
    col1, col2, col3 = st.columns(3)   
    col1.metric("$\large Attendance$", f"{attended[selected_event]}")
    col2.metric("$\large Registered$", f"{signed_up[selected_event]}")
    col3.metric("$\large Conversion$", f"{at_percent}%")


#     df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)

#     if selected_year > 2010:
#         first_state_name = df_population_difference_sorted.states.iloc[0]
#         first_state_population = format_number(df_population_difference_sorted.population.iloc[0])
#         first_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[0])
#     else:
#         first_state_name = '-'
#         first_state_population = '-'
#         first_state_delta = ''
#     st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

#     if selected_year > 2010:
#         last_state_name = df_population_difference_sorted.states.iloc[-1]
#         last_state_population = format_number(df_population_difference_sorted.population.iloc[-1])   
#         last_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[-1])   
#     else:
#         last_state_name = '-'
#         last_state_population = '-'
#         last_state_delta = ''
#     st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

with col[0]:
    st.markdown('#### Attendee Breakdown')
    
    mask = df_analytics["Event"] == selected_event
    df_analytics_masked = df_analytics[mask]
    df_job_position = pd.DataFrame(df_analytics_masked["Your Job Position"].value_counts().reset_index())
    
    fig_pie = px.pie(df_job_position, values='count', names='Your Job Position')
    
  
    st.plotly_chart(fig_pie, use_container_width=True,sharing="streamlit", )
    # if selected_year > 2010:
    #     # Filter states with population difference > 50000
    #     # df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference_absolute > 50000]
    #     df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference > 50000]
    #     df_less_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference < -50000]
        
    #     # % of States with population difference > 50000
    #     states_migration_greater = round((len(df_greater_50000)/df_population_difference_sorted.states.nunique())*100)
    #     states_migration_less = round((len(df_less_50000)/df_population_difference_sorted.states.nunique())*100)
    #     donut_chart_greater = make_donut(states_migration_greater, 'Inbound Migration', 'green')
    #     donut_chart_less = make_donut(states_migration_less, 'Outbound Migration', 'red')
    # else:
    #     states_migration_greater = 0
    #     states_migration_less = 0
    #     donut_chart_greater = make_donut(states_migration_greater, 'Inbound Migration', 'green')
    #     donut_chart_less = make_donut(states_migration_less, 'Outbound Migration', 'red')

    # migrations_col = st.columns((0.2, 1, 0.2))
    # with migrations_col[1]:
    #     st.write('Inbound')
    #     st.altair_chart(donut_chart_greater)
    #     st.write('Outbound')
    #     st.altair_chart(donut_chart_less)

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
    
    
    
    
    # with st.expander('About', expanded=True):
    #     st.write('''
    #         - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
    #         - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
    #         - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
    #         ''')