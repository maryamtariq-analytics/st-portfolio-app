import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
from xgboost import XGBRegressor
from xgboost import plot_importance
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_absolute_error
import streamlit as st

st.title('STOCK & SALES ANALYSIS')

st.header('*EXECUTIVE SUMMARY*', divider='orange' )
st.subheader('Business Problem:')
st.markdown("""
A grocery store is facing a supply chain issue. Groceries are highly perishable items. When overstocked, money is wasted 
on excessive storage and waste, but when understocked, we risk losing customers. The store wants to know how to better stock 
the items that they sell. Need to accurately predict the stock levels of products based on sales data and sensor data 
on an hourly basis in order to more intelligently procure products from the suppliers.
""")
st.subheader('Methodology:')
st.markdown("""
- *Exploratory Data Analysis*
- *Data Wrangling* by merging different datasets, data cleaning and removing outliers.
- *Feature Engineering*
- Performed *Grid Search* and *Cross Validation* to determine best set of Model Hyperparameters.
- Applied *Gradient Boosted Regressor* to run analysis.
- *Evaluation of Results* by measuring performance Metrics.
""")
st.subheader('Skills:')
st.markdown("""
**Language:** Python \n
**Data Manipulation Libraries:** NumPy, Pandas, Datetime \n
**Statistics Libraries:** Scikit-Learn, XGBoost \n
**Visualization Library:** Matplotlib, Plotly \n
**App & Dashboard Tool:** Streamlit \n
**Statistics and Analytical Models:** XGBRegressor
""")
st.subheader('Results:')
st.markdown("""
#### EDA Results
- **Fruit & vegetables** are the 2 most frequently bought product categories
- **Non-members** are the most frequent buyers within the store
- **Cash** is the most frequently used payment method
- Almost throughout the day its busy with regards to number of transactions as its a grocery store
#### Variable/Feature Importance Results
- **Unit price** and **temperature** are important in predicting the stock.
- **Product Quantity** and **hour of the day** are also important in predicting the stock.
- **Product categories** was not an important feature in predicting.
""")
st.subheader('Business Recommendations:')
st.markdown("""
- Although cash is the most common, consider promoting the benefits of digital payments (e.g., faster checkout, 
contactless transactions). This could improve operational efficiency and customer experience, especially during busy 
hours.
- Create incentives for non-members to join a membership program. Offer benefits such as discounts, exclusive offers, 
or early access to new products for members. This can increase customer retention and foster brand loyalty.
- Capitalize on the popularity of popular categories by offering promotions or bundles. You could introduce a loyalty 
program that rewards frequent buyers of fruit and vegetables, encouraging repeat purchases.
Implement strategies to reduce checkout congestion during peak hours. Consider self-checkout options or mobile payment 
solutions to speed up transactions.
- Implement an automated stock monitoring system that uses real-time sales data to adjust stock based on the hour and 
quantity sold. This can reduce both overstock and stockouts during peak times.
""")
st.subheader('Next Steps:')
st.markdown("""
- More data is required in order to test this model for production as we need larger samples. With more data and time, 
it can add real value to the business.
- As temperature was significant in predicting, we can also opt to use open source data like weather.
""")
##########################################################################################################
##########################################################################################################
st.header('PROJECT', divider='rainbow')

st.subheader('DATASETS')
st.markdown('#### Sales Data:')
url = "https://raw.githubusercontent.com/maryamtariq-analytics/Sales-StockAnalysis/refs/heads/main/sales.csv"
sales_data = pd.read_csv(url)
sales_data.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
st.write(sales_data)

st.markdown('#### Sensor Stock Data:')
url1 = "https://raw.githubusercontent.com/maryamtariq-analytics/Sales-StockAnalysis/refs/heads/main/sensor_stock_levels.csv"
sensor_stock_data = pd.read_csv(url1)
sensor_stock_data.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
st.write(sensor_stock_data)

st.markdown('#### Sensor Temperature Data:')
url2 = "https://raw.githubusercontent.com/maryamtariq-analytics/Sales-StockAnalysis/refs/heads/main/sensor_storage_temperature.csv"
sensor_temp_data = pd.read_csv(url2)
sensor_temp_data.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
st.write(sensor_temp_data)

# remove missing values
sales_data = sales_data.dropna()
sensor_stock_data = sensor_stock_data.dropna()
sensor_temp_data = sensor_temp_data.dropna()

