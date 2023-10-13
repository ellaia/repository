import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import RFECV
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from datetime import datetime

# Load the Excel file into a DataFrame
file_path = "6-data_with_CCC_Not_Null.xlsx"
df = pd.read_excel(file_path)


# 1. Replace missing values with column medians for numeric columns only
for col in df.select_dtypes(include=[np.number]).columns:
    df[col].fillna(df[col].median(), inplace=True)


# 2. Remove outliers using IQR method only for numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns
Q1 = df[numeric_cols].quantile(0.25)
Q3 = df[numeric_cols].quantile(0.75)
IQR = Q3 - Q1
df = df[~((df[numeric_cols] < (Q1 - 4 * IQR)) | (df[numeric_cols] > (Q3 + 4 * IQR))).any(axis=1)]


# 3. Feature selection using RFECV with RandomForest as the estimator
X = df.drop(columns=['CASH_CONVERSION_CYCLE', 'Country', 'Company', 'Year'])
y = df['CASH_CONVERSION_CYCLE']
estimator = RandomForestRegressor()
selector = RFECV(estimator, step=1, cv=5)
selector = selector.fit(X, y)
X_selected = selector.transform(X)
selected_features = X.columns[selector.support_]



# 4. Modeling approaches - Fixed Effects with only selected features


# 4. Modeling approaches
# OLS
X_ols = sm.add_constant(X_selected)
ols_model = sm.OLS(y, X_ols).fit()

# Fixed Effects
df_fixed_effects = df.copy()
df_fixed_effects['Company'] = df_fixed_effects['Company'].astype('category')
df_fixed_effects['Country'] = df_fixed_effects['Country'].astype('category')
X_fixed_effects = sm.add_constant(df_fixed_effects[selected_features])
fe_model = sm.OLS.from_formula(f"CASH_CONVERSION_CYCLE ~ {'+'.join(selected_features)} + C(Company) + C(Country)", data=df_fixed_effects).fit()
fe_model = sm.OLS.from_formula(f"CASH_CONVERSION_CYCLE ~ {'+'.join(selected_features)} + C(Company) + C(Country)", data=df_fixed_effects).fit()

# 5. Performance statistics
ols_r2 = r2_score(y, ols_model.predict(X_ols))
ols_mse = mean_squared_error(y, ols_model.predict(X_ols))

fe_r2 = r2_score(y, fe_model.predict(df_fixed_effects))
fe_mse = mean_squared_error(y, fe_model.predict(df_fixed_effects))

# 6. Save all outputs to Excel
output_filename = f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
with pd.ExcelWriter(output_filename) as writer:
    df.to_excel(writer, sheet_name='Original Data', index=False)
    df_fixed_effects['OLS_CCC_Calculated'] = ols_model.predict(X_ols)
    df_fixed_effects['FixedEffect_CCC_Calculated'] = fe_model.predict(df_fixed_effects)
    df_fixed_effects.to_excel(writer, sheet_name='Cleaned Data', index=False)
    pd.DataFrame(selected_features, columns=['Selected Features']).to_excel(writer, sheet_name='Selected Features', index=False)
    pd.DataFrame(ols_model.params, columns=['OLS Coefficients']).to_excel(writer, sheet_name='OLS Coefficients', index=True)
    pd.DataFrame(fe_model.params, columns=['Fixed Effects Coefficients']).to_excel(writer, sheet_name='Fixed Effects Coefficients', index=True)
    pd.DataFrame({'Model': ['OLS', 'Fixed Effects'], 'R2': [ols_r2, fe_r2], 'MSE': [ols_mse, fe_mse]}).to_excel(writer, sheet_name='Performance Stats', index=False)
    pd.DataFrame({'Model': ['OLS', 'Fixed Effects'], 'P-values': [ols_model.pvalues, fe_model.pvalues], 'T-statistics': [ols_model.tvalues, fe_model.tvalues]}).to_excel(writer, sheet_name='Feature Stats', index=False)
