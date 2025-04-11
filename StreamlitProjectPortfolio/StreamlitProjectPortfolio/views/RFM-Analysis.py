import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import plotly.colors
pio.templates.default = 'plotly_white'
from datetime import datetime
import streamlit as st

st.title('RFM ANALYSIS')

st.header('*EXECUTIVE SUMMARY*', divider='orange')
st.subheader('Business Problem:')
st.write("""
Business professionals often require surgical analysis of their users, segmentation wise in order to make efficient 
strategies for retaining and acquiring users for their businesses. These tasks can be done by conducting RFM Analysis 
where its used to understand and segment customers based on their buying behaviour. RFM stands for recency, frequency, 
and monetary value, which are three key metrics that provide information about customer engagement, loyalty, and value 
to a business. 
""")

st.subheader('Methodology:')
st.markdown("""
* Data Wrangling (Converted data into a viable format for use in analysis).
* Calculated RFM values.
* Calculated Recency, Frequency, Monetary Value scores.
* Calculated collective RFM score.
* Created segments (Low Value, Mid Value, High Value) based on RFM scores.
* Created more granular customer segments (Champions, Potential Loyalists, At Risk Customers, Can't Lose, Lost) for 
deeper surgical analysis.
* Analyze RFM segments and distributions made.
""")
st.subheader('Skills:')
st.markdown("""
**Programming Language:** Python \n
**Data Manipulation Libraries:** Pandas,  Datetime \n 
**Visualization Libraries:** Plotly \n
**App and Dashboard Tool:** Streamlit
""")

##########################################################################################################
##########################################################################################################
st.header('PROJECT', divider='rainbow')
st.subheader('DATASET')
url = "https://raw.githubusercontent.com/maryamtariq-analytics/RFM-Analysis/refs/heads/main/rfm_data.csv"
data = pd.read_csv(url)
st.write("E-commerce data is shown below:")
st.write(data)

##########################################################################################################

st.subheader('DATA WRANGLING', divider='orange')

# convert 'purchase date' to datetime
data['PurchaseDate'] = pd.to_datetime(data['PurchaseDate'])

code = """
# convert 'purchase date' to datetime
data['PurchaseDate'] = pd.to_datetime(data['PurchaseDate'])
"""
st.code(code)

##########################################################################################################

st.subheader('Calculating RFM Values', divider='orange')

st.write("""
* ***Recency:*** Subtracted the purchase date from the current date and extracted the number of days. It gives us the 
number of days since the customer’s last purchase, representing their recency value.
* ***Frequency:*** Grouped the data by ‘CustomerID’ and counted the number of unique ‘OrderID’ values to determine the 
number of purchases made by each customer, it gives us the frequency value, representing the total number of purchases 
made by each customer.
* ***Monetary Value:*** Grouped the data by ‘CustomerID’ and summed the ‘TransactionAmount’ values to calculate the 
total amount spent by each customer, it gives us the monetary value, representing the total monetary contribution of 
each customer.
""")

# calculate Recency
data['Recency'] = (datetime.now() - data['PurchaseDate']).dt.days

# calculate Frequency
frequency_data = data.groupby('CustomerID')['OrderID'].count().reset_index()
frequency_data.rename(columns={'OrderID': 'Frequency'}, inplace=True)
data = data.merge(frequency_data, on='CustomerID', how='left')

# calculate Monetary Value
monetary_data = data.groupby('CustomerID')['TransactionAmount'].sum().reset_index()
monetary_data.rename(columns={'TransactionAmount': 'MonetaryValue'}, inplace=True)
data = data.merge(monetary_data, on='CustomerID', how='left')

