Wholesale Customers Clustering (UCI)

This project performs unsupervised clustering on the UCI Wholesale Customers dataset to discover meaningful customer segments based on annual product spending and basic metadata.[1]

## Project overview

- Goal: Segment wholesale customers into distinct groups using unsupervised learning for downstream marketing and operations strategies.[1]
- Dataset: UCI Wholesale Customers with annual spend on six product categories plus Channel and Region.[1]
- Approach: End-to-end pipeline with EDA, preprocessing, PCA-based dimensionality reduction, and K-Means clustering (k = 2).[1]

## Dataset

- Each row represents a single wholesale customer.[1]
- Numeric spending features (annual): **Fresh**, Milk, Grocery, Frozen, Detergents_Paper, Delicassen (currency unspecified).[1]
- Categorical features:  
  - Channel: 1 = Horeca, 2 = Retail.[1]
  - Region: 1 = Lisbon, 2 = Oporto, 3 = Other.[1]

## Methodology

### Exploratory analysis

- Inspected data types, ranges, and summary statistics using `info()` and `describe()`.[1]
- Visualized distributions with histograms, KDE plots, and boxplots, revealing strong right skew and extreme outliers in spending variables.[1]
- Used a correlation heatmap to identify high correlation among Grocery, Milk, and Detergents_Paper, motivating dimensionality reduction via PCA.[1]
- Explored Channel and Region distributions with value counts and grouped boxplots to understand category-level differences.[1]

### Preprocessing

- Outliers: Removed extreme outliers using IQR/Z-score style rules to stabilize transformations and reduce skew.[1]
- Skew correction: Applied Box–Cox transformation (with +1 shift) on all positive numeric spending columns to obtain approximately symmetric features; stored lambda parameters in the notebook.[1]
- Scaling: Standardized the transformed numeric features using `StandardScaler` prior to PCA and clustering.[1]
- Encoding: One-hot encoded Channel and Region with `drop_first=False` to keep all categories explicit.[1]

The final clustering dataset combined selected PCA components from numeric features with the one-hot encoded Channel and Region dummies.[1]

### Dimensionality reduction (PCA)

- Fitted PCA on scaled, Box–Cox-transformed numeric spending features.[1]
- Used explained variance ratios and scree plots to select components, focusing on the first two for visualization.[1]
- Interpretation:  
  - PC1 acts as an overall spending magnitude axis.[1]
  - PC2 captures product-mix differences between “fresh-oriented” and “packaged-oriented” spending.[1]
- Example transformation: `X_pca = PCA(n_components=2).fit_transform(X_scaled)` for plotting and exploratory clustering.[1]

### Clustering (K-Means)

- Algorithm choice: K-Means chosen as an efficient, interpretable method suited for distance-based clustering after scaling and PCA.[1]
- Model selection:  
  - Elbow method (inertia vs k) and Silhouette score evaluated for k from 2 to 10.[1]
  - Both diagnostics pointed to k = 2 as optimal (clear elbow and highest silhouette around k = 2, consistent with visual separation in PC space).[1]
- Final model:  
  - `KMeans(n_clusters=2, random_state=42)` fitted on PCA components (with experiments including dummies in X).[1]
  - Cluster labels appended as a `Cluster` column to the dataframe.[1]
- Evaluation:  
  - Silhouette score ≈ 0.5, indicating reasonably well-separated clusters.[1]
  - Stability checks with multiple random seeds showed consistent cluster proportions.[1]

## Cluster profiles

### Region distribution

Region counts by cluster:[1]

| Cluster | Region_1 | Region_2 | Region_3 |
|--------|----------|----------|----------|
| 0      | 38       | 20       | 126      |
| 1      | 17       | 10       | 107      |[1]

### Channel distribution

Channel counts by cluster:[1]

| Cluster | Channel_1 | Channel_2 |
|--------|-----------|-----------|
| 0      | 182       | 2         |
| 1      | 50        | 84        |[1]

### Mean feature profile (PCA space)

Cluster-level means from the processed dataframe:[1]

| Cluster | PCA1      | PCA2      | Channel_1 | Channel_2 | Region_1 | Region_2 | Region_3 |
|--------|-----------|-----------|-----------|-----------|----------|----------|----------|
| 0      | -1.200108 | 0.049839  | 0.989130  | 0.010870  | 0.206522 | 0.108696 | 0.684783 |
| 1      | 1.647910  | -0.068436 | 0.373134  | 0.626866  | 0.126866 | 0.074627 | 0.798507 |[1]

## Segment interpretation

### Cluster 0 – Retail / high-volume

- Composition: Heavily dominated by Channel 1 (≈98.9% of members) with a majority of customers in Region 3.[1]
- Behavior: Higher relative spend on grocery, packaged goods, and detergents/paper, consistent with retail and resale activity.[1]
- Business view: Represents supermarkets and retail stores making large, predictable bulk purchases of packaged and household items.[1]

### Cluster 1 – Horeca / fresh-focused

- Composition: Strong Horeca presence, with ≈62.7% Channel 2 customers and a mixed regional distribution.[1]
- Behavior: Greater emphasis on fresh, frozen, and delicatessen products, matching restaurant and café purchasing patterns.[1]
- Business view: Aligns with restaurants, hotels, and cafés that buy fresh ingredients and specialty items more frequently but in smaller per-order volumes.[1]

## Actionable insights

- Retail-focused segment (Cluster 0):  
  - Promote bulk discounts, bundled offers around Grocery and Detergents_Paper, and dedicated account managers for large retail clients.[1]
  - Offer consolidated invoicing and scheduled bulk shipments to streamline operations.[1]

- Horeca-focused segment (Cluster 1):  
  - Provide tight delivery windows, smaller pack sizes, and curated combinations of Fresh, Frozen, and Delicatessen items aligned to menus.[1]
  - Introduce subscription-style replenishment and priority delivery slots for time-sensitive orders.[1]

- Next steps and extensions:  
  - Enrich the dataset with order frequency, temporal patterns, and profitability metrics to build more nuanced segments (e.g., RFM-based clustering).[1]
  - Explore hierarchical clustering or higher k to uncover potential subsegments within retail and Horeca groups, with domain expert validation.[1]

## Limitations

- Cluster boundaries are sensitive to preprocessing choices such as outlier removal strategy, Box–Cox parameters, and scaling decisions.[1]
- The analysis relies only on spending levels plus Channel and Region, without behavioral, profitability, or temporal features.[1]
- Using only two clusters yields a coarse segmentation; more granular segments may exist and should be explored in follow-up work.[1]
