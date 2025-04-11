import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import requests

#####################################################################################################
#####################################################################################################

st.title('RETAIL STORE ANALYSIS VISUALIZATIONS')

st.header('*EXECUTIVE SUMMARY*', divider='orange')
st.subheader('Business Problem:')
st.markdown("""
An online retail store wants to analyse what the major contributing factors are to the revenue so that they can 
strategically plan for the next year. 
""")
st.subheader('Methodology:')
st.markdown("""
- Drafted questions that could be answered from the dataset given.
- Performed *data wrangling* to bring dataset into a viable form.
- Used *visualization* libraries to answer the drafted questions and get insights from retail data.
""")
st.subheader('Skills:')
st.markdown("""
**Language:** Python \n
**Data Manipulation Library:** NumPy, Pandas \n
**Visualization Libraries:** Matplotlib, Seaborn, Plotly \n
**App & Dashboard Tool:** Streamlit
""")
st.subheader('Results:')
st.markdown("""
- **Top sales countries** include the UK, Netherlands, Ireland, Germany, and France, while Saudi Arabia, Bahrain, South 
Africa, Brazil, and Lebanon rank **lowest in sales**. 
- **Ireland** and **France** show a rise in sales from April to July, with significant drops in August and December. 
**Switzerland** sees generally steady sales with occasional peaks in January, June, and fall, but no sales in December. 
- **Key revenue** comes from a core group of repeat buyers within 2-4 months post-purchase, primarily 
driven by best customers and loyal clients, with fewer high-frequency buyers. 
- The majority of **customer loyalty wanes after six months**. 
- Additionally, **select products contribute more revenue**, while others yield low returns or losses.
""")
st.subheader('Business Recommendations:')
st.markdown("""
- **Customer Retention and Loyalty Programs:** Since most customers tend to repurchase within 2–4 months, design loyalty 
or reminder campaigns that prompt purchases around this timeframe. Emphasize retention tactics before the six-month mark, 
where retention drops significantly.
- **Product Portfolio Optimization:** Increase focus on high-revenue products with dedicated advertising and placement 
strategies. For loss-generating products, consider phasing them out or bundling with more popular items to boost their 
sales potential.
- **Reevaluate Underperforming Products Regularly:** Create a quarterly review of low-performing products, focusing on 
those that contribute less to revenue or go into loss. Determine if they should be discounted, bundled, or phased out 
to streamline the product offering and reduce inventory costs. 
- **Data Driven Promotions for Slow Months:** Run targeted discounts or limited-time offers during historically slower 
months (like August or December in some regions) to drive traffic and increase sales, filling the seasonal gaps in revenue.
""")
st.subheader('Next Steps:')
st.markdown("""
- **Experiment with Targeted Promotions:** Run small-scale A/B tests for campaigns in low-performing regions to gauge 
effectiveness before larger rollouts.
- **Create a Retention Dashboard:** Track retention rates monthly for different customer segments and identify early 
signs of decline.
- **Product Lifecycle Review:** Regularly assess product sales data to optimize the catalog, maximizing profitability 
and customer satisfaction.
""")
####################################################################################################
####################################################################################################
st.header('PROJECT', divider='rainbow')
st.subheader('DATASET', divider='orange')

file_id = "1cOaFCxLFabruDpXDA5r6VmTEtTx2g0ZQ"
download_url = f"https://drive.google.com/uc?id={file_id}&export=download"

# Download the file
response = requests.get(download_url)
if response.status_code == 200:
    # Save the file locally
    with open("data.csv", "wb") as file:
        file.write(response.content)

    # Load the CSV file into a DataFrame
    data = pd.read_csv("data.csv")
    st.write(data)
else:
    st.error("Failed to download the file. Please check the URL or file permissions.")

####################################################################################################
####################################################################################################
# DATA WRANGLING
data = data.dropna()
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

####################################################################################################
####################################################################################################
data2 = data[['Country', 'Quantity']]
data3 = data2.groupby('Country').sum().sort_values(by='Quantity', ascending=False).reset_index()
data4 = data3.head(5)
data5 = data3.tail(5)

