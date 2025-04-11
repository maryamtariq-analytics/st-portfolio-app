import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import streamlit as st

st.title('DYNAMIC PRICING MODEL')

st.header('*EXECUTIVE SUMMARY*', divider='orange')
st.subheader('Business Problem:')
st.write("""
Ride hailing services require to maximize revenue and profits by keeping in mind various factors of supply and demand 
of both riders and drivers. In a dynamic pricing strategy, the aim is to maximize revenue and profitability by pricing 
items at the right level that balances supply and demand dynamics. It allows businesses to adjust prices dynamically 
based on factors like time of day, day of the week, customer segments, inventory levels, seasonal fluctuations, 
competitor pricing, and market conditions.
""")

st.subheader('Methodology:')
st.markdown("""
* *Exploratory Data Analysis* (Relation of 'Expected Ride Duration vs. Historical Cost of Ride', Historical Cost of 
Ride Distribution by Vehicle Type, Correlation Matrix).
* Engineered a *Dynamic Pricing Model.*
""")
st.subheader('Skills:')
st.markdown("""
**Programming Language:** Python \n
**Data Manipulation Libraries:** NumPy, Pandas \n 
**Visualization Libraries:** Plotly \n
**App and Dashboard Tool:** Streamlit \n
**Statistics & Machine Learning Library:** Scikit-Learn \n
**Analytical Models:** Random Forest Regressor
""")

########################################################################################################
########################################################################################################
st.header('PROJECT', divider='rainbow')
st.subheader('DATASET')
url = "https://raw.githubusercontent.com/maryamtariq-analytics/Dynamic-Pricing-Model/refs/heads/main/dynamic_pricing.csv"
data = pd.read_csv(url)
st.write("""
Ride hailing service data:
""")
st.write(data)

##########################################################################################################
st.subheader('EXPLORATORY DATA ANALYSIS', divider='orange')

fig = px.scatter(data, x='Expected_Ride_Duration', y='Historical_Cost_of_Ride',
                title='Expected Ride Duration vs. Historical Cost of Ride',
                trendline='ols')
st.plotly_chart(fig)

fig1 = px.box(data, x='Vehicle_Type', y='Historical_Cost_of_Ride',
             title='Historical Cost of the Ride Distribution by Vehicle Type')
st.plotly_chart(fig1)

st.write("###### CORRELATION MATRIX")
corr_matrix = data.corr(numeric_only=True)
st.write(corr_matrix)

fig2 = go.Figure(data=go.Heatmap(z = corr_matrix.values,
                                 x = corr_matrix.columns,
                                 y = corr_matrix.columns,
                                 colorscale = 'Blues'))

fig2.update_layout(title='Correlation Matrix')
st.plotly_chart(fig2)

###########################################################################################################
st.subheader('DYNAMIC PRICING STRATEGY', divider='orange')
st.write("Now need to implement a dynamic pricing strategy aiming to adjust the ride costs dynamically based on the demand "
         "and supply levels observed in the data. It will capture high-demand periods and low-supply scenarios to "
         "increase prices, while low-demand periods and high-supply situations will lead to price reductions.")
st.write("""
* Calculate the ***Demand Multiplier*** by comparing the number of riders to percentiles representing high and low 
demand levels. If the number of riders exceeds the percentile for high demand, the demand multiplier is set as the 
number of riders divided by the high-demand percentile. Otherwise, if the number of riders falls below the percentile 
for low demand, the demand multiplier is set as the number of riders divided by the low-demand percentile.
* Calculated the ***Supply Multiplier*** by comparing the number of drivers to percentiles representing high and low supply 
levels. If the number of drivers exceeds the low-supply percentile, the supply multiplier is set as the high-supply 
percentile divided by the number of drivers. On the other hand, if the number of drivers is below the low-supply 
percentile, the supply multiplier is set as the low-supply percentile divided by the number of drivers.
""")
# calculate demand multiplier based on percentile for high and low demand
high_demand_percentile = 75
low_demand_percentile = 25

data['demand_multiplier'] = np.where(data['Number_of_Riders'] > np.percentile(data['Number_of_Riders'], high_demand_percentile),
                                     data['Number_of_Riders'] / np.percentile(data['Number_of_Riders'], high_demand_percentile),
                                     data['Number_of_Riders'] / np.percentile(data['Number_of_Riders'], low_demand_percentile))

# calculate supply_multiplier based on percentile for high and low supply
high_supply_percentile = 75
low_supply_percentile = 25

data['supply_multiplier'] = np.where(data['Number_of_Drivers'] > np.percentile(data['Number_of_Drivers'], low_supply_percentile),
                                     np.percentile(data['Number_of_Drivers'], high_supply_percentile) / data['Number_of_Drivers'],
                                     np.percentile(data['Number_of_Drivers'], low_supply_percentile) / data['Number_of_Drivers'])

# define price adjustment factors for high and low demand/supply
demand_threshold_high = 1.2
demand_threshold_low = 0.8
supply_threshold_high = 0.8
supply_threshold_low = 1.2

