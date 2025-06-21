# task.py
import streamlit as st
import requests
import xml.etree.ElementTree as ET
import fitz  # PyMuPDF
import cohere
from gtts import gTTS
import uuid
import os

st.set_page_config(page_title="AI Research Summarizer", layout="wide")
st.title("📚 AI Research Paper Summarizer & Podcast Generator")

COHERE_API_KEY = "API Key"
co = cohere.Client(COHERE_API_KEY)

#Utility Functions 
def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def fetch_pdfs_from_arxiv(topic, count=3, sort_by="relevance"):
    url = f"http://export.arxiv.org/api/query?search_query=all:{topic}&sortBy={sort_by}&max_results={count}"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    pdf_links = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        for link in entry.findall("{http://www.w3.org/2005/Atom}link"):
            if link.attrib.get('type') == 'application/pdf':
                pdf_links.append(link.attrib['href'])
    return pdf_links

def fetch_text_from_pdf_url(url):
    response = requests.get(url)
    with open("temp_paper.pdf", "wb") as f:
        f.write(response.content)
    with fitz.open("temp_paper.pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def classify_topic(text, topic_list):
    prompt = f"Classify the following academic paper content into one of the topics: {', '.join(topic_list)}\n\n{text[:2000]}"
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=50,
        temperature=0.3
    )
    return response.generations[0].text.strip()

def generate_summary(text):
    prompt = f"Summarize this research paper in simple terms for a podcast audience:\n\n{text[:8000]}"
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=500,
        temperature=0.5
    )
    return response.generations[0].text.strip()

def generate_cross_paper_synthesis(summaries):
    combined = "\n\n".join([f"Paper {i+1}: {s}" for i, s in enumerate(summaries)])
    prompt = f"Synthesize the following summaries into one cohesive overview that compares and contrasts their contributions and findings:\n\n{combined}"
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=600,
        temperature=0.5
    )
    return response.generations[0].text.strip()

def text_to_speech(text):
    tts = gTTS(text)
    file_path = f"temp_audio_{uuid.uuid4().hex}.mp3"
    tts.save(file_path)
    return file_path

def extract_metadata(text):
    title_line = text.split("\n")[0]
    return f"Title: {title_line}\nSource: arXiv or uploaded"

#UI and Logic
st.sidebar.header("Input Options")
input_mode = st.sidebar.radio("Choose input method:", ["Search by Topic", "Upload PDF"])
topic_list_input = st.sidebar.text_area("Enter topic list (comma-separated)", "NLP, Computer Vision, Reinforcement Learning, Robotics")
topic_list = [t.strip() for t in topic_list_input.split(",") if t.strip()]
paper_text = ""
paper_title = ""

if input_mode == "Search by Topic":
    topic = st.text_input("🔍 Enter a research topic")
    if topic:
        with st.spinner("Fetching top 3 papers from arXiv..."):
            pdf_urls = fetch_pdfs_from_arxiv(topic, count=3)

        if pdf_urls:
            summaries = []
            for i, pdf_url in enumerate(pdf_urls):
                st.markdown(f"#### 📄 Paper {i+1}: [Link]({pdf_url})")
                with st.spinner(f"Processing Paper {i+1}..."):
                    paper_text = fetch_text_from_pdf_url(pdf_url)
                    summary = generate_summary(paper_text)
                    summaries.append(summary)

            with st.spinner("Synthesizing summaries across papers..."):
                synthesis = generate_cross_paper_synthesis(summaries)
                audio_path = text_to_speech(synthesis)

            st.success("✅ Cross-paper synthesis completed!")
            st.markdown("### 🔗 Cross-paper Synthesis Summary:")
            st.write(synthesis)

            st.markdown("### 🔊 Podcast:")
            audio_file = open(audio_path, "rb")
            st.audio(audio_file.read(), format="audio/mp3")

            st.download_button("⬇ Download Synthesis", synthesis, file_name="cross_paper_summary.txt")
            st.download_button("⬇ Download Audio", audio_file, file_name="cross_paper_summary.mp3")

        else:
            st.error("No papers found. Try another topic.")

elif input_mode == "Upload PDF":
    uploaded_file = st.file_uploader("📄 Upload your research paper (PDF)", type="pdf")
    if uploaded_file:
        with st.spinner("Extracting content from uploaded PDF..."):
            paper_text = extract_text_from_pdf(uploaded_file)
            paper_title = extract_metadata(paper_text)

        st.subheader("📄 Extracted Paper Preview")
        st.text_area("Content", paper_text[:3000] + ("..." if len(paper_text) > 3000 else ""), height=300)

        if st.button("✨ Analyze & Summarize"):
            with st.spinner("Classifying topic..."):
                classified_topic = classify_topic(paper_text, topic_list)

            with st.spinner("Generating summary..."):
                summary = generate_summary(paper_text)

            with st.spinner("Creating podcast audio..."):
                audio_path = text_to_speech(summary)

            st.success("✅ Summary & Podcast Ready")

            st.markdown(f"### 🏷 Classified Topic: `{classified_topic}`")
            st.markdown("### 📌 Citation Info:")
            st.text(paper_title)
            st.markdown("### ✍️ Summary:")
            st.write(summary)

            st.markdown("### 🔊 Podcast:")
            audio_file = open(audio_path, "rb")
            st.audio(audio_file.read(), format="audio/mp3")

            st.download_button("⬇ Download Summary", summary, file_name="summary.txt")
            st.download_button("⬇ Download Audio", audio_file, file_name="summary.mp3")
