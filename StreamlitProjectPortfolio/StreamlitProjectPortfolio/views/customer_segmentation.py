import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy.stats import iqr
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime
import streamlit as st

st.title('CUSTOMER SEGMENTATION')

st.header('*EXECUTIVE SUMMARY*', divider='orange')
st.subheader('Business Problem:')
st.write("Segmenting customers based on their **demographic(income, education, children, age, marital status)** and the"
         " **behavioural (amount spent)** in order to gain a better understanding of company's customer's personalities "
         "and habits to effectively design the business and marketing strategies.")
st.subheader('Methodology:')
st.markdown("""
- Engineered a new *variable feature*.
- Performed a detailed *Exploratory Data Analysis* and *cleaned* data.
- Constructed a *Clustering Model* to segment customers into clusters to understand their behaviours and buying patterns.
""")
st.subheader('Skills:')
st.markdown("""
**Language:** Python \n
**Data Manipulation Libraries:** NumPy, Pandas, Datetime \n
**Statistics Libraries:** SciPy, Scikit-Learn \n
**Visualization Library:** Matplotlib, Seaborn, Plotly \n
**App & Dashboard Tool:** Streamlit \n
**Statistics and Analytical Algorithm:** Interquartile Range, KMeans Clustering Algorithm
""")
st.subheader('Results & Business Recommendations:')
st.write("""
- ***Income*** was really the key indicator that determined the amount a customer will spend.
- In terms of ***Education*** we noticed customers with graduate education level and above tends to spend 12 times 
higher than those customers with undergraduate education level because customers with graduate education level and 
above earns above 2 times than customers with undergraduate education level.
- On average there was a decline on the ***Total Amount Spent*** as the ***Total Children*** increases.
##### Young Customers (earn less, spend less)
- **Affordable Products/Services:** Offer low-cost, high-value products or services. Focus on essentials or entry-level 
offerings.
- **Discounts and Promotions:** Utilize discounts, bundle offers, and loyalty programs to encourage spending. Target 
students and early-career professionals.
- **Digital Engagement:** Leverage social media platforms and influencer marketing to create brand awareness, as younger 
customers tend to engage more online.
##### Older Customers (earn more spend more)
- **Upselling and Cross-selling:** Encourage upgrades to higher-tier products, bundle complementary services, and offer 
personalized recommendations based on purchasing behavior.
- **Experiential Marketing:** Organize exclusive events, experiential promotions, or personalized consultations that 
focus on luxury experiences.
- **Premium Products/Services:** Develop exclusive, high-end products or services that cater to their lifestyle, 
focusing on luxury, convenience, and quality.
##### Older Customers (earn moderate, spend less)
- **Referral Programs:** Implement referral programs where these customers can benefit from recommending products to 
friends and family, rewarding them for loyalty.
- **Upgrade Incentives:** Provide incentives for gradual upgrades (e.g., trade-in programs) that allow them to step up 
from basic to mid-range products over time.
- **Value-based Marketing:** Highlight the long-term value and durability of products or services, emphasizing quality 
over luxury.
### General Strategy
- **Personalized Marketing:** Use data from these clusters to personalize communication. Tailored email marketing and 
targeted ads based on income, spending habits, and age demographics can improve customer engagement.
- **Omnichannel Approach:** Ensure seamless experiences across both digital and physical channels, as different clusters 
may prefer distinct shopping methods.
- **Customer Feedback Loop:** Continuously gather feedback from each cluster to adjust your offerings, ensuring you 
remain aligned with their evolving needs and preferences.
""")
st.header('Next Steps:')
st.markdown("""
- Analyze cluster behaviour over time by conducting time series analysis on customer transactions, spending patterns or 
engagement level.
- Based on the segmentation, run A/B tests for different types of messaging, promotions, and product offerings in order 
to make personalized marketing strategies.
-  Analyze customer satisfaction and feedback analysis.
- Re-segmentation with additional variables.
- Conduct customer funnel analysis to map the customer journey for each cluster from initial awareness to purchase and 
post-purchase stages. Look for bottlenecks or areas for improvement in the customer experience.
""")
################################################################################################################
################################################################################################################
st.header('PROJECT', divider='rainbow')
st.subheader('DATA SET:', divider='orange')
url = "https://raw.githubusercontent.com/maryamtariq-analytics/CustomerSegmentation-KMeans/refs/heads/main/MarketingCampaign-CustomerSegmentation.csv"
data = pd.read_csv(url, sep='\t')
st.write(data)

