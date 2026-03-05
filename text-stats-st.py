import streamlit as st
from collections import Counter
import re

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="Text Stats",
    page_icon="📊",
    layout="centered",
)

# ── LOAD CSS ──────────────────────────────────────────────
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────
STOP_WORDS = {
    'the','a','an','and','or','but','in','on','at','to','for','of','with',
    'as','is','was','are','were','be','been','being','it','its','this','that',
    'these','those','i','you','he','she','we','they','my','your','his','her',
    'our','their','by','from','up','about','into','than','then','so','if',
    'not','no','nor','do','did','does','have','has','had','will','would',
    'can','could','should','may','might','shall','just','also','more','all',
    'which','who','what','there','when','where','how','out','one','two',
    'three','any','each','every','both','own','over','such',
}

CONJUNCTIONS = [
    'for','and','nor','but','or','yet','so','after','although','as',
    'as if','as long as','as soon as','as though','because','before',
    'even if','even though','if','in case','in order that','lest',
    'now that','once','provided that','rather than','since','so that',
    'than','that','though','unless','until','when','whenever','where',
    'whereas','wherever','whether','while',
]

DEFAULT_WORDS_OF_INTEREST = "Phelan, Schneider, Lepecki, loss, losing, lost, grief"

# ── HEADER ────────────────────────────────────────────────
st.markdown("<h1 style='margin-bottom:0'>📊 Text Stats</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#9e8f7a; margin-top:4px; font-size:1.05rem'>Paste your text below and get instant stats.</p>", unsafe_allow_html=True)

# ── SIDEBAR SETTINGS ──────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    top_x = st.slider("Top N most-common words", min_value=5, max_value=25, value=10)
    st.markdown("---")
    st.markdown("**Words to track**")
    st.markdown("<p class='edit-note'>Comma-separated list</p>", unsafe_allow_html=True)
    woi_input = st.text_area("", value=DEFAULT_WORDS_OF_INTEREST, height=120, label_visibility="collapsed")
    words_of_interest = [w.strip() for w in woi_input.split(',') if w.strip()]
    case_sensitive = st.toggle("Case sensitive", value=False, help="On: 'Loss' and 'loss' count separately. Off: both count together.")

# ── TEXT INPUT ────────────────────────────────────────────
text = st.text_area(
    "Your text",
    placeholder="Paste your essay, thesis chapter, or any text here…",
    height=220,
    label_visibility="collapsed",
)

analyse = st.button("Analyse →", type="primary", use_container_width=True)

# ── ANALYSIS ──────────────────────────────────────────────
if analyse and text.strip():
    clean = re.sub(r'[^A-Za-z\s]', '', text).lower()
    words_list = clean.split()

    # Basic counts
    word_count         = len(text.split())
    char_total         = len(text)
    char_no_spaces     = len(text.replace(' ', '').replace('\n', ''))
    space_count        = text.count(' ')
    para_count         = len([p for p in text.split('\n\n') if p.strip()])
    sentence_count     = len(re.findall(r'[.!?]+', text))
    reading_mins       = word_count / 238
    write_academic_hrs = word_count / 200
    write_general_hrs  = word_count / 500

    def fmt_hours(hrs):
        if hrs < 1/60:
            return "under a minute"
        elif hrs < 1:
            return f"~{hrs * 60:.0f} mins"
        else:
            return f"~{hrs:.1f} hrs"

    # ── TIMINGS ──
    st.markdown("<div class='section-header'>⏱️ Timings </div>", unsafe_allow_html=True)

    if reading_mins < 1:
        reading_str = "Under 1 min read"
    else:
        reading_str = f"~{reading_mins:.1f} min read"

    st.markdown(f"""
    <div style='display:flex;gap:10px;flex-wrap:wrap;margin:0.5rem 0 1.5rem 0'>
        <div class='reading-badge'>📖 {reading_str}</div>
        <div class='reading-badge' style='background:#4a3520'>✍️ Academic &nbsp;{fmt_hours(write_academic_hrs)}</div>
        <div class='reading-badge' style='background:#6b5030'>✍️ General &nbsp;{fmt_hours(write_general_hrs)}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── BASIC COUNTS ──
    st.markdown("<div class='section-header'>📊 Key Stats </div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='stat-grid'>
        <div class='stat-card'><div class='value'>{word_count:,}</div><div class='label'>Words</div></div>
        <div class='stat-card'><div class='value'>{sentence_count:,}</div><div class='label'>Sentences</div></div>
        <div class='stat-card'><div class='value'>{para_count:,}</div><div class='label'>Paragraphs</div></div>
        <div class='stat-card'><div class='value'>{char_total:,}</div><div class='label'>Characters (total)</div></div>
        <div class='stat-card'><div class='value'>{char_no_spaces:,}</div><div class='label'>Chars (no spaces)</div></div>
        <div class='stat-card'><div class='value'>{space_count:,}</div><div class='label'>Spaces</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── TOP WORDS ──
    st.markdown(f"<div class='section-header'>🔤 Top {top_x} Words <span style='font-family:Source Sans 3;font-size:0.85rem;font-weight:300;color:#9e8f7a'>(filler words removed)</span></div>", unsafe_allow_html=True)

    meaningful = [w for w in words_list if w not in STOP_WORDS and len(w) > 2]
    top_words  = Counter(meaningful).most_common(top_x)

    if top_words:
        max_count = top_words[0][1]
        bars_html = ""
        for word, count in top_words:
            pct = int((count / max_count) * 100)
            bars_html += f"""
            <div class='word-row'>
                <div class='word-label'>{word}</div>
                <div class='word-bar-wrap'><div class='word-bar' style='width:{pct}%'></div></div>
                <div class='word-count'>{count}×</div>
            </div>"""
        st.markdown(bars_html, unsafe_allow_html=True)

    # ── WORDS OF INTEREST ──
    st.markdown("<div class='section-header'>🔍 Words of Interest</div>", unsafe_allow_html=True)

    flags = 0 if case_sensitive else re.IGNORECASE
    woi_html = ""
    for w in words_of_interest:
        count = len(re.findall(rf'\b{re.escape(w)}\b', text, flags))
        count_class = "woi-count-found" if count > 0 else "woi-count-zero"
        woi_html += f"""
        <div class='woi-row'>
            <span class='woi-word'>{w}</span>
            <span class='{count_class}'>{count}×</span>
        </div>"""
    st.markdown(woi_html, unsafe_allow_html=True)

    # ── CONJUNCTIONS ──
    st.markdown("<div class='section-header'>🔗 Conjunctions</div>", unsafe_allow_html=True)

    conj_totals = {}
    for conj in CONJUNCTIONS:
        c = len(re.findall(rf'\b{re.escape(conj)}\b', clean))
        if c:
            conj_totals[conj] = c

    total_conj = sum(conj_totals.values())
    st.markdown(f"<p style='color:#5a4a35'><strong>{total_conj:,}</strong> total conjunction uses across <strong>{len(conj_totals)}</strong> distinct conjunctions</p>", unsafe_allow_html=True)

    pills_html = ""
    for conj, cnt in sorted(conj_totals.items(), key=lambda x: -x[1]):
        pills_html += f"<span class='conj-pill'>{conj} <strong>{cnt}</strong></span>"
    st.markdown(pills_html, unsafe_allow_html=True)

elif analyse and not text.strip():
    st.warning("Please paste some text first!")