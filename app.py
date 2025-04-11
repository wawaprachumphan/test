st.title("📊 Chat with Your Data")
st.subheader("อัปโหลดไฟล์ของคุณ แล้วเริ่มสำรวจข้อมูลได้ทันที!")

uploaded_file = st.file_uploader("เลือกไฟล์ CSV", type=["csv"])

if uploaded_file is not None:
    st.success("✅ ไฟล์อัปโหลดสำเร็จ!")

    # (โค้ดประมวลผลต่อ เช่น Pandas dataframe, แสดงตาราง, กราฟ, และ QA)
else:
    st.info("กรุณาอัปโหลดไฟล์เพื่อเริ่มต้น")
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
st.title("💬 C (sv) mini")

st.markdown(
    "<div style='font-size: 1.2rem; font-weight: 500;'>One Upload. Your Questions, My Sharp Insights — Powered by Gemini.</div>",
    unsafe_allow_html=True
)

st.markdown("&nbsp;<br>", unsafe_allow_html=True)


# 5. Upload CSV
# 5. Upload CSV
st.markdown('<p style="font-size:16px;">📁 Please upload your CSV file.</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("📊 Preview of the information in the file.")
    st.dataframe(df.head())

    # แปลง DataFrame เป็นข้อความแบบย่อส่งให้โมเดล
    summary_text = f"""
นี่คือตัวอย่างข้อมูลจากไฟล์ CSV ที่ผู้ใช้อัปโหลด:
- จำนวนแถว: {df.shape[0]} แถว
- จำนวนคอลัมน์: {df.shape[1]} คอลัมน์
- ชื่อคอลัมน์: {', '.join(df.columns)}
- ตัวอย่าง 5 แถวแรก:
{df.head().to_string(index=False)}
"""
    st.session_state.df_summary = summary_text

    # สร้าง session แชท
    st.session_state.chat = model.start_chat(
        history=[
            {"role": "user", "parts": [summary_text]},
            {"role": "model", "parts": ["I’ve reviewed the data. Feel free to ask me anything about it 🙂"]}
        ]
    )
    st.success(" ✅ Ready to Talk. Do you need a hand with anything?")

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
