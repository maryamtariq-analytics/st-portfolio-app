import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import streamlit as st
import requests

st.title('CUSTOMER RETENTION COHORT ANALYSIS')

st.header('*EXECUTIVE SUMMARY*', divider='orange')
st.subheader('Business Problem:')
st.write("""
The business is noticing a decline in customer retention over time and is unsure which factors are driving this trend. 
Using cohort analysis, the goal is to identify patterns in customer retention behavior, track how different cohorts of 
customers engage with the product or service over time, and find opportunities to enhance retention and reduce churn.
""")

st.subheader('Methodology:')
st.markdown("""
- *Data Wrangling* (cleaning data, date manipulation).
- Conducted *Retention Cohort Analysis* (using Time and Behaviour patterns).
- Interpreted Results.
""")
st.subheader('Skills:')
st.markdown("""
**Programming Language:** Python \n
**Data Manipulation Libraries:** Pandas \n 
**Visualization Libraries:** Seaborn, Matplotlib \n
**App and Dashboard Tool:** Streamlit \n
**Statistics:** Aggregating
""")
st.subheader('Results:')
st.markdown("""
***1. Initial Drop in Retention (CohortIndex 1 to 2)***
- Across all cohorts, the retention drops drastically from **100%** in the first month to around **20-40%** by the 
second month (CohortIndex 2). \n
***2. Long-term Retention (After Month 2)***
- After the second month, retention continues to decline but at a slower rate.
- For example, in the **January 2011** cohort, retention falls from 24% in the second month to 13% by the 12th month. \n
***3. Variation in Cohorts***
- Some cohorts retain customers better than others over time. For example, the **December 2010** cohort maintains 
retention levels higher than many other cohorts after 6-7 months.
- In contrast, the **June 2011** cohort shows a significant drop in retention early on, with 10% retention by the fourth 
month. \n
***4. Churn Patterns***
- For most cohorts, retention drops significantly after 2-4 months and stabilizes at lower percentages in subsequent 
months. This suggests that the **critical time to focus on reducing churn** may be within the first few months. \n
***5. Potential Outliers***
- Some months, like **August 2011**, exhibit relatively better retention in the longer term (12% after 12 months). This 
could indicate that some events or strategies implemented during those months had a positive effect on long-term 
retention.
- We can see that **December 2010** has an Outlier where 50% are still active at almost the year mark.
""")
st.subheader('Business Recommendations:')
st.write("""
- **Early Churn:** Since most of the cohorts experience a sharp drop in retention between the 1st and 2nd months, the 
business should focus on engaging customers **immediately after their first purchase**. Initiatives like onboarding 
programs, discounts, or personalized recommendations could help reduce early churn.
- **Critical Retention Period:** Since retention declines sharply in the first few months (typically up to 4 months), 
strategies to boost engagement and customer satisfaction during this time could have a strong impact on overall 
retention rates.
- **Cohort-specific Analysis:** Some cohorts perform better than others. The business should investigate what actions 
or promotions were happening in months like **December 2010** or **August 2011**, where retention is relatively higher, 
and replicate those successful strategies for other cohorts.
- **Long-term Engagement:** After around 6 months, retention stabilizes for most cohorts, albeit at a much lower level. 
Offering loyalty programs or incentives for customers to return periodically could help maintain engagement over the 
long term.
""")
st.subheader('Next Steps:')
st.markdown("""
- **Analyze Other Variables:** Examine additional factors (e.g., customer demographics, purchase categories, acquisition 
channels, marketing tactics) to see if certain groups or segments have better retention. This can reveal deeper insights 
into why certain cohorts retain better. 
- **Segment Analysis:** Look into Demographic segmentation and Behavioral segmentation.
- **Predictive Modelling:** Build a machine learning model to predict customer churn based on the cohort analysis data. 
Use features like: time since last purchase, total number of purchases, demographic and behavioral variables.
- **A/B Testing of Retention Strategies:** Implement the retention strategies (e.g., loyalty programs, re-engagement 
campaigns, personalized offers) and run A/B tests to measure the impact on customer retention for different cohorts.
""")
##############################################################################################################
##############################################################################################################
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

##############################################################################################################
st.subheader('DATA WRANGLING', divider='orange')

# convert to date to 'datetime'
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
code = """
# convert to date to 'datetime'
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
"""
st.code(code)

# drop rows with no customer id
data = data.dropna(subset=['CustomerID'])
code0 = """
# drop rows with no customer id
data = data.dropna(subset=['CustomerID'])
"""
st.code(code0)

# function for getting month
def get_month(x):
    return dt.datetime(x.year, x.month, 1)

st.write("We will make a new column indicating just the **month** and the **year** and will pass 1 in place of "
         "day to only make month and year remain prominent in this column:")
# apply the function
data['InvoiceMonth'] = data['InvoiceDate'].apply(get_month)
code1 = """
# function for getting month
def get_month(x):
    return dt.datetime(x.year, x.month, 1)

# apply the function
data['InvoiceMonth'] = data['InvoiceDate'].apply(get_month)
"""
st.code(code1)

