# Text Stats

A simple web app for grabbing summary statistics from a piece of text — built for thesis writers, researchers, or anyone who wants to understand their writing better.

## What it does

Paste any text and instantly get:

- **Basic counts** — words, sentences, paragraphs, characters, spaces, and estimated reading time
- **Top repeated words** — most common meaningful words (filler words like "the", "and" filtered out), shown as a bar chart
- **Words of interest** — track how many times specific words appear (e.g. key authors, themes, terms)
- **Conjunction breakdown** — count of all conjunctions used, as a rough measure of sentence complexity

## Using the app

1. Go to the app URL
2. Paste your text into the box
3. Edit your **words of interest** in the sidebar (comma-separated)
4. Hit **Analyse →**

## Running locally

Make sure you have Python installed, then:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploying to Streamlit Cloud

1. Fork or clone this repo to your own GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select this repo → set main file to `app.py`
4. Hit **Deploy**

## Files

```
├── app.py                  # Main Streamlit app
├── style.css               # Styling
├── requirements.txt        # Python dependencies
└── README.md
```