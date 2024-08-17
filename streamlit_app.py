import streamlit as st
import pandas as pd
import random
import plotly.express as px  # Correct import

# Setting page layout
st.set_page_config(
    page_title="ABA Simulated Salaries",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar for API Key and User Info
st.sidebar.header("About App")
st.sidebar.markdown('This is an app that was generated through a text-to-code method using GPT, Sonnet, Artifacts and an open source code interpretor by <a href="https://ai.jdavis.xyz" target="_blank">0xjdavis</a>.', unsafe_allow_html=True)

# Calendly
st.sidebar.markdown("""
    <hr />
    <center>
    <div style="border-radius:8px;padding:8px;background:#fff";width:100%;">
    <img src="https://avatars.githubusercontent.com/u/98430977" alt="Oxjdavis" height="100" width="100" border="0" style="border-radius:50%"/>
    <br />
    <span style="height:12px;width:12px;background-color:#77e0b5;border-radius:50%;display:inline-block;"></span> <b>I'm available for new projects!</b><br />
    <a href="https://calendly.com/0xjdavis" target="_blank"><button style="background:#126ff3;color:#fff;border: 1px #126ff3 solid;border-radius:8px;padding:8px 16px;margin:10px 0">Schedule a call</button></a><br />
    </div>
    </center>
    <br />
""", unsafe_allow_html=True)

# Copyright
st.sidebar.caption("©️ Copyright 2024 J. Davis")

# Function to get ABA-approved law schools from CSV
@st.cache_data
def get_aba_schools():
    # Load the CSV data into a DataFrame
    url = "aba-accredited-schools.csv"  # Replace with your actual CSV file path or URL if hosted online
    df = pd.read_csv(url, header=None)
    schools = df[0].tolist()  # Extract the school names from the first column
    return schools[:100]  # Return only top 100 schools

# Function to simulate salary data
def simulate_salary(school_name):
    # This is a simplified simulation and doesn't reflect real data
    base_salary = 70000
    random_factor = random.uniform(0.8, 1.5)
    return int(base_salary * random_factor)

# Main function
def main():
    st.title("Top 100 ABA-Approved Law Schools")
    st.write("Ranked by Simulated Average Salary for Recent Graduates")
    
    # Get the list of schools
    schools = get_aba_schools()

    # Create a dataframe with schools and simulated salaries
    data = {
        'School': schools,
        'Simulated Average Salary': [simulate_salary(school) for school in schools]
    }
    df = pd.DataFrame(data)

    # Sort the dataframe by salary in descending order
    df_sorted = df.sort_values('Simulated Average Salary', ascending=False).reset_index(drop=True)

    # Add a rank column
    df_sorted['Rank'] = df_sorted.index + 1

    # Reorder columns
    df_sorted = df_sorted[['Rank', 'School', 'Simulated Average Salary']]

    # Create a Plotly box plot for the salary distribution
    fig = px.box(
        df_sorted,
        y='Simulated Average Salary',
        x='School',
        title='Salary Distribution for Top 100 Law Schools',
        labels={'Simulated Average Salary': 'Salary (USD)', 'School': 'Law School'},
        points="all"  # Display all points for clarity
    )
    fig.update_layout(xaxis=dict(tickangle=-45), height=600)
    
    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)

    # Display the dataframe
    st.dataframe(df_sorted, width=800)
    st.write("Note: The salary data in this app is simulated and does not reflect actual reported salaries. In a real-world scenario, accurate salary data should be obtained from reliable sources.")

if __name__ == "__main__":
    main()