code0 = """
# calculate Recency
data['Recency'] = (datetime.now() - data['PurchaseDate']).dt.days

# calculate Frequency
frequency_data = data.groupby('CustomerID')['OrderID'].count().reset_index()
frequency_data.rename(columns={'OrderID': 'Frequency'}, inplace=True)
data = data.merge(frequency_data, on='CustomerID', how='left')

# calculate Monetary Value
monetary_data = data.groupby('CustomerID')['TransactionAmount'].sum().reset_index()
monetary_data.rename(columns={'TransactionAmount': 'MonetaryValue'}, inplace=True)
data = data.merge(monetary_data, on='CustomerID', how='left')
"""
st.code(code0)

st.write("""
Looking at the data to look att RFM values calculated:
""")
st.write(data)

#########################################################################################################
st.subheader('Calculating RFM Scores', divider='orange')

st.write("""
* ***Recency:*** Assign scores from 5 to 1 where a higher score indicates a more recent purchase. It means that customers 
who have purchased more recently will receive higher recency scores.
* ***Frequency:*** Assign scores from 1 to 5 where a higher score indicates a higher purchase frequency. Customers who 
made more frequent purchases will receive higher frequency scores.
* ***Monetary Value:*** Assign scores from 1 to 5, where a higher score indicates a higher amount spent by the customer.
""")

# define scoring criteria for each RFM value
recency_scores = [5,4,3,2,1]      # higher score for lower frequency (more recent)
frequency_scores = [1,2,3,4,5]    # higher score for higher frequency
monetary_scores = [1,2,3,4,5]     # higher score for higher monetary value


# calculate RFM scores
data['RecencyScore'] = pd.cut(data['Recency'], bins=5, labels=recency_scores)
data['FrequencyScore'] = pd.cut(data['Frequency'], bins=5, labels=frequency_scores)
data['MonetaryScore'] = pd.cut(data['MonetaryValue'], bins=5, labels=monetary_scores)

# convert RFM scores to numeric types
data['RecencyScore'] = data['RecencyScore'].astype(int)
data['FrequencyScore'] = data['FrequencyScore'].astype(int)
data['MonetaryScore'] = data['MonetaryScore'].astype(int)

code1 = """
# define scoring criteria for each RFM value
recency_scores = [5,4,3,2,1]      # higher score for lower frequency (more recent)
frequency_scores = [1,2,3,4,5]    # higher score for higher frequency
monetary_scores = [1,2,3,4,5]     # higher score for higher monetary value
"""

code2 = """
# calculate RFM scores
data['RecencyScore'] = pd.cut(data['Recency'], bins=5, labels=recency_scores)
data['FrequencyScore'] = pd.cut(data['Frequency'], bins=5, labels=frequency_scores)
data['MonetaryScore'] = pd.cut(data['MonetaryValue'], bins=5, labels=monetary_scores)
"""
code3 = """
# convert RFM scores to numeric types
data['RecencyScore'] = data['RecencyScore'].astype(int)
data['FrequencyScore'] = data['FrequencyScore'].astype(int)
data['MonetaryScore'] = data['MonetaryScore'].astype(int)
"""
st.code(code1)
st.write("""
Define 5 bins for each value and assign the corresponding scores to each bin: 
""")
st.code(code2)
st.write("""
Convert their datatype into integers to further use these scores:
""")
st.code(code3)
#########################################################################################################
st.subheader('RFM Value Segmentation', divider='orange')
st.write("""
Need to calculate the final RFM Score and the value segments according to the scores. To calculate the RFM score, we 
add the scores obtained for recency, frequency and monetary value:
""")

# calculate RFM Score by combining the individual scores
data['RFM_Score'] = data['RecencyScore'] + data['FrequencyScore'] + data['MonetaryScore']

# create RFM segments based on the RFM score
segment_labels = ['Low Value', 'Mid Value', 'High Value']
data['Value Segment'] = pd.qcut(data['RFM_Score'], q=3, labels=segment_labels)

