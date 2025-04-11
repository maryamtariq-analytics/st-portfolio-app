import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy.stats import chi2_contingency, chisquare
import streamlit as st

plt.style.use('seaborn')

st.title('MOBILE APP A/B TESTING')

st.header('*EXECUTIVE SUMMARY*', divider='orange')
st.subheader('Business Problem:')
st.markdown("""
Testing two versions of a game app to see which one keeps players coming back more. The key difference is a change in 
one game feature. We’ll compare how many players return after 1 day and 7 days for each version to figure out which 
feature works better for customer retention.
""")
st.subheader('Methodology:')
st.markdown("""
- Designed A/B Test by stating hypothesis, deciding control and experiment groups and finalising a statistical test.
- Performed *Exploratory Data Analysis*.
- Checked *Sample Ratio Mismatch (SRM).*
- Balanced *Sample Ratio Mismatch (SRM)* of sample distributions.
- Performed A/B Test by conducting a *Chi-Squared Statistical Test*.

""")
st.subheader('Skills:')
st.markdown("""
**Language:** Python \n
**Data Manipulation Libraries:** NumPy, Pandas \n
**Statistics Libraries:** SciPy \n
**Visualization Library:** Matplotlib, Seaborn, Plotly \n
**App & Dashboard Tool:** Streamlit \n
**Statistics:** Contingency table, Chi-squared test statistic
""")
st.subheader('Results:')
st.markdown("""
- **Being in the group that sees the first gate at level 40 has no effect on retention after 1 day** , meaning we 
failed to reject our null hypothesis. This may be because 1 day is too short of a time period to properly capture the 
way user engagement does or does not change. Or it may mean that the users who play our game on a daily basis are 
indifferent to where a gate is located!
- **Being in the group that sees the first gate at level starting at gate 40 does affect user retention after 7 days** , 
meaning we can reject our null hypothesis.
""")
st.subheader('Business Recommendations:')
st.markdown("""
- **Retain the Current Gate Placement:** These results show that users who play our game on a weekly basis have lower 
overall user retention if the first game gate is moved up to level 40. In this case, it may be best to keep the gate 
where it is rather than move it since we observed a negative change in user retention.
- **Investigate User Behaviour Beyond 7 Days:** However, because we saw no significant change in retention after 1 day 
yet we saw one after 7 days, it may be beneficial to run this type of experiment over longer time periods. For example, 
testing how retention changes after 7 and 14 days.
- **Segmentation of User Types:** Segment your users based on play patterns. For example, casual players might react 
differently to gates compared to more engaged players. Personalizing gate placement for different segments could 
improve overall retention. This can be implemented by analyzing high-engagement versus low-engagement users and 
adjusting gameplay or challenges accordingly.
- **Optimize User Experience Around The Gate:** Analyze the gate's mechanics. Could it be too difficult or disruptive 
at level 40? Consider making the gate less challenging, adding a reward system, or offering a small in-game incentive 
(like extra lives, bonuses, or faster progression) to make passing the gate more appealing.
""")
st.subheader('Next Steps:')
st.write("""
1. Testing different hypothesis like run additional A/B tests with varied gate placements. \n
2. Segment users based on engagement patterns and tailor the experience. \n
3. Explore user behavior for longer periods (14 or 30 days) to assess long-term effects. \n
4. Test in-game incentives or rewards around the gate to mitigate the negative effect on retention. \n
These strategies can help us refine the game's design and improve user retention while balancing both engagement and 
monetization goals.
""")

################################################################################################################
################################################################################################################

# DATASET
st.header('PROJECT', divider='rainbow')
st.subheader('DATASET:')
url = "https://raw.githubusercontent.com/maryamtariq-analytics/AB-Testing---Mobile-Game-App/refs/heads/main/AB%20Testing%20Mobile%20App%20-%20Cookie%20Cats.csv"
st.markdown("""
The variables of our use will be: 
- **version**: Informs at what level the users see the gates (either at level 30 or level 40).
- **retention_1**: Either user is retained after 1 day or not.
- **retention_7**: Either user is retained after 7 days or not.
""")
data = pd.read_csv(url)
st.write(data)

