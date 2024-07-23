import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle

model = pickle.load(open('model.pkl', 'rb'))

def preprocess_data(data):
    # Check if all required columns are present
    required_columns = [
        'machineID', 'volt', 'rotate', 'pressure', 'vibration', 'model', 'age',
        'comp', 'errorID', 'day', 'month', 'year', 'datetime'
    ]
    
    missing_cols = [col for col in required_columns if col not in data.columns]
    if missing_cols:
        st.error(f"Missing columns in the uploaded file: {', '.join(missing_cols)}")
        return None

    # Convert datetime if 'datetime' column is present
    if 'datetime' in data.columns:
        data['datetime'] = pd.to_datetime(data['datetime'])
        data['day'] = data['datetime'].dt.day
        data['month'] = data['datetime'].dt.month
        data['year'] = data['datetime'].dt.year
        data['time'] = data['datetime'].dt.time
        data.drop(columns='datetime', inplace=True)
        data.rename(columns={'comp':'maint'},inplace=True)


        data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.time
        data['hour'] = [t.hour for t in data['time']]
        data['minute'] = [t.minute for t in data['time']]
        
        # Cyclic encoding
        data['hour_sin'] = np.sin(2 * np.pi * data['hour'] / 24)
        data['hour_cos'] = np.cos(2 * np.pi * data['hour'] / 24)
        data['minute_sin'] = np.sin(2 * np.pi * data['minute'] / 60)
        data['minute_cos'] = np.cos(2 * np.pi * data['minute'] / 60)
        data.drop(columns=['hour', 'minute', 'time'], inplace=True)
    
    # Ensure columns for encoding and preprocessing
    cate_col1 = ['model', 'maint', 'errorID']
    data = pd.get_dummies(data, columns=cate_col1, drop_first=True)
    
    num_col1 = ['machineID', 'volt', 'rotate', 'pressure', 'vibration', 'age', 'year']
    scaler = MinMaxScaler()
    data[num_col1] = scaler.fit_transform(data[num_col1])
    
    # Cyclic encoding for day and month
    data['day_sin'] = np.sin(2 * np.pi * data['day'] / 365.0)
    data['day_cos'] = np.cos(2 * np.pi * data['day'] / 365.0)
    data['month_sin'] = np.sin(2 * np.pi * data['month'] / 12.0)
    data['month_cos'] = np.cos(2 * np.pi * data['month'] / 12.0)
    data.drop(columns=['day', 'month'], inplace=True)
    
    # Define the columns expected by the model
    expected_columns = [
        'machineID', 'volt', 'rotate', 'pressure', 'vibration', 'age', 'year',
        'hour_sin', 'hour_cos', 'minute_sin', 'minute_cos', 'model_model2',
        'model_model3', 'model_model4', 'maint_comp1', 'maint_comp2',
        'maint_comp3', 'maint_comp4', 'errorID_error1', 'errorID_error2',
        'errorID_error3', 'errorID_error4', 'errorID_error5', 'day_sin',
        'day_cos', 'month_sin', 'month_cos'
    ]
    
    # Add missing columns with default value 0
    for col in expected_columns:
        if col not in data.columns:
            data[col] = 0

    # Ensure the dataframe has exactly the required columns
    data = data[expected_columns]

    return data.astype('int')


st.title('Model Deployment with Streamlit')
bar = st.sidebar.radio('Navbar',['Home',' Predictor'])
if bar == 'Home':
    st.write('HI,welcome to the 1st predictive maintenance project. be sure to include these columns in your dataset for uploading')
    st.write('machineID, volt, rotate, pressure, vibration, model, age,maint, failure, errorID, day, month, year, hour_sin,hour_cos, minute_sin, minute_cos')
else:
    st.header('Upload your CSV file')
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        required_columns = [
            'machineID', 'volt', 'rotate', 'pressure', 'vibration', 'model', 'age',
            'maint', 'errorID', 'day', 'month', 'year', 'hour_sin',
            'hour_cos', 'minute_sin', 'minute_cos'
        ]
    
        missing_cols = [col for col in required_columns if col not in data.columns]
        if missing_cols:
            st.error(f"Missing columns in the uploaded file: {', '.join(missing_cols)}")
        else:
            st.write("Original Data:")
            st.write(data.head())
        
            processed_data = preprocess_data(data)
            if processed_data is not None:
                st.write("Preprocessed Data:")
                st.write(processed_data.head())
                predictions = model.predict(processed_data)
            
                target_columns = ['NoFail', 'Failure_comp1', 'failure_comp2', 'failure_comp3', 'failure_comp4']
                y_pred_df = pd.DataFrame(predictions, columns=target_columns, index=processed_data.index)
                predicted_components = y_pred_df.idxmax(axis=1)
                st.write("Predictions:")
                st.write(predicted_components)
                
                

    else:
        st.write("Please upload a CSV file to make predictions.")
