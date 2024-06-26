import streamlit as st
import requests
import time
import os
    
st.title("Saratoga City Code Chatbot")

api_key = st.secrets["api_key"]
os.environ["api_key"] = api_key



user_input = st.text_input("Enter your query:", "Which city are we talking about?")
namespace = st.text_input("Enter the namespace:", "Saratoga_CA")
thread_id = st.text_input("Enter the thread_id", "thread_VXoSkmz2GEKqDVIdwCykUUBa")


# session_state = get_session_state()
# history = session_state["history"]

# Button to trigger API call
if st.button("Submit"):

    if user_input and namespace and thread_id:
        st.write("Calling API...")

        url = "https://api.runpod.ai/v2/nysr8clq7it18g/run"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "input": {
                "user_input": user_input,
                "namespace": namespace,
                "thread_id": thread_id,
            }
        }
        # st.write(payload)

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
                    f"https://api.runpod.ai/v2/nysr8clq7it18g/status/{job_id}",
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
                    st.write("**Bot Answer**")
                    st.write(answer)

                    references = output[1]
                    st.write("**References:**")
                    st.write(references)

                    # history.append({"Question": query, "Answer": answer})
                    # history = history[-8:]
                    # session_state["history"] = history  # Update session state

                    # st.write("**History:**")
                    # st.write(history)

                else:
                    print("No output found in the response.")

        else:
            st.write("Error:", response.status_code)
    else:
        st.write("Please fill in both query and namespace fields.")