st.subheader('FEATURE ENGINEERING:', divider='orange')
st.write("Since customer segmentation is based upon *Total Amount Spent*, we'll engineer this feature:")
data['TotalAmountSpent'] = data['MntFishProducts'] + data['MntFruits'] + data['MntGoldProds'] + data['MntSweetProducts'] + data['MntWines']
code = '''
data['TotalAmountSpent'] = data['MntFishProducts'] + data['MntFruits'] + data['MntGoldProds'] + data['MntSweetProducts'] + data['MntWines']
'''
st.code(code, language='python')

#################################################################################################################
#################################################################################################################

st.header('EXPLORATORY DATA ANALYSIS:', divider='rainbow')
# UNI-VARIATE ANALYSIS
st.subheader('UNI-VARIATE ANALYSIS:', divider='orange')
# AGE
st.markdown('### 1. *AGE*')
data['Age'] = data['Year_Birth'].apply(lambda x : datetime.now().year - x)
age_stats = data['Age'].describe()
st.write(age_stats)

sns.histplot(data=data, x='Age', bins=list(range(10, 150, 10)))
plt.title("Distribution of Customer's Age")
plt.show()
st.pyplot(plt)

st.write('Most of the customers belong in the age range of `40-60` years old.')

# EDUCATION
st.markdown('### 2. *EDUCATION*')
data['Education'] = data['Education'].replace({'Graduation':'Graduate', 'PhD':'Postgraduate', 'Master':'Postgraduate', '2n Cycle':'Postgraduate', 'Basic':'Undergraduate'})

data['Education'].value_counts().plot.bar(figsize=(8,6))
plt.xticks(rotation=45)
plt.title("Frequency of Customer's Education (proportion)")
st.pyplot(plt)
plt.close()

st.write("Half of our customer's highest education level is first degree graduation. About 50% of customers have their "
         "education level at bachelor's degree which is then followed by customers with postgraduate level of "
         "education.")

# MARITAL STATUS
st.markdown('### 3. *MARITAL STATUS*')
data["Marital_Status"] = data["Marital_Status"].replace({"Together":"Married", "Absurd":"Single", "Divorced":"Single", "Alone":"Single", "YOLO":"Single", "Widow":"Single"})

fig = px.bar(data["Marital_Status"].value_counts(normalize=True),
             title = "Proportion of Customer's Marital Status",
             height=500)
fig.update_layout(yaxis_title = "Freuency [proportion]")
st.plotly_chart(fig)

st.write('Close to 65% of customers are married while the remaining close to 35% are single.')

# INCOME
st.markdown('### 4. *INCOME*')

sns.histplot(data=data, x='Income', binwidth=1e4)
plt.title("Distribution of Customer's Income")
st.pyplot(plt)
plt.close()

st.write("Majority of customer's income is within 0-100k dollars. However we have other customer's that "
         "earn way more than that (above 600k$).")

# KID HOME
st.markdown('### 5. *KID HOME*')

data["Kidhome"].value_counts(normalize=True).plot.bar()
plt.ylabel("Frequency")
plt.title("Proportion of Customer's Kid")
st.pyplot(plt)
plt.close()

st.write("Above half of customer's do not have kids at home.")

# TEEN HOME
st.markdown('### 6. *TEEN HOME*')

data["Teenhome"].value_counts(normalize=True).plot.bar()
plt.ylabel("Frequency")
plt.title("Proportion of Customer's Teen at Home")
st.pyplot(plt)
plt.close()

st.write("Above 50% of customer's do not have teen at home.")

# TOTAL CHILDREN
st.markdown('### 7. *TOTAL CHILDREN*')

data['Total Children'] = data['Kidhome'] + data['Teenhome']

data["Total Children"].value_counts(normalize=True).sort_index().plot.bar()
plt.ylabel("Frequency")
plt.title("Proportion of Customer's Total Children at Home")
st.pyplot(plt)
plt.close()

st.write('Close to half of entire customers have the total number of 1 children, while in the remaining half above '
         'quarter of customers have no children at all.')

# TOTAL AMOUNT SPENT
st.markdown('### 8. *TOTAL AMOUNT SPENT*')
tas_stats = data['TotalAmountSpent'].describe()
st.write(tas_stats)

