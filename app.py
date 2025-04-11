st.title("📊 Chat with Your Data")
st.subheader("อัปโหลดไฟล์ของคุณ แล้วเริ่มสำรวจข้อมูลได้ทันที!")

uploaded_file = st.file_uploader("เลือกไฟล์ CSV", type=["csv"])

if uploaded_file is not None:
    st.success("✅ ไฟล์อัปโหลดสำเร็จ!")

    # (โค้ดประมวลผลต่อ เช่น Pandas dataframe, แสดงตาราง, กราฟ, และ QA)
else:
    st.info("กรุณาอัปโหลดไฟล์เพื่อเริ่มต้น")
