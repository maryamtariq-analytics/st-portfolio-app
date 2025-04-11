import streamlit as st

# Add the Material Icons stylesheet
st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" rel="stylesheet">',
            unsafe_allow_html=True)

# HERO section
col1, col2 = st.columns(2, gap='small', vertical_alignment='center')

with col1:
    st.title("Maryam Tariq")
    st.write('**DATA ANALYSIS | BUSINESS INTELLIGENCE**')
with col2:
    st.write("""
    - <span class="material-icons" style="vertical-align: middle; font-size: 16px;">email</span> maryam.tariq.analytics@gmail.com 
    - <span class="material-icons" style="vertical-align: middle; font-size: 16px;">phone</span> (+92) 336 5188821 
    - <span class="material-icons" style="vertical-align: middle; font-size: 16px;">linkedin</span> <a href="https://www.linkedin.com/in/ladymt/" style="text-decoration: none; display: inline-block; vertical-align: middle;">LinkedIn</a>
    """, unsafe_allow_html=True)






st.divider()
############################################################################################################
# SKILLS
st.write("\n")
st.markdown("### *SKILLS*")
st.write("""
- ***Programming & Databases:*** Python (NumPy, Pandas, Statsmodels, SciPy, Scikit-Learn, Imbalance-Learn, XG Boost, 
PyCaret, Fastai, PyTorch, Hugging Face), SQL, BigQuery.
- ***Statistics & Models:*** Descriptive Statistics, Inferential Statistics, A/B Testing, Regression (Linear, Multiple-Linear, 
Logistic, Decision Tree Regressor), Classification (Logistic Regression, Naive Bayes, Decision Tree Classifier), 
Clustering (K-Means), Ensemble (Random Forest, Gradient Boosting, Voting Regressor/Classifier), Deep Learning,
Time Series Analysis.
- ***Visualization & Dashboard:*** Matplotlib, Seaborn, Plotly, Power BI, Streamlit.
""")

st.divider()
##########################################################################################################

# PROJECTS
st.markdown("### *PROJECTS*")
st.write("**Full projects can be accessed through left side bar*")
st.write('##### Customer Retention Cohort Analysis')
st.write("""
- Developed a cohort analysis model to track **user behaviour pattern** to identify critical **user retention trends** 
in order to devise actions for increasing customer lifetime value and enhanced targeted marketing strategies.
""")
st.write('##### Mobile App A/B Testing')
st.write("""
- **Designed an A/B testing framework** for a gaming app to compare the effect of two feature versions on customer 
retention rates, using the **chi-square test for independence**.
""")
st.write('##### Optimizing Marketing Campaign')
st.write("""
- Designed a data driven **marketing campaign optimization strategy** to **reduce customer acquisition costs** through 
targeted analytics for different client types utilizing **correlation analysis** and **multiple linear regression**. 
""")
st.write('##### Customer Segmentation')
st.write("""
- Analyzed **customer spending behaviour** by segmenting into clusters in order to **improve customer retention** and 
**acquisition strategies** utilizing **KMeans clustering algorithm**. 
""")
st.write('##### Stock and Sales Analysis')
st.write("""
- Addressed a supply chain issue by **predicting features contributing to optimum stock levels** based on sales and 
sensor data of a grocery store.
- Perfromed **data wrangling** and applied **gradient boosted regression algorithm** with a **0.224 MAE**.
""")
st.write('##### Fraud Detection')
st.write("""
- Engineered a fraudulent transaction detection algorithm utilizing **ensembled machine learning algorithms, reducing 
false positives** with **97% accuracy**.
""")
st.write('##### Retail Store Analysis Visualizations')
st.write("""
- **Drafted questions** and **generated data visualizations** to answer business questions and provide insights 
regarding business revenue. 
""")
st.write('##### Dynamic Pricing Model')
st.write("""
* Created a model to **maximize revenue** and **profits** by adjusting prices dynamically via **balancing supply** and 
**demand dynamics** and implementing a **Random Forest Regressor** for a ride hailing business.
""")
st.write('##### RFM Analysis')
st.write("""
* Granularly analyzed customer buying behavior using **recency**, **frequency** and **monetary value** as metrics for use 
in surgical marketing campaigns and other strategic business growth projects.
""")

st.divider()
##########################################################################################################

# EXPERIENCE
st.markdown("### *EXPERIENCE*")
st.write('##### Behavioral Economics Virtual Experience | Standard Bank | November 2024')
st.write("""
- **Researched** behavioral economics concepts applied to the financial services sector.
- Applied the EAST and TESTS frameworks to identify opportunities to **expand the adoption** of a product.
- Carried out **statistical analysis** on the **significance of marketing initiatives** in adopting the product.
""")
st.write('##### Data Science Virtual Experience | Boston Consulting Group | October 2024')
st.write("""
- **Outlined a strategic investigation approach** for an Energy sector client to determine factors leading to customer churn
- Conducted thorough **Exploratory Data Analysis** and **Feature Engineering** techniques for trend interpretation
- Engineered and optimized a Random Forest model, achieving an **85% accuracy rate** in predicting customer churn
""")
st.write('##### Data Analytics Virtual Experience | Accenture North America | October 2024')
st.write("""
- **Cleaned, modelled** and **analyzed datasets** to uncover insights into content trends to inform strategic decisions.
- **Prepared reports** to communicate key insights for the client and internal stakeholders.
""")

st.divider()
############################################################################################################
# EDUCATION
st.markdown('### *EDUCATION*')
st.write('##### Practical Deep Learning Course | fast.ai | 2024 - Present')
st.write("""
- Course on building and deploying state of the art deep learning models, encompassing computer vision, natural language 
processing, and tabular data.
- **Tools:** Fastai, PyTorch, Hugging Face
""")
st.write('##### BSc Economics (Major), Social Sciences | Shaheed Zulfiqar Ali Bhutto Institute of Science & Tech, ISB | Islamabad, Pakistan | 2023 | CGPA: 3.5/4')
st.write("""
- **Relevant Coursework:** Maths and Stats, Statistical Inference, Basic Econometrics, Game Theory, Mathematical 
Economics, Industrial Economics.
""")

st.divider()
############################################################################################################
# CERTIFICATIONS
st.markdown('### *CERTIFICATIONS*')
st.write('##### Data Analysis & Insights in SQL Mini Sprint | Clicked')
st.write('##### Machine Learning in E-commerce | DataWorkshop')

st.divider()
#############################################################################################################
# INVOLVEMENT
st.markdown('### *INVOLVEMENT*')
st.write('##### Data Classification Volunteer | Zooniverse | Dec 2024 - Present')
st.write("""
- Contribute to classifying data related to Particle and Astro Physics for use in science research.
""")

st.divider()