sns.histplot(data=data, x="TotalAmountSpent", binwidth=200, stat="percent")
plt.title("Distribution of Total Amount Spent on Product by Customers [Proportion]")
st.pyplot(plt)
plt.close()

st.write("Close to half of customers total amount spent on the company's product is within 0 to 200 dollars.")

#################################################################################################################
# BI-VARIATE ANALYSIS
st.subheader('BI-VARIATE ANALYSIS:', divider='orange')

# AGE VS TOTAL AMOUNT SPENT
st.markdown('### 1. *AGE vs TOTAL AMOUNT SPENT*')

sns.scatterplot(data=data, x='Age', y='TotalAmountSpent')
plt.title('Relationship between Age and Total Amount Spent')
st.pyplot(plt)
plt.close()

st.write("There's no correlation between *Age* and *Total Amount Spent*, meaning Age does not infer the *Total Amount "
         "Spent* of money by customers.")

def group_age(age):
    if age < 20:
        return '11-20'
    elif age > 20 and age < 31:
        return '21-30'
    elif age > 30 and age <41:
        return "31-40"
    elif age > 40 and age <51:
        return "41-50"
    elif age > 50 and age <61:
        return "51-60"
    elif age > 60 and age <71:
        return "61-70"
    elif age > 70 and age <81:
        return "71-80"
    elif age > 80:
        return ">80"

data['Age Group'] = data['Age'].apply(group_age)
# to order plotly index
order = ["21-30", "31-40", "41-50", "51-60", "61-70", "71-80", ">80"]

mask = data.groupby('Age Group')['TotalAmountSpent'].median()
mask = mask.reset_index()

fig1 = px.bar(data_frame=mask, x='Age Group', y='TotalAmountSpent', height=500)

annotation = []
for x, y in zip(mask['Age Group'], mask['TotalAmountSpent']):
    annotation.append(dict(x=x, y=y + 20,
                          text=str(round(y,2)) + '$',
                          font=dict(family='Arial', size=14, color='rgb(66,99,236)'), showarrow=False))

fig1.update_xaxes(categoryorder='array', categoryarray=order)
fig1.update_layout(annotations=annotation)
st.plotly_chart(fig1)

st.write("We can see the average values for the distribution of each Age Group value. It's seen that "
         "the group who spend most on average is customers within the range of greater than 80, which is then followed "
         "by customers in the age range of 21-30. Let's look at the distribution of the comparison.")

plt.figure(figsize=(8, 8))
sns.violinplot(x="Age Group", y="TotalAmountSpent", data=data, cut=0, order=order)
plt.title("Relationship between Age Range and Total Amount Spent")
st.pyplot(plt)
plt.close()

st.write('We can see from the summary above that most age range have outliers within them. For example the above 80 '
         'customer age range have a lot of outliers.')

# AGE VS INCOME
st.markdown('### 2. *AGE* vs *INCOME*')
income_iqr = iqr(data['Income'], nan_policy='omit')

low = np.nanquantile(data['Income'], 0.25) - 1.5 * income_iqr
high = np.nanquantile(data['Income'], 0.75) + 1.5 * income_iqr

data_cut = data[data['Income'].between(low, high)]

mask = data_cut.groupby("Age Group")["Income"].mean()
mask = mask.reset_index()
fig2 = px.bar(data_frame=mask, x="Age Group", y="Income", height=500)

annotation = []
for x, y in zip(mask["Age Group"], mask["Income"]):
    annotation.append(
        dict(x=x, y=y +5000,
             text=str(round(y, 2)) + '$',
             font=dict(family='Arial', size=14, color='rgb(66, 99, 236)'), showarrow=False)
    )
fig2.update_xaxes(categoryorder='array', categoryarray= ["21-30", "31-40"])
fig2.update_layout(annotations=annotation)

st.plotly_chart(fig2)

st.write('Interesting to see that the age group that earns more on average are the customers within above 80+, '
         'followed by customers within 71-80. Apart from customer age within 21-30. We can see a trend which postulates '
         'that as the age group increases so do the Income.')

# EDUCATION VS TOTAL AMOUNT SPENT
st.markdown('### 3. *EDUCATION vs TOTAL AMOUNT SPENT*')

mask = data.groupby("Education")["TotalAmountSpent"].median()
mask = mask.reset_index()
fig3 = px.bar(data_frame=mask, x="Education", y="TotalAmountSpent", height=500,
            title = "Relationsip Between Education and Total Amount Spent [Average Spent]")