st.write(data)
#################################################################################################################
#################################################################################################################
st.header('COHORT ANALYSIS', divider='rainbow')

st.markdown("#### Getting *Cohort Month*")
st.write("""
The following code assigns each customer a cohort month based on when they made their *first purchase* (or invoice). Each 
customer's transactions are labeled with the month of their first purchase (or first invoice), which becomes their 
cohort month:
""")
data['CohortMonth'] = data.groupby('CustomerID')['InvoiceMonth'].transform('min')
code2 = """
data['CohortMonth'] = data.groupby('CustomerID')['InvoiceMonth'].transform('min')
"""
st.code(code2)

st.write("Looking at the dataset's tail so that we can get some sense for InvoiceMonth and CohortMonth:")
st.write(data.tail(30))
st.write("""
- We can see that we've an Invoice for **Dec,2011** but the first time this customer was acquired was back in **May**, 
so this is going to be one of our Cohorts, and some customers have been in the system for even a year **(2010-12)**.
""")

st.markdown("#### Getting *Cohort Index*")
st.write("""
The following code calculates the ***Cohort Index***, which tracks how many months have passed since a customer’s first 
purchase. This is done by calculating the difference between the current transaction year and month (`invoice_year` and 
`invoice_month`) and the cohort year and month (`cohort_year` and `cohort_month`), then converting that time difference into 
months:
""")

# create a date element function to get a series for subtraction
def get_date_elements(df, column):
    day = df[column].dt.day
    month = df[column].dt.month
    year = df[column].dt.year
    return day, month, year
code3 = """
# create a date element function to get a series for subtraction
def get_date_elements(df, column):
    day = df[column].dt.day
    month = df[column].dt.month
    year = df[column].dt.year
    return day, month, year
"""
st.code(code3, language='python')

# as its going to return three elements, so we need to assign them names as well, we dont need the day so we'll skip its name
# get date elements for our cohort and invoice columns
_, invoice_month, invoice_year = get_date_elements(data, 'InvoiceMonth')
_, cohort_month, cohort_year = get_date_elements(data, 'CohortMonth')
code4 = """
# as its going to return three elements, so we need to assign them names as well, we dont need the day so we'll skip its name
# get date elements for our cohort and invoice columns
_, invoice_month, invoice_year = get_date_elements(data, 'InvoiceMonth')
_, cohort_month, cohort_year = get_date_elements(data, 'CohortMonth')
"""
st.code(code4, language='python')

year_difference = invoice_year - cohort_year
month_difference = invoice_month - cohort_month
# calculating the 'Cohort Index'
data['CohortIndex'] = year_difference*12 + month_difference+1
code5 = """
year_difference = invoice_year - cohort_year
month_difference = invoice_month - cohort_month
# calculating the 'Cohort Index'
data['CohortIndex'] = year_difference*12 + month_difference+1
"""
st.code(code5, language='python')

st.write('Looking at the `CohortIndex` column below:')
st.write(data)

##################################################################################################################
st.subheader('Creating Pivot Tables:', divider='orange')

st.markdown("""
Following we'll be grouping customers by their **cohort month** (when they first purchased) and the **number of months 
since their first purchase** (cohort index). It then counts the number of unique customers in each group, helping track 
how many customers from each cohort are still active over time, which is crucial for retention analysis:
""")
# count customerID by grouping by CohortMonth(when they're acquired) and CohortIndex(how long they've been active)
# and also number of unique CustomerIDs
cohort_data = data.groupby(['CohortMonth', 'CohortIndex'])['CustomerID'].nunique().reset_index()

# format the CohortMonth column to 'Month Year' format
cohort_data['CohortMonth'] = cohort_data['CohortMonth'].dt.strftime('%B %Y')

# set CohortMonth as a categorical variable with the order based on the original datetime values
cohort_data['CohortMonth'] = pd.Categorical(cohort_data['CohortMonth'],
                                            categories=pd.to_datetime(cohort_data['CohortMonth'].unique()).strftime('%B %Y'),
                                            ordered=True)
code6 = """
# count customerID by grouping by CohortMonth(when they're acquired) and CohortIndex(how long they've been active) 
# and also number of unique CustomerIDs
cohort_data = data.groupby(['CohortMonth', 'CohortIndex'])['CustomerID'].nunique().reset_index()

# format the CohortMonth column to 'Month Year' format
cohort_data['CohortMonth'] = cohort_data['CohortMonth'].dt.strftime('%B %Y')

# set CohortMonth as a categorical variable with the order based on the original datetime values
cohort_data['CohortMonth'] = pd.Categorical(cohort_data['CohortMonth'],
                                            categories=pd.to_datetime(cohort_data['CohortMonth'].unique()).strftime('%B %Y'),
                                            ordered=True)
"""
st.code(code6, language='python')
st.write(cohort_data)

