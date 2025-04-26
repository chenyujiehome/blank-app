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
            st.json(data)
        elif file_type == "jsonl":
            st.subheader("JSONL 文件内容：")
            lines = uploaded_file.readlines()
            for i, line in enumerate(lines):
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
