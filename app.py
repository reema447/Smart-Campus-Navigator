import streamlit as st
import pandas as pd
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="Smart Campus Navigator", layout="wide")

# 2. تحميل البيانات (حل مشكلة المسار)
DATA_FILENAME = "data.csv"
try:
    df = pd.read_csv(DATA_FILENAME)
except:
    # إنشاء بيانات وهمية إذا لم يجد الملف لضمان عمل التطبيق
    df = pd.DataFrame(columns=["room", "type", "building", "floor", "entrance"])

# 3. الـ CSS الاحترافي (للتوسيط، البطاقات، ولون الخط الأبيض)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');

.stApp {
    background: linear-gradient(135deg,#0f0c29,#1a1a2e,#16213e);
    color: white;
    font-family: 'Cairo', sans-serif;
}

/* إجبار التوسيط لكل محتوى الصفحة */
[data-testid="stVerticalBlock"] {
    align-items: center !important;
}

/* العناوين المتوهجة */
.main-title {
    text-align: center;
    font-size: 65px;
    font-weight: 900;
    color: #ffffff;
    text-shadow: 0 0 20px #00f5a0;
}

/* جملة الترحيب (يا هلا بالمهندس) */
.special-welcome {
    text-align: center;
    font-size: 40px;
    font-weight: 900;
    background: linear-gradient(to right, #00b09b, #96c93d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 20px 0;
}

/* تنسيق الأزرار كبطاقات عريضة تحت بعضها */
div.stButton > button {
    display: block;
    width: 650px !important; /* عرض البطاقة */
    max-width: 90vw;
    height: 80px !important;
    background: linear-gradient(90deg, #00f5a0, #00d9f5) !important;
    color: #0d0d12 !important;
    font-size: 24px !important;
    font-weight: 900 !important;
    border-radius: 20px !important;
    margin: 15px auto !important;
    border: none !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.3);
}

/* جعل لون الأرقام المدخلة "أبيض" ليناسب الموقع */
input {
    color: white !important; 
    text-align: center !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

div[data-baseweb="input"] {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 2px solid #00f5a0 !important;
    border-radius: 15px !important;
    width: 650px !important;
    max-width: 90vw;
    margin: 20px auto !important;
}

/* إخفاء الزوائد */
header, footer, #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 4. منطق التطبيق
if "page" not in st.session_state:
    st.session_state.page = 1

# --- الصفحة 1: البداية (مع زر متوسط) ---
if st.session_state.page == 1:
    st.markdown('<div class="main-title">Smart Campus Navigator</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; font-size:30px; color:#00f5a0;">يا مرحبَـا</div>', unsafe_allow_html=True)
    if st.button("ابدأ الرحلة"):
        st.session_state.page = 2
        st.rerun()

# --- الصفحة 2: الرقم الجامعي (لون أبيض) ---
elif st.session_state.page == 2:
    st.markdown('<div class="main-title">التحقق من الهوية</div>', unsafe_allow_html=True)
    student_id = st.text_input("", placeholder="أدخل الرقم الجامعي هنا")
    
    if student_id:
        if len(student_id) == 9:
            code = student_id[3:5]
            msg = "يا هلا بالمهندس ⚙️" if code == "81" else "يا هلا بالمهندس التقني 🎓" if code == "80" else "يا هلا بك"
            st.markdown(f'<div class="special-welcome">{msg}</div>', unsafe_allow_html=True)
            if st.button("استمرار"):
                st.session_state.page = 3
                st.rerun()

# --- الصفحة 3: الوجهة (أزرار بطاقات تحت بعض) ---
elif st.session_state.page == 3:
    st.markdown('<div class="main-title">أين وجهتك اليوم؟</div>', unsafe_allow_html=True)
    if st.button("🏫 القاعات الدراسية"):
        st.session_state.type = "قاعات دراسية"; st.session_state.page = 4; st.rerun()
        
    if st.button("👨‍🏫 مكاتب أعضاء هيئة التدريس"):
        st.session_state.type = "مكاتب اعضاء هيئة التدريس"; st.session_state.page = 4; st.rerun()
        
    if st.button("🏢 المكاتب الإدارية"):
        st.session_state.type = "مكاتب ادارية"; st.session_state.page = 4; st.rerun()

# --- الصفحة 4: البحث ---
elif st.session_state.page == 4:
    st.markdown(f'<div class="main-title">البحث في {st.session_state.type}</div>', unsafe_allow_html=True)
    room = st.text_input("", placeholder="اكتب رقم القاعة أو المكتب (مثل: 101)")
    
    if room:
        result = df[(df["room"].astype(str) == room) & (df["type"] == st.session_state.type)]
        if not result.empty:
            st.success(f"📍 الموقع: مبنى {result.iloc[0]['building']} - دور {result.iloc[0]['floor']}")
        else:
            st.error("❌ الرقم غير موجود في هذا القسم")
            
    if st.button("⬅️ عودة"):
        st.session_state.page = 1; st.rerun()