annotation = []
for x, y in zip(mask["Education"], mask["TotalAmountSpent"]):
    annotation.append(
        dict(x=x, y=y +20,
             text=str(round(y, 2)) + '$',
             font=dict(family='Arial', size=14, color='rgb(66, 99, 236)'), showarrow=False)
    )
fig3.update_xaxes(categoryorder='array', categoryarray= order)
fig3.update_layout(annotations=annotation)

st.plotly_chart(fig3)

st.write("We see that there isn't much difference between average spent for both graduate and postgraduate customer. "
         "However we see much drop for customers who have undergraduate level of education. We can postulate that "
         "customers who have Graduate education level and above spends approximately 7 times than customers who are "
         "undergraduate. That's way too much.")

# EDUCATION VS INCOME
st.markdown('### 4. *EDUCATION vs INCOME*')

mask = data_cut.groupby("Education")["Income"].mean()
mask = mask.reset_index()
fig4 = px.bar(data_frame=mask, x="Education", y="Income", height=500,
            title = "Relationsip Between Customer's Education Level and Income [Average Income]")

annotation = []
for x, y in zip(mask["Education"], mask["Income"]):
    annotation.append(
        dict(x=x, y=y +1500,
             text=str(round(y, 2)) + '$',
             font=dict(family='Arial', size=14, color='rgb(66, 99, 236)'), showarrow=False)
    )
fig4.update_xaxes(categoryorder='array', categoryarray= order)
fig4.update_layout(annotations=annotation)

st.plotly_chart(fig4)

st.write("Customers with graduate and post graduate education level earns 2 times above than customers who have "
         "undergraduate education level.")

# MARITAL STATUS AND TOTAL AMOUNT SPENT
st.markdown('### 5. *MARITAL STATUS vs TOTAL AMOUNT SPENT*')

mask = data.groupby("Marital_Status")["TotalAmountSpent"].median()
mask = mask.reset_index()
fig5 = px.bar(data_frame=mask, x="Marital_Status", y="TotalAmountSpent", height=500,
             title="Relationship between Customer's Marital Status and Total Amount Spent [Average Spent]")

annotation = []
for x, y in zip(mask["Marital_Status"], mask["TotalAmountSpent"]):
    annotation.append(
        dict(x=x, y=y +50,
             text=str(round(y, 2)) + '$',
             font=dict(family='Arial', size=14, color='rgb(66, 99, 236)'), showarrow=False)
    )
fig5.update_xaxes(categoryorder='array', categoryarray= ["21-30", "31-40"])
fig5.update_layout(annotations=annotation)

st.plotly_chart(fig5)

st.write("There isn't any relationship between customer's marital status and the average amount spent.")

# MARITAL STATUS AND INCOME
st.markdown('### 6. *MARITAL STATUS vs INCOME*')

mask = data_cut.groupby("Marital_Status")["Income"].mean()
mask = mask.reset_index()
fig6 = px.bar(data_frame=mask, x="Marital_Status", y="Income", height=500,
             title="Relationship between Customer's Marital Status and Income [Average Income]")

annotation = []
for x, y in zip(mask["Marital_Status"], mask["Income"]):
    annotation.append(
        dict(x=x, y=y +5000,
             text=str(round(y, 2)) + '$',
             font=dict(family='Arial', size=14, color='rgb(66, 99, 236)'), showarrow=False)
    )
fig6.update_xaxes(categoryorder='array', categoryarray= ["21-30", "31-40"])
fig6.update_layout(annotations=annotation)
st.plotly_chart(fig6)

st.write("Also in terms of Marital Status and Income there isn't any relationship concerning that. Customer's earn "
         "approximately equal.")

# KIDS HOME VS TOTAL AMOUNT SPENT
st.markdown('### 7. *KIDS HOME vs TOTAL AMOUNT SPENT*')

mask = data.groupby("Kidhome")["TotalAmountSpent"].median()
mask = mask.reset_index()
fig7 = px.bar(data_frame=mask, x="Kidhome", y="TotalAmountSpent", height=500,
             title="Relationship between Customer's Kid and Amount Spent [Average]")

annotation = []
for x, y in zip(mask["Kidhome"], mask["TotalAmountSpent"]):
    annotation.append(
        dict(x=x, y=y +50,
             text=str(round(y, 2)) + '$',
             font=dict(family='Arial', size=14, color='rgb(66, 99, 236)'), showarrow=False)
    )