####################################################################################################
st.subheader('ANALYSIS', divider='orange')
st.markdown("#### 1) Which Countries have good Online Retail Buying Behaviour?")

fig = px.bar(data4, x='Quantity', y='Country', title='Top 5 Countries by Sale')
# Update the y-axis to reverse the order
fig.update_yaxes(categoryorder='total ascending')
st.plotly_chart(fig)

fig0 = px.bar(data5, x='Quantity', y='Country', title='Bottom 5 Countries by Sale')
st.plotly_chart(fig0)

st.markdown("""
- **UK, Netherlands, EIRE, Germany** and **France** are the top countries by sales.
- **Saudi Arabia, Bahrain, South Africa, Brazil** and **Lebanon** are among the lowest performing countries with respect to 
Sales.
""")
#####################################################################################################
st.markdown("#### 2) Identify Countries generating good Sales Revenue excluding UK")

# create a revenue column
data['Revenue'] = data['UnitPrice'] * data['Quantity']
df = data[['Country', 'Revenue']]
# excluding UK from the list
df = df[df['Country'] != 'United Kingdom']
df0 = df.groupby('Country').sum().sort_values(by='Revenue', ascending=False).reset_index()

fig1 = px.bar(df0, x='Revenue', y='Country', title='Sales Revenue by Country')
# Update the y-axis to reverse the order
fig1.update_yaxes(categoryorder='total ascending')
st.plotly_chart(fig1)

# average sales by country
avg_rev = data.groupby('Country')['Revenue'].mean().sort_values(ascending=False).reset_index()

fig2 = px.bar(avg_rev, x='Revenue', y='Country', title='Average Sales Revenue by Country')
# Update the y-axis to reverse the order
fig2.update_yaxes(categoryorder='total ascending')
st.plotly_chart(fig2)

###################################################################################################
st.markdown("#### 3) Plot sales trends to identify in which months do Sales increase and decrease for EIRE, France and "
            "Switzerland")

# Filter data for specified countries
countries = ['EIRE', 'France', 'Switzerland']
filtered_data = data[data['Country'].isin(countries)]
# Group data by month and country, summing quantities
monthly_sales = filtered_data.groupby([filtered_data['InvoiceDate'].dt.to_period('M'), 'Country'])['Quantity'].sum().reset_index()
# Rename the period column for better readability
monthly_sales.rename(columns={'InvoiceDate': 'Month'}, inplace=True)
# Convert the period to datetime for plotting
monthly_sales['Month'] = monthly_sales['Month'].dt.to_timestamp()
# Create the plot
fig3 = px.line(monthly_sales, x='Month', y='Quantity', color='Country', title='Sales Trend of Quantity by Month and Country')
st.plotly_chart(fig3)

# Filter data for specified countries
countries = ['EIRE', 'France', 'Switzerland']
filtered_data = data[data['Country'].isin(countries)]
# Group data by month and country, summing quantities
monthly_sales = filtered_data.groupby([filtered_data['InvoiceDate'].dt.to_period('M'), 'Country'])['Revenue'].sum().reset_index()
# Rename the period column for better readability
monthly_sales.rename(columns={'InvoiceDate': 'Month'}, inplace=True)
# Convert the period to datetime for plotting
monthly_sales['Month'] = monthly_sales['Month'].dt.to_timestamp()
# Create the plot
fig4 = px.line(monthly_sales, x='Month', y='Revenue', color='Country', title='Sales Trend of Sales Revenue by Month and Country')
st.plotly_chart(fig4)

st.markdown("""
- **EIRE (IRELAND)** and **FRANCE:** We notice a continuous rise and fall in Sales patterns and than in the mid of year 
from April to July, the Sales only tend to increase. In August, sales decrease drastically (a month earlier for France). 
Than through fall and winter till November, the Sales increase. In December the Sales decrease.
- **SWITZERLAND:** Sales seem to be stagnant except experiencing sharp increase in months of January, June and in 
Fall months. However, there're no Sales in December. 
""")
####################################################################################################
st.markdown("#### 4) How Many Times are the Customers buying from us?")