##########################################################################################################
##########################################################################################################
st.header('EXPLORATORY DATA ANALYSIS', divider='rainbow')

st.subheader('*Frequently Bought Product Categories*')
fig1 = px.histogram(sales_data['category'])
st.plotly_chart(fig1)

st.subheader('*Customer Type*')
fig2 = px.histogram(sales_data['customer_type'])
st.plotly_chart(fig2)

st.subheader('*Payment Type*')
fig3 = px.histogram(sales_data['payment_type'])
st.plotly_chart(fig3)

## MANIPULATIONS FOR PLOTTING 'HOURLY' TIME
sales_data['timestamp'] = pd.to_datetime(sales_data['timestamp'])
sales_data['hour'] = sales_data['timestamp'].dt.hour
# count the number of transactions per hour
hourly_transactions = sales_data.groupby('hour').size().reset_index(name='transaction_count')
# sorting by hours
hourly_transactions = hourly_transactions.sort_values(by='hour')

st.subheader('*Frequent Buying Hours*')
fig4 = px.bar(hourly_transactions, x='hour', y='transaction_count')
st.plotly_chart(fig4)

st.subheader('*EDA* ANALYSIS', divider='orange')
st.markdown("""
- **Fruit & vegetables** are the 2 most frequently bought product categories 
- **Non-members** are the most frequent buyers within the store 
- **Cash** is the most frequently used payment method 
- Almost throughout the day its busy with regards to number of transactions as its a grocery store 
""")
#########################################################################################################
#########################################################################################################

st.header('DATA WRANGLING', divider='rainbow')

st.subheader('MANIPULATING *TIME* FORMATS', divider='orange')
st.markdown('### Converting `timestamp` Column to *datetime* Type:')

# FUNCTION TO CONVERT `timestamp` FORMAT
sales_data['timestamp'] = pd.to_datetime(sales_data['timestamp'])
sensor_stock_data['timestamp'] = pd.to_datetime(sensor_stock_data['timestamp'])
sensor_temp_data['timestamp'] = pd.to_datetime(sensor_temp_data['timestamp'])

code1 = """
sales_data['timestamp'] = pd.to_datetime(sales_data['timestamp'])
sensor_stock_data['timestamp'] = pd.to_datetime(sensor_stock_data['timestamp'])
sensor_temp_data['timestamp'] = pd.to_datetime(sensor_temp_data['timestamp'])
"""
st.code(code1, language='python')

st.markdown('### Converting `timestamp` to Hourly Format:')

sales_data['timestamp'] = sales_data['timestamp'].dt.floor('H')
sensor_stock_data['timestamp'] = sensor_stock_data['timestamp'].dt.floor('H')
sensor_temp_data['timestamp'] = sensor_temp_data['timestamp'].dt.floor('H')

code2 = """
sales_data['timestamp'] = sales_data['timestamp'].dt.floor('H')
sensor_stock_data['timestamp'] = sensor_stock_data['timestamp'].dt.floor('H')
sensor_temp_data['timestamp'] = sensor_temp_data['timestamp'].dt.floor('H')
"""
st.code(code2, language='python')

##############################################################################################################

st.subheader('GROUPING AND AGGREGATING DATA:', divider='orange')
st.write('We want to to aggregate the datasets in order to combine rows which have the same value for `timestamp`. For '
         'the `sales` data, we want to group the data by `timestamp` but also by `product_id`. When we aggregate, we '
         'must choose which columns to aggregate by the grouping. For now, lets aggregate `quantity`:')
sales_agg = sales_data.groupby(['timestamp', 'product_id']).agg({'quantity': 'sum'}).reset_index()
st.markdown('#### *Sales Aggregate:*')
st.write(sales_agg)
st.write('This shows us the average stock percentage of each product at unique hours within the week of sample data. '
         'Finally, for the `sensor_temp_data`, `product_id` does not exist in this table, so we simply need to group by '
         '`timestamp` and aggregate the `temperature`:')
st.write('We now have an aggregated `sales_data` where each row represents a unique combination of hour during which the '
         'sales took place from that weeks worth of data and the `product_id`. We summed the `quantity` and we took the '
         'mean average of the `unit_price`. For the `sensor_stock_data`, we want to group it in the same way and aggregate '
         'the `estimated_stock_pct`:')