fig7.update_xaxes(categoryorder='array', categoryarray= ["21-30", "31-40"])
fig7.update_layout(annotations=annotation)
st.plotly_chart(fig7)

st.write("Customer's who don't have kids at home spend way high than those who have. They spend about 12 times than "
         "others on average.")

# KIDS HOME VS INCOME
st.markdown('### 8. *KIDS HOME vs INCOME*')

mask = data_cut.groupby("Kidhome")["Income"].mean()
mask = mask.reset_index()
fig8 = px.bar(data_frame=mask, x="Kidhome", y="Income", height=500, title="Relationship between Marital Status and Total Amount Spent")

annotation = []
for x, y in zip(mask["Kidhome"], mask["Income"]):
    annotation.append(
        dict(x=x, y=y +5000,
             text=str(round(y, 2)) + '$',
             font=dict(family='Arial', size=14, color='rgb(66, 99, 236)'), showarrow=False)
    )
fig8.update_xaxes(categoryorder='array', categoryarray= ["21-30", "31-40"])
fig8.update_layout(annotations=annotation)
st.plotly_chart(fig8)

st.write("Customer's who don't have kids earn more than others.")

# TEEN HOMES VS TOTAL AMOUNT SPENT
st.markdown('### 9. *TEEN HOMES vs TOTAL AMOUNT SPENT*')

mask = data.groupby("Teenhome")["TotalAmountSpent"].median()
mask = mask.reset_index()
fig9 = px.bar(data_frame=mask, x="Teenhome", y="TotalAmountSpent", height=500, title="Relationship between Marital Status and Total Amount Spent")

annotation = []
for x, y in zip(mask["Teenhome"], mask["TotalAmountSpent"]):
    annotation.append(
        dict(x=x, y=y +50,
             text=str(round(y, 2)) + '$',
             font=dict(family='Arial', size=14, color='rgb(66, 99, 236)'), showarrow=False)
    )
fig9.update_layout(annotations=annotation)
st.plotly_chart(fig9)

st.write("We can see from the above relationship the upward trend concerning Teens at home and Average Amount Spent. As"
         "the number of teens increase so do the average amount spent increases.")

# TEENS HOME VS INCOME
st.markdown('### 10. *TEENS HOME vs INCOME*')

mask = data_cut.groupby("Teenhome")["Income"].mean()
mask = mask.reset_index()
fig10 = px.bar(data_frame=mask, x="Teenhome", y="Income", height=500, title="Relationship between Marital Status and Total Amount Spent")

annotation = []
for x, y in zip(mask["Teenhome"], mask["Income"]):
    annotation.append(
        dict(x=x, y=y +5000,
             text=str(round(y, 2)) + '$',
             font=dict(family='Arial', size=14, color='rgb(66, 99, 236)'), showarrow=False)
    )
fig10.update_layout(annotations=annotation)
st.plotly_chart(fig10)

st.write("There is little trend in terms of average income collected and number of teens at home.")

# TOTAL CHILDREN VS AMOUNT SPENT
st.markdown('### 11. *TOTAL CHILDREN vs TOTAL AMOUNT SPENT*')

mask = data.groupby("Total Children")["TotalAmountSpent"].median()
mask = mask.reset_index()
fig11 = px.bar(data_frame=mask, x="Total Children", y="TotalAmountSpent", height=500,
             title="Relationship between Marital Status and Amount Spent [Average Spent]")

annotation = []
for x, y in zip(mask["Total Children"], mask["TotalAmountSpent"]):
    annotation.append(
        dict(x=x, y=y +50,
             text=str(round(y, 2)) + '$',
             font=dict(family='Arial', size=14, color='rgb(66, 99, 236)'), showarrow=False)
    )
fig11.update_layout(annotations=annotation)
st.plotly_chart(fig11)

st.write("As the Total number of Children increases so do the Amount Spent. Also we see that customers who don't have "
         "children spend way more than others.")

# INCOME VS TOTAL AMOUNT SPENT
st.markdown('### 12. *INCOME vs TOTAL AMOUNT SPENT*')

fig12 = px.scatter(data_frame=data_cut, x="Income",
                 y="TotalAmountSpent", title="Relationship Between Customer's Income and Total Amount Spent",
                height=500,
                color_discrete_sequence = px.colors.qualitative.G10[1:])
st.plotly_chart(fig12)

