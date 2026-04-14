Machine Learning Customer Churn Analysis

## 📌 Project Overview

This project focuses on Exploratory Data Analysis (EDA) for a customer churn dataset.
The main goal is to understand customer behavior and identify key factors that influence churn (customer attrition).

This analysis serves as the foundation for building predictive machine learning models for customer retention.

## 📁 Dataset Description

The dataset contains customer-level information including:

Target Variable
Churn: Whether the customer left within the last month (Yes/No)
Services
Phone service, multiple lines, internet service
Online security, backup, device protection
Tech support, streaming TV & movies
Customer Account Information
Tenure (how long they’ve been a customer)
Contract type
Payment method
Monthly charges
Total charges
Demographics
Gender
Senior citizen status
Partner and dependents
🔍 Key Steps in the Analysis
1. Data Loading & Exploration
Initial inspection using .head(), .info(), .describe()
Identification of:
Categorical vs numerical features
Data types inconsistencies
Missing values
2. Data Cleaning
Converted TotalCharges from object → numeric
Handled missing values (coercion + inspection)
Standardized column names
3. Feature Encoding
🔹 Binary Encoding
Converted Yes/No features → 0/1
🔹 One-Hot Encoding (OHE)
Applied to categorical variables with more than 2 categories
4. Correlation Analysis

A correlation heatmap was used to identify relationships between features and churn.

##### 📉 Features negatively correlated with churn:
  - Tenure (-0.35) → Long-term customers are less likely to churn
  - Two-year contract (-0.30) → Strong retention effect
  - One-year contract (-0.18) → Moderate retention
##### 📈 Features positively correlated with churn:
  - Fiber optic internet (+0.31) → Higher churn rate
  - Electronic check payment (+0.30) → Higher churn rate
5. Multicollinearity Check (VIF)
  - Detected multicollinearity among features
  - Important for:
    - Linear models (e.g., Logistic Regression)
    - Feature selection decisions
##### 📊 Key Insights
- Customers with longer tenure are significantly less likely to churn
- Contract type is one of the strongest predictors of churn
- Certain payment methods and services are associated with higher churn
- Data preprocessing (encoding + cleaning) is critical before modeling
##### ⚙️ Tech Stack
- Python 🐍
- Pandas
- NumPy
- Matplotlib / Seaborn
- Jupyter Notebook
##### 🚀 Next Steps
- Build predictive models:
- Logistic Regression
- Random Forest
- Gradient Boosting (XGBoost / LightGBM)
## Apply:
- Feature selection
- Hyperparameter tuning
- Threshold optimization (for recall vs precision trade-offs)
##### 📌 How to Run
# Clone repo
git clone <your-repo-url>

# Install dependencies
pip install -r requirements.txt

# Open notebook
jupyter notebook
💡 Business Impact

Understanding churn drivers helps companies:

Reduce customer loss
Improve retention strategies
Increase lifetime value (LTV)
👨‍💻 Author

Saul Gasca
Software Engineer | Data Scientist
