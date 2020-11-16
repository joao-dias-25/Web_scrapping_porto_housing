import streamlit as st
import numpy as np
import pandas as pd



st.title("""Find the best deal with ML """)


st.subheader("Flat offers dataset in 5 districts in downtown Porto city")
st.write("### (dataset scrapped from imovirtual on 10.11.2020)")

st.sidebar.header('User input')

st.sidebar.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.6IYBP2TAe_FANL6h54mO9AHaEh%26pid%3DApi&f=1",
                 use_column_width=True)

path = st.sidebar.text_input('# CSV file path (not available at the moment) ')
if path:
    your_df = pd.read_csv(path)
    your_df

st.sidebar.markdown("choose your **params**")
x = st.sidebar.slider(label="price €",
                               min_value=10000,
                               max_value=1000000,
                               step=10000,
                               value=(50000, 800000))
y = st.sidebar.slider(label='sqm (m²)', min_value=10, max_value=600, step=10, value=(40,300))


#@st.cache
def load_data():
    ei = pd.read_csv("clean.csv")
    ei=ei.loc[(ei.price>=x[0]) & (ei.price<=x[1])]
    ei=ei.loc[(ei.areau>=y[0]) & (ei.areau<=y[1])]
    dist = st.sidebar.multiselect("choose district",
                                  list(ei['district'].unique()),
                                  default= ei['district'].unique())
    cond = st.sidebar.multiselect("choose condition",
                                  list(ei['estado'].unique()),
                                  default=ei['estado'].unique())
    ei=ei.loc[lambda x: x['district'].isin(dist)]
    ei=ei.loc[lambda x: x['estado'].isin(cond)]
    return ei

df=load_data()


import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


if st.button("show ML code",key=0):
    with st.echo():
        # Basic linear regression with one feature (sqm m²).
        X = df.areau.values.reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, df.price)
        x_range = np.linspace(X.min(), X.max(), 100)
        y_range = model.predict(x_range.reshape(-1, 1))

else:
    # Basic linear regression with one feature.
    X = df.areau.values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, df.price)
    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))




fig = px.scatter(df, x='areau', y='price',opacity=0.65, title='Linear Regression based on your choices',
                 color="creation_date", hover_data=['link'])
fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
st.plotly_chart(fig)


if st.checkbox('Show dataframe'):
    st.markdown('### Raw data')
    st.write(df)

import plotly.figure_factory as ff

x0 = np.array(df.loc[df.Tipolo==0]['price'])
x1 = np.array(df.loc[df.Tipolo==1]['price'])
x2 = np.array(df.loc[df.Tipolo==2]['price'])
x3 = np.array(df.loc[df.Tipolo==3]['price'])
x4 = np.array(df.loc[df.Tipolo==4]['price'])

hist_data = [x0,x1,x2,x3,x4]

group_labels = ['1 room Ap', '2 rooms Ap','3 rooms Ap','4 rooms Ap','5 rooms Ap' ]
colors = ['#835AF1', '#7FA6EE', '#B8A7A8','#2BCDC1', '#F66095']

# Create distplot with curve_type set to 'normal'
fig2 = ff.create_distplot(hist_data, group_labels, bin_size=10000, colors=colors)


fig2.update_layout(title='Flat offers distribuition on square meters', autosize=False,
                  width=800, height=800,
                  margin=dict(l=40, r=40, b=40, t=40))
if st.sidebar.checkbox('View offers distribution graph'):
    st.plotly_chart(fig2)


st.sidebar.markdown("Made with love by **João Dias**")