st.write("We can postulate that Income and Total Amount Spent are correlated, we can see from the above analysis "
         "that as the Income increases so does the TotalAmountSpent. So from the analysis we can postulate that Income "
         "is one of key factor that determines how much a customer might spend.")

st.divider()

####################################################################################################################
# MULTI-VARIATE ANALYSIS
st.subheader('MULTI-VARIATE ANALYSIS:', divider='orange')

# EDUCATION VS INCOME VS TOTAL AMOUNT SPENT
st.markdown('### 1. *EDUCATION vs INCOME vs TOTAL AMOUNT SPENT*')

fig13 = px.scatter(
    data_frame=data_cut,
    x = "Income",
    y= "TotalAmountSpent",
    title = "Relationship between Income VS Total Amount Spent Based on Education",
    color = "Education",
    height=500
)
st.plotly_chart(fig13)

st.write("Customers with an Undergraduate education level generally spend less than other customers with higher levels "
         "of education. This is because undergraduate customers typically earn less than other customers, which "
         "affects their spending habits. ")

st.divider()

###################################################################################################################

st.subheader('**EXPLORATORY DATA ANALYSIS Conclusion:**')
st.markdown("""
- ***Income*** was really the key indicator that determined the amount a customer will spend.
- In terms of ***Education*** we noticed customers with graduate education level and above tends to spend 12 times 
higher than those customers with undergraduate education level. The reason for this is because customers with graduate 
education level and above earns above 2 times than customers with undergraduate education level.
- On average there was a decline on the ***Total Amount Spent*** as the ***Total Children*** increases.
""")

####################################################################################################################
####################################################################################################################

st.header('SEGMENTATION MODELLING', divider='rainbow')
st.write("We'll first construct the `KMeans` model with ***two*** features and then build the final model with "
         "***three*** features:")
st.subheader('*KMeans Model with 2 Features*:', divider='orange')

# fill null values with median
data['Income'].fillna(data['Income'].median(), inplace=True)
# get the variables to work on
data1 = data[['Income', 'TotalAmountSpent']]
# normalize skewed features and transform it into normal distribution
data1_log = np.log(data1)
# scale the result using Scikit-learn's 'StandardScalar()'
std_scaler = StandardScaler()
data_scaled = std_scaler.fit_transform(data1_log)

code1 = """
# fill null values with median
data['Income'].fillna(data['Income'].median(), inplace=True)
# get the variables to work on
data1 = data[['Income', 'TotalAmountSpent']]
# normalize skewed features and transform it into normal distribution
data1_log = np.log(data1)
# scale the result using Scikit-learn's 'StandardScalar()'
std_scaler = StandardScaler()
data_scaled = std_scaler.fit_transform(data1_log)
"""
st.code(code1, language='python')

# initializing KMeans Clustering Model
model = KMeans(n_clusters=3, random_state=42)
# fitting the KMeans model to the data
model.fit(data_scaled)
# assigning cluster labels to each row in the dataset
data2 = data1.assign(ClusterLabel = model.labels_)

code2 = """
# initializing KMeans Clustering Model
model = KMeans(n_clusters=3, random_state=42)
# fitting the KMeans model to the data
model.fit(data_scaled)
# assigning cluster labels to each row in the dataset
data2 = data1.assign(ClusterLabel = model.labels_)
"""
st.code(code2, language='python')

st.subheader('Results')
result1 = data2.groupby('ClusterLabel')[['Income', 'TotalAmountSpent']].median()
st.write(result1)
# visualizing clusters
# visualizing clusters
fig14 = px.scatter(data_frame=data2,
                  x='Income',
                  y='TotalAmountSpent',
                  title='Relationship between Income vs Total Amount Spent',
                  color='ClusterLabel',
                  height=500)
st.plotly_chart(fig14)

st.markdown("""
We can see that there is a trend within the clusters:
* Cluster 0 translates to customers who earn moderate and spend moderate.
* Cluster 1 represent customers that earn less and spend less.
* Cluster 2 represents customers that earn more and spend more.
""")

#################################################################################################################
st.subheader('*KMeans Model with 3 Features*:', divider='orange')

# get the variables to work on
data3 = data[['Age', 'Income', 'TotalAmountSpent']]
# normalize skewed features and transform it into normal distribution
data3_log = np.log(data3)
# scale the result using Scikit-learn's 'StandardScalar()'
std_scaler = StandardScaler()
data3_scaled = std_scaler.fit_transform(data3_log)