##################################################################################################################
##################################################################################################################

# A/B TEST DESIGN
st.header('A/B TEST DESIGN', divider='rainbow')

# Hypothesis
st.subheader('Hypothesis:', divider='orange')
st.markdown('#### 1.')
st.markdown('***NULL HYPOTHESIS 1:*** Being in the group that sees the first gate at level 40 has no effect on '
            'user retention after 1 day.')
st.markdown('***ALTERNATIVE HYPOTHESIS 1:*** Being in the group that sees the first gate at level 40 affects user '
            'retention after 1 day.')
st.markdown('#### 2.')
st.markdown('***NULL HYPOTHESIS 2:*** Being in the group that sees the first gate at level 40 has no effect on '
            'user retention after 7 days.')
st.markdown('***ALTERNATIVE HYPOTHESIS 2:*** Being in the group that sees the first gate at level 40 affects user '
            'retention after 7 days.')

# Control & Experiment Groups
st.subheader('Control & Experiment Groups:', divider='orange')
st.markdown("***CONTROL GROUP:*** **Gate 30** because this is the baseline group that does not experience the change.")
st.markdown(
    "***EXPERIMENTAL GROUP:*** **Gate 40** because this is the group that experiences the change we're testing.")

# Statistical Test
st.subheader('Statistical Test', divider='orange')
st.write("""
##### Chi-Square Test for Independence
- Use ***Chi-Square Test for Independence*** because our data is categorical (whether users were retained after 1 and 7 
days or not) and to assess whether the retention rates after 1 and 7 days are independent of the group assignment 
(control vs. experiment).
""")
##################################################################################################################
##################################################################################################################

st.header('DATA WRANGLING', divider='rainbow')

# converting 'version' Object type to String type
st.subheader('Data Type Conversion:', divider='orange')
data['version'] = data['version'].astype(str)
code = """
# converting 'version' Object type to String type
data['version'] = data['version'].astype(str)
"""
st.code(code, language='python')

##################################################################################################################
###################################################################################################################

st.header('EXPLORATORY DATA ANALYSIS', divider='rainbow')

# checking data distribution
st.subheader('Data Distribution & Sample Ratio Mismatch:', divider='orange')
st.write(data['version'].value_counts())
data['version'].value_counts().plot(kind='bar')
st.pyplot(plt)
plt.close()

st.markdown('#### Checking *Sample Ratio Mismatch*:')
st.markdown("""
Although our data looks fairly balanced, we want to confirm this mathematically before putting it through a statistical 
test to know if this slight mismatch is normal or not by checking *Sample Ratio Mismatch*:
""")


# defining SRM function
def SRM(dataframe):
    gate_30 = dataframe['version'].value_counts().loc['gate_30']
    gate_40 = dataframe['version'].value_counts().loc['gate_40']

    st.write(f'Number of players in Group A (gate_30): {gate_30}')
    st.write(f'Number of players in Group B(gate_40): {gate_40}')

    observed = [gate_30, gate_40]
    total_player = sum(observed)
    expected = [total_player / 2, total_player / 2]

    chi = chisquare(observed, f_exp=expected)
    st.write(f'p-value: {round(chi[1], 4)}\n')
    if chi[1] < 0.01:
        st.write('SRM detected')
    else:
        st.write('No SRM detected')


code_minusinfinty = """
# defining SRM function
def SRM(dataframe):
    gate_30 = dataframe['version'].value_counts().loc['gate_30']
    gate_40 = dataframe['version'].value_counts().loc['gate_40']

    st.write(f'Number of players in Group A (gate_30): {gate_30}')
    st.write(f'Number of players in Group B(gate_40): {gate_40}')

    observed = [gate_30, gate_40]
    total_player = sum(observed)
    expected = [total_player / 2, total_player / 2]

    chi = chisquare(observed, f_exp=expected)
    st.write(f'p-value: {round(chi[1], 4)}\n')
    if chi[1] < 0.01:
        st.write('SRM detected')
    else:
        st.write('No SRM detected')
"""
st.code(code_minusinfinty, language='python')
code_minusinfinty0 = """
# passing data to the 'SRM' function
SRM(data)
"""
st.code(code_minusinfinty0, language='python')
# passing data to the 'SRM' function
st.write(SRM(data))
st.write("""
- Our `SRM` function indicates that ***there's a significant difference*** in the distribution of our two groups. We'll 
handle the distribution below:
""")

