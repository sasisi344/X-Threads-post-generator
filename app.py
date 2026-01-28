import streamlit as st
import os
from logic import scrape_article, generate_posts
from dotenv import load_dotenv

load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="Blog to SNS Post Generator", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1DA1F2;
        color: white;
        font-weight: bold;
    }
    .post-container {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("Settings")
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key:
        st.success("✅ API Key: 設定済み")
    else:
        st.error("❌ API Key: 未設定")
        st.info("`.env` ファイルに `GEMINI_API_KEY` を設定してください。")

# --- Header ---
st.title("📝 Blog to SNS Post Generator")
st.write("Enter a blog URL to automatically generate X and Threads posts.")

# --- Persona Selection ---
persona_options = {
    "🌟 インフルエンサー": "influencer",
    "📊 マーケティング（CMO）": "cmo",
    "✍️ ブロガー": "blogger",
    "👤 一般人": "general",
    "🔧 ギーク": "geek"
}
selected_persona = st.selectbox("投稿スタイルを選択", list(persona_options.keys()))

# --- URL Input ---
url = st.text_input("Blog URL", placeholder="https://example.com/blog-post")

if st.button("投稿を作成する"):
    if not url:
        st.error("Please enter a URL.")
    elif not api_key:
        st.error("Please provide a Gemini API Key in the sidebar.")
    else:
        with st.spinner("Analyzing blog content and generating posts..."):
            # 1. Scrape
            content = scrape_article(url)
            
            if content.startswith("Error"):
                st.error(content)
            else:
                # 2. Generate with selected persona
                persona_key = persona_options[selected_persona]
                posts = generate_posts(content, api_key=api_key, persona=persona_key)
                
                if "error" in posts:
                    st.error(posts["error"])
                else:
                    # --- Results Display ---
                    st.success("Generation Complete!")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🐦 X (Twitter)")
                        st.markdown('<div class="post-container">', unsafe_allow_html=True)
                        st.text_area("X Post", value=posts["x_post"], height=200)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    with col2:
                        st.subheader("🧵 Threads")
                        st.markdown('<div class="post-container">', unsafe_allow_html=True)
                        st.text_area("Threads Post", value=posts["threads_post"], height=300)
                        st.markdown('</div>', unsafe_allow_html=True)