# Calculate customer purchase frequency
customer_frequency = data['CustomerID'].value_counts().reset_index()
customer_frequency.columns = ['CustomerID', 'PurchaseCount']

# Create the histogram using Plotly Express
fig5 = px.histogram(customer_frequency, x='PurchaseCount', nbins=30, title='Customer Purchase Frequency')
fig5.update_layout(xaxis_title='Number of Purchases',
                  yaxis_title='Number of Customers',
                  bargap=0.1)
st.plotly_chart(fig5)

st.markdown("""
- Majority of customers made only a small number of purchases.
- High purchase frequency is rare.
""")
####################################################################################################
st.markdown("#### 5) Which Countries Contribute to 80% of Sales Revenue?")

# Calculate cumulative revenue percentage
df0['CumulativeRevenue'] = df0['Revenue'].cumsum() / df0['Revenue'].sum() * 100

# Create bar trace for revenue by country
bar_trace = go.Bar(x=df0['Country'], y=df0['Revenue'], name='Revenue', marker_color='skyblue')

# Create line trace for cumulative revenue percentage (Pareto line)
line_trace = go.Scatter(x=df0['Country'], y=df0['CumulativeRevenue'], name='Cumulative % Revenue (Pareto)',
                        mode='lines+markers', line=dict(color='red', width=2), yaxis='y2')

# Create the figure with secondary y-axis for the Pareto line
figa = go.Figure(data=[bar_trace, line_trace])

# Set up layout with a secondary y-axis for the cumulative percentage
figa.update_layout(
    title='Country Sales Revenues with Pareto Line',
    xaxis=dict(title='Country'),
    yaxis=dict(title='Revenue'),
    yaxis2=dict(title='Cumulative % Revenue',
                overlaying='y',
                side='right',
                range=[0, 100]  # Ensure the secondary y-axis goes up to 100%
               ),
    shapes=[
        # Add 80% horizontal line for Pareto threshold
        dict(
            type="line",
            xref="paper", yref="y2",
            x0=0, y0=80, x1=1, y1=80,
            line=dict(color="grey", width=1, dash="dash"))
    ],
    annotations=[
        # Add text annotation for 80% line
        dict(
            x=1, y=80, xref="paper", yref="y2",
            text="80%",
            showarrow=False,
            font=dict(color="grey"))
    ])
st.plotly_chart(figa)

st.markdown("""
- **Netherlands, Ireland, Germany, France, Australia, Switzerland, Spain** and **Belgium** contribute to 80% of the Sales 
Revenue.
""")
####################################################################################################
st.markdown("#### 6) What are the Top/Bottom 10 Products contributing to the Sales Revenue? (Excluding UK)")

# Filter out rows where Country is 'UK'
data_filtered = data[data['Country'] != 'United Kingdom']
# Group by StockCode and calculate the sum of Revenue, then sort
prod_rev = data_filtered.groupby('StockCode')['Revenue'].sum().sort_values(ascending=False).reset_index()
prod_top = prod_rev.head(10)
prod_bottom = prod_rev.tail(10)
prod_top_styled = prod_top.style.background_gradient(subset=['Revenue'], cmap='Greens')
st.write(prod_top_styled)
prod_bottom_styled = prod_bottom.style.background_gradient(subset=['Revenue'], cmap='Oranges')
st.write(prod_bottom_styled)

####################################################################################################
st.markdown("#### 7) Understand the overall customer purchasing behaviour  in terms of RFM")

# Calculate customer monetary value
customer_monetary_value = data.groupby('CustomerID')['Revenue'].sum().reset_index()
customer_monetary_value.columns = ['CustomerID', 'MonetaryValue']

# Merge frequency and monetary value
customer_rfm = pd.merge(customer_frequency, customer_monetary_value, on='CustomerID')

# Define quantiles for segmentation
quantiles = customer_rfm[['PurchaseCount', 'MonetaryValue']].quantile([0.25, 0.5, 0.75])

