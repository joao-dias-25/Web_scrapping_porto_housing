import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")



st.title("""Price regression on flats in Porto city""")


st.write('''#### Flat offers in 5 districts in Porto city 
(dataset scrapped from Imovirtual.com on 10.11.2020)''')
st.markdown("---")

col1, col2 = st.beta_columns(2)
st.sidebar.image("porto.png",
                 use_column_width=True)
st.sidebar.header('User input')


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




fig = px.scatter(df, x='areau', y='price',opacity=0.65,
                 title='Linear Regression based on your choices',
                 color="creation_date", hover_data= ['link'])
fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
fig.update_layout(autosize=False,
                  width=500, #height=400,
                  margin=dict(l=0, r=40, b=0, t=40),
                  coloraxis_colorbar=dict(
                      title="Days since creation date",
                      thicknessmode="pixels", thickness=20,
                      lenmode="pixels", len=250)
                      #dtick=5)
                  )

with col1:
    st.plotly_chart(fig)



if st.checkbox('Show selected dataframe'):
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


fig2.update_layout(title='Flat offers distribuition on price', autosize=False,
                 width=500, #height=800,
                  margin=dict(l=0, r=40, b=0, t=40))

with col2:
    st.plotly_chart(fig2)


st.sidebar.markdown("Made with love by **João Dias**")
