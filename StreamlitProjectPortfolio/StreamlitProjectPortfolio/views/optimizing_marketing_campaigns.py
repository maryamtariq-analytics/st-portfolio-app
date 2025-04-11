import pandas as pd
import seaborn as sns
import plotly.express as px
import scipy.stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import streamlit as st

st.title('OPTIMIZING MARKETING CAMPAIGNS')
st.header('*EXECUTIVE SUMMARY*', divider='orange')
st.subheader('Business Problem:')
st.markdown("""
Dealing with three Account Types for Hospitals (Small Hospital, Medium Hospital, Big Hospital). There are organic 
sales streams and other Marketing tactics of Phone, Email, Flyers and Salesperson contacts that generate Sales and 
Revenue. We need to determine which Marketing tactics are more effective for each Sales Account Type.
- What's the impact of each Marketing Strategy on Sales?
- Impact of competition on Sales.
- How different types of Clients can have different Marketing Strategies.
""")
st.subheader('Methodology:')
st.markdown("""
- Engineered new variables.
- Performed Exploratory Data Analysis.
- Ran *Correlation* analysis.
- Ran *Linear Regression Analysis* to determine most effective Marketing strategies for generating higher revenue.
""")
st.subheader('Skills:')
st.markdown("""
**Language:** Python \n
**Data Manipulation Library:** Pandas \n
**Statistics Libraries:** SciPy, Statsmodels \n
**Visualization Libraries:** Seaborn, Plotly \n
**App & Dashboard Tool:** Streamlit \n
**Statistics and Analytical Models:** Correlation Analysis, Multiple Linear Regression
""")
st.subheader('Results:')
st.markdown("""
For `Private Facility`, **Sales_Contact_2** would be one variable that we'll focus on, **Sales Contact 2** seems 
profitable for `Small Facility`, for `Medium Facility` both **Campaign Flyer** and **Sales Contacts** are beneficial 
and for `Large Facilities` we would want to put more focus on **Sales Contacts** because they have higher level of 
success.
""")
st.subheader('Business Recommendations & Next Steps:')
st.markdown("""
- When we create the campaign we should reserve more money for the above Marketing campaign tactics because return on 
investment(ROI) is quite high for each dollar spent. 
- **Phone Campaign** for `Large Facility` is resulting in losses (-3.5 dollars). Coordinate this to 
create a nice Marketing Campaign for `Large Facility` that seems to work across different tactics. For `Small Facility` 
we are only getting back 80 cents per dollar spent and **Phone Campaign** is neutral (not loosing or 
gaining anything over it).
- **Consider Sales Cycle**: Sales Visits have very significant impact on Amounts collected, need to consider the fact 
that this Marketing tactic may be further down in the Sales Cycle which is making it more significant, for example maybe 
the customer receives an email and than has some conservation over the phone and than later the salesman is able to 
close the deal, so need to consider this cycle. 
- **Synergy between Marketing Tactics**: Additionally we need to consider that there maybe a synergy between multiple 
tactics that we're not picking up in our Model so that may warrant further Analysis. However we can see from our current 
Analysis which of our Campaigns work together, for example we can see that Flyer was significant for Big and Medium 
Hospitals and Sales Visit was significant for each Hospital but however a particular Sales Visit was different for each 
of our Account Types. Additionally the Phone for the small Hospital didn't have any negative effect which may indicate 
that its intertwined with Sales visit with other Campaigns. The tactics that were able to drive the most significant 
ROI were the Sales Contacts. Placing more investment in these areas would benefit an overall campaign. These **visits 
might be more significant due to position in sales cycle**. However Flyers were also significant in accounts collected. 
**Synergy between these tactics may need exploration**.
""")

################################################################################################################
################################################################################################################

st.header('PROJECT', divider='rainbow')
st.subheader('DATASET')
url = "https://raw.githubusercontent.com/maryamtariq-analytics/OptimizingMarketingCampaigns/refs/heads/main/OptimizingMarketingCampaigns-CampaignData.csv"
data = pd.read_csv(url)
st.write(data)

#################################################################################################################

st.subheader('FEATURE ENGINEERING')
st.write("Creating new columns for **month** and **year** by extracting both from dates:")
# extracting MONTH and YEAR from dates
data['Calendardate'] = pd.to_datetime(data['Calendardate'])
data['Calendar_Month'] = data['Calendardate'].dt.month
data['Calendar_Year'] = data['Calendardate'].dt.year

