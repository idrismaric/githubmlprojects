# -*- coding: utf-8 -*-
"""price-predictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ska6gKK5shSPSpFnibpz_9RH0xuvVwrg
"""
!pip install xgboost

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

from google.colab import drive
drive.mount('/content/drive/')

# %cd '/content/drive/MyDrive/'

data_load = pd.read_csv('Transactions.csv')

print('\033[1mData loaded\033[0m')

data_load = data_load[data_load['trans_group_en'] == 'Sales']

data = data_load.sample(n=30000)

data['square_feet_area'] = data['procedure_area']*10.77

data_ml = data[['procedure_name_en', 'property_type_en', 'property_sub_type_en', 'reg_type_en', 'area_name_en', 'building_name_en', 'project_name_en', 'master_project_en', \
                'nearest_landmark_en','nearest_metro_en', 'nearest_mall_en', 'rooms_en', 'has_parking', 'square_feet_area' ,'no_of_parties_role_1' , 'no_of_parties_role_2',
      'no_of_parties_role_3','actual_worth']]

categorical_columns = data_ml.select_dtypes(include=['object']).columns

data_ml[categorical_columns] = data_ml[categorical_columns].fillna(data_ml[categorical_columns].mode().iloc[0])

data_ml= data_ml.fillna(data_ml.median())

cat_cols = data_ml.select_dtypes(include=['object']).columns.tolist()

data_ml = pd.get_dummies(data_ml, columns=cat_cols)

print('\033[1mPerformed Data pre-processing\033[0m')
print('\033[1mSelecting X and y to train\033[0m')

x =  data_ml.drop('actual_worth', axis = 1)
X =x.values

y = data_ml['actual_worth'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

xgb_model = xgb.XGBRegressor()

print('\033[1mFitting the model...\033[0m')
print('\033[1mThis will take some time. So stick with us...\033[0m')

xgb_model.fit(X_train, y_train)

print('Model successfully fit')
y_pred = xgb_model.predict(X_test)

print('\033[1mPrinting RMSE and Regressor score to assess accuracy\033[0m')
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"RMSE: {rmse}")

r2 = r2_score(y_test,y_pred)
print('Regressor Score is =',r2)
