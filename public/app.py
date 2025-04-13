
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="تطبيق الإنذار المحلي - ولاية تيسمسيلت", layout="wide")

st.title("تطبيق الإنذار المحلي - ولاية تيسمسيلت")
st.markdown("مرحباً بك في تطبيق **DZ Alert** الذي يعرض خريطة الولاية وأرقام الطوارئ ومعلومات الإنذار.")

# ======= عرض الخريطة التفاعلية =======
st.header("خريطة تفاعلية لولاية تيسمسيلت")

map_center = [35.6072, 1.8104]  # إحداثيات وسط تيسمسيلت
m = folium.Map(location=map_center, zoom_start=9)
folium.Marker(map_center, tooltip="تيسمسيلت").add_to(m)
st_data = st_folium(m, width=700, height=500)

# ======= أرقام الطوارئ =======
st.header("أرقام الطوارئ لولاية تيسمسيلت")

col1, col2 = st.columns(2)
with col1:
    st.subheader("الشرطة الوطنية")
    st.write("رقم الطوارئ: **1548**")
    st.button("اتصال سريع", key="police")

    st.subheader("الدرك الوطني")
    st.write("رقم الطوارئ: **1055**")
    st.button("اتصال سريع", key="gendarmerie")

with col2:
    st.subheader("الحماية المدنية")
    st.write("رقم الطوارئ: **14**")
    st.button("اتصال سريع", key="civil")

    st.subheader("محافظة الغابات")
    st.write("رقم الطوارئ: **1070**")
    st.button("اتصال سريع", key="forest")

# ======= خانات الإنذار =======
st.header("نظام الإنذار المبكر")

alert = st.radio("هل هناك طارئ؟", ["لا يوجد", "حريق", "فيضانات", "زلازل", "هجوم"])
if alert != "لا يوجد":
    st.warning(f"تم الإبلاغ عن حالة: {alert} في ولاية تيسمسيلت!")
else:
    st.success("لا توجد حالات طارئة حالياً في الولاية.")

st.markdown("---")
st.caption("جميع الحقوق محفوظة © DZ Alert 2023")