stock_agg = sensor_stock_data.groupby(['timestamp', 'product_id']).agg({'estimated_stock_pct': 'mean'}).reset_index()
st.markdown('#### *Stock Aggregate:*')
st.write(stock_agg)
temp_agg = sensor_temp_data.groupby(['timestamp']).agg({'temperature': 'mean'}).reset_index()
st.markdown('#### *Temperature Aggregate:*')
st.write(temp_agg)
st.write('This gives us the average temperature of the storage facility where the produce is stored in the warehouse by '
         'unique hours during the week.')

#################################################################################################################

st.subheader('MERGING DATA SETS', divider='orange')
merged_data = stock_agg.merge(sales_agg, on=['timestamp', 'product_id'], how='left')
st.write(merged_data)
merged_data1 = merged_data.merge(temp_agg, on=['timestamp'], how='left')
st.write(merged_data1)

# combining some more features
product_categories = sales_data[['product_id', 'category']]
product_categories = product_categories.drop_duplicates()
product_price = sales_data[['product_id', 'unit_price']]
product_price = product_price.drop_duplicates()

# continuing merging
merged_data2 = merged_data1.merge(product_categories, on='product_id', how='left')
st.write(merged_data2)
merged_data3 = merged_data2.merge(product_price, on='product_id', how='left')
st.write(merged_data3)

############################################################################################################

st.subheader('DATA CLEANING', divider='orange')
# filling null values in 'quantity' column with 0
merged_data3['quantity'] = merged_data3['quantity'].fillna(0)
code3 = """
# filling null values in 'quantity' column with 0
merged_data3['quantity'] = merged_data3['quantity'].fillna(0)
"""
st.code(code3, language='python')
st.write(merged_data3)
#########################################################################################################

st.subheader('FEATURE ENGINEERING', divider='orange')
st.write("""
Transform data into a numeric format for a machine learning model: 
- `timestamp`: Explode this column into day of week, day of month and hour.
- `category`: Convert it into numeric from its categorical form.
- `product_id`: Drop this column since it will add no value by including it in the predictive model. Hence, we shall 
remove it from the modeling process.
""")
# making new columns from 'timestamp' column
merged_data3['timestamp_day_of_month'] = merged_data3['timestamp'].dt.day
merged_data3['timestamp_day_of_week'] = merged_data3['timestamp'].dt.dayofweek
merged_data3['timestamp_hour'] = merged_data3['timestamp'].dt.hour
merged_data3.drop(columns=['timestamp'], inplace=True)
code4 = """
# making new columns from 'timestamp' column
merged_data3['timestamp_day_of_month'] = merged_data3['timestamp'].dt.day
merged_data3['timestamp_day_of_week'] = merged_data3['timestamp'].dt.dayofweek
merged_data3['timestamp_hour'] = merged_data3['timestamp'].dt.hour
merged_data3.drop(columns=['timestamp'], inplace=True)
"""
st.code(code4, language='python')
st.write(merged_data3)

# converting categorical data into numeric data
merged_data3 = pd.get_dummies(merged_data3, columns=['category'])
code5 = """
# converting categorical data into numeric data
merged_data3 = pd.get_dummies(merged_data3, columns=['category'])
"""
st.code(code5, language='python')
st.write(merged_data3)
# dropping 'product_id' column
merged_data3.drop(columns=['product_id'], inplace=True)
code6 = """
# dropping 'product_id' column
merged_data3.drop(columns=['product_id'], inplace=True)
"""
st.code(code6, language='python')
st.write(merged_data3)
#########################################################################################################
#########################################################################################################

st.header('MODELLING', divider='rainbow')

st.markdown("""
- Use `estimated_stock_pct` as the target variable, since the problem statement was focused on being able to predict the 
stock levels of products on an hourly basis.
""")
# create dependent and independent variables
x = merged_data3.drop(columns=['estimated_stock_pct'])
y = merged_data3['estimated_stock_pct']
code7 = """
# create dependent and independent variables
x = merged_data3.drop(columns=['estimated_stock_pct'])
y = merged_data3['estimated_stock_pct']
"""
st.code(code7, language='python')

# splitting into training and testing data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.24, random_state=42)
code8 = """
# splitting into training and testing data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.24, random_state=42)
"""
st.code(code8)

