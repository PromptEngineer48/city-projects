import streamlit as st
import requests
import time
import os

st.title("Runpod AI Endpoint Caller")

# Accessing the secret
api_key = st.secrets["api_key"]
# st.write("api_key:", api_key)

# Setting environment variable
os.environ["api_key"] = api_key

query = st.text_input("Enter your query:", "Which city are we talking about?")
namespace = st.text_input("Enter the namespace:", "Saratoga_CA")

# Button to trigger API call
if st.button("Submit"):

    if query and namespace:
        # st.write("Calling API...")
        url = "https://api.runpod.ai/v2/rtcmp1n94s380a/run"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {"input": {"query": query, "namespace": namespace}}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            # st.write("API Response:")
            # st.json(result)

            job_id = result.get("id")
            status = result.get("status")
            # st.write("JOB ID=>", job_id)

            st.title("Bot Reply:")

            while status != "COMPLETED":
                # st.write("Waiting for job to complete...")
                time.sleep(1)  # Wait for 1 second before checking again
                status_response = requests.get(
                    f"https://api.runpod.ai/v2/rtcmp1n94s380a/status/{job_id}",
                    headers=headers,
                )
                if status_response.status_code == 200:
                    status_result = status_response.json()
                    status = status_result.get("status")
                else:
                    st.write(
                        "Error while checking status:", status_response.status_code
                    )
                    break

            if status == "COMPLETED":
                # st.write("Job completed! Results:")
                # st.json(status_result)

                output = status_result.get("output")
                if output:
                    answer = output[
                        0
                    ]  # Extracting the first element from the 'output' list
                    # print("Answer:", answer)
                    # st.title("Bot Reply:")
                    st.write(answer)
                else:
                    print("No output found in the response.")

        else:
            st.write("Error:", response.status_code)
    else:
        st.write("Please fill in both query and namespace fields.")
