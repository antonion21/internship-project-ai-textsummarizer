# AI Text Summarizer

This project was created as a personal learning exercise while preparing internship applications.  
The goal was to gain practical experience with **AI/NLP**, **Docker containerization**, and simple **cloud deployment**.  
It demonstrates how a small machine learning service can be packaged and shared as a reproducible application — while also serving as a showcase project in my CV.

---

## ✨ Features
- Summarize pasted text **or** a provided URL
- Abstractive summarization using a lightweight Transformer model (DistilBART)
- Extract top-3 keywords with YAKE (language selectable)
- Simple Gradio web interface
- Docker support for reproducible environments
- Deployable on Hugging Face Spaces
- Optional integration with Google Drive (via PyDrive2)

---

## 🛠 Tech Stack
- **Languages:** Python  
- **AI/ML:** Hugging Face Transformers (DistilBART), YAKE  
- **Frontend:** Gradio  
- **Deployment:** Docker, Hugging Face Spaces  
- **Optional Integration:** Google Drive (via PyDrive2)

---

## 📦 Requirements
All dependencies are listed in `requirements.txt`:


```
transformers
torch --index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)
gradio
yake
requests
beautifulsoup4
PyDrive2
````

---

## 🚀 How to Run

### ▶️ Run locally

```bash
# clone repository
git clone https://github.com/antonion21/internship-project-ai-textsummarizer.git
cd internship-project-ai-textsummarizer

# create virtual environment
python -m venv .venv
# activate: 
#   Windows: .venv\Scripts\activate
#   Linux/Mac: source .venv/bin/activate

# install requirements
pip install -r requirements.txt

# start app
python app.py

# open in browser:
# http://127.0.0.1:7860
````

---

### 🐳 Run with Docker

```bash
# build image
docker build -t ai-summarizer .

# run container (exposes port 7860)
docker run -p 7860:7860 ai-summarizer

# open in browser:
# http://localhost:7860
```

---

## ☁️ Deployment (optional)

The app can be deployed on **Hugging Face Spaces** by uploading:

* `app.py`
* `requirements.txt`
* `README.md`

HF Spaces will automatically install dependencies and start the app.
