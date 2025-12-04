import time
import streamlit as st
import json
import os
from datetime import datetime
from streamlit_extras.add_vertical_space import add_vertical_space

# --------------------- #
# 🎨 PAGE CONFIG
# --------------------- #
st.set_page_config(
    page_title="Visvera | AI Interview Evaluation",
    layout="wide",
    page_icon="🎯",
)

# --------------------- #
# 💅 CUSTOM CSS STYLE
# --------------------- #
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* === FONT GLOBAL === */
html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"], [data-testid="stHeader"], [data-testid="stSidebar"], .stMarkdown, .stTextInput, .stTextArea, .stSelectbox, .stExpander, .stDataFrame, .stDownloadButton, .stButton {
    font-family: 'Poppins', sans-serif !important;
    color: #F5F5F5 !important;
}

/* === TITLE GRADIENT === */
h1 {
    font-weight: 700 !important;
    background: linear-gradient(90deg, #06D6A0, #118AB2, #8338EC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 20px;
}

/* === HEADINGS === */
h2, h3, h4 {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* === BUTTON === */
.stButton button, .stDownloadButton button {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    background-color: #118AB2 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    transition: 0.3s ease;
}
.stButton button:hover, .stDownloadButton button:hover {
    background-color: #06D6A0 !important;
    color: #1A1A1A !important;
}

/* === PROGRESS BAR === */
.stProgress > div > div > div {
    background-color: #118AB2 !important;
    border-radius: 10px;
}
.stProgress > div { height: 8px !important; border-radius: 10px; }

/* === EXPANDER HEADER === */
.st-expanderHeader p {
    font-weight: 600 !important;
    color: #FFFFFF !important;
}

/* === CUSTOM EXPANDER CARD === */
.video-expander {
    background-color: #f5f5f5 !important;
    border-radius: 12px !important;
    padding: 15px !important;
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
}
.video-expander h4 {
    color: #333 !important;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --------------------- #
# 🧠 HEADER
# --------------------- #
st.title("Visvera - AI Interview Evaluation System")

st.markdown("""
<div style="
    background-color: rgba(255, 255, 255, 0.04);
    padding: 14px 18px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 14px;
">
    <b>🧠 Simulasi Sistem Visvera</b><br>
    Aplikasi ini menampilkan hasil evaluasi wawancara berbasis AI yang dikembangkan oleh tim.<br>
    Seluruh skor dan analisis dihasilkan langsung oleh model yang dibangun sendiri, namun bersifat simulasi dan digunakan hanya untuk keperluan demonstrasi sistem.
</div>
""", unsafe_allow_html=True)


st.markdown("---")

# --------------------- #
# 🧩 SIDEBAR
# --------------------- #
with st.sidebar:
    st.markdown("<h3 style='text-align:center;'>📁 Menu</h3>", unsafe_allow_html=True)
    add_vertical_space(1)
    st.markdown(
        "<div style='text-align:center; font-size:14px; opacity:0.7;'>Gunakan tab di bawah untuk melihat hasil analisis wawancara kandidat.</div>",
        unsafe_allow_html=True,
    )
    add_vertical_space(2)
    st.markdown("<b>🗂️ Data Sources:</b>", unsafe_allow_html=True)
    st.write("- hasil_final_evaluasi_assesment_verbal.json")
    st.write("- hasil_final_evaluasi_assesment_noVerbal.json")
    st.write("- hasil_final_evaluasi_assesment.json")

# --------------------- #
# 📂 FUNGSI LOAD JSON (AUTO SEARCH)
# --------------------- #
def load_json(filename):
    # Coba cari di folder data/
    data_path_1 = os.path.join("data", filename)

    for path in [data_path_1]:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                st.warning(f"⚠️ Error loading {path}: {e}")
                return None
    
    st.warning(f"⚠️ File {filename} not found in either /data or root folder.")
    return None

# --------------------- #
# 📁 LOAD SEMUA DATA
# --------------------- #
verbal_data = load_json("hasil_final_evaluasi_assesment_verbal.json")
nonverbal_data = load_json("hasil_final_evaluasi_assesment_noVerbal.json")
final_data = load_json("hasil_final_evaluasi_assesment.json")

# --------------------- #
# 📤 UPLOAD SECTION
# --------------------- #
st.markdown("## 📤 Upload Candidate Interview Videos")
st.write("Upload 5 videos (1 for each question). Supported formats: mp4, mov, webm")

uploaded_videos = st.file_uploader(
    "Drag and drop files here",
    type=["mp4", "mov", "webm"],
    accept_multiple_files=True
)

uploads_dir = "uploaded_videos"
os.makedirs(uploads_dir, exist_ok=True)

if uploaded_videos:
    st.success("✅ All videos uploaded successfully!")

    progress_bar = st.progress(0)
    status_text = st.empty()

    st.markdown("### 🎥 Candidate Video Preview")

    # === EXPANDER PREVIEW VIDEO === #
    for i, video in enumerate(uploaded_videos, start=1):
        file_path = os.path.join(uploads_dir, f"question_{i}_{video.name}")
        with open(file_path, "wb") as f:
            f.write(video.getbuffer())

        with st.expander(f"🎯 Question {i}", expanded=False):
            st.markdown(
                f"""
                <div class="video-expander">
                    <h4>Question {i}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.video(file_path, format="video/mp4", start_time=0)

            # Simulasi progress analisis
            video_progress = st.progress(0)
            progress_text = st.empty()
            for p in range(0, 101, 25):
                time.sleep(0.3)
                video_progress.progress(p)
                progress_text.text(f"⏳ Analyzing Question {i}: {p}%")

            video_progress.progress(100)
            progress_text.text("✅ Analysis complete.")
            st.success(f"💬 Verbal analysis for Question {i} complete.")

        progress_bar.progress(i * 20)
        status_text.text(f"🎥 Analyzing Video Question {i}...")

    progress_bar.empty()
    status_text.success("✅ All video analyses completed!")

    # --------------------- #
    # 📊 TABS
    # --------------------- #
    tab1, tab2, tab3 = st.tabs([
        "🗣️ Verbal Assessment",
        "👁️ Nonverbal Assessment",
        "📊 Final Result"
    ])

    # --- TAB 1: VERBAL --- #
    with tab1:
        st.header("🗣️ Verbal Assessment Result")

        if verbal_data:
            for idx, s in enumerate(verbal_data, start=1):
                with st.expander(f"Question {idx} - Score: {s['score']}"):
                    st.write(f"**Formula Score:** {s['verbal_formula_score']}")
                    st.write(f"**Reason:** {s['reason']}")
            
            st.download_button(
                label="💬 Download Verbal Results (JSON)",
                data=json.dumps(verbal_data, indent=4, ensure_ascii=False),
                file_name="hasil_verbal.json",
                mime="application/json"
            )
        else:
            st.warning("⚠️ Verbal data not found. Ensure the JSON file exists in /data folder.")

    # --- TAB 2: NONVERBAL --- #
    with tab2:
        st.header("👁️ Nonverbal Assessment Result")

        if nonverbal_data:
            nv = nonverbal_data["assessment_nonVerbal"]
            st.subheader("📉 Nonverbal Metrics")
            st.json(nv["metrics"])
            
            st.subheader("🎯 Scores")
            st.write(f"**Face Focus:** {nv['scores']['FaceFocus']}")
            st.write(f"**Gaze Movement:** {nv['scores']['GazeMovement']}")
            st.write(f"**Nonverbal Formula Score:** {nv['nonVerbal_formula_score']}")
            st.write(f"**Final Score:** {nv['final_score']}")
            st.info(f"📋 {nv['summary']}")

            st.download_button(
                label="👁️ Download Nonverbal Results (JSON)",
                data=json.dumps(nonverbal_data, indent=4, ensure_ascii=False),
                file_name="hasil_nonverbal.json",
                mime="application/json"
            )
        else:
            st.warning("⚠️ Nonverbal data not found. Ensure the JSON file exists in /data folder.")

    # --- TAB 3: FINAL RESULT --- #
    with tab3:
        st.header("📊 Combined Final Evaluation")

        if final_data:
            overview = final_data["scoresOverview"]
            st.metric("🧠 Decision", final_data["decision"])
            st.metric("📅 Reviewed At", final_data["reviewedAt"])
            
            st.subheader("Scores Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Project", overview["project"])
            col2.metric("Interview", overview["interview"])
            col3.metric("Total", overview["total"])
            
            st.subheader("Interview Scores Detail")
            for idx, s in enumerate(final_data["reviewChecklistResult"]["interviews"]["scores"], start=1):
                with st.expander(f"Question {idx} - Score: {s['score']}"):
                    st.write(s.get("reason", "No reason provided"))

            st.subheader("📝 Overall Notes")
            st.success(final_data["overallNotes"])

            st.download_button(
                label="💾 Download Final Results (JSON)",
                data=json.dumps(final_data, indent=4, ensure_ascii=False),
                file_name="hasil_final.json",
                mime="application/json"
            )
        else:
            st.warning("⚠️ Final data not found. Ensure the JSON file exists in /data folder.")

else:
    st.info("👋 Please upload 5 interview videos to start the evaluation.")

st.markdown("""
<hr style="border: 0.5px solid rgba(255,255,255,0.1); margin-top: 40px;">

<div style="text-align: center; font-size: 12px; color: #888;">
    © 2025 <b>Visvera</b> — Team <b>A25-CS364</b><br>
    Project Capstone Asah led by Dicoding in association with Accenture
</div>
""", unsafe_allow_html=True)


