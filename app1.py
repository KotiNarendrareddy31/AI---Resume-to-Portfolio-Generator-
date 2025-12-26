import streamlit as st
import os
import io
import zipfile
from dotenv import load_dotenv

from google import genai
from PyPDF2 import PdfReader
from docx import Document

# ==================================================
# ENV + CONFIG
# ==================================================
load_dotenv()

st.set_page_config(
    page_title="AI Portfolio Website Generator",
    page_icon="💻",
    layout="wide"
)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

# Gemini client (NEW SDK)
client = genai.Client(api_key=API_KEY)

# Use the standard model ID
MODEL_NAME = "gemini-2.5-flash"

# ==================================================
# RESUME EXTRACTION
# ==================================================
def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs)

def extract_resume(uploaded_file):
    data = uploaded_file.read()
    if uploaded_file.name.lower().endswith(".pdf"):
        return extract_text_from_pdf(data)
    if uploaded_file.name.lower().endswith(".docx"):
        return extract_text_from_docx(data)
    return ""

# ==================================================
# PROMPT
# ==================================================
def build_prompt(resume_text):
    return f"""
You are a senior front-end developer.
Create a PROFESSIONAL portfolio website based on the resume provided.

RULES:
- Clean layout, light theme, good spacing.
- Semantic HTML.
- Include sections for: Hero, About, Experience, Skills, and Contact.

MUST INCLUDE:
<link rel="stylesheet" href="style.css">
<script defer src="script.js"></script>

OUTPUT FORMAT (MANDATORY):
===HTML===
(html code)

===CSS===
(css code)

===JS===
(js code)

RESUME CONTENT:
{resume_text}
"""

# ==================================================
# GEMINI CALL (FIXED FOR NEW SDK)
# ==================================================
def call_gemini(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        # New SDK returns text directly if successful
        if response and response.text:
            return response.text.strip()
            
        return None

    except Exception as e:
        # Check if the error is due to model name prefix
        st.error(f"🔥 Gemini API error: {e}")
        return None

# ==================================================
# PARSER & HELPERS
# ==================================================
def parse_blocks(text):
    def extract(tag):
        if tag not in text:
            return ""
        # Split by tag and then by the next separator
        parts = text.split(tag)
        if len(parts) > 1:
            return parts[1].split("===")[0].strip().replace("```html", "").replace("```css", "").replace("```javascript", "").replace("```js", "").replace("```", "")
        return ""

    return (
        extract("===HTML==="),
        extract("===CSS==="),
        extract("===JS===")
    )

def inject_assets(html):
    if "<link rel" not in html:
        html = html.replace("<head>", "<head>\n<link rel='stylesheet' href='style.css'>")
    if "script.js" not in html:
        html = html.replace("</body>", "<script src='script.js'></script>\n</body>")
    return html

def enhance_css(ai_css):
    base_css = """
@import url('[https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap](https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap)');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Poppins', sans-serif; background: #f8fafc; color: #334155; line-height: 1.6; }
.container { max-width: 1100px; margin: auto; padding: 0 2rem; }
section { padding: 4rem 0; }
.card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }
"""
    return base_css + "\n\n" + (ai_css or "")

def create_zip(html, css, js):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("index.html", html)
        z.writestr("style.css", css)
        z.writestr("script.js", js)
    buffer.seek(0)
    return buffer

# ==================================================
# STREAMLIT UI
# ==================================================
st.title("🚀 AI Portfolio Website Generator")

uploaded = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded:
    resume_text = extract_resume(uploaded)
    if not resume_text.strip():
        st.error("❌ Resume text extraction failed")
        st.stop()

    st.success("✅ Resume loaded successfully")

    if st.button("Generate Portfolio Website"):
        with st.spinner("✨ Gemini is coding your website..."):
            ai_text = call_gemini(build_prompt(resume_text))

            if not ai_text:
                st.error("⚠️ AI did not generate code. Please check your API quota or key.")
                st.stop()

            html, css, js = parse_blocks(ai_text)

            if not html.strip():
                st.error("⚠️ Failed to parse HTML from AI response.")
                st.info("AI Response received:\n" + ai_text[:500] + "...")
                st.stop()

            html = inject_assets(html)
            css = enhance_css(css)
            zip_file = create_zip(html, css, js)

            st.success("🎉 Portfolio generated successfully!")
            st.download_button(
                "⬇️ Download Website ZIP",
                zip_file,
                file_name="portfolio_website.zip",
                mime="application/zip"
            )

            with st.expander("🔍 Preview HTML Code"):
                st.code(html, language="html")
