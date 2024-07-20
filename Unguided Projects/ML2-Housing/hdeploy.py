import pickle
import streamlit as st 
import numpy as np 
import pandas as pd
from sklearn.impute import SimpleImputer


xgbmodel = pickle.load(open('xmodel.pkl','rb'))
rfmodel = pickle.load(open('rfmodel.pkl','rb'))

st.title("House Price Prediction by XGB or Random FOREST")
bar = st.sidebar.radio('Navbar',['Home','XGB','RandomForest'])





if bar == 'Home':
    st.write("HI, welcome to house predictor.Here you can predict the price of house by providing the dataset which should contain certain values for requireed prediction.")
    st.write('here are the values which are necessary for prediction-')
    column_details = {
    "Column": ['LotFrontage', 'LotArea', 'OverallQual', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1', 'BsmtUnfSF', 
               'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'GrLivArea', 'BsmtFullBath', 'FullBath', 'HalfBath', 'TotRmsAbvGrd', 
               'Fireplaces', 'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'MSZoning_RL', 
               'MSZoning_RM', 'LotShape_Reg', 'Neighborhood_NoRidge', 'Neighborhood_NridgHt', 'Neighborhood_StoneBr', 
               'HouseStyle_2Story', 'RoofStyle_Gable', 'RoofStyle_Hip', 'Exterior1st_VinylSd', 'Exterior2nd_VinylSd', 
               'ExterQual_Gd', 'ExterQual_TA', 'Foundation_CBlock', 'Foundation_PConc', 'BsmtQual_Gd', 'BsmtQual_TA', 
               'BsmtExposure_Gd', 'BsmtExposure_No', 'BsmtFinType1_GLQ', 'HeatingQC_TA', 'CentralAir_Y', 'Electrical_SBrkr', 
               'KitchenQual_Gd', 'KitchenQual_TA', 'GarageType_Attchd', 'GarageType_BuiltIn', 'GarageType_Detchd', 
               'GarageFinish_Unf', 'PavedDrive_Y', 'SaleType_New', 'SaleType_WD', 'SaleCondition_Partial'],
    "Description": [
        'Linear feet of street connected to property', 'Lot size in square feet', 'Rates the overall material and finish of the house',
        'Original construction date', 'Remodel date (same as construction date if no remodeling or additions)', 'Masonry veneer area in square feet',
        'Type 1 finished square feet', 'Unfinished square feet of basement area', 'Total square feet of basement area', 'First Floor square feet',
        'Second floor square feet', 'Above grade (ground) living area square feet', 'Basement full bathrooms', 'Full bathrooms above grade',
        'Half baths above grade', 'Total rooms above grade (does not include bathrooms)', 'Number of fireplaces', 'Year garage was built',
        'Size of garage in car capacity', 'Size of garage in square feet', 'Wood deck area in square feet', 'Open porch area in square feet',
        'Residential Low Density', 'Residential Medium Density', 'Regular', 'Northridge', 'Northridge Heights', 'Stone Brook', 'Two story', 'Gable',
        'Hip', 'Vinyl Siding', 'Vinyl Siding', 'Good', 'Average/Typical', 'Cinder Block', 'Poured Concrete', 'Good (90-99 inches)',
        'Typical (80-89 inches)', 'Good Exposure', 'No Exposure', 'Good Living Quarters', 'Average/Typical', 'Yes', 'Standard Circuit Breakers & Romex',
        'Good', 'Typical/Average', 'Attached to home', 'Built-In (Garage part of house - typically has room above garage)', 'Detached from home',
        'Unfinished', 'Paved', 'Home just constructed and sold', 'Warranty Deed - Conventional', 'Home was not completed when last assessed (associated with New Homes)'
        ]
    }
    srt = pd.DataFrame(column_details)
    st.title("Column Details")
    st.table(srt)







