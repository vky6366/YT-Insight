import streamlit as st
from head.store import VectorStore
# Page title
st.set_page_config(page_title="YT Insight", layout="centered")
st.title("📺 YouTube Insight")

# Input section
yt_url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
question = st.text_input("Enter your question", placeholder="Eg: Generate a summary")
vs = VectorStore(yt_url)
# Display output section only if URL is entered
if yt_url:
    st.markdown("---")
    st.subheader("📄 Output:")
    st.info(vs.my_invoke(question))
else:
    st.markdown("📝 Please enter a YouTube video URL to begin.")
