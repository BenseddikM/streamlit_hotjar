import os
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path
from bs4 import BeautifulSoup
import shutil
from datetime import datetime, timedelta

# Your provided functions are placed here

import os

import streamlit as st
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

# Streamlit app settings
st.set_page_config(page_title='Fancy Streamlit App')

@st.cache_data
def create_data():
    # Generate sample data
    np.random.seed(42)
    date_rng = pd.date_range(start='1/1/2020', end='1/1/2021', freq='D')
    data = pd.DataFrame(date_rng, columns=['date'])
    data['y1'] = np.random.randn(len(date_rng)).cumsum()
    data['y2'] = np.random.randn(len(date_rng)).cumsum()
    data['y3'] = np.random.randn(len(date_rng)).cumsum()
    return data

@st.cache_data
def create_charts(data):
    # Create Plotly charts
    fig1 = px.line(data, x='date', y='y1', title='Line Chart')
    fig2 = px.scatter(data, x='date', y='y2', title='Scatter Plot')
    fig3 = px.bar(data, x='date', y='y3', title='Bar Chart')
    fig4 = px.pie(data, values='y1', names='date', title='Pie Chart')
    return fig1, fig2, fig3, fig4

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
    HOTJAR_ELEMENT = "hotjar"
    inject_script_to_streamlit(HOTJAR_TRACK_CODE, HOTJAR_ELEMENT)

@st.cache_resource
def inject_script_to_streamlit(script, element_id, inject_head=True):
    # Insert the script in the head tag of the static template inside your virtual
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


# Generate sample data
np.random.seed(42)
date_rng = pd.date_range(start='1/1/2020', end='1/1/2021', freq='D')

data = create_data()
fig1, fig2, fig3, fig4 = create_charts(data)

# App title
st.title('Fancy Streamlit App with Multiple Charts')

# Call the functions to inject the provided code

inject_hotjar()

# Sidebar
st.sidebar.header('Options')
chart_type = st.sidebar.selectbox('Choose a chart type', ['Line Chart', 'Scatter Plot', 'Bar Chart', 'Pie Chart'])
slider_value = st.sidebar.slider('Select a range for y1 values', int(data['y1'].min()), int(data['y1'].max()), (int(data['y1'].min()), int(data['y1'].max())))

# Filter data based on the selected range
filtered_data = data[(data['y1'] >= slider_value[0]) & (data['y1'] <= slider_value[1])]

# Update Plotly charts with filtered data
fig1.update_traces(x=filtered_data['date'], y=filtered_data['y1'])
fig2.update_traces(x=filtered_data['date'], y=filtered_data['y2'])
fig3.update_traces(x=filtered_data['date'], y=filtered_data['y3'])
fig4.update_traces(values=filtered_data['y1'], labels=filtered_data['date'])

# Display the selected chart in Streamlit
if chart_type == 'Line Chart':
    st.plotly_chart(fig1, use_container_widt=True)
elif chart_type == 'Scatter Plot':
    st.plotly_chart(fig2, use_container_widt=True)
elif chart_type == 'Bar Chart':
    st.plotly_chart(fig3, use_container_widt=True)
elif chart_type == 'Pie Chart':
    st.plotly_chart(fig4, use_container_widt=True)