## hyperparameter grid
#cv_params = {'max_depth': [4,5,6,7,8],
#             'min_child_weight': [1,2,3,4,5],
#             'learning_rate': [75,100,125]}
## instantiate the regressor
#xgb = XGBRegressor(objective='reg:squarederror', random_state=42)
## scoring metric
#scoring = ['neg_mean_absolute_error']
## GridSearch setup
#xgb_cv = GridSearchCV(xgb, cv_params, scoring=scoring, cv=10, refit=False)
code8 = """
# hyperparameter grid
cv_params = {'max_depth': [4,5,6,7,8],
             'min_child_weight': [1,2,3,4,5],
             'learning_rate': [75,100,125]}
# instantiate the regressor
xgb = XGBRegressor(objective='reg:squarederror', random_state=42)
# scoring metric
scoring = ['neg_mean_absolute_error']
# GridSearch setup
xgb_cv = GridSearchCV(xgb, cv_params, scoring=scoring, cv=10, refit=False)
"""
st.code(code8, language='python')

## access the cross validation results
#cv_results = xgb_cv.cv_results_
# get the index of the best score for 'neg_mean_absolute_error'
#best_index = cv_results['rank_test_neg_mean_absolute_error'].argmin()  # best rank corresponds to the lowest error
#best_mae_score = cv_results['mean_test_neg_mean_absolute_error'][best_index]
#best_params = cv_results['params'][best_index]
code9 = """
# access the cross validation results
cv_results = xgb_cv.cv_results_
# get the index of the best score for 'neg_mean_absolute_error'
best_index = cv_results['rank_test_neg_mean_absolute_error'].argmin()  # best rank corresponds to the lowest error
best_mae_score = cv_results['mean_test_neg_mean_absolute_error'][best_index]
best_params = cv_results['params'][best_index]
"""
st.code(code9, language='python')

##################################################################################################################

st.subheader('Metrics', divider='orange')

st.metric(label='#### Best *Mean Absolute Error* Score:', value=0.224)
st.markdown("""
-  An MAE of **0.224** indicates a **moderate level of error**. The average prediction is off by around 22.4% of the 
possible range of values, which could be significant depending on our performance expectations.
""")

st.write("""
#### Best Parameters:
**learning_rate:** 0.1 \n
**max_depth:** 4 \n
**min_child_weight:** 4 \n
**n_estimators:** 75
 """)
##################################################################################################################

st.subheader('Important Features', divider='orange')
image_url = "https://raw.githubusercontent.com/maryamtariq-analytics/Sales-StockAnalysis/main/FeatureImportance.png"
st.image(image_url)

###################################################################################################################
###################################################################################################################
st.header('RESULTS & BUSINESS RECOMMENDATIONS', divider='rainbow')

st.markdown("""
### *RESULTS:*
#### EDA Results
- **Fruit & vegetables** are the 2 most frequently bought product categories
- **Non-members** are the most frequent buyers within the store
- **Cash** is the most frequently used payment method
- **11am** is the busiest hour with regards to number of transactions
#### Variable/Feature Importance Results
- **Unit price** and **temperature** are important in predicting the stock.
- **Product Quantity** and **hour of the day** are also important in predicting the stock.
- **Product categories** was not an important feature in predicting.
### *BUSINESS RECOMMENDATIONS:*
- Although cash is the most common, consider promoting the benefits of digital payments (e.g., faster checkout, 
contactless transactions). This could improve operational efficiency and customer experience, especially during busy 
hours.
- Create incentives for non-members to join a membership program. Offer benefits such as discounts, exclusive offers, 
or early access to new products for members. This can increase customer retention and foster brand loyalty.
- Capitalize on the popularity of popular categories by offering promotions or bundles. You could introduce a loyalty 
program that rewards frequent buyers of fruit and vegetables, encouraging repeat purchases.
Implement strategies to reduce checkout congestion during peak hours. Consider self-checkout options or mobile payment 
solutions to speed up transactions.
- Implement an automated stock monitoring system that uses real-time sales data to adjust stock based on the hour and 
quantity sold. This can reduce both overstock and stockouts during peak times.
""")

##################################################################################################################
##################################################################################################################
st.header('NEXT STEPS', divider='rainbow')
st.markdown("""
- An MAE of 0.224 suggests the model is not perfectly accurate, and there may be room to further tune the model, 
explore additional features to improve its predictive performance or even trying different model architectures.
- More data is required in order to test this model for production as we need larger samples. With more data and time, 
it can add real value to the business.
- As temperature was significant in predicting, we can also opt to use open source data like weather.
""")

##################################################################################################################
##################################################################################################################
st.divider()