st.markdown("#### Handling *Sample Ratio Mismatch*")
st.markdown("""
Randomly sample from each group in our original dataset to obtain a new dataset with balanced groups. In our case, each 
group will have 44,000 observations:
""")
control = data[data['version'] == 'gate_30']
treatment = data[data['version'] == 'gate_40']

balanced_data = pd.concat([
    control.sample(n=44000, axis='index', random_state=222),
    treatment.sample(n=44000, axis='index', random_state=222)], ignore_index=True)
code = """
control = data[data['version'] == 'gate_30']
treatment = data[data['version'] == 'gate_40']

balanced_data = pd.concat([
    control.sample(n = 44000, axis='index', random_state=222),
    treatment.sample(n=44000, axis='index', random_state=222)], ignore_index=True)
"""
st.code(code, language='python')

st.write("Calling our `SRM` function again to check the balance:")
code0 = """
SRM(balanced_data)
"""
st.code(code0)
st.write(SRM(balanced_data))
st.markdown("""
- Our *Sample Ratio Mismatch* has disappeared.
""")

##############################################################################################################

# checking retention rate of both groups
st.subheader('Average ***Retention Rate*** of both Groups:', divider='orange')
st.write("Average retention after 1 and 7 days for both the control and treatment groups:")
retention_rate = round(balanced_data.groupby('version')[['retention_1', 'retention_7']].mean() * 100, 4)
st.write(retention_rate)
st.write("Both groups performed pretty similarly, with our **control group (gate 30)** tending to have a *higher "
         "retention* rate after both 1 and 7 days, visualized below:")

# visualizing retention rate
st.markdown('##### *Bar* Plot:')
plt.figure(figsize=(8, 6))
sns.barplot(x=balanced_data['version'], y=balanced_data['retention_7'], ci=False)
plt.ylim(0, 0.2)
plt.title('Retention Rate after 1 week', pad=20)
plt.xlabel('Group', labelpad=15)
plt.ylabel('Average Retention', labelpad=15)

st.pyplot(plt)
plt.close()

st.markdown('##### *Kernel Density Estimation (KDE)* Plot:')


def bootstrap_distribution(group, limit=1000):
    # function borrowed from https://www.kaggle.com/code/serhanturkan/a-b-testing-for-mobile-game-cookie-cats
    bootstrap_retention = pd.DataFrame([balanced_data.sample(frac=1, replace=True).groupby("version")[group].mean()
                                        for i in range(limit)])

    sns.set(rc={"figure.figsize": (18, 5)})
    bootstrap_retention.plot.kde()
    plt.title("KDE Plot of the 1 day retention's bootstrap distributions"
              if group == "retention_1"
              else "KDE Plot of the 7 day retention's bootstrap distributions",
              fontweight="bold")
    plt.xlabel("Retention rate")
    # display plot using streamlit
    st.pyplot(plt)


st.write(bootstrap_distribution('retention_1'))
st.write(bootstrap_distribution('retention_7'))
st.write("""
- There's a difference between both the control and treatment groups for 1-day retention and 7-day retention. 
- Gap between the groups in the 7-day retention chart is much larger than in the 1-day retention chart. 
- Treatment group retention is slightly lower than the control group. 
""")

####################################################################################################################
####################################################################################################################

st.header('CONDUCTING TEST', divider='rainbow')

st.write("""
Perform a statistical test to determine whether the difference between our control and experiment group is 
statistically significant or not:
""")
st.subheader('Contingency Table:', divider='orange')
st.markdown("Contingency tables to see frequency differences in retention between our groups:")
day_retention = pd.crosstab(balanced_data['version'], balanced_data['retention_1'])
week_retention = pd.crosstab(balanced_data['version'], balanced_data['retention_7'])

