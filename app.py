import streamlit as st
import json
import requests

st.title('Property Evaluation')


with open('input_options.json') as f:
    side_bar_options = json.load(f)
    options = {}
    for key, value in side_bar_options.items():
        if key == 'city':
            options[key] = st.sidebar.selectbox(key, value)
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

    payload = json.dumps({'inputs': options})
    
    try:

        response = requests.post(
            url="64.225.10.251:5002/invocations",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        
        if response.status_code == 200:
            try:
                # Parse the JSON response
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
