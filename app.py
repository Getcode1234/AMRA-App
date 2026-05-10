import streamlit as st
import pandas as pd
import time
try:
    import backend # This imports Sobia's backend.py file
except ImportError:
    st.error("Error: 'backend.py' file not found. Please make sure Sobia's file is in the same folder and named 'backend.py'.")

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="AMRA - Affordable Medicine Finder", 
    layout="wide", 
    page_icon="💊"
)

# 2. LANGUAGE DICTIONARY
languages = {
    "English": {
        "title": "💊 AMRA: Affordable Medicine Recommendation Agent",
        "subtitle": "Find cost-effective, DRAP-approved alternatives for your prescribed brand.",
        "search_label": "Enter Brand Name:",
        "placeholder": "e.g. Panadol, Augmentin...",
        "button": "Find Affordable Alternatives",
        "searching": "Searching for",
        "results_for": "Results for",
        "table_head": "Comparison Table (Sorted by Price)",
        "disclaimer": "**Note:** Please consult with a medical professional before switching medications.",
        "error": "Please enter a medicine name first."
    },
    "Urdu (اردو)": {
        "title": "💊 ایمرا: سستی ادویات کا ساتھی",
        "subtitle": "اپنی برانڈڈ دوا کا سستا متبادل تلاش کریں۔",
        "search_label": "دوا کا نام درج کریں:",
        "placeholder": "مثال کے طور پر: پیناڈول",
        "button": "سستا متبادل تلاش کریں",
        "searching": "تلاش جاری ہے...",
        "results_for": "نتائج برائے",
        "table_head": "قیمت کے لحاظ سے متبادل ادویات",
        "disclaimer": "**نوٹ:** دوا تبدیل کرنے سے پہلے ڈاکٹر سے مشورہ ضرور کریں۔",
        "error": "براہ کرم پہلے دوا کا نام درج کریں۔"
    },
    "Arabic (العربية)": {
        "title": "💊 AMRA: وكيل توصية الأدوية الميسورة",
        "subtitle": "ابحث عن بدائل فعالة من حيث التكلفة لمعالجة دوائك.",
        "search_label": "أدخل اسم الدواء:",
        "placeholder": "مثال: بنادول",
        "button": "البحث عن بدائل أرخص",
        "searching": "جاري البحث عن",
        "results_for": "نتائج لـ",
        "table_head": "جدول المقارنة (مرتب حسب السعر)",
        "disclaimer": "**ملاحظة:** يرجى استشارة الطبيب قبل تبديل الأدوية.",
        "error": "يرجى إدخال اسم الدواء أولاً."
    }
}

# 3. CUSTOM CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        background-color: #007bff; 
        color: white; 
        border-radius: 8px; 
        font-weight: bold;
        width: 100%;
    }
    .stSidebar .stButton>button {
        background-color: #343a40; 
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR - CONTROL PANEL
st.sidebar.title("⚙️ AMRA Control Panel")
selected_lang = st.sidebar.selectbox("Select Language", list(languages.keys()))
lang = languages[selected_lang]

st.sidebar.divider()
st.sidebar.subheader("App Info")
st.sidebar.info("Tier 1: Presentation Layer\nFramework: Streamlit\nStatus: Final Integration")

st.sidebar.subheader("System Actions")
if st.sidebar.button("🗑️ Clear System Cache"):
    st.sidebar.success("Cache Cleared!")
if st.sidebar.button("🔄 Rerun Engine"):
    st.rerun()

st.sidebar.divider()
st.sidebar.info(f"**Dev:** Arfa (UI/UX)\n**Team:** Adeen, Sobia, Zahra")

# 5. MAIN INTERFACE
st.title(lang["title"])
st.write(lang["subtitle"])
st.divider()

# 6. CONNECTION TO SOBIA'S BACKEND
def get_medicine_alternatives(medicine_query):
    try:
        # Using Sobia's specific function name: get_cheap_medicines
        df = backend.get_cheap_medicines(medicine_query) 
        return df
    except Exception as e:
        st.error(f"Backend Connection Error: {e}")
        return pd.DataFrame()

# 7. SEARCH INTERFACE
st.subheader(lang["search_label"])
user_input = st.text_input("", placeholder=lang["placeholder"])

if st.button(lang["button"]):
    if user_input:
        with st.spinner(f"{lang['searching']} '{user_input}'..."):
            results_df = get_medicine_alternatives(user_input)
            
            if not results_df.empty:
                st.success(f"{lang['results_for']} '{user_input}':")
                st.subheader(lang["table_head"])
                st.dataframe(results_df, use_container_width=True)
                st.warning(lang["disclaimer"])
            else:
                st.error("No results found or Backend is not responding.")
    else:
        st.error(lang["error"])