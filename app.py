import os
import datetime
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.express as px
import streamlit as st
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

# Streamlit app settings
st.set_page_config(page_title='🔖 Streamlit Template',
				   layout='wide',
				   initial_sidebar_state="collapsed")

# App title
st.title('📑 Streamlit Template')

st.write("---")

# Create the container for the indicators
indicators_container = st.container()

# Add the indicators to the container
with indicators_container:    
    # Display indicators
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Metric 1", value="20 km", delta="2 km")
    col2.metric(label="Metric 1", value="10 °F", delta="20 °F")
    col3.metric(label="Metric 1", value="1000 ph", delta="-5000 ph")

# Function for adding a logo to the app

# Add logo to the sidebar
@st.cache_resource
def add_logo():
    """Add logo to the top of the sidebar"""
    image_html = f'<img src="https://www.21.co/images/21.co.svg?imwidth=2048" style="width: 6em;" />'
    app_html = f'''
    <style>
        .sidebar .sidebar-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding-top: 0em;
            padding-bottom: 0em;
        }}
        .sidebar .sidebar-content .logo {{
            margin-bottom: 0em;
        }}
    </style>
    <div class="logo">{image_html}</div>
    '''
    st.sidebar.markdown(app_html, unsafe_allow_html=True)

add_logo()
st.sidebar.markdown('---')


# Functions for generating sample data and creating charts

@st.cache_data
def create_data():
    """Generate sample data"""
    np.random.seed(42)
    date_rng = pd.date_range(start='1/1/2020', end='1/1/2021', freq='D')
    data = pd.DataFrame(date_rng, columns=['date'])
    data['y1'] = np.random.randn(len(date_rng)).cumsum()
    data['y2'] = np.random.randn(len(date_rng)).cumsum()
    data['y3'] = np.random.randn(len(date_rng)).cumsum()

    return data

def create_charts(data):
    """Create Plotly charts"""
    fig1 = px.line(data,
                   x='date',
                   y='y1',
                   title='Line Chart',
                   color_discrete_sequence=['#eda820'])
    fig2 = px.scatter(data,
                      x='date',
                      y='y2',
                      title='Scatter Plot',
                      color_discrete_sequence=['#eda820'])
    fig3 = px.bar(data,
                  x='date',
                  y='y3',
                  title='Bar Chart',
                  color_discrete_sequence=['#eda820'])
    fig4 = px.pie(data,
                  values='y1',
                  names='date',
                  title='Pie Chart',
                  color_discrete_sequence=['#eda820'])
    fig5 = px.histogram(data,
                       x='y1',
                       title='Histogram Chart',
                       nbins=20,
                       color_discrete_sequence=['#eda820'])
    return fig1, fig2, fig3, fig4, fig5


# Functions for injecting Hotjar tracking code

HOTJAR_TRACK_CODE = """
<!-- Hotjar Tracking Code for https://benseddikm-streamlit-hotjar-app-drdwuu.streamlit.app/ -->
<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:3451826,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
"""


def inject_hotjar():
    """Inject Hotjar tracking code"""
    HOTJAR_ELEMENT = "hotjar"
    inject_script_to_streamlit(HOTJAR_TRACK_CODE, HOTJAR_ELEMENT)


@st.cache_resource
def inject_script_to_streamlit(script, element_id, inject_head=True):
    """Insert script into Streamlit app's index.html"""
    index_path = Path(st.__file__).parent / "static" / "index.html"
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")

    # Check if the script has already been injected
    if soup.find(id=element_id):
        print(f'Script with id {element_id} is already injected.')
        return

    bck_index = index_path.with_suffix('.bck')
    if bck_index.exists():
        shutil.copy(bck_index, index_path)  # recover from backup
    else:
        shutil.copy(index_path, bck_index)  # keep a backup
    html = str(soup)

    # Add the id attribute to the script tag
    script_with_id = script.replace('<script>', f'<script id="{element_id}">')

    if inject_head:
        new_html = html.replace('<head>', '<head>\n' + script_with_id)
    else:
        new_html = html.replace('<body>', '<body>\n' + script_with_id)
    index_path.write_text(new_html)
    print(f'Injected {element_id}')

# Main app code

# Generate sample data and create charts
data = create_data()
fig1, fig2, fig3, fig4, fig5 = create_charts(data)


# Inject Hotjar tracking code
inject_hotjar()

# Sidebar
st.sidebar.header('Options')
chart_type = st.sidebar.selectbox('Choose a chart type', ['Line Chart', 'Scatter Plot', 'Bar Chart', 'Pie Chart'])
slider_value = st.sidebar.slider('Select a range for y1 values', int(data['y1'].min()), int(data['y1'].max()), (int(data['y1'].min()), int(data['y1'].max())))
number = st.sidebar.number_input('Insert a number')
uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files=True)

d = st.sidebar.date_input("Date Filter", datetime.date(2019, 7, 6))

# Filter data based on the selected range
filtered_data = data[(data['y1'] >= slider_value[0]) & (data['y1'] <= slider_value[1])]

tab1, tab2 = st.tabs(["Chart", "Data Table"])
with tab1:
    # Create three columns
    col1, col2 = st.columns(2)

    # Display the selected chart in Streamlit
    if chart_type == 'Line Chart':
        col1.plotly_chart(fig1, use_container_width=True)
        col2.plotly_chart(fig2, use_container_width=True)
    elif chart_type == 'Scatter Plot':
        col1.plotly_chart(fig1, use_container_width=True)
        col2.plotly_chart(fig3, use_container_width=True)
    elif chart_type == 'Bar Chart':
        col1.plotly_chart(fig2, use_container_width=True)
        col2.plotly_chart(fig3, use_container_width=True)
    elif chart_type == 'Pie Chart':
        col1.plotly_chart(fig1, use_container_width=True)
        col2.plotly_chart(fig2, use_container_width=True)

with tab2:
    edited_df = st.experimental_data_editor(data, num_rows="dynamic", use_container_width=True)

st.plotly_chart(fig5, use_container_width=True)