# calculate adjusted_ride_cost for dynamic pricing
data['adjusted_ride_cost'] = data['Historical_Cost_of_Ride'] * (np.maximum(data['demand_multiplier'], demand_threshold_low) * np.maximum(data['supply_multiplier'], supply_threshold_high))

code = """
# calculate demand multiplier based on percentile for high and low demand
high_demand_percentile = 75
low_demand_percentile = 25

data['demand_multiplier'] = np.where(data['Number_of_Riders'] > np.percentile(data['Number_of_Riders'], high_demand_percentile),
                                     data['Number_of_Riders'] / np.percentile(data['Number_of_Riders'], high_demand_percentile),
                                     data['Number_of_Riders'] / np.percentile(data['Number_of_Riders'], low_demand_percentile))

# calculate supply_multiplier based on percentile for high and low supply
high_supply_percentile = 75
low_supply_percentile = 25

data['supply_multiplier'] = np.where(data['Number_of_Drivers'] > np.percentile(data['Number_of_Drivers'], low_supply_percentile),
                                     np.percentile(data['Number_of_Drivers'], high_supply_percentile) / data['Number_of_Drivers'],
                                     np.percentile(data['Number_of_Drivers'], low_supply_percentile) / data['Number_of_Drivers'])


"""
st.code(code)
st.write("""
Now the goal is to adjust ride prices upward during high demand/low supply and downward during low demand/high supply, 
but with safeguards to prevent extreme price fluctuations. Following are the thresholds we use:
* **demand_threshold_high** = 1.2: The minimum multiplier applied during high demand (prevents prices from dropping too 
low even if demand is high).
* **demand_threshold_low** = 0.8: The minimum multiplier applied during low demand (prevents prices from dropping below 
80% of historical cost).
* **supply_threshold_high** = 0.8: The minimum multiplier applied during high supply (prevents prices from dropping too 
low even if drivers are abundant).
* **supply_threshold_low** = 1.2: The minimum multiplier applied during low supply (not directly used here, but sets a 
floor for extreme scarcity). \n
**Demand Multiplier** and **Supply Multiplier** are capped at 0.8 to limit price reductions. \n
The final price is a product of the two multipliers, ensuring both demand and supply influence the adjustment.
""")
codeminusinfinity = """
# define price adjustment factors for high and low demand/supply
demand_threshold_high = 1.2
demand_threshold_low = 0.8
supply_threshold_high = 0.8
supply_threshold_low = 1.2

# calculate adjusted_ride_cost for dynamic pricing
data['adjusted_ride_cost'] = data['Historical_Cost_of_Ride'] * (np.maximum(data['demand_multiplier'], demand_threshold_low) * np.maximum(data['supply_multiplier'], supply_threshold_high))
"""
st.code(codeminusinfinity)

st.write("Looking at the data gain:")
st.write(data)

st.write("##### PROFIT PERCENTAGE WE GOT AFTER IMPLEMENTING DYNAMIC PRICING STRATEGY:")

# calculate the profit percentage for each ride
data['profit_percentage'] = ((data['adjusted_ride_cost'] - data['Historical_Cost_of_Ride']) / data['Historical_Cost_of_Ride']) * 100

# identify profitable rides where profit percentage is positive
profitable_rides = data[data['profit_percentage'] > 0]
# identify loss rides where profit percentage is negative
loss_rides = data[data['profit_percentage'] < 0]

# calculate the count of profitable and loss rides
profitable_count = len(profitable_rides)
loss_count = len(loss_rides)

# create a donut chart to show the distribution of profitable and loss rides
labels = ['Profitable Rides', 'Loss Rides']
values = [profitable_count, loss_count]

fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
fig3.update_layout(title='Profitability of Rides (Dynamic Pricing vs Historical Pricing)')
st.plotly_chart(fig3)

st.write("""
Now let’s have a look at the relationship between the expected ride duration and the cost of the ride based on the 
dynamic pricing strategy:
""")

fig4 = px.scatter(data,
                 x='Expected_Ride_Duration',
                 y='adjusted_ride_cost',
                 title='Expected Ride Duration vs. Cost of Ride',
                 trendline='ols')

st.plotly_chart(fig4)

###########################################################################################################
st.subheader('TRAINING A PREDICTIVE MODEL', divider='orange')

st.write("Data preprocessing pipeline to preprocess the data:")
def data_preprocessing_pipeline(data):
    # identify numerical and categorical features
    numeric_features = data.select_dtype(include=['float', 'int']).columns
    categorical_features = data.select_dtype(include['object']).columns

    # handle missing values in numeric features
    data[numeric_features] = data[numeric_features].fillna(data[numeric_features].mean())

    # detect and handle outliers in numeric features using IQR
    for feature in numeric_features:
        Q1 = data[feature].quantile(0.25)
        Q3 = data[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)
        data[feature] = np.where((data[feature] < lower_bound) | (data[feature] > upper_bound),
                                 data[feature].mean(),
                                 data[feature])

    # handle missing values in categorical features
    data[categorical_features] = data[categorical_features].fillna(data[categorical_features].mode().iloc[0])

    return data

