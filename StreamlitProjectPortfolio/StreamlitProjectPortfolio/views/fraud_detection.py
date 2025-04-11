import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, RocCurveDisplay, ConfusionMatrixDisplay
from imblearn.over_sampling import RandomOverSampler
import streamlit as st

st.title('FRAUD DETECTION')

st.header('*EXECUTIVE SUMMARY*', divider='orange')
st.subheader('Business Problem:')
st.markdown("""
A typical organization loses an estimated 5% of its yearly revenue to fraud. Identify and prevent fraudulent 
transactions, minimizing financial losses while ensuring a smooth customer experience. Detect fraudulent behavior based 
upon past fraud.
""")
st.subheader('Methodology:')
st.markdown("""
- *Data Wrangling* (checked class balance, resampled data).
- Built an *Ensemble Model* consisting of three classification algorithms.
- *Evaluated Results* using various Metrics. 
""")
st.subheader('Skills:')
st.markdown("""
**Language:** Python \n
**Data Manipulation Libraries:** Pandas, Datetime \n
**Statistics Libraries:** SciPy, Scikit-Learn, Imbalance-Learn \n
**Visualization Libraries:** Matplotlib, Seaborn \n
**App & Dashboard Tool:** Streamlit \n
**Statistics and Analytical Algorithms:** Random Over-Sampling, Logistic Regression, Random Forest Classifier, Decision 
Tree Classifier, Ensemble Model
""")
st.subheader('Results:')
st.write("""
- A **precision** of ***88.6%*** indicates that the model is fairly reliable at predicting fraud, with a relatively low 
false-positive rate.
- A **recall** of ***85.7%*** means the model is catching most fraudulent transactions, but it still misses about 14.3% of them.
- The **F1-Score** of ***87.1%*** reflects a good balance between precision and recall, showing that the model is effective at 
detecting fraud.
- Our model has a high **accuracy** of ***98.95%***, which means it’s generally good at classifying transactions correctly.
- An **AUC-ROC score** of ***0.9729*** means our fraud detection model is highly effective at distinguishing between 
fraudulent and legitimate transactions. It suggests that the model is reliable and has a very low chance of mixing up 
frauds with legitimate transactions.
""")
st.subheader('Business Recommendations:')
st.write("""
- With a recall of 85.7%, about 14.3% of fraudulent transactions are missed. These undetected frauds could lead to 
significant financial losses. We can consider **additional layers of review** or investigation for transactions that are 
flagged as borderline cases (high probability but below the threshold).
- Explore **threshold tuning** to reduce false negatives or implement manual review processes for transactions close to the 
threshold.
- **Segment transactions** by customer profiles or transaction types to identify whether specific groups are more prone to 
fraud. Tailor fraud prevention strategies for high-risk customer segments.
""")
st.subheader('Next Steps:')
st.write("""
- **Test other algorithms** for potential performance improvements.
- **Enhance feature engineering** with behavioral, temporal, and geolocation data.
- **Deploy a monitoring dashboard** for real-time tracking.
- **Plan regular model retraining** to adapt to evolving fraud tactics.
""")

################################################################################################################
################################################################################################################

st.header('PROJECT', divider='rainbow')
st.subheader('DATA SET', divider='orange')
st.write("Features in the dataset are anonymized to ensure no sensitive information is exposed:")
url = "https://raw.githubusercontent.com/maryamtariq-analytics/FraudDetection/refs/heads/main/creditcard_sampledata_2.csv"
data = pd.read_csv(url)
st.write(data)

################################################################################################################
################################################################################################################
st.header('DATA WRANGLING', divider='rainbow')
st.subheader('Checking Class Balance', divider='orange')

st.write("##### Class Count:")
fraud = data[['Unnamed: 0', 'Class']]
fraud_total = fraud.groupby(['Class']).count()
fraud_total = fraud_total.rename(columns={'Unnamed: 0': 'Count'})
st.write(fraud_total)

st.write("##### Class Count (Percentage):")
fraud_percentage = fraud_total / fraud_total.sum() * 100
fraud_percentage = fraud_percentage.rename(columns={'Unnamed: 0': 'Percentage'})
st.write(fraud_percentage)

st.write('- **The Class is highly imbalanced!**')

###############################################################################################################

st.subheader("Visualizing Class Imbalance", divider='orange')
st.write("To visualize Class Imbalance, we first need to split our variables into *dependent* and *independent* variables:")
# splitting features into independent and dependent variables
y = data['Class']

