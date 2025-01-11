# Store Sales Analysis and Prediction

## Overview
The `store.ipynb` notebook is a comprehensive project designed for analyzing store sales data and building predictive models. The project extends beyond the notebook, featuring a Power BI dashboard for data visualization and a deployed predictive model using Streamlit for user interaction.

## Features
- **Data Loading**: Reads sales data from `train.csv`.
- **Exploratory Data Analysis (EDA)**: In-depth analysis of sales patterns and trends.
- **Data Processing**: Handles missing values, encodes categorical features, and scales data for modeling.
- **Predictive Modeling**: Utilizes algorithms such as XGBoost and Lasso regression for forecasting sales.
- **Visualization**: Data visualizations within the notebook and an interactive Power BI dashboard.
- **Deployment**: Streamlit application for real-time prediction based on user inputs.

## Prerequisites
Ensure the following are installed in your Python environment:
- Python 3.x
- pandas
- numpy
- matplotlib
- scikit-learn
- xgboost
- streamlit

Additionally, Power BI is required to view and interact with the dashboard.

## Usage
### Notebook
1. Clone this repository or download the `store.ipynb` notebook.
2. Place the `train.csv` file in the same directory as the notebook.
3. Open the notebook using Jupyter Notebook or any compatible IDE.
4. Run the cells sequentially to execute the analysis and modeling.

### Power BI Dashboard
1. Open the Power BI file associated with this project.
2. Interact with the dashboard to explore sales trends and patterns.

### Streamlit Application
1. Run the Streamlit app using the following command:
   ```bash
   streamlit run app.py
   ```
2. Use the web interface to input data and receive sales predictions.

## Dataset
The notebook expects a dataset named `train.csv` containing store sales data. Ensure the file is properly formatted and includes relevant features for analysis and modeling.

## Outputs
The project generates:
- Visualizations and insights into sales data.
- Processed data suitable for predictive modeling.
- Predictive model performance metrics.
- Interactive tools (Power BI dashboard and Streamlit app) for data exploration and prediction.

## Notes
- Customize the notebook and Streamlit app as needed to fit your dataset.
- Update dependencies to the latest versions to avoid compatibility issues.

## Acknowledgments
This project integrates Python, Power BI, and Streamlit to provide a full-stack solution for store sales analysis and prediction.

