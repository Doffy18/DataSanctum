# Predictive Maintenance (PdM) Analysis

This project is focused on predictive maintenance (PdM), utilizing data analysis and machine learning techniques to predict and prevent potential machine failures. The analysis leverages multiple datasets related to machine telemetry, errors, maintenance activities, and failure history.

## Project Structure

### Notebook
- **pm.ipynb**: The main Jupyter Notebook where the data is processed, analyzed, and used for predictive modeling.

### Data
The notebook reads the following datasets:
1. **PdM_telemetry.csv**: Telemetry data that records time-series measurements of machine performance.
2. **PdM_errors.csv**: Error logs capturing various issues reported by the machines.
3. **PdM_failures.csv**: A record of machine failures categorized by type.
4. **PdM_maint.csv**: Maintenance logs indicating performed maintenance activities.
5. **PdM_machines.csv**: Metadata about the machines, such as model type and age.

### Key Sections
1. **Data Cleaning**: Handles missing or inconsistent data across the datasets.
2. **Exploratory Data Analysis (EDA)**: Investigates trends and relationships in the data.
3. **Feature Engineering**: Creates new features from raw data to improve model accuracy.
4. **Modeling**: Develops predictive models to estimate the likelihood of failures or errors.

## Installation and Setup

To run this project, ensure you have the following:

### Prerequisites
- Python 3.8 or later
- Jupyter Notebook

### Required Libraries
Install the necessary Python packages using pip:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Running the Notebook
1. Clone this repository or download the project files.
2. Open the terminal or command prompt and navigate to the project directory.
3. Launch Jupyter Notebook:
   ```bash
   jupyter notebook pm.ipynb
   ```
4. Execute the cells in sequence to reproduce the analysis.

## Outcomes
The project aims to:
- Predict machine failures before they occur, minimizing downtime.
- Provide insights for maintenance scheduling.
- Identify critical factors influencing failures through data analysis.



