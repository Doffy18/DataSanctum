import streamlit as st 
import pickle
import math
import numpy as np

model = pickle.load(open('model1.pkl', 'rb'))
dataset = pickle.load(open('data.pkl','rb'))

st.title('Simple Flower Predictor for fun')
bar = st.sidebar.radio('NavBar',['Home','Show_Dataset','Predict'])
if bar =='Home':
    st.write('Hi, i made this for fun simply to review my deployment skill')
if bar == 'Show_Dataset':
    st.write(dataset)
if bar == 'Predict':
     pl=st.text_input('Petal length')
     pw = st.text_input('Petal Width')
     sl = st.text_input('Sepal Length')
     sw = st.text_input('Sepal width')
     if st.button('Predict'):
        if sl and sw and pl and pw:
            input_data = np.array([[float(sl), float(sw), float(pl), float(pw)]]) 
            p = model.predict(input_data)
            prediction = math.trunc(p[0])

            if prediction == 0:
                st.write('flower is a Iris setosa')
            elif prediction == 1:
                st.write('flower is a Iris versicolor')
            else:
                st.write('flower is a Iris virginica')
     
   