elif bar == 'XGB':
    st.title('Prediction by XGBoost')
    
    def preprocess_data(data):
        # Define the correct feature set based on the sample data
        expected_columns = [
            'LotFrontage', 'LotArea', 'OverallQual', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1',
            'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'GrLivArea', 'BsmtFullBath', 'FullBath', 'HalfBath',
            'TotRmsAbvGrd', 'Fireplaces', 'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF',
            'MSZoning_RL', 'MSZoning_RM', 'LotShape_Reg', 'Neighborhood_NoRidge', 'Neighborhood_NridgHt', 'Neighborhood_StoneBr',
            'HouseStyle_2Story', 'RoofStyle_Gable', 'RoofStyle_Hip', 'Exterior1st_VinylSd', 'Exterior2nd_VinylSd',
            'ExterQual_Gd', 'ExterQual_TA', 'Foundation_CBlock', 'Foundation_PConc', 'BsmtQual_Gd', 'BsmtQual_TA',
            'BsmtExposure_Gd', 'BsmtExposure_No', 'BsmtFinType1_GLQ', 'HeatingQC_TA', 'CentralAir_Y', 'Electrical_SBrkr',
            'KitchenQual_Gd', 'KitchenQual_TA', 'GarageType_Attchd', 'GarageType_BuiltIn', 'GarageType_Detchd',
            'GarageFinish_Unf', 'PavedDrive_Y', 'SaleType_New', 'SaleType_WD', 'SaleCondition_Partial'
        ]
        
        # Ensuring that all expected columns are in the data
        for col in expected_columns:
            if col not in data.columns:
                data[col] = 0

        data = data[expected_columns]
        data_numerical = data.select_dtypes(include=[float, int])
        data_numerical.fillna(data_numerical.mean(), inplace=True)
        df = pd.DataFrame(data_numerical, columns=expected_columns)
        df.astype(int, errors='ignore') 
        return df

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)
        processed_data = preprocess_data(new_data)
        st.write(processed_data.shape[1])  # This shows the number of columns in the processed data

    if st.button('Predict'):
        if 'processed_data' in locals():  # Ensure that processed_data exists
            prediction = xgbmodel.predict(processed_data)
            st.write(prediction)
        else:
            st.write("Please upload a CSV file.")



else:
    st.title('Prediction by RandomForest')    
    def preprocess_data(data):
        # Define the correct feature set based on the sample data
        expected_columns = [
            'LotFrontage', 'LotArea', 'OverallQual', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1',
            'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'GrLivArea', 'BsmtFullBath', 'FullBath', 'HalfBath',
            'TotRmsAbvGrd', 'Fireplaces', 'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF',
            'MSZoning_RL', 'MSZoning_RM', 'LotShape_Reg', 'Neighborhood_NoRidge', 'Neighborhood_NridgHt', 'Neighborhood_StoneBr',
            'HouseStyle_2Story', 'RoofStyle_Gable', 'RoofStyle_Hip', 'Exterior1st_VinylSd', 'Exterior2nd_VinylSd',
            'ExterQual_Gd', 'ExterQual_TA', 'Foundation_CBlock', 'Foundation_PConc', 'BsmtQual_Gd', 'BsmtQual_TA',
            'BsmtExposure_Gd', 'BsmtExposure_No', 'BsmtFinType1_GLQ', 'HeatingQC_TA', 'CentralAir_Y', 'Electrical_SBrkr',
            'KitchenQual_Gd', 'KitchenQual_TA', 'GarageType_Attchd', 'GarageType_BuiltIn', 'GarageType_Detchd',
            'GarageFinish_Unf', 'PavedDrive_Y', 'SaleType_New', 'SaleType_WD', 'SaleCondition_Partial'
        ]
        
        # Ensure that all expected columns are in the data
        for col in expected_columns:
            if col not in data.columns:
                data[col] = 0

        data = data[expected_columns]
        data_numerical = data.select_dtypes(include=[float, int])
        data_numerical.fillna(data_numerical.mean(), inplace=True)
        df = pd.DataFrame(data_numerical, columns=expected_columns)
        df.astype(int, errors='ignore')  # Convert columns to integer type if possible
        return df

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)
        processed_data = preprocess_data(new_data)
        st.write(processed_data.shape[1])  # This shows the number of columns in the processed data

    if st.button('Predict'):
        if 'processed_data' in locals():  # Ensure that processed_data exists
            prediction = rfmodel.predict(processed_data)
            st.write(prediction)
        else:
            st.write("Please upload a CSV file.")