code = """
# extracting MONTH and YEAR from dates
data['Calendardate'] = pd.to_datetime(data['Calendardate'])
data['Calendar_Month'] = data['Calendardate'].dt.month
data['Calendar_Year'] = data['Calendardate'].dt.year
"""
st.code(code, language='python')

#################################################################################################################
#################################################################################################################

st.header('EXPLORATORY DATA ANALYSIS', divider='rainbow')

# understanding distributions
st.subheader('*Understanding Client Distributions:*', divider='orange')
client_type_count = data['Client Type'].value_counts(normalize=True).reset_index()
st.write(client_type_count)
# Create the Plotly bar chart
fig = px.bar(client_type_count, x='Client Type', y='proportion', title='Distribution of Client Type', color='Client Type',
             color_discrete_sequence=px.colors.qualitative.Vivid)
st.plotly_chart(fig)
st.write("""
- Out of all Client Types, a lion's share of Customers consist of Large Facilities, than Small Facilities and so on and 
the smallest share is that of Private Facilities.
""")

# continuing our Categorical Analysis
st.subheader('Categorical Analysis: `Number of Competition` & `Client Type`', divider='orange')
st.write(pd.crosstab(data['Number of Competition'], data['Client Type'], margins=True, normalize='columns'))
st.write("""
Looking at *Client Type* and *Number of Competition*, we're able to look at *margins* and normalize it so that we can 
look at *percentages*:
- **High Competition** is only 16% and **Low Competition** is 83%.
""")

# grouping and taking the Means
st.subheader('Grouped Analysis: `Number of Competition` (Mean)', divider='orange')
st.write(data.groupby('Number of Competition').mean(numeric_only=True))
st.write("""
- The mean of *Amount Collected* for **High Competition** is double the *Amount Collected* for **Low Competition**. 
- The *Unit Sold* is also double for **High Competition**. 
- Although we can see that majority of our Market is **Low Competition**, most of our Sales are coming from **High 
Competition** Markets.
""")

st.subheader('Grouped Analysis: `Client Type` (Mean)', divider='orange')
st.write(data.groupby('Client Type').mean(numeric_only=True))
st.write("""
- Even though **Medium Facility** is not the most popular among our client base but by looking at *Amount Collected* 
and *Unit Sold*, its bringing in alot more money than the other Markets. Need to understand what's the Marketing 
Strategy around Medium Facility and maybe that could be applied to other Markets.
""")
##################################################################################################################
##################################################################################################################

st.header('CORRELATION ANALYSIS', divider='rainbow')

st.subheader('Correlation of All Variables:', divider='orange')
st.write(data.corr(numeric_only=True))

### CORRELATION OF 'AMOUNT COLLECTED' WITH OTHER VARIABLES
st.subheader('Correlation of `Amount Collected` with Other Variables:', divider='orange')
## consolidated strategy for Targeting
# set a palette so that we can create the conditional formatting in the table below
cm = sns.light_palette('green', as_cmap=True)
# isolating the columns we deem as important
correlation_analysis = pd.DataFrame(data[['Amount Collected', 'Campaign (Email)', 'Campaign (Flyer)', 'Campaign (Phone)',
                                         'Sales Contact 1', 'Sales Contact 2', 'Sales Contact 3', 'Sales Contact 4',
                                         'Sales Contact 5']].corr()['Amount Collected']).reset_index()
# change the names of the column
correlation_analysis.columns = ['Impacting Variable', 'Degree of Linear Impact (Correlation)']
# resave the data again by eliminating the 'Amount Collected' because we dont want to see it correlated with itself
correlation_analysis = correlation_analysis[correlation_analysis['Impacting Variable'] != 'Amount Collected']
# sort values in descending order
correlation_analysis = correlation_analysis.sort_values('Degree of Linear Impact (Correlation)', ascending=False)
# set the style background
st.write(correlation_analysis.style.background_gradient(cmap=cm))

st.write("""
- `Sales Contact 2` is **highly** correlated with the `Amount Collected` followed by `Flyer Campaign` and so on.
- The least correlated variables with `Amount Collected` are `Sales Contact 5` and `Phone Campaign`. \n
""")

