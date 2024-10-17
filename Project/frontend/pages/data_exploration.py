"""This page will go over the db file and be used to display some of the data
before and after cleaning."""

import requests
import pandas as pd
import streamlit as st

st.title("Get to know the data!")

# Add a button in the sidebar
if st.sidebar.button("Scroll to Top"):
    # Use Streamlit's ability to render HTML and embed JavaScript to scroll to the top
    st.markdown(
        """
        <script>
        document.documentElement.scrollTop = 0;
        </script>
        """,
        unsafe_allow_html=True,
    )

# Radio buttons for single table selection
table_option = st.radio(
    "Select what you want to examine:",
    ("Raw Data", "Cleaned, Numeric Data"),
    key="table_option",
)

INPUT_QUERY = ""
if table_option == "Raw Data":
    INPUT_QUERY = "SELECT * FROM combined_data;"
elif table_option == "Cleaned, Numeric Data":
    INPUT_QUERY = "SELECT * FROM cleaned_data;"

query = st.text_area(label="Enter your SQL query here:", value=INPUT_QUERY)

if st.button("Submit"):
    response = requests.post(
        "http://fastapi_route:8000/query", json={"query": query}, timeout=15
    )

    if response.status_code == 200:
        try:
            result = response.json()
            data_dict = result.get("data", {})
            columns = data_dict.get("columns", [])
            data = data_dict.get("data", [])

            # Check if data and columns are not empty
            if data and columns:
                # Convert the JSON response to a pandas DataFrame with column names
                df = pd.DataFrame(data, columns=columns)
                st.dataframe(df)  # Display DataFrame in Streamlit

        except requests.exceptions.JSONDecodeError:
            st.error("Error: The response is not in JSON format.")
            st.write("Response content:", response.text)

    else:
        st.error(f"Error: Received status code {response.status_code}")
        st.write("Response content:", response.text)