x = data.copy()
x = x.drop(['Unnamed: 0', 'Amount', 'Class'], axis=1)
code = """
# splitting features into independent and dependent variables
y = data['Class']

x = data.copy()
x = x.drop(['Unnamed: 0', 'Amount', 'Class'], axis=1)
"""
st.code(code, language='python')

# a function to create scatter plot
def plot_data(x, y):
    # create a figure and axis
    fig, ax = plt.subplots()
    # plot class 0
    ax.scatter(x.loc[y == 0, x.columns[0]], x.loc[y == 0, x.columns[1]], label='CLASS 0', alpha=0.5, linewidth=0.15)
    # plot class 1
    ax.scatter(x.loc[y == 1, x.columns[0]], x.loc[y == 1, x.columns[1]], label='CLASS 1', alpha=0.5, linewidth=0.15, c='r')
    # add legend
    ax.legend()
    # show plot
    return fig
fig = plot_data(x,y)
st.pyplot(fig)

################################################################################################################
st.subheader('Balancing Class Imbalance (*Over-Sampling*)', divider='orange')
st.write("We need to first split our data into training and testing data because after that we apply "
         "***Over-Sampling*** to only training data and leave out the testing data that's unaltered by the sampling "
         "adjustment in order to understand how well our classification model predicts on the actual class distribution "
         "observed in real world: ")
# splitting data into training and testing data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

code0 = """
# splitting data into training and testing data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
"""
st.code(code0, language='python')

# using 'over-sampling' technique to adjust class imbalance
method = RandomOverSampler()
# fitting sampling technique just to training data
x_resampled, y_resampled = method.fit_resample(x_train, y_train)
code5 = """
# using 'over-sampling' technique to adjust class imbalance
method = RandomOverSampler()
# fitting sampling technique just to training data
x_resampled, y_resampled = method.fit_resample(x_train, y_train)
"""
st.code(code5, language='python')

st.write('#### Visualizing Balanced Class:')
fig0 = plot_data(x_resampled, y_resampled)
st.pyplot(fig0)

st.write("#### Comparing Both Imbalanced & Balanced Data:")
def compare_plot(x, y, x_resampled, y_resampled):
    # create a fig with two subplots (1 row, 2 columns)
    fig, axs = plt.subplots(1, 2)

    # plot the original data in the first subplot
    axs[0].scatter(x.loc[y == 0, x.columns[0]], x.loc[y == 0, x.columns[1]], label="Class #0", alpha=0.5, linewidth=0.15)
    axs[0].scatter(x.loc[y == 1, x.columns[0]], x.loc[y == 1, x.columns[1]], label="Class #1", alpha=0.5, linewidth=0.15, c='r')
    axs[0].set_title('Original Set')
    axs[0].legend()

    # plot the resampled data in the second subplot
    axs[1].scatter(x_resampled.loc[y_resampled == 0, x_resampled.columns[0]], x_resampled.loc[y_resampled == 0, x_resampled.columns[1]], label="Class #0", alpha=0.5, linewidth=0.15)
    axs[1].scatter(x_resampled.loc[y_resampled == 1, x_resampled.columns[0]], x_resampled.loc[y_resampled == 1, x_resampled.columns[1]], label="Class #1", alpha=0.5, linewidth=0.15, c='r')
    axs[1].set_title('Resampled Set')
    axs[1].legend()

    # return the fig object
    return fig

fig1 = compare_plot(x,y,x_resampled,y_resampled)
st.pyplot(fig1)
st.write("- The darkened red points in resampled data show the oversampled data points to bring balance in the dataset's "
         "class.")

#################################################################################################################
#################################################################################################################

st.header('MODELLING', divider='rainbow')

st.write("""
We use an ***Ensemble Model*** encompassing of following predictive models:
- **Logistic Regression**
- **Random Forest Classifier**
- **Decision Tree Classifier**
""")

# define the three classifiers to use in the ensemble
clf1 = LogisticRegression(class_weight={0:1, 1:15},
                          random_state=5,
                          solver='liblinear')
clf2 = RandomForestClassifier(class_weight={0:1, 1:12},
                              criterion='gini',
                              max_depth=8,
                              max_features='log2',
                              min_samples_leaf=10,
                              n_estimators=30,
                              n_jobs=-1,
                              random_state=5)
clf3 = DecisionTreeClassifier(random_state=5,
                              class_weight='balanced')

# combine classifiers in an ensemble model
ensemble_model = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('dt', clf3)], voting='soft')

