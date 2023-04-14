import os
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path
from bs4 import BeautifulSoup
import shutil

# Your provided functions are placed here

import os

import streamlit as st
import shutil
from pathlib import Path
from bs4 import BeautifulSoup


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
data = pd.DataFrame({
    'x': np.linspace(1, 100, num=100),
    'y1': np.random.randn(100).cumsum(),
    'y2': np.random.randn(100).cumsum(),
    'y3': np.random.randn(100).cumsum(),
})

# Create Plotly charts
fig1 = px.line(data, x='x', y='y1', title='Line Chart')
fig2 = px.scatter(data, x='x', y='y2', title='Scatter Plot')
fig3 = px.bar(data, x='x', y='y3', title='Bar Chart')

# Streamlit app settings
st.set_page_config(page_title='Fancy Streamlit App', layout='wide')

# App title
st.title('Fancy Streamlit App with Multiple Charts')

# Call the functions to inject the provided code
inject_hotjar()

# Sidebar
st.sidebar.header('Options')
chart_type = st.sidebar.selectbox('Choose a chart type', ['Line Chart', 'Scatter Plot', 'Bar Chart'])

# Display the selected chart in Streamlit
if chart_type == 'Line Chart':
    st.plotly_chart(fig1)
elif chart_type == 'Scatter Plot':
    st.plotly_chart(fig2)
elif chart_type == 'Bar Chart':
    st.plotly_chart(fig3)
