
import gradio as gr
import folium
from folium.plugins import MarkerCluster

# إعداد بيانات الموقع الأساسي (ولاية تيسمسيلت)
lat, lon = 35.6078, 1.9096

# أنواع الطوارئ
emergencies = [
    "لا يوجد", "حريق", "فيضانات", "زلزال", "هجوم", "تسرب غاز",
    "انقطاع الكهرباء", "طريق زلقة", "شجار", "حادث مرور", "كارثة صناعية"
]

# متغيرات تخزين الحادث الحالي والموقع
current_emergency = {"type": "لا يوجد", "location": (lat, lon)}

# إنشاء خريطة تفاعلية
def create_map(click_data=None):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    marker_cluster = MarkerCluster().add_to(m)
    
    if click_data is not None:
        clicked_lat, clicked_lon = click_data["lat"], click_data["lon"]
        current_emergency["location"] = (clicked_lat, clicked_lon)
        folium.Marker([clicked_lat, clicked_lon], tooltip="موقع البلاغ").add_to(marker_cluster)
    
    map_html = "map.html"
    m.save(map_html)
    return map_html

# وظيفة التبليغ عن حالة طارئة
def report_emergency(emergency_type):
    current_emergency["type"] = emergency_type
    if emergency_type != "لا يوجد":
        return f"تم التبليغ عن حالة: {emergency_type} في ولاية تيسمسيلت!"
    return "لا توجد طوارئ حالياً."

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("### خريطة تفاعلية لولاية تيسمسيلت")
    map_output = gr.HTML()
    
    gr.Markdown("## أرقام الطوارئ لولاية تيسمسيلت")
    with gr.Row():
        gr.Markdown("#### الدرك الوطني\nرقم الطوارئ: 1055\n:green[📞 اتصال سريع]")
        gr.Markdown("#### الشرطة الوطنية\nرقم الطوارئ: 1548\n:blue[📞 اتصال سريع]")
    with gr.Row():
        gr.Markdown("#### محافظة الغابات\nرقم الطوارئ: 1070\n:orange[📞 اتصال سريع]")
        gr.Markdown("#### الحماية المدنية\nرقم الطوارئ: 14\n:red[📞 اتصال سريع]")

    gr.Markdown("## نظام الإنذار المبكر")
    dropdown = gr.Dropdown(choices=emergencies, label="هل هناك طارئ؟", value="لا يوجد")
    result = gr.Textbox(label="نتيجة الإبلاغ", interactive=False)
    
    dropdown.change(fn=report_emergency, inputs=dropdown, outputs=result)

    gr.Markdown("### انقر على الخريطة لتحديد موقع الحادث")
    map = gr.Map(label="خريطة تحديد الموقع", update_on_click=True)
    
    map.select(fn=create_map, inputs=map, outputs=map_output)

demo.launch()