code1 = """
# define the three classifiers to use in the ensemble
clf1 = LogisticRegression(class_weight={0:1, 1:15},
                          random_state=5,
                          solver='liblinear')
clf2 = RandomForestClassifier(class_weight={0:1, 1:12},
                              criterion='gini',
                              max_depth=8,
                              max_features='log2',
                              min_samples_leaf=10,
                              n_estimators=30,
                              n_jobs=-1,
                              random_state=5)
clf3 = DecisionTreeClassifier(random_state=5,
                              class_weight='balanced')

# combine classifiers in an ensemble model
ensemble_model = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('dt', clf3)], voting='soft')
"""
st.code(code1, language='python')

# fit and predict
ensemble_model.fit(x_train, y_train)
predicted = ensemble_model.predict(x_test)
probs = ensemble_model.predict_proba(x_test)

code2 = """
# fit and predict
ensemble_model.fit(x_train, y_train)
predicted = ensemble_model.predict(x_test)
probs = ensemble_model.predict_proba(x_test)
"""
st.code(code2, language='python')
################################################################################################################
st.header('EVALUATION & RESULTS', divider='rainbow')

# getting metric results
st.write('#### CLASSIFICATION REPORT:')
report_dict = classification_report(y_test, predicted, output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()
st.dataframe(report_df)
st.write("""
- A **precision** of ***88.6%*** indicates that the model is fairly reliable at predicting fraud, with a relatively low 
false-positive rate.
- A **recall** of ***85.7%*** means the model is catching most fraudulent transactions, but it still misses about 14.3% of them.
- The **F1-Score** of ***87.1%*** reflects a good balance between precision and recall, showing that the model is effective at 
detecting fraud.
- Our model has a high **accuracy** of ***98.95%***, which means it’s generally good at classifying transactions correctly.
""")

st.write('#### AUC-ROC SCORE:')
st.write(roc_auc_score(y_test, probs[:,1]))

# Plot the ROC Curve
fig30, ax = plt.subplots(figsize=(6, 6))  # Create a Matplotlib figure
RocCurveDisplay.from_predictions(y_test, probs[:, 1], ax=ax)  # Plot on the given axis
plt.title('ROC Curve')  # Add a title for better clarity
# Display the plot in Streamlit
st.pyplot(fig30)

st.write("""
- An **AUC-ROC score** of ***0.9729*** means our fraud detection model is highly effective at distinguishing between 
fraudulent and legitimate transactions. It suggests that the model is reliable and has a very low chance of mixing up 
frauds with legitimate transactions.
""")

st.write('#### CONFUSION MATRIX:')
# create helper function to plot confusion matrix
def conf_matrix_plot(model, x_data, y_data):
    model_pred = model.predict(x_data)
    cm = confusion_matrix(y_data, model_pred, labels=model.classes_)

    # Create a confusion matrix plot
    plt.figure(figsize=(8, 6))  # Set the figure size
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')

    # Display the plot in Streamlit
    st.pyplot(plt)

conf_matrix_plot(ensemble_model, x_test, y_test)

st.write("""
- **True Positives = 78:** Transactions that were actually fraudulent and correctly identified as fraud by our model.   
- **True Negatives = 2089:** Transactions that were not fraudulent and were correctly identified as non-fraudulent by 
our model. 
- **False Positives = 10:** Transactions that were not fraudulent but were incorrectly classified as fraud by our model.   
- **False Negatives = 13:** Transactions that were actually fraudulent but were incorrectly classified as non-fraudulent 
by your model. These are missed fraud cases. 
""")

##############################################################################################################
##############################################################################################################
st.header('BUSINESS RECOMMENDATIONS', divider='rainbow')
st.write("""
- With a recall of 85.7%, about 14.3% of fraudulent transactions are missed. These undetected frauds could lead to 
significant financial losses. We can consider **additional layers of review** or investigation for transactions that are 
flagged as borderline cases (high probability but below the threshold).
- Explore **threshold tuning** to reduce false negatives or implement manual review processes for transactions close to the 
threshold.
- **Segment transactions** by customer profiles or transaction types to identify whether specific groups are more prone to 
fraud. Tailor fraud prevention strategies for high-risk customer segments.
""")

##############################################################################################################
##############################################################################################################
st.header('NEXT STEPS', divider='rainbow')
st.write("""
- **Test other algorithms** for potential performance improvements.
- **Enhance feature engineering** with behavioral, temporal, and geolocation data.
- **Deploy a monitoring dashboard** for real-time tracking.
- **Plan regular model retraining** to adapt to evolving fraud tactics.
""")

###############################################################################################################
###############################################################################################################
st.divider()