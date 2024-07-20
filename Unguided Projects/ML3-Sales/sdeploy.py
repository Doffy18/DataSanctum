import pickle
import pandas as pd 
import numpy as np 
import streamlit as st 

model = pickle.load(open('modelx.pkl','rb'))
st.title('sales predictor')
bar=st.sidebar.radio('Navbar',['Home','Predict'])
if bar == 'Home':
    st.write('this is the deployment of sales predictor, this project was mainly focus on EDA side so there isnt much on this. the dataset should contain columns like store,item,sales,date')
else:
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        data['date'] = pd.to_datetime(data['date'])
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month
        data['day'] = data['date'].dt.day
        data=data = data[['store', 'item', 'year', 'month', 'day']]


        model1 = model.predict(data)
        model1=np.round(model1).astype(int)
        st.write(model1)