st.markdown('#### Day Retention')
st.write(day_retention)
st.markdown('#### Week Retention')
st.write(week_retention)

st.subheader('Statistical Test:', divider='orange')


# function to run our statistical test
def chi2test(data):
    _, p, _, _ = chi2_contingency(data)
    significance_level = 0.05

    st.write(f'p-value = {round(p, 4)}, significance level = {significance_level}')

    if p > significance_level:
        st.write('Two groups have no significant difference')
    else:
        st.write('Two groups have a significant difference')


code1 = """
# function to run our statistical test
def chi2test(data):
    _, p, _, _ = chi2_contingency(data)
    significance_level = 0.05

    st.write(f'p-value = {round(p, 4)}, significance level = {significance_level}')

    if p > significance_level:
        st.write('Two groups have no significant difference')
    else:
        st.write('Two groups have a significant difference')
"""

st.code(code1)
code2 = """
# run the test on our data
chi2test(day_retention)
"""

st.markdown('#### *Testing Hypothesis 1 (Day Retention)*')
st.code(code2)
# run the test on our data
st.write(chi2test(day_retention))

st.write("""
- **P-value** of *0.08* which is *higher* than our **significance level**, means there's ***not a significant 
difference*** in the retention of our control and treatment groups after 1 day.
""")

st.markdown('#### *Testing Hypothesis 2 (Week Retention)*')
code3 = """
chi2test(week_retention)
"""
st.code(code3)
st.write(chi2test(week_retention))

st.write("""
- **P-value** of *0.001* which is *lower* than our **significance level** means there's a ***statistically 
significant difference*** in retention after 7 days between the control and treatment groups.
""")

###################################################################################################################
###################################################################################################################
st.header('RESULTS & BUSINESS RECOMMENDATIONS', divider='rainbow')
st.subheader('RESULTS', divider='orange')
st.write("""
- **Being in the group that sees the first gate at level 40 has no effect on retention after 1 day** , meaning we 
failed to reject our null hypothesis. This may be because 1 day is too short of a time period to properly capture the 
way user engagement does or does not change. Or it may mean that the users who play our game on a daily basis are 
indifferent to where a gate is located!
- **Being in the group that sees the first gate at level starting at gate 40 does affect user retention after 7 days** , 
meaning we can reject our null hypothesis.
""")
st.subheader('BUSINESS RECOMMENDATIONS', divider='orange')
st.write("""
- **Retain the Current Gate Placement:** These results show that users who play our game on a weekly basis have lower 
overall user retention if the first game gate is moved up to level 40. In this case, it may be best to keep the gate 
where it is rather than move it since we observed a negative change in user retention.
- **Investigate User Behaviour Beyond 7 Days:** However, because we saw no significant change in retention after 1 day 
yet we saw one after 7 days, it may be beneficial to run this type of experiment over longer time periods. For example, 
testing how retention changes after 7 and 14 days.
- **Segmentation of User Types:** Segment your users based on play patterns. For example, casual players might react 
differently to gates compared to more engaged players. Personalizing gate placement for different segments could 
improve overall retention. This can be implemented by analyzing high-engagement versus low-engagement users and 
adjusting gameplay or challenges accordingly.
- **Optimize User Experience Around The Gate:** Analyze the gate's mechanics. Could it be too difficult or disruptive 
at level 40? Consider making the gate less challenging, adding a reward system, or offering a small in-game incentive 
(like extra lives, bonuses, or faster progression) to make passing the gate more appealing. 
""")
st.subheader('NEXT STEPS', divider='orange')
st.write("""
1. Testing different hypothesis like run additional A/B tests with varied gate placements. \n
2. Segment users based on engagement patterns and tailor the experience. \n
3. Explore user behavior for longer periods (14 or 30 days) to assess long-term effects. \n
4. Test in-game incentives or rewards around the gate to mitigate the negative effect on retention. \n
These strategies can help us refine the game's design and improve user retention while balancing both engagement and monetization goals.
""")

st.divider()
###############################################################################################################
###############################################################################################################