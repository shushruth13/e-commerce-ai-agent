import streamlit as st
import httpx

API_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Data Q&A", page_icon="🤖")
st.title("AI Data Q&A Agent")
st.write("Ask any question about your sales, ads, or eligibility data.")

question = st.text_input("Enter your question:", "What are my sales in the last 7 days?")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = httpx.post(API_URL, json={"question": question}, timeout=120)
                if response.status_code == 200:
                    data = response.json()
                    st.success("**Answer:**\n" + data["answer"])
                    st.markdown(f"**SQL Query:**\n```sql\n{data['sql']}\n```")
                    if data["data"]:
                        st.markdown("**Raw Data:**")
                        st.dataframe(data["data"])
                else:
                    st.error(f"API Error: {response.text}")
            except httpx.TimeoutException:
                st.error("The server took too long to respond. Please try again or use a simpler question.")
            except Exception as e:
                st.error(f"Error: {e}") 