code3 = """
# get the variables to work on
data3 = data[['Age', 'Income', 'TotalAmountSpent']]
# normalize skewed features and transform it into normal distribution
data3_log = np.log(data3)
# scale the result using Scikit-learn's 'StandardScalar()'
std_scaler = StandardScaler()
data3_scaled = std_scaler.fit_transform(data3_log)
"""
st.code(code3, language='python')

# initializing KMeans Clustering Model
model = KMeans(n_clusters=3, random_state=42)
# fitting the KMeans model to the data
model.fit(data3_scaled)
# assigning cluster labels to each row in the dataset
data4 = data3.assign(ClusterLabel = model.labels_)
code4 = """
# initializing KMeans Clustering Model
model = KMeans(n_clusters=3, random_state=42)
# fitting the KMeans model to the data
model.fit(data3_scaled)
# assigning cluster labels to each row in the dataset
data4 = data3.assign(ClusterLabel = model.labels_)
"""
st.code(code4, language='python')

st.subheader('Results')
result2 = data4.groupby('ClusterLabel').agg({'Age':'mean', 'Income':'median', 'TotalAmountSpent':'median'}).round()
st.write(result2)
# visualizing clusters
fig15 = px.scatter_3d(data_frame=data4, x='Income', y='TotalAmountSpent', z='Age',
                  color='ClusterLabel', height=500, title='Visualizing Cluster Result using 3 Features')
st.plotly_chart(fig15)

st.markdown("""
We can see from the above summary that:
* Cluster 0 depicts young customers that earn less and also spend less.
* Cluster 1 translates to older customers that earn a lot and also spend a lot.
* Cluster 2 depicts older customers that earn moderate and also spend less.
""")

###############################################################################################################
###############################################################################################################

st.header('BUSINESS RECOMMENDATIONS', divider='rainbow')
st.markdown("""
##### Young Customers (earn less, spend less)
- **Affordable Products/Services:** Offer low-cost, high-value products or services. Focus on essentials or entry-level 
offerings.
- **Discounts and Promotions:** Utilize discounts, bundle offers, and loyalty programs to encourage spending. Target 
students and early-career professionals.
- **Digital Engagement:** Leverage social media platforms and influencer marketing to create brand awareness, as younger 
customers tend to engage more online.
##### Older Customers (earn more spend more)
- **Upselling and Cross-selling:** Encourage upgrades to higher-tier products, bundle complementary services, and offer 
personalized recommendations based on purchasing behavior.
- **Experiential Marketing:** Organize exclusive events, experiential promotions, or personalized consultations that 
focus on luxury experiences.
- **Premium Products/Services:** Develop exclusive, high-end products or services that cater to their lifestyle, 
focusing on luxury, convenience, and quality.
##### Older Customers (earn moderate, spend less)
- **Referral Programs:** Implement referral programs where these customers can benefit from recommending products to 
friends and family, rewarding them for loyalty.
- **Upgrade Incentives:** Provide incentives for gradual upgrades (e.g., trade-in programs) that allow them to step up 
from basic to mid-range products over time.
- **Value-based Marketing:** Highlight the long-term value and durability of products or services, emphasizing quality 
over luxury.
### General Strategy
- **Personalized Marketing:** Use data from these clusters to personalize communication. Tailored email marketing and 
targeted ads based on income, spending habits, and age demographics can improve customer engagement.
- **Omnichannel Approach:** Ensure seamless experiences across both digital and physical channels, as different clusters 
may prefer distinct shopping methods.
- **Customer Feedback Loop:** Continuously gather feedback from each cluster to adjust your offerings, ensuring you 
remain aligned with their evolving needs and preferences.
""")

################################################################################################################
################################################################################################################
st.header('NEXT STEPS', divider='rainbow')
st.markdown("""
- Analyze cluster behaviour over time by conducting time series analysis on customer transactions, spending patterns or 
engagement level.
- Based on the segmentation, run A/B tests for different types of messaging, promotions, and product offerings in order 
to make personalized marketing strategies.
-  Analyze customer satisfaction and feedback analysis.
- Re-segmentation with additional variables.
- Conduct customer funnel analysis to map the customer journey for each cluster from initial awareness to purchase and 
post-purchase stages. Look for bottlenecks or areas for improvement in the customer experience.
""")

###############################################################################################################
###############################################################################################################

st.divider()