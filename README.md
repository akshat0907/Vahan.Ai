_**📚 AI Research Paper Summarizer & Podcast Generator**_

This project is a multi-agent AI system that allows users to:

- Search academic papers by topic (arXiv)

- Upload their own research paper (PDF)

- Classify the paper topic

- Generate an easy-to-understand summary

- Synthesize multiple paper summaries

- Create a podcast-style audio from the summary

_**🚀 Features**_

- Topic-Based Search: Enter a research topic and fetch top relevant papers.

- PDF Upload: Analyze your own academic paper by uploading a file.

- Topic Classification: Classifies content against a user-provided list of domains (e.g., NLP, Robotics).

- Summarization: Uses Cohere's Command model to create human-readable summaries.

- Cross-Paper Synthesis: Merges insights from multiple papers into one overview.

- Podcast Generation: Converts text into audio using gTTS.

- Citation Preview: Displays basic metadata (title/source) for traceability.

_**🧠 Technologies Used**_

- Streamlit – Interactive web UI

- Cohere API – LLM for classification and summarization

- arXiv API – Fetch academic papers

- PyMuPDF (fitz) – PDF content extraction

- gTTS – Text-to-speech for podcast

- Python – Core scripting


_**Problem Faced**_

- In a previously similar made project, I chained file using a different approach, but for this one that approach was not working so that was a difficulty for me.

- Generally I use gemini API model for my project, but this time that thing was also not working due to some reason (maximum limit reached for the free API) so I faced some issue due to that also.

- Synthesizing 3+ paper summaries into a single cohesive overview that isn't redundant or generic.