# Segment customers based on quantiles
def segment_customer(row):
    if row['PurchaseCount'] >= quantiles['PurchaseCount'][0.75] and row['MonetaryValue'] >= quantiles['MonetaryValue'][0.75]:
        return 'Best Customers'
    elif row['PurchaseCount'] >= quantiles['PurchaseCount'][0.5] and row['MonetaryValue'] >= quantiles['MonetaryValue'][0.5]:
        return 'Loyal Customers'
    elif row['PurchaseCount'] < quantiles['PurchaseCount'][0.25] and row['MonetaryValue'] < quantiles['MonetaryValue'][0.25]:
        return 'Lost Cheap Customers'
    elif row['PurchaseCount'] >= quantiles['PurchaseCount'][0.75]:
        return 'Big Spender'
    elif row['MonetaryValue'] >= quantiles['MonetaryValue'][0.75]:
        return 'Potential to Become Best Customer'
    elif row['PurchaseCount'] >= quantiles['PurchaseCount'][0.25]:
        return 'Occasional Buyers'
    else:
      return 'Look Out Buyers'

customer_rfm['Segment'] = customer_rfm.apply(segment_customer, axis=1)

# Create the bar chart using Plotly Express
segment_counts = customer_rfm['Segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'CustomerCount']

fig7 = px.bar(segment_counts, x='CustomerCount', y='Segment', orientation='h', title='Customer Segmentation by Segment')
fig7.update_layout(xaxis_title='Number of Customers', yaxis_title='Customer Segment')
fig7.update_yaxes(categoryorder='total ascending')
st.plotly_chart(fig7)

# Prepare the data for the chart
data['InvoiceMonth'] = data['InvoiceDate'].dt.to_period('M')
monthly_revenue = data.groupby(['InvoiceMonth', 'CustomerID'])['Revenue'].sum().reset_index()
monthly_revenue = pd.merge(monthly_revenue, customer_rfm[['CustomerID', 'Segment']], on='CustomerID')
segment_monthly_revenue = monthly_revenue.groupby(['InvoiceMonth', 'Segment'])['Revenue'].sum().reset_index()
# Convert 'InvoiceMonth' to string for serialization
segment_monthly_revenue['InvoiceMonth'] = segment_monthly_revenue['InvoiceMonth'].astype(str) # Convert Period to string

# Create the line chart using Plotly Express
fig8 = px.line(segment_monthly_revenue, x='InvoiceMonth', y='Revenue', color='Segment', title='Monthly Revenue by Customer Segment')
fig8.update_layout(xaxis_title='Month', yaxis_title='Sales Revenue')
st.plotly_chart(fig8)

st.markdown("""
- The store generates most from the **Best Customers** and **Loyal Customers** followed by **Occasional Buyers**.
- The store generates less from **Big Spenders, Lost Cheap Customer, Look Out Buyers** and **Potential to Become Best 
Customers.**
""")
####################################################################################################
st.markdown("#### 8) Identify Products that are Selling High but generating lesser Sales Revenue and Selling Less but generating Highier Sales Revenue ")
st.write('Zoom in on the graph to further analyze:')

fig9 = px.scatter(data, x='Quantity', y='Revenue', color='Description',
                 title='Product-wise Sales Revenue vs Quantity',
                 labels={'Quantity': 'Quantity', 'Revenue': 'Sales Revenue'},
                 hover_data=['Description']) # Show product names on hover
st.plotly_chart(fig9)

####################################################################################################
st.markdown("#### 9) What is the Customer Purchase latency between 1st purchase and 2nd purse?")

# Calculate first purchase month for each customer
data['FirstPurchaseMonth'] = data.groupby('CustomerID')['InvoiceDate'].transform('min').dt.month_name()
# Calculate the time difference in months from the first purchase for each purchase
data['MonthsToRepeatPurchase'] = (data['InvoiceDate'].dt.to_period('M') -
                                  data.groupby('CustomerID')['InvoiceDate'].transform('min').dt.to_period('M')).apply(lambda x: x.n)
# Filter only repeat purchases (exclude first purchase month for each customer)
repeat_purchases = data[data['MonthsToRepeatPurchase'] > 0]
# Define the correct order for months
month_order = ['December', 'November', 'October', 'September', 'August', 'July', 'June', 'May', 'April', 'March', 'February',
              'January']
# Set 'FirstPurchaseMonth' as a categorical type with the specified order
repeat_purchases['FirstPurchaseMonth'] = pd.Categorical(repeat_purchases['FirstPurchaseMonth'], categories=month_order, ordered=True)
# Create a pivot table with the percentage of customers who made repeat purchases per month
pivot_table = pd.pivot_table(repeat_purchases, values='CustomerID',
                             index='FirstPurchaseMonth',
                             columns='MonthsToRepeatPurchase',
                             aggfunc='count',
                             fill_value=0)
# Calculate percentage for each cell relative to the row total
pivot_table = pivot_table.div(pivot_table.sum(axis=1), axis=0) * 100
# Convert to numpy array for Plotly
z_values = pivot_table.values
# Ensure all values are rounded, converted to string, and have a '%' sign appended
z_text = np.array([['{:.1f}%'.format(val) for val in row] for row in z_values])

# Plotly Heatmap
fig10 = go.Figure(data=go.Heatmap(
    z=z_values,
    x=pivot_table.columns.astype(str),  # Month numbers
    y=pivot_table.index,  # First purchase month names
    text=z_text,  # Add percentage text
    texttemplate="%{text}",  # Display text as it is
    colorscale="Blues",
    colorbar=dict(title='Percentage %')))
# Customize layout
fig10.update_layout(title="% of Customers by Month of First Purchase and Months to Repeat Purchase",
                  xaxis_title="Months to Repeat Purchase",
                  yaxis_title="Month of 1st Purchase")

st.plotly_chart(fig10)

st.markdown("""
- The **majority of customers** tend to make repeat purchases within 2–4 months after their first purchase.
- **After 6 months**, the percentages drop significantly, suggesting a decrease in customer retention over time.
- **July** and **August** stand out, especially in the 2nd and 3rd month columns. This could imply that customers who first 
purchase in summer months are more likely to make follow-up purchases within a few months.
- Very **small portion of customers** make purchases beyond 6 months from their initial purchase date, as reflected by 
the low values in later months (9–12). This suggests that the majority of customer loyalty is concentrated in the early 
months.
""")
####################################################################################################
#st.markdown("#### 10) What is the Customer Retention Rate? ")

#image_url1 = "https://raw.githubusercontent.com/maryamtariq-analytics/CohortAnalysis/main/CohortAnalysis2.png"
#st.image(image_url1)

#st.markdown("""
#- We can see that most of customers are not retained as explored above that a large chunk of customers consist of **Occasional
#Buyers, Lost Cheap Customers** and **Look Out Buyers.**
#""")
####################################################################################################
####################################################################################################
st.subheader('BUSINESS RECOMMENDATIONS', divider='orange')
st.markdown("""
- **Customer Retention and Loyalty Programs:** Since most customers tend to repurchase within 2–4 months, design loyalty 
or reminder campaigns that prompt purchases around this timeframe. Emphasize retention tactics before the six-month mark, 
where retention drops significantly.
- **Product Portfolio Optimization:** Increase focus on high-revenue products with dedicated advertising and placement 
strategies. For loss-generating products, consider phasing them out or bundling with more popular items to boost their 
sales potential.
- **Reevaluate Underperforming Products Regularly:** Create a quarterly review of low-performing products, focusing on 
those that contribute less to revenue or go into loss. Determine if they should be discounted, bundled, or phased out 
to streamline the product offering and reduce inventory costs. 
- **Data Driven Promotions for Slow Months:** Run targeted discounts or limited-time offers during historically slower 
months (like August or December in some regions) to drive traffic and increase sales, filling the seasonal gaps in revenue.
""")

####################################################################################################
####################################################################################################
st.subheader('NEXT STEPS', divider='orange')
st.markdown("""
- **Experiment with Targeted Promotions:** Run small-scale A/B tests for campaigns in low-performing regions to gauge 
effectiveness before larger rollouts.
- **Create a Retention Dashboard:** Track retention rates monthly for different customer segments and identify early 
signs of decline.
- **Product Lifecycle Review:** Regularly assess product sales data to optimize the catalog, maximizing profitability 
and customer satisfaction.
""")

####################################################################################################
####################################################################################################
st.divider()