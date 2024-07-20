import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string

cv = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

def transf(text):
    ps = PorterStemmer()  
    text = text.lower()  
    tokens = nltk.word_tokenize(text)  
    tokens = [token for token in tokens if token.isalnum()]
    
    filtered_tokens = [
        token for token in tokens 
        if token not in stopwords.words('english') and token not in string.punctuation
    ]

    stemmed_tokens = [ps.stem(token) for token in filtered_tokens]
    
    return " ".join(stemmed_tokens)

st.title('SMS CLASSIFIER')
input_sms=st.text_input('Add sms')
if st.button('Predict'):
    #preprocess
    transformed_sms = transf(input_sms)
    #vectorize
    vector_input=cv.fit_transform([transformed_sms])
    #predict
    result = model.predict(vector_input)[0]
    #display
    if result == 1:
                    st.write('Spam')
    else:
                    st.write('Not Spam')