code4 = """
# calculate RFM Score by combining the individual scores
data['RFM_Score'] = data['RecencyScore'] + data['FrequencyScore'] + data['MonetaryScore']
"""
code5 = """
# create RFM segments based on the RFM score
segment_labels = ['Low Value', 'Mid Value', 'High Value']
data['Value Segment'] = pd.qcut(data['RFM_Score'], q=3, labels=segment_labels)
"""
st.code(code4)
st.write("""
Create RFM segments based on the scores. We divided RFM scores into three segments, namely “Low Value”, “Mid Value”, and 
“High Value”:
""")
st.code(code5)
st.write("""
Have a look at the data:
""")
st.write(data)
st.write("""
Let's have a look at the Segment Distribution:
""")

# RFM Segment Distribution
segment_counts = data['Value Segment'].value_counts().reset_index()
segment_counts.columns = ['Value Segment', 'Count']

pastel_colors = px.colors.qualitative.Pastel

# create the bar chart
fig_segment_dist = px.bar(segment_counts, x='Value Segment', y='Count',
                          color='Value Segment', color_discrete_sequence=pastel_colors,
                          title='RFM Value Segment Distribution')

# update the layout
fig_segment_dist.update_layout(xaxis_title='RFM Value Segment',
                              yaxis_title='Count',
                              showlegend=False)

st.plotly_chart(fig_segment_dist)

###########################################################################################################
st.subheader('RFM Customer Segments', divider='orange')

st.write("""
These segments are determined by dividing RFM scores into distinct ranges or groups, allowing for a more granular 
analysis of overall customer RFM characteristics:
""")

# create a new column for RFM customer segments
data['RFM Customer Segments'] = ''

# assign RFM Segments based on RFM Score
data.loc[data['RFM_Score'] >= 9, 'RFM Customer Segments'] = 'Champions'
data.loc[(data['RFM_Score'] >= 6) & (data['RFM_Score'] < 9), 'RFM Customer Segments'] = 'Potential Loyalists'
data.loc[(data['RFM_Score'] >= 5) & (data['RFM_Score'] < 6), 'RFM Customer Segments'] = 'At Risk Customers'
data.loc[(data['RFM_Score'] >= 4) & (data['RFM_Score'] < 5), 'RFM Customer Segments'] = "Can't Lose"
data.loc[(data['RFM_Score'] >= 3) & (data['RFM_Score'] < 4), 'RFM Customer Segments'] = 'Lost'

code6 = """
# create a new column for RFM customer segments
data['RFM Customer Segments'] = ''

# assign RFM Segments based on RFM Score
data.loc[data['RFM_Score'] >= 9, 'RFM Customer Segments'] = 'Champions'
data.loc[(data['RFM_Score'] >= 6) & (data['RFM_Score'] < 9), 'RFM Customer Segments'] = 'Potential Loyalists'
data.loc[(data['RFM_Score'] >= 5) & (data['RFM_Score'] < 6), 'RFM Customer Segments'] = 'At Risk Customers'
data.loc[(data['RFM_Score'] >= 4) & (data['RFM_Score'] < 5), 'RFM Customer Segments'] = "Can't Lose"
data.loc[(data['RFM_Score'] >= 3) & (data['RFM_Score'] < 4), 'RFM Customer Segments'] = 'Lost'
"""
st.code(code6)
st.write("""
These segments, such as “Champions”, “Potential Loyalists”, and “Can’t Lose” provide a more strategic perspective on 
customer behaviour and characteristics in terms of recency, frequency, and monetary aspects.
""")
########################################################################################################
st.subheader('RFM Analysis', divider='orange')

st.write("""
Now let’s analyze the distribution of customers across different RFM customer segments within each value segment:
""")

segment_product_counts = data.groupby(['Value Segment', 'RFM Customer Segments']).size().reset_index(name='Count')

segment_product_counts = segment_product_counts.sort_values('Count', ascending=False)

fig_treemap_segment_product = px.treemap(segment_product_counts,
                                         path=['Value Segment', 'RFM Customer Segments'],
                                         values='Count',
                                         color='Value Segment', color_discrete_sequence=px.colors.qualitative.Pastel,
                                         title='RFM Customer Segments by Value')

