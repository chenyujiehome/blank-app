import streamlit as st
import json

st.title("🗂️ JSON/JSONL 文件展示器")

uploaded_file = st.file_uploader("上传一个 JSON 或 JSONL 文件", type=["json", "jsonl"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    try:
        if file_type == "json":
            data = json.load(uploaded_file)
            st.subheader("JSON 文件内容：")
            # 判断data类型，支持list和dict
            if isinstance(data, list):
                max_index = len(data) - 1
                index = st.number_input("选择要展示的 index（从0开始）", min_value=0, max_value=max_index, value=0, step=1)
                st.json(data[index])
            elif isinstance(data, dict):
                keys = list(data.keys())
                key = st.selectbox("选择要展示的 key", keys)
                st.json({key: data[key]})
            else:
                st.warning("仅支持以list或dict为顶层结构的JSON文件。")
        elif file_type == "jsonl":
            st.subheader("JSONL 文件内容：")
            lines = uploaded_file.readlines()
            max_index = len(lines) - 1
            index = st.number_input("选择要展示的 index（从0开始）", min_value=0, max_value=max_index, value=0, step=1)
            for i, line in enumerate(lines):
                if i == index:
                    try:
                        obj = json.loads(line)
                        st.markdown(f"**第 {i+1} 行：**")
                        st.json(obj)
                    except Exception as e:
                        st.error(f"第 {i+1} 行解析失败: {e}")
        else:
            st.error("仅支持 .json 或 .jsonl 文件！")
    except Exception as e:
        st.error(f"文件解析失败: {e}")
else:
    st.info("请上传一个 JSON 或 JSONL 文件进行展示。")
