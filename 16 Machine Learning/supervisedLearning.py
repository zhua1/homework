# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import Lasso, Ridge, ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn import ensemble
import seaborn as sns

# Read data in 
f = pd.read_csv('kc_house_data.csv')
# Get house age column, at the time of record
f['Record Year'] = pd.to_datetime(f['date']).dt.year
f['Age'] = f['Record Year'] - f['yr_built']
f['sqft_ratio'] = f['sqft_living'] / f['sqft_living15']
f['lot_ratio'] = f['sqft_lot'] / f['sqft_lot15']

# Get correlation
corr_matrix = f.corr()
# Pick columns that are most relevant
col = ['zipcode', 'bedrooms', 'bathrooms', 'Age', 'sqft_living', 'lot_ratio', 'sqft_ratio', 'sqft_lot', 'waterfront', 'grade', 'condition', 'view', 'sqft_basement']
X = f[col]
y = f['price']

X = pd.get_dummies(X, columns = ['zipcode', 'grade', 'Age', 'view', 'condition'])

# train and test part
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state = 42)
## Define the model
#model = LinearRegression()
## Fit the model to training data
#model.fit(X_train, y_train)
## Predict on train and test sets
#y_train_pred = model.predict(X_train)
#y_test_pred = model.predict(X_test)
#
## Linear Regression
#print('Train R^2:',r2_score(y_train, y_train_pred))
#print('Test R^2:',r2_score(y_test, y_test_pred))
#print('Train RMSE:',mean_squared_error(y_train, y_train_pred)**.5)
#print('Test RMSE:',mean_squared_error(y_test, y_test_pred)**.5)
#Train R^2: 0.8383813490474585
#Test R^2: 0.8357893010148014
#Train RMSE: 145310.88294919417
#Test RMSE: 157558.98447877436




# Lasso
lasso = Lasso(random_state=42)
lasso.fit(X_train, y_train)
y_pred_lasso = lasso.predict(X_test)

RMSE_Lasso = mean_squared_error(y_test, y_pred_lasso)**.5
r2_Lasso = r2_score(y_test, y_pred_lasso)

print('Lasso RMSE', RMSE_Lasso)
print('Lasso R^2', r2_Lasso)
#Lasso RMSE 157550.89165075365
#Lasso R^2 0.8358061695522704

coeff = pd.DataFrame(X_train.columns)

coeff['Coefficient Estimates'] = pd.Series(lasso.coef_)

coeff














# Highest R^2 (accuracy score)-------------------------------------------------------------------------------------#
f = pd.read_csv('kc_house_data.csv')
X = f.drop(['id', 'price', 'date', 'zipcode'], axis=1)
y = f['price']

# train and test part
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state = 42)

## Try ensemble
model = ensemble.GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2, learning_rate = .1, loss = 'ls', random_state = 42)

model.fit(X_train, y_train)

model.score(X_test, y_test)
# Ensemble R^2: 0.87544182776095

# test-size: .1, random_state: 2, clf.score = 0.9206329971855278

model.get_params()

model.predict(X.loc[0].values.reshape(1, -1))






# See how pricing is distributed
sns.distplot(y)
plt.show()

# Use data transformation to normalize the data
# Using log to normalize: lessen the impact of outliers
sns.distplot(np.log(y))
plt.show()


plt.scatter(f['sqft_living'], f['price'])
plt.show()

# Feature Engineering: make more variables elsewhere
f['sqft_ratio'] = f['sqft_living'] / f['sqft_living15']

# Converting categories to dummies
col = ['bathrooms', 'sqft_living', 'sqft_ratio', 'grade', 'zipcode']

X = f[col]

X = pd.get_dummies(X, columns = ['zipcode'])

# train and test part
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state = 42)

# Define the model
model = LinearRegression()

# Fit the model to training data
model.fit(X_train, y_train)

# Predict on train and test sets
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Print R^2 Scores
print('Train R^2:',r2_score(y_train, y_train_pred))
print('Test R^2:',r2_score(y_test, y_test_pred))

print('Train RMSE:',mean_squared_error(y_train, y_train_pred)**.5)
print('Test RMSE:',mean_squared_error(y_test, y_test_pred)**.5)


# create dataframe
pd.DataFrame({'true_values': y_train, 'predicted': y_train_pred, 'price_diff': y_train - y_train_pred})





# Print Coefficients
model_features = X.columns
print(list(zip(model.coef_, model_features)))








# Define the model
lasso = Lasso(random_state=42)
lasso.fit(X_train, y_train)
y_pred_lasso = lasso.predict(X_test)

RMSE_Lasso = mean_squared_error(y_test, y_pred_lasso)**.5
r2_Lasso = r2_score(y_test, y_pred_lasso)

print('Lasso RMSE', RMSE_Lasso)
print('Lasso R^2', r2_Lasso)

# Define the model
ridge = Ridge(random_state=42)
ridge.fit(X_train, y_train)
y_pred_ridge = ridge.predict(X_test)

RMSE_ridge = mean_squared_error(y_test, y_pred_ridge)**.5
r2_ridge = r2_score(y_test, y_pred_ridge)

print('Ridge RMSE', RMSE_ridge)
print('Ridge R^2', r2_ridge)


# Define the model
elastic_net = ElasticNet(random_state=42)
elastic_net.fit(X_train, y_train)
y_pred_elastic = elastic_net.predict(X_test)

RMSE_elastic = mean_squared_error(y_test, y_pred_elastic)**.5
r2_elastic = r2_score(y_test, y_pred_elastic)

print('Elastic Net RMSE', RMSE_elastic)
print('Elastic Net R^2', r2_elastic)


# K neighbors
knn = KNeighborsRegressor(n_neighbors = 8)

knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

RMSE_knn = mean_squared_error(y_test, y_pred_knn)**.5
r2_knn = r2_score(y_test, y_pred_knn)

print('KNN RMSE', RMSE_knn)
print('KNN R^2', r2_knn)