import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. ตั้งค่า Gemini API
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "your-gemini-key"))

# 2. โหลด Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="คุณคือผู้ช่วยวิเคราะห์ข้อมูล CSV ที่เก่งมาก พูดจาชัดเจน กระชับ และมีเหตุผล"
)

# 3. Session state
if "chat" not in st.session_state:
    st.session_state.chat = None
if "df_summary" not in st.session_state:
    st.session_state.df_summary = ""
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# 4. UI
st.set_page_config(page_title="CSV Gemini Chatbot", layout="centered")

# 🧩 Custom Theme: ขาว เทา ดำ เท่ๆ
st.markdown("""
    <style>
        .stApp {
            background-color: #f3f4f6;
            color: #1f2937;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3 {
            color: #111827;
        }

        .stMarkdown, .stTextInput, .stDataFrame {
            color: #1f2937;
        }

        .stButton>button {
            background-color: #374151;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-weight: 500;
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #111827;
            color: #f9fafb;
        }

        section[data-testid="stFileUploader"] > label {
            color: #1f2937;
            font-weight: 500;
        }

        .stDataFrame {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px;
        }

        .stAlert-success {
            background-color: #d1fae5;
            color: #065f46;
            border-left: 5px solid #10b981;
        }

        .stAlert-error {
            background-color: #fee2e2;
            color: #991b1b;
            border-left: 5px solid #ef4444;
        }

        textarea {
            background-color: #ffffff !important;
            color: #111827 !important;
            border-radius: 6px !important;
        }
    </style>
""", unsafe_allow_html=True)

# หัวเรื่อง
st.title("💬 C (sv) mini")
st.markdown(
    "<div style='font-size: 1.2rem; font-weight: 500;'>One Upload. Your Questions, My Sharp Insights — Powered by Gemini.</div>",
    unsafe_allow_html=True
)

st.markdown("&nbsp;<br>", unsafe_allow_html=True)

# 5. Upload CSV
st.markdown('<p style="font-size:16px;">📁 Please upload your CSV file.</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("📊 Preview of the information in the file.")
    st.dataframe(df.head())

    summary_text = f"""
นี่คือตัวอย่างข้อมูลจากไฟล์ CSV ที่ผู้ใช้อัปโหลด:
- จำนวนแถว: {df.shape[0]} แถว
- จำนวนคอลัมน์: {df.shape[1]} คอลัมน์
- ชื่อคอลัมน์: {', '.join(df.columns)}
- ตัวอย่าง 5 แถวแรก:
{df.head().to_string(index=False)}
"""
    st.session_state.df_summary = summary_text

    # เริ่มแชท
    st.session_state.chat = model.start_chat(
        history=[
            {"role": "user", "parts": [summary_text]},
            {"role": "model", "parts": ["I’ve reviewed the data. Feel free to ask me anything about it 🙂"]}
        ]
    )
    st.success("✅ Ready to Talk. Do you need a hand with anything?")

# 6. แสดงประวัติแชท
for msg in st.session_state.chat_log:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. แชท
if st.session_state.chat:
    prompt = st.chat_input("Ask me anything about the CSV file.")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_log.append({"role": "user", "content": prompt})

        try:
            response = st.session_state.chat.send_message(prompt)
            st.chat_message("assistant").markdown(response.text)
            st.session_state.chat_log.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")
