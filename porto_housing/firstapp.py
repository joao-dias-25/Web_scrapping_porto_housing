import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff

st.title("first app :)")
st.write("""Data scrapped from a real estate website on
 all apartment offers in 5 districts in downtown Porto city""")

st.sidebar.markdown("## Controls")
st.sidebar.markdown("choose your **params**")
x = st.sidebar.slider(label="price €",
                               min_value=10000,
                               max_value=1000000,
                               step=10000,
                               value=(50000, 800000))
y = st.sidebar.slider(label='sqm m2', min_value=10, max_value=1000, step=10, value=(40,300))
st.sidebar.markdown("Made with love by **João Dias**")

st.write(f"price={x} square meter={y}")

ei = pd.read_csv("clean.csv")
ei=ei.loc[(ei.price>=x[0]) & (ei.price<=x[1])]
df=ei.loc[(ei.areau>=y[0]) & (ei.areau<=y[1])]

if st.checkbox('Show dataframe'):
    st.write(df)

import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


X = df.areau.values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, df.price)

x_range = np.linspace(X.min(), X.max(), 100)
y_range = model.predict(x_range.reshape(-1, 1))

fig = px.scatter(df, x='areau', y='price',opacity=0.65, hover_data=['link'])
fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
st.plotly_chart(fig)


x0 = np.array(df.loc[df.Tipolo==0]['areau'])
x1 = np.array(df.loc[df.Tipolo==1]['areau'])
x2 = np.array(df.loc[df.Tipolo==2]['areau'])
x3 = np.array(df.loc[df.Tipolo==3]['areau'])
x4 = np.array(df.loc[df.Tipolo==4]['areau'])

hist_data = [x0,x1,x2,x3,x4]

group_labels = ['1 room Ap', '2 rooms Ap','3 rooms Ap','4 rooms Ap','5 rooms Ap' ]
colors = ['#835AF1', '#7FA6EE', '#B8F7D4','#2BCDC1', '#F66095']

# Create distplot with curve_type set to 'normal'
fig2 = ff.create_distplot(hist_data, group_labels, bin_size=10, colors=colors)


fig2.update_layout(title='Flat offers distribuition on square meters', autosize=False,
                  width=800, height=800,
                  margin=dict(l=40, r=40, b=40, t=40))
st.plotly_chart(fig2)