st.markdown("""
The code creates a pivot table that allows us to see customer retention (or other behaviors) over time, broken down by 
cohort. Each cohort represents customers who made their first purchase in the same month, and each column shows how 
many of those customers made purchases in subsequent months.
""")
# create a pivot table by using 'cohort_data' dataframe
cohort_table = cohort_data.pivot(index='CohortMonth', columns=['CohortIndex'], values='CustomerID')
code7 = """
# create a pivot table by using 'cohort_data' dataframe
cohort_table = cohort_data.pivot(index='CohortMonth', columns=['CohortIndex'], values='CustomerID')
"""
st.code(code7, language='python')
st.write(cohort_table)

st.write("**In Percentages:**")
percentage_cohort_table = cohort_table.divide(cohort_table.iloc[:,0], axis=0)
st.write(percentage_cohort_table)
###############################################################################################################
st.subheader('Visualizing Pivot Tables', divider='orange')

# visualize cohort_table in a heatmap
plt.figure(figsize=(21,10))
sns.heatmap(cohort_table, annot=True, cmap='Blues', annot_kws={"size": 18})
st.pyplot(plt)
plt.close()

st.write("**In Percentages:**")
# visualize the percentage_cohort_table in a heatmap
plt.figure(figsize=(21, 10))
sns.heatmap(percentage_cohort_table, annot=True, cmap='coolwarm', fmt='.0%', annot_kws={"size": 20})
plt.show()
st.pyplot(plt)

###############################################################################################################
###############################################################################################################
st.header('RESULTS & ANALYSIS', divider='rainbow')
st.markdown("""
**AXES:**
- **Y-axis (CohortMonth):** This lists the months in which customers made their **first purchase** (e.g., December 2010, 
January 2011, etc.). Each row corresponds to a distinct cohort of customers.
- **X-axis (CohortIndex):** This shows the number of months that have passed since the customers’ first purchase 
(starting from 1, representing the first month). \n
**INTERPRETING RESULTS:** \n
***1. Initial Drop in Retention (CohortIndex 1 to 2)***
- Across all cohorts, the retention drops drastically from **100%** in the first month to around **20-40%** by the 
second month (CohortIndex 2). \n
***2. Long-term Retention (After Month 2)***
- After the second month, retention continues to decline but at a slower rate.
- For example, in the **January 2011** cohort, retention falls from 24% in the second month to 15% by the 12th month. \n
***3. Variation in Cohorts***
- Some cohorts retain customers better than others over time. For example, the **December 2010** cohort maintains 
retention levels higher than many other cohorts after 6-7 months.
- In contrast, the **June 2011** cohort shows a significant drop in retention early on, with 10% retention by the fourth 
month. \n
***4. Churn Patterns***
- For most cohorts, retention drops significantly after 2-4 months and stabilizes at lower percentages in subsequent 
months. This suggests that the **critical time to focus on reducing churn** may be within the first few months.  \n
***5. Potential Outliers***
- Some months, like **January 2011**, exhibit relatively better retention in the longer term (15% after 12 months). This 
could indicate that some events or strategies implemented during those months had a positive effect on long-term 
retention.
- We can see that **December 2010** has an Outlier where 50% are still active at almost the year mark. 
""")

################################################################################################################
################################################################################################################
st.header('BUSINESS RECOMMENDATIONS', divider='rainbow')
st.markdown("""
- **Early Churn:** Since most of the cohorts experience a sharp drop in retention between the 1st and 2nd months, the 
business should focus on engaging customers **immediately after their first purchase**. Initiatives like onboarding 
programs, discounts, or personalized recommendations could help reduce early churn.
- **Critical Retention Period:** Since retention declines sharply in the first few months (typically up to 4 months), 
strategies to boost engagement and customer satisfaction during this time could have a strong impact on overall 
retention rates.
- **Cohort-specific Analysis:** Some cohorts perform better than others. The business should investigate what actions 
or promotions were happening in months like **December 2010** or **August 2011**, where retention is relatively higher, 
and replicate those successful strategies for other cohorts.
- **Long-term Engagement:** After around 6 months, retention stabilizes for most cohorts, albeit at a much lower level. 
Offering loyalty programs or incentives for customers to return periodically could help maintain engagement over the 
long term.
""")

################################################################################################################
################################################################################################################
st.header('NEXT STEPS', divider='rainbow')
st.markdown("""
- **Analyze Other Variables:** Examine additional factors (e.g., customer demographics, purchase categories, acquisition 
channels, marketing tactics) to see if certain groups or segments have better retention. This can reveal deeper insights 
into why certain cohorts retain better. 
- **Segment Analysis:** Look into Demographic segmentation and Behavioral segmentation.
- **Predictive Modelling:** Build a machine learning model to predict customer churn based on the cohort analysis data. 
Use features like: time since last purchase, total number of purchases, demographic and behavioral variables.
- **A/B Testing of Retention Strategies:** Implement the retention strategies (e.g., loyalty programs, re-engagement 
campaigns, personalized offers) and run A/B tests to measure the impact on customer retention for different cohorts.
""")

###############################################################################################################
st.divider()