import streamlit as st
import json
import requests
import pandas as pd

st.title('Property Evaluation')

with open('input_options.json') as f:
    side_bar_options = json.load(f)
    options = {}
    for key, value in side_bar_options.items():
        if key == 'city':
            selected_city = st.sidebar.selectbox(key, value)
            for city in value:
                options[f'city_{city.replace(" ", "_")}'] = 1 if city == selected_city else 0
        else:
            min_val, max_val = value
            if isinstance(min_val, float) or isinstance(max_val, float):
                min_val, max_val = float(min_val), float(max_val)
                current_value = (min_val + max_val) / 2
                options[key] = st.sidebar.slider(key, min_val, max_val, value=current_value)
            else:
                current_value = (min_val + max_val) // 2
                options[key] = st.sidebar.slider(key, min_val, max_val, value=current_value)

st.write(options)

if st.button('Predict'):
    input_data = {key: [value] for key, value in options.items()}
    input_df = pd.DataFrame(input_data)

    payload = {
        "dataframe_split": {
            "columns": input_df.columns.tolist(),
            "data": input_df.values.tolist()
        }
    }

    try:
        response = requests.post(
            url="http://64.225.10.251:5001/invocations",
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            try:
                prediction = response.json().get('predictions')[0]
                st.write(f'The predicted median house value is: ${prediction:,}')
            except json.JSONDecodeError:
                st.error("Error decoding the JSON response from the API.")
                st.write("Response content:", response.text)
        else:
            st.error(f"API request failed with status code {response.status_code}.")
            st.write("Response content:", response.text)
    except requests.RequestException as e:
        st.error(f"An error occurred while making the API request: {e}")