st.plotly_chart(fig_treemap_segment_product)

st.write("""
Analyzing the distribution of RFM values within the Champions segment:
""")

# Filter the data to include only the customers in the Champions segment
champions_segment = data[data['RFM Customer Segments'] == 'Champions']

fig1 = go.Figure()
fig1.add_trace(go.Box(y=champions_segment['RecencyScore'], name='Recency'))
fig1.add_trace(go.Box(y=champions_segment['FrequencyScore'], name='Frequency'))
fig1.add_trace(go.Box(y=champions_segment['MonetaryScore'], name='Monetary'))

fig1.update_layout(title='Distribution of RFM Values within Champions Segment',
                  yaxis_title='RFM Value',
                  showlegend=True)

st.plotly_chart(fig1)

st.write("""
Analyzing the correlation of the recency, frequency, and monetary scores within the champions segment:
""")
correlation_matrix = champions_segment[['RecencyScore', 'FrequencyScore', 'MonetaryScore']].corr()

# Visualize the correlation matrix using a heatmap
fig_heatmap = go.Figure(data=go.Heatmap(
                   z=correlation_matrix.values,
                   x=correlation_matrix.columns,
                   y=correlation_matrix.columns,
                   colorscale='Blues',
                   colorbar=dict(title='Correlation')))

fig_heatmap.update_layout(title='Correlation Matrix of RFM Values within Champions Segment')

st.plotly_chart(fig_heatmap)

st.write("""
Analyzing the number of customers in all the segments:
""")

pastel_colors = plotly.colors.qualitative.Pastel

segment_counts = data['RFM Customer Segments'].value_counts()

# Create a bar chart to compare segment counts
fig2 = go.Figure(data=[go.Bar(x=segment_counts.index, y=segment_counts.values,
                            marker=dict(color=pastel_colors))])

# Set the color of the Champions segment as a different color
champions_color = 'rgb(158, 202, 225)'
fig2.update_traces(marker_color=[champions_color if segment == 'Champions' else pastel_colors[i]
                                for i, segment in enumerate(segment_counts.index)],
                  marker_line_color='rgb(8, 48, 107)',
                  marker_line_width=1.5, opacity=0.6)

# Update the layout
fig2.update_layout(title='Comparison of RFM Segments',
                  xaxis_title='RFM Segments',
                  yaxis_title='Number of Customers',
                  showlegend=False)

st.plotly_chart(fig2)

st.write("""
Now let’s have a look at the recency, frequency, and monetary scores of all the segments:
""")
# calculate the average Recency, Frequency, and Monetary scores for each segment
segment_scores = data.groupby('RFM Customer Segments')[['RecencyScore', 'FrequencyScore', 'MonetaryScore']].mean().reset_index()

# Create a grouped bar chart to compare segment scores
fig3 = go.Figure()

# add bars for Recency score
fig3.add_trace(go.Bar(
    x=segment_scores['RFM Customer Segments'],
    y=segment_scores['RecencyScore'],
    name='Recency Score',
    marker_color='rgb(158,202,225)'))

# add bars for Frequency score
fig3.add_trace(go.Bar(
    x=segment_scores['RFM Customer Segments'],
    y=segment_scores['FrequencyScore'],
    name='Frequency Score',
    marker_color='rgb(94,158,217)'))

# add bars for Monetary score
fig3.add_trace(go.Bar(
    x=segment_scores['RFM Customer Segments'],
    y=segment_scores['MonetaryScore'],
    name='Monetary Score',
    marker_color='rgb(32,102,148)'))

# update the layout
fig3.update_layout(
    title='Comparison of RFM Segments based on Recency, Frequency, and Monetary Scores',
    xaxis_title='RFM Segments',
    yaxis_title='Score',
    barmode='group',
    showlegend=True)

st.plotly_chart(fig3)

st.divider()