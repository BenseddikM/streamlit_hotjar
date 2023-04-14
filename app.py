import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

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

# Add Hotjar tracking code
hotjar_code = """
<!-- Hotjar Tracking Code for my site -->
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

st.markdown(hotjar_code, unsafe_allow_html=True)

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
