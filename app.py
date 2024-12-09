import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure set_page_config is the first Streamlit command
st.set_page_config(
    page_title="Drug Overdose Deaths Analysis",
    page_icon="💊",
    layout="wide"
)

# Load the dataset
@st.cache_data
def load_data():
    try:
        file_path = "Ch. 26 - Drug Overdose Deaths 1999-2018_Drug Overdose Deaths 1999-2018.csv"  # Ensure this matches your dataset's name
        data = pd.read_csv(file_path)
        data.columns = data.columns.str.strip()  # Strip any extra spaces in column names
        data['Year'] = pd.to_datetime(data['Report Date']).dt.year  # Extract year from report date
        return data
    except FileNotFoundError:
        st.error(f"File not found: {file_path}. Please ensure the dataset is in the correct directory.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading the dataset: {e}")
        return pd.DataFrame()

# Load dataset
data = load_data()

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Visualizations"])

# Home Page
if page == "Home":
    st.title("💊 Welcome to the Drug Overdose Deaths Analysis App!")
    st.write(
        """
        This app provides insights into drug overdose deaths in the United States from 1999 to 2018.
        
        ### Features:
        - Explore trends over the years for different states.
        - Visualize deaths by drug type and demographics.
        - Analyze state-wise comparisons and trends.
        
        ### Data Source:
        The data used in this app is publicly available from the **CDC Wonder Database**.
        
        ### How to Use:
        - Navigate to the **Visualizations** page to explore interactive charts.
        """
    )

# Visualizations Page
elif page == "Visualizations":
    st.title("Drug Overdose Deaths Visualizations")

    if not data.empty:
        # Required columns
        required_columns = ['Year', 'State', 'Cause of Death Description', 'Drug Overdose Death Count']
        missing_columns = [col for col in required_columns if col not in data.columns]

        if missing_columns:
            st.error(f"The dataset is missing the required columns: {', '.join(missing_columns)}")
        else:
            # Sidebar Filters
            st.sidebar.title("Filters")
            selected_year = st.sidebar.selectbox(
                "Select Year",
                ["All"] + sorted(data['Year'].unique().tolist())
            )
            selected_state = st.sidebar.selectbox(
                "Select State",
                ["All"] + sorted(data['State'].unique().tolist())
            )
            selected_cause = st.sidebar.selectbox(
                "Select Cause of Death",
                ["All"] + sorted(data['Cause of Death Description'].unique().tolist())
            )

            # Apply filters
            filtered_data = data.copy()
            if selected_year != "All":
                filtered_data = filtered_data[filtered_data['Year'] == int(selected_year)]
            if selected_state != "All":
                filtered_data = filtered_data[filtered_data['State'] == selected_state]
            if selected_cause != "All":
                filtered_data = filtered_data[filtered_data['Cause of Death Description'] == selected_cause]

            # Line Chart
            st.write("### Trends of Drug Overdose Deaths Over the Years")
            line_data = filtered_data.groupby('Year')['Drug Overdose Death Count'].sum().reset_index()
            if not line_data.empty:
                line_fig = px.line(
                    line_data,
                    x="Year",
                    y="Drug Overdose Death Count",
                    title="Trends of Drug Overdose Deaths Over the Years",
                    labels={"Drug Overdose Death Count": "Number of Deaths"}
                )
                st.plotly_chart(line_fig)
            else:
                st.write("No data available for the selected filters.")

            # Bar Chart
            st.write("### State-wise Drug Overdose Deaths")
            state_data = filtered_data.groupby('State')['Drug Overdose Death Count'].sum().reset_index()
            if not state_data.empty:
                bar_fig = px.bar(
                    state_data,
                    x="State",
                    y="Drug Overdose Death Count",
                    title="State-wise Drug Overdose Deaths",
                    labels={"Drug Overdose Death Count": "Number of Deaths"}
                )
                st.plotly_chart(bar_fig)
            else:
                st.write("No data available for the selected filters.")

            # Scatter Plot
            st.write("### Deaths vs Cause of Death")
            if not filtered_data.empty:
                scatter_fig = px.scatter(
                    filtered_data,
                    x="Cause of Death Description",
                    y="Drug Overdose Death Count",
                    title="Deaths vs Cause of Death",
                    labels={"Drug Overdose Death Count": "Number of Deaths"},
                    color="State"
                )
                st.plotly_chart(scatter_fig)
            else:
                st.write("No data available for the selected filters.")

            # Histogram
            st.write("### Distribution of Death Counts")
            if not filtered_data.empty:
                hist_fig = px.histogram(
                    filtered_data,
                    x="Drug Overdose Death Count",
                    nbins=30,
                    title="Distribution of Death Counts",
                    labels={"Drug Overdose Death Count": "Number of Deaths"},
                    color="State",
                    marginal="box"  # Adds box plot on the side
                )
                st.plotly_chart(hist_fig)
            else:
                st.write("No data available for the selected filters.")
    else:
        st.warning("No data available to display. Please check your dataset.")