st.markdown("#### Correlation of `Amount Collected` with other variables broken down by `Account Type`:")
st.markdown("""
As the above correlation analysis is not broken down by `Account Type` which is our key question because we want to be 
able to understand what **Campaign Type** we should use for each individual `Account Type`, following we'll look at that:
""")

# the only difference here is to use 'groupby' clause
cm = sns.light_palette("green", as_cmap=True)
correlation_analysis = pd.DataFrame(data.groupby('Client Type')[['Amount Collected',
         'Campaign (Email)', 'Campaign (Flyer)', 'Campaign (Phone)',
         'Sales Contact 1', 'Sales Contact 2', 'Sales Contact 3',
         'Sales Contact 4', 'Sales Contact 5']].corr()['Amount Collected']).reset_index()
correlation_analysis = correlation_analysis.sort_values(['Client Type','Amount Collected'],ascending=False)
correlation_analysis.columns = ['Acc Type','Variable Impact on Sales','Impact']
correlation_analysis = correlation_analysis[correlation_analysis['Variable Impact on Sales']!='Amount Collected'].reset_index(drop=True)
st.write(correlation_analysis.style.background_gradient(cmap=cm))

st.write("""
- When we isolate one independent variable like `Sales Contact 2`, its very different for each Facility type. 
- We can look at each variable separately, for instance we can see that Email is not very effective for 
Large Facility.
""")

###################################################################################################################
###################################################################################################################

st.header('LINEAR REGRESSION ANALYSIS', divider='rainbow')

# little bit cleaning, replacing empty strings
data.columns=[mystring.replace(" ", "_") for mystring in data.columns]
data.columns=[mystring.replace("(", "") for mystring in data.columns]
data.columns=[mystring.replace(")", "") for mystring in data.columns]

# ols formula # a multiple linear regression model to predict 'Amout Collected'
results = smf.ols('Amount_Collected ~ Campaign_Email+Campaign_Flyer+Campaign_Phone+Sales_Contact_1+\
                   Sales_Contact_2+Sales_Contact_3+Sales_Contact_4+Sales_Contact_5', data=data).fit()

st.write(results.summary())
st.write("We want a **P-Value** less than the *Significance Level* of *0.5* to be *95%* confident, so we can see that "
         "P-Value for **Phone** is higher than 0.5, so we'll filter it out:")

# a filter to eliminate 'Campaign (Phone)'
df = pd.read_html(results.summary().tables[1].as_html(),header=0,index_col=0)[0]

df=df.reset_index()
df=df[df['P>|t|'] < 0.05][['index','coef']]
st.write(df)

# run the above equation for each 'Account Types' independently
consolidated_summary = pd.DataFrame()

st.subheader('Linear Regression Analysis for each `Account Type` Independently:', divider='orange')
# cycle through list of 'Account Types'
for acctype in list(set(list(data['Client_Type']))):
    temp_data = data[data['Client_Type'] == acctype].copy()
    results = smf.ols('Amount_Collected ~ Campaign_Email+Campaign_Flyer+Campaign_Phone+Sales_Contact_1+\
                   Sales_Contact_2+Sales_Contact_3+Sales_Contact_4+Sales_Contact_5', data=temp_data).fit()

    df = pd.read_html(results.summary().tables[1].as_html(), header=0, index_col=0)[0].reset_index()
    # filter varaiables that pass the 'significance level'
    df = df[df['P>|t|'] < 0.05][['index', 'coef']]
    df.columns = ['Variable', 'Coefficent (Impact)']
    df['Account Type'] = acctype
    df = df.sort_values('Coefficent (Impact)', ascending=False)
    df = df[df['Variable'] != 'Intercept']
    st.write(acctype)
    consolidated_summary = pd.concat([consolidated_summary, df], ignore_index=True)
    st.write(df)
    #st.write(results.summary())

st.write("""
- **Sales Contact 2** is important for a `Small Facility`
- **Campaign Flyer** is important for `Medium Facility`
- **Sales Contact 1** seems to work better for a `Large Facility`
- Only **Sales Contact 2** is important for `Private Facility`
""")

##################################################################################################################
##################################################################################################################

st.header('RESULTS & BUSINESS RECOMMENDATIONS', divider='rainbow')

