import streamlit as st
from head.store import vector_store
# Page title
st.set_page_config(page_title="YouTube Transcript App", layout="centered")
st.title("📺 YouTube Transcript Viewer")

# Input section
yt_url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
question = st.text_input("Enter your question", placeholder="Eg: Generate a summary")
vs = vector_store(yt_url)
# Display output section only if URL is entered
if yt_url:
    st.markdown("---")
    st.subheader("📄 Output:")
    st.info(vs.my_invoke(question))
else:
    st.markdown("📝 Please enter a YouTube video URL to begin.")