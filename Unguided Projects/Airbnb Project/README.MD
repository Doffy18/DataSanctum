# Airbnb Price Prediction - 2026 DS Kickoff

In this new year 2026, kicking off my data science journey with a fun tribute to traditional AI: implementing a simple MLP neural network for Airbnb price prediction, using Random Forest *only* for principled feature selection. Not a heavy modern ML production project—just a light-hearted nod to classic neural nets on a multi-city Airbnb dataset.

## Tech Stack

| Category | Libraries/Packages |
|----------|-------------------|
| Data Processing | pandas, numpy, scikit-learn (preprocessing, scaling) |
| Modeling | scikit-learn (RandomForestRegressor), Pytorch |
| Visualization | matplotlib, seaborn |
| Environment | Python 3.10+, Jupyter Notebook |

## About the Dataset

**Source**: [Kaggle Airbnb Listings (https://www.kaggle.com/datasets/mysarahmadbhat/airbnb-listings-reviews?resource=download)

**Details**:
- ~280k listings across 10 cities (Paris, New York, Istanbul, etc.)
- 33 features: location, host details, amenities, review scores, price
- Target: `price` (normalized to USD via country exchange rates)
- Real-world messiness: missing values, mixed types, extreme outliers

## Dataset Snapshot

Basic preprocessing: outlier capping (IQR), missing value imputation, currency standardization.

## Quick ML Flow

- **EDA**: Price log-transformed (right-skewed), basic univariate/bivariate summaries
- **Features**: Frequency encoding (neighborhood/property_type), one-hot (city/room_type), amenity binarization (>1000 occurrences), host_since → years, log1p on skeweds
- **Selection**: RF feature importance → top ~20 features (city_Istanbul 0.38, bedrooms 0.14, Heating 0.06, threshold 0.0005)

## Models Tested

| Model | R² (Validation) | Quick Take |
|-------|-----------------|------------|
| Random Forest | 0.7886 | Solid baseline for tabular data |
| MLP Neural Net | ~0.72 | Classic dense NN attempt on scaled features |

## Conclusion
Tree-based models naturally beat simple MLPs on tabular data—ensembles handle interactions better than plain dense layers. Fun exercise! RF for feature selection + MLP implementation = nice 2026 warm-up.