st.write("Use the following coefficient table to see how much return we can derive from each dollar we "
         "spend, here we can clearly see that for different `Account Type` different Campaigns and Different Sales "
         "Contact are effective with different extent: ")
st.write(consolidated_summary)

st.subheader('Case Explanation - *Small Facility*', divider='orange')
st.write("""
- Each dollar spent on `Sales Contact 2`, we should expect almost 80 cents back.
""")
st.subheader("Case Explanation - *Medium Facility*", divider='orange')
st.write("""
- Highly effective with `Flyer Campaigns` as each dollar spent returns 4 dollars on average. 
- `Sales Contact 2` shows promising results with `Sales Contact 1` followed by `Sales Contact 3`.
- All other strategies show no impact and can be dropped to save costs.
         """)
st.subheader('Case Explanation - *Large Facility*', divider='orange')
st.write("""
- Each dollar spent on our `Sales Contact 1`, we should expect almost 12 dollars back.
- Each dollar spent on `Sales Contact 4`, we should expect almost 11 dollars back.
- `Phone Campaign` for is resulting in losses (-3.5 dollars).
""")
st.subheader('Case Explanation - *Private Facility*', divider='orange')
st.write("""
- Each dollar spent on our `Sales Contact 2` we should expect 6 dollars back.
""")

##################################################################################################################
# some optimization and heat map
consolidated_summary.reset_index(inplace=True)
consolidated_summary.drop('index', inplace=True, axis=1)

consolidated_summary.columns = ['Variable','Return on Investment','Account Type']
consolidated_summary['Return on Investment']= consolidated_summary['Return on Investment'].apply(lambda x: round(x,1))
#st.write(consolidated_summary.style.background_gradient(cmap='RdYlGn'))

st.subheader('Final *Return on Investment* Table:', divider='orange')
# Apply heatmap first, keep the data as numbers for the heatmap
styled_df = consolidated_summary.style.background_gradient(cmap='RdYlGn', subset=['Return on Investment']) \
                                  .format({'Return on Investment': '${:.1f}'})

# Show the styled DataFrame with the heatmap and formatted values
st.write(styled_df)
#################################################################################################################

st.subheader('BUSINESS RECOMMENDATIONS & NEXT STEPS', divider='orange')

st.write("""
- For `Private Facility`, **Sales_Contact_2** would be one variable that we'll focus on, **Sales Contact 2** seems 
profitable for `Small Facility`, for `Medium Facility` both **Campaign Flyer** and **Sales Contacts** are beneficial 
and for `Large Facilities` we would want to put more focus on **Sales Contacts** because they have higher level of success.
- When we create the campaign we should reserve more money for the above Marketing campaign tactics because return on 
investment(ROI) is quite high for each dollar spent. 
- **Phone Campaign** for `Large Facility` is resulting in losses (-3.5 dollars). Coordinate this to 
create a nice Marketing Campaign for `Large Facility` that seems to work across different tactics. For `Small Facility` 
we are only getting back 80 cents per dollar spent and **Phone Campaign** is neutral (not loosing or 
gaining anything over it).
- **Consider Sales Cycle**: Sales Visits have very significant impact on Amounts collected, need to consider the fact 
that this Marketing tactic may be further down in the Sales Cycle which is making it more significant, for example maybe 
the customer receives an email and than has some conservation over the phone and than later the salesman is able to 
close the deal, so need to consider this cycle. 
- **Synergy between Marketing Tactics**: Additionally we need to consider that there maybe a synergy between multiple 
tactics that we're not picking up in our Model so that may warrant further Analysis. However we can see from our current 
Analysis which of our Campaigns work together, for example we can see that Flyer was significant for Big and Medium 
Hospitals and Sales Visit was significant for each Hospital but however a particular Sales Visit was different for each 
of our Account Types. Additionally the Phone for the small Hospital didn't have any negative effect which may indicate 
that its intertwined with Sales visit with other Campaigns. The tactics that were able to drive the most significant 
ROI were the Sales Contacts. Placing more investment in these areas would benefit an overall campaign. These **visits 
might be more significant due to position in sales cycle**. However Flyers were also significant in accounts collected. 
**Synergy between these tactics may need exploration**.
""")

##############################################################################################################
##############################################################################################################
st.divider()