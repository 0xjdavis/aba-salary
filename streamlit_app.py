import streamlit as st
import pandas as pd
import random
import plotly.express as px

# Set page title
st.set_page_config(page_title="Top 100 ABA Law Schools by Simulated Salary")

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

    # Create a Plotly bar chart for the top 10 schools by simulated salary
    top_10_schools = df_sorted.head(10)
    fig = px.bar(
        top_10_schools,
        x='Simulated Average Salary',
        y='School',
        orientation='h',
        title='Top 10 Law Schools by Simulated Average Salary',
        labels={'Simulated Average Salary': 'Salary (USD)', 'School': 'Law School'},
        text='Simulated Average Salary'
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(yaxis=dict(autorange="reversed"), height=500)
    
    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)

    # Display the dataframe
    st.dataframe(df_sorted, width=800)
    st.write("Note: The salary data in this app is simulated and does not reflect actual reported salaries. In a real-world scenario, accurate salary data should be obtained from reliable sources.")

if __name__ == "__main__":
    main()