code0 = """
def data_preprocessing_pipeline(data):
    # identify numerical and categorical features
    numeric_features = data.select_dtype(include=['float', 'int']).columns
    categorical_features = data.select_dtype(include['object']).columns
    
    # handle missing values in numeric features
    data[numeric_features] = data[numeric_features].fillna(data[numeric_features].mean())
    
    # detect and handle outliers in numeric features using IQR 
    for feature in numeric_features:
        Q1 = data[feature].quantile(0.25)
        Q3 = data[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)
        data[feature] = np.where((data[feature] < lower_bound) | (data[feature] > upper_bound),
                                data[feature].mean(),
                                data[feature])
        
    # handle missing values in categorical features
    data[categorical_features] = data[categorical_features].fillna(data[categorical_features].mode().iloc[0])
    
    return data
"""
st.code(code0)

st.write("As vehicle type is a valuable factor, we need to convert it into a numerical feature:")
data['Vehicle_Type'] = data['Vehicle_Type'].map({'Premium': 1, 'Economy': 0})
code1 = """
data['Vehicle_Type'] = data['Vehicle_Type'].map({'Premium': 1, 'Economy': 0})
"""
st.code(code1)
st.write(data)

# splitting data
x = np.array(data[["Number_of_Riders", "Number_of_Drivers", "Vehicle_Type", "Expected_Ride_Duration"]])
y = np.array(data[['adjusted_ride_cost']])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# reshape y to 1D array
y_train = y_train.ravel()
y_test = y_test.ravel()
code2 = """
# splitting data
x = np.array(data[["Number_of_Riders", "Number_of_Drivers", "Vehicle_Type", "Expected_Ride_Duration"]])
y = np.array(data[['adjusted_ride_cost']])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# reshape y to 1D array
y_train = y_train.ravel()
y_test = y_test.ravel()
"""
st.code(code2)
# training a Random Forest Regression Model
model = RandomForestRegressor()
model.fit(x_train, y_train)
code3 = """
# training a Random Forest Regression Model
model = RandomForestRegressor()
model.fit(x_train, y_train)
"""
st.code(code3)

st.write("Test the model using some input values:")


def get_vehicle_type_numeric(vehicle_type):
    vehicle_type_mapping = {'Premium': 1,
                            'Economy': 0}

    vehicle_type_numeric = vehicle_type_mapping.get(vehicle_type)

    return vehicle_type_numeric


# predicting using user input
def predict_price(number_of_riders, number_of_drivers, vehicle_type, expected_ride_duration):
    vehicle_type_numeric = get_vehicle_type_numeric(vehicle_type)
    if vehicle_type_numeric is None:
        raise ValueError('Invalid vehicle type')

    input_data = np.array([[number_of_riders, number_of_drivers, vehicle_type_numeric, expected_ride_duration]])
    predicted_price = model.predict(input_data)

    return predicted_price
code4 = """
def get_vehicle_type_numeric(vehicle_type):
    vehicle_type_mapping = {'Premium': 1,
                           'Economy': 0}
    
    vehicle_type_numeric = vehicle_type_mapping.get(vehicle_type)
    
    return vehicle_type_numeric

# predicting using user input
def predict_price(number_of_riders, number_of_drivers, vehicle_type, expected_ride_duration):
    vehicle_type_numeric = get_vehicle_type_numeric(vehicle_type)
    if vehicle_type_numeric is None:
        raise ValueError('Invalid vehicle type')
        
    input_data = np.array([[number_of_riders, number_of_drivers, vehicle_type_numeric, expected_ride_duration]])
    predicted_price = model.predict(input_data)
    
    return predicted_price
"""
st.code(code4)

# Example prediction using user input values
user_number_of_riders = 50
user_number_of_drivers = 25
user_vehicle_type = "Economy"
Expected_Ride_Duration = 30

predicted_price = predict_price(user_number_of_riders, user_number_of_drivers, user_vehicle_type, Expected_Ride_Duration)
code5 = """
# Example prediction using user input values
user_number_of_riders = 50
user_number_of_drivers = 25
user_vehicle_type = "Economy"
Expected_Ride_Duration = 30

predicted_price = predict_price(user_number_of_riders, user_number_of_drivers, user_vehicle_type, Expected_Ride_Duration)
"""
st.code(code5)
st.write('***Predicted Price:***', predicted_price)

st.write("#### COMPARISON OF ACTUAL & PREDICTED RESULTS:")

# predict on test set
y_pred = model.predict(x_test)
code6 = """
# predict on test set
y_pred = model.predict(x_test)
"""
st.code(code6)

# create a scatter plot with actual vs predicted values
fig5 = go.Figure()

fig5.add_trace(go.Scatter(x=y_test.flatten(), y=y_pred, mode='markers', name='Actual vs Predicted'))

# add a line representing the ideal case
fig5.add_trace(go.Scatter(x=[min(y_test.flatten()), max(y_test.flatten())], y=[min(y_test.flatten()), max(y_test.flatten())],
                         mode='lines', name='Ideal', line=dict(color='red', dash='dash')))

fig5.update_layout(title='Actual vs Predicted Values', xaxis_title='Actual Values', yaxis_title='Predicted Values',
                  showlegend=True)
st.plotly_chart(fig5)

st.divider()