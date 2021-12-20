import pandas as pd
import numpy as np
from numpy import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import pickle

dataset = pd.read_csv("datasets.csv")

len(dataset)

dataset.shape
dependent_variable = 'yield'
independent_variables = dataset.columns.tolist()
independent_variables.remove(dependent_variable)

x= dataset[independent_variables].values
y = dataset[dependent_variable].values

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.3, random_state= 0)

scaler = MinMaxScaler()
x_train =scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

#fitting the trainning model
mlr = LinearRegression()
mlr.fit(x_train,y_train)
pickle.dump(mlr, open('model.pkl','wb'))

y_pred = mlr.predict(x_test)

math.sqrt(mean_squared_error(y_test,y_pred))
