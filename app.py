import streamlit as st
from efficiency_map import process_efficiency_map
import os

# 创建必要目录
os.makedirs("temp_uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)

# 页面基本设置
st.set_page_config(page_title="效率MAP图生成系统", layout="centered")
st.title("💙 效率MAP图生成系统 V1.0")

# 上传文件区域
uploaded_file = st.file_uploader("📁 上传 Excel 文件（*.xlsx）", type=["xlsx", "xls"])

# 侧边栏设置
st.sidebar.header("图表设置")
chart_title = st.sidebar.text_input("🖋️ 图表标题", value="效率map图")
plot_curve = st.sidebar.radio("📉 是否绘制外特性曲线", ["是", "否"], horizontal=True)
contour_interval = st.sidebar.number_input("🌀 等高线间隔", min_value=1, max_value=20, value=2, step=1)

# 生成按钮
if st.button("🚀 生成效率图"):
    if uploaded_file is None:
        st.warning("⚠️ 请上传一个 Excel 文件！")
    else:
        # 保存上传文件
        save_path = os.path.join("temp_uploads", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ 文件上传成功，正在处理...")

        try:
            # 调用图表处理函数
            output_img_path = process_efficiency_map(
                save_path,
                chart_title,
                plot_curve == "是",
                contour_interval
            )

            # 展示图像
            st.image(output_img_path, caption="效率Map图", use_column_width=True)

            # 下载按钮
            with open(output_img_path, "rb") as img_file:
                st.download_button(
                    label="📥 下载图像",
                    data=img_file,
                    file_name="efficiency_map.png",
                    mime="image/png"
                )
        except Exception as e:
            st.error(f"❌ 出错啦：{e}")
