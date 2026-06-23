import streamlit as st
from ai import ask_ai
import PyPDF2

st.set_page_config(
    page_title="Smart Learn AI",
    page_icon="🤖",
    layout="wide"
)

# Session State
if "started" not in st.session_state:
    st.session_state.started = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "student_type" not in st.session_state:
    st.session_state.student_type = "🎓 College Student"

# =========================
# GLOBAL CSS STYLING
# =========================
st.markdown("""
<style>
/* ----- Google Font ----- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #E0E7FF 100%);
}

/* ----- Hero Container ----- */
.hero {
    background: linear-gradient(135deg, #1E3A8A 0%, #4F46E5 50%, #7C3AED 100%);
    padding: 50px 30px 40px;
    border-radius: 40px;
    text-align: center;
    color: white;
    box-shadow: 0 25px 50px -10px rgba(79, 70, 229, 0.4);
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}

.hero h1 {
    font-size: 52px;
    font-weight: 900;
    letter-spacing: -1px;
    margin: 0 0 8px 0;
}

.hero .subtitle {
    font-size: 22px;
    font-weight: 300;
    color: #E0E7FF;
    margin-bottom: 6px;
}

.hero .desc {
    font-size: 18px;
    color: #C7D2FE;
    max-width: 600px;
    margin: 0 auto 25px;
    line-height: 1.6;
}

/* ----- CTA Button (glowing, animated) ----- */
.cta-wrapper {
    text-align: center;
    margin: -10px 0 30px;
}

.cta-wrapper .stButton button {
    background: linear-gradient(135deg, #FBBF24, #F59E0B) !important;
    color: #1E3A8A !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    padding: 16px 50px !important;
    border-radius: 60px !important;
    border: none !important;
    box-shadow: 0 8px 30px rgba(245, 158, 11, 0.5) !important;
    transition: all 0.3s ease !important;
    animation: pulse-glow 2.5s infinite !important;
    position: relative;
    overflow: hidden;
}

.cta-wrapper .stButton button::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.3) 40%, rgba(255,255,255,0.3) 60%, rgba(255,255,255,0) 100%);
    transform: rotate(30deg) translateX(-100%);
    animation: shimmer 4s infinite;
}

.cta-wrapper .stButton button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 12px 40px rgba(245, 158, 11, 0.7) !important;
}

@keyframes shimmer {
    0% { transform: rotate(30deg) translateX(-100%); }
    100% { transform: rotate(30deg) translateX(100%); }
}

@keyframes pulse-glow {
    0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.5); }
    70% { box-shadow: 0 0 0 20px rgba(245, 158, 11, 0); }
    100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
}

/* ----- Feature Cards (glass) ----- */
.feature-card {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 24px 16px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 8px 32px rgba(79,70,229,0.06);
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
}

.feature-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(79,70,229,0.12);
    background: rgba(255, 255, 255, 0.8);
}

.feature-card h3 {
    font-size: 20px;
    font-weight: 700;
    color: #1E3A8A;
    margin: 0 0 8px;
}

.feature-card p {
    color: #475569;
    font-size: 15px;
    line-height: 1.5;
    margin: 0;
}

/* ----- Steps ----- */
.step {
    background: white;
    padding: 24px 16px;
    border-radius: 20px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.04);
    text-align: center;
    border-bottom: 4px solid #4F46E5;
    transition: transform 0.2s;
}

.step:hover {
    transform: translateY(-4px);
}

.step h4 {
    font-size: 18px;
    font-weight: 700;
    color: #1E3A8A;
    margin: 0 0 6px;
}

.step p {
    color: #475569;
    font-size: 14px;
    margin: 0;
}

/* ----- Metrics ----- */
.metric-box {
    background: white;
    padding: 16px 10px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    font-size: 16px;
    color: #1E3A8A;
}

.metric-box b {
    font-size: 28px;
    display: block;
    font-weight: 800;
    color: #4F46E5;
}

/* ----- Why Choose Cards (gradient background, left accent) ----- */
.why-card {
    background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
    padding: 18px 14px;
    border-radius: 20px;
    border-left: 6px solid #4F46E5;
    box-shadow: 0 4px 16px rgba(79,70,229,0.05);
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
}

.why-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(79,70,229,0.12);
}

.why-card .icon {
    font-size: 32px;
    display: block;
    margin-bottom: 4px;
}

.why-card .text {
    font-size: 15px;
    color: #1E293B;
    font-weight: 500;
}

/* ----- Tech Stack Badges (vibrant, each with distinct colour) ----- */
.tech-badge {
    display: inline-block;
    padding: 10px 22px;
    border-radius: 40px;
    font-size: 16px;
    font-weight: 600;
    color: white;
    margin: 0 6px 10px 6px;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.tech-badge:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.tech-badge .tech-icon {
    margin-right: 8px;
}

/* Individual colours for each tech */
.tech-python { background: linear-gradient(135deg, #2563EB, #4F46E5); }
.tech-streamlit { background: linear-gradient(135deg, #DC2626, #EF4444); }
.tech-groq { background: linear-gradient(135deg, #7C3AED, #A78BFA); }
.tech-pypdf2 { background: linear-gradient(135deg, #059669, #10B981); }

/* ----- Sidebar & Chat (unchanged) ----- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #EEF2FF, #FFFFFF);
}
[data-testid="stSidebar"] * {
    color: #312E81;
    font-weight: 600;
}

.stChatMessage {
    background: #EEF2FF;
    border-radius: 22px;
    padding: 15px;
    border: 1px solid #C7D2FE;
    box-shadow: 0 5px 15px rgba(79,70,229,0.08);
}

div.stButton > button {
    background: #4F46E5;
    color: white;
    border-radius: 30px;
    height: 48px;
    font-weight: 700;
    border: none;
}
div.stButton > button:hover {
    background: #7C3AED;
    box-shadow: 0 0 25px rgba(124,58,237,0.4);
}

.stChatInputContainer {
    background: white;
    border-radius: 30px;
    border: 1px solid #C7D2FE;
}

.footer {
    margin-top: 30px;
    text-align: center;
    color: #94A3B8;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# WELCOME PAGE
# =========================
if not st.session_state.started:
    # ----- HERO -----
    st.markdown("""
    <div class="hero">
        <h1>🎓 Smart Learn AI</h1>
        <div class="subtitle">Your AI‑Powered Learning Companion</div>
        <div class="desc">
            Get instant tutoring, analyse PDFs, generate quizzes, and plan your studies – all in one place.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ----- CTA BUTTON -----
    st.markdown('<div class="cta-wrapper">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Learning", use_container_width=True):
            st.session_state.started = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")  # spacing

    # ----- HOW IT WORKS (3 steps) -----
    st.markdown("### 📌 How It Works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="step">
            <h4>1. Choose a Tool</h4>
            <p>Pick from AI Tutor, PDF Teacher, Quiz Maker, or Study Planner.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="step">
            <h4>2. Ask or Upload</h4>
            <p>Type your question or upload a PDF to get started instantly.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="step">
            <h4>3. Learn & Improve</h4>
            <p>Receive clear explanations, quizzes, and personalised study plans.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ----- FEATURES (glass cards) -----
    st.markdown("### ✨ Core Features")
    cols = st.columns(4)
    features = [
        ("📚 AI Tutor", "Get step‑by‑step explanations and examples on any topic."),
        ("📄 PDF Teacher", "Upload your notes and ask questions based on the content."),
        ("📝 Quiz Maker", "Generate practice quizzes with answers and explanations."),
        ("📅 Study Planner", "Build a daily revision schedule tailored to your needs.")
    ]
    for col, (title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # ----- METRICS -----
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box"><b>5+</b> AI Features</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><b>4</b> Learning Tools</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><b>~3 sec</b> Avg Response</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><b>School+</b> All Levels</div>', unsafe_allow_html=True)

    st.write("")

    # ----- WHY CHOOSE (cards with gradient background + left accent) -----
    st.markdown("### 🌟 Why Choose Smart Learn AI?")
    why_cols = st.columns(3)
    benefits = [
        ("🚀", "Learn difficult concepts faster with AI explanations"),
        ("📄", "Study directly from your PDF notes and materials"),
        ("📝", "Generate custom quizzes and practice tests instantly"),
        ("📅", "Create personalised daily study plans and revision schedules"),
        ("🎯", "Designed for both School & College students"),
        ("⚡", "Lightning‑fast responses powered by Groq AI")
    ]
    for i, (icon, text) in enumerate(benefits):
        col = why_cols[i % 3]
        with col:
            st.markdown(f"""
            <div class="why-card">
                <span class="icon">{icon}</span>
                <span class="text">{text}</span>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # ----- TECHNOLOGY STACK (badges with distinct colours) -----
    st.markdown("### 🛠 Technology Stack")
    st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <span class="tech-badge tech-python"><span class="tech-icon">🐍</span>Python</span>
        <span class="tech-badge tech-streamlit"><span class="tech-icon">🚀</span>Streamlit</span>
        <span class="tech-badge tech-groq"><span class="tech-icon">🧠</span>Groq AI</span>
        <span class="tech-badge tech-pypdf2"><span class="tech-icon">📄</span>PyPDF2</span>
    </div>
    <p style="text-align:center; color:#475569; font-size:15px; margin-top:0;">
        Built as an AI‑Powered Educational Assistant.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Smart Learn AI v1.0 | AI‑Powered Learning Assistant | Built with Python, Streamlit, Groq API & PyPDF2")

    st.stop()   # prevent main app from loading

# =========================
# MAIN APP (after clicking Start)
# =========================
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1E3A8A, #4F46E5, #7C3AED);
    padding: 30px 20px;
    border-radius: 30px;
    color: white;
    text-align: center;
    box-shadow: 0 15px 30px rgba(79,70,229,0.25);
    margin-bottom: 25px;
">
    <h1 style="font-size:36px; font-weight:800; margin:0;">🤖 Smart Learn AI</h1>
    <p style="font-size:18px; color:#E0E7FF; margin:5px 0 0;">AI Tutor • PDF Learning • Quiz Generator • Study Planner</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("""
# 💜 Smart Learn AI
Learn smarter.
""")

mode = st.sidebar.selectbox(
    "Choose Tool",
    [
        "💬 AI Tutor",
        "📄 PDF Teacher",
        "📝 Quiz Maker",
        "🧠 Explain Topic",
        "📅 Study Planner"
    ]
)

uploaded = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
pdf_text = ""

if uploaded:
    reader = PyPDF2.PdfReader(uploaded)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text
    st.sidebar.success("PDF Ready ✅")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask your AI Tutor...")

if question:
    prompt = question

    if mode == "📝 Quiz Maker":
        prompt = f"Create a quiz:\n\n{question}\n\nGive questions, answers and explanations."
    elif mode == "🧠 Explain Topic":
        prompt = f"Explain this topic:\n\n{question}\n\nTeach step by step."
    elif mode == "📅 Study Planner":
        prompt = f"Create a study plan:\n\n{question}\n\nMake a daily timetable."

    if pdf_text:
        prompt = f"PDF Notes:\n\n{pdf_text[:2500]}\n\nQuestion:\n\n{prompt}"

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.spinner("✨ AI is thinking..."):
        answer = ask_ai(prompt)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)

st.sidebar.markdown("---")
st.sidebar.info("💜 Smart Learn AI\n\nPowered by Groq ⚡")