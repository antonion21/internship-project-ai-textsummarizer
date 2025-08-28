import os
import re
import requests
from bs4 import BeautifulSoup
import gradio as gr
from transformers import pipeline
import yake
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

#small fast modell
MODEL_NAME = os.getenv("MODEL_NAME", "sshleifer/distilbart-cnn-12-6")

#load pipelines
summarizer = pipeline("summarization", model=MODEL_NAME)
kw_extractor = yake.KeywordExtractor(lan=os.getenv("KW_LANG", "en"), n=1, top=3)

def fetch_url_text(url: str, timeout: int = 10) -> str:
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        #remove obvious noise like nav, script, style ...
        for bad in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            bad.decompose()

        text = soup.get_text(separator=" ")
        text = re.sub(r"\s+", " ", text).strip()
        #ignore short texts (they usually dont make sense)
        return text if len(text) > 400 else ""
    except Exception:
        return ""

def chunk_text(text: str, max_chars: int = 2000):
    """Fetch HTML, strip obvious noise, and return plain text (simple heuristic)."""
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

def summarize(text: str, url: str, target_words: int, kw_lang: str):
    source = text.strip()
    if url.strip():
        fetched = fetch_url_text(url.strip())
        if fetched:
            source = fetched

    if not source:
        return "Hey! Please enter some text or a valid URL so I can summarize it for you.", ""

    #choose yake lang, exception -> en
    try:
        _ = yake.KeywordExtractor(lan=kw_lang, n=1, top=3)
        kw_extractor.lan = kw_lang
    except Exception:
        kw_extractor.lan = "en"

    #distilbart expects max_length/min_length in tokens ->here we approximate with words
    min_len = max(20, target_words // 3)
    max_len = max(40, target_words)

    outputs = []
    for c in chunk_text(source, max_chars=2000):
        out = summarizer(
            c, max_length=max_len, min_length=min_len, do_sample=False
        )[0]["summary_text"]
        outputs.append(out)

    final = " ".join(outputs)
    kws = [k[0] for k in kw_extractor.extract_keywords(final)]
    #google drive upload
    link = upload_to_gdrive(final, ", ".join(kws))
    return final, ", ".join(kws) + f"\nGoogle Drive Link: {link}"

def upload_to_gdrive(summary, keywords, filename="summary.txt"):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  #open browser for authentication
    drive = GoogleDrive(gauth)
    content = f"Summary:\n{summary}\n\nKeywords:\n{keywords}"
    file = drive.CreateFile({'title': filename})
    file.SetContentString(content)
    file.Upload()
    return file['alternateLink']  #return link (for sharing)

with gr.Blocks() as demo:
    gr.Markdown("# AI Text Summarizer\nSummarize text or URLs using a Transformer model. Also returns top keywords (YAKE).")

    with gr.Row():
        txt = gr.Textbox(label="Your Text", lines=10, placeholder="Paste an article, blog post, or your own notes here...")
        url = gr.Textbox(label="URL (optional)", placeholder="e.g. https://example.com/article")

    with gr.Row():
        target = gr.Slider(60, 220, value=120, step=10, label="Target summary length (approx. words)")
        kw_lang = gr.Dropdown(choices=["en", "de", "fr", "es", "it", "nl", "hu"], value="en", label="Keyword language")

    btn = gr.Button("Summarize")

    out_sum = gr.Textbox(label="Summary", lines=10)
    out_kw = gr.Textbox(label="Top Keywords", lines=1)

    btn.click(fn=summarize, inputs=[txt, url, target, kw_lang], outputs=[out_sum, out_kw])

    gr.Markdown("Made by Antonio as part of a personal project for internship applications.")

if __name__ == "__main__":
    demo.queue()
    #hf spaces requires host=0.0.0.0 and port=7860 (only needed when not running via docker)
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))
