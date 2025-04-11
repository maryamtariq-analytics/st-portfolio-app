import streamlit as st

# page setup
about_page = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True
)

project_1_page = st.Page(
    page="views/cohort_analysis.py",
    title="Customer Retention Cohort Analysis",
    icon=":material/groups_3:"
)

project_2_page = st.Page(
    page="views/mobile_app_AB_testing.py",
    title="Mobile App A/B Testing",
    icon=":material/lab_panel:"
)

project_3_page = st.Page(
    page="views/optimizing_marketing_campaigns.py",
    title="Optimizing Marketing Campaigns",
    icon=":material/stacked_line_chart:"
)


project_4_page = st.Page(
    page="views/customer_segmentation.py",
    title="Customer Segmentation",
    icon=":material/bubble_chart:"
)

project_5_page = st.Page(
    page="views/sales_and_stock_analysis.py",
    title="Stock and Sales Analysis",
    icon=":material/grouped_bar_chart:"
)

project_6_page = st.Page(
    page="views/fraud_detection.py",
    title="Fraud Detection",
    icon=":material/mystery:"
)

project_7_page = st.Page(
    page="views/retail_store_analysis_visualizations.py",
    title="Retail Store Analysis Visualizations",
    icon=":material/local_mall:"
)

project_8_page = st.Page(
    page="views/DynamicPricingModel.py",
    title="Dynamic Pricing Model",
    icon=":material/attach_money:"
)

project_9_page = st.Page(
    page="views/RFM-Analysis.py",
    title="RFM Analysis",
    icon=":material/dashboard:"
)

## navigation setup (without sections)
#pg = st.navigation(pages=[about_page, project_1_page, project_2_page, project_3_page, project_4_page, project_5_page, project_6_page, project_7_page])

# navigation setup (with sections)
pg = st.navigation(
    {
        "Info": [about_page],
        "Projects": [project_1_page, project_2_page, project_3_page, project_4_page, project_5_page, project_6_page,
                     project_7_page, project_8_page, project_9_page]
    }
)

# insert logo
st.logo('https://github.com/maryamtariq-analytics/certs/blob/main/PortfolioLogo.png?raw=true',
        size='large')

# run navigation
pg.run()