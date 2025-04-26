import streamlit as st
import json

st.title("🗂️ JSON/JSONL 文件展示器")

# 初始化 session_state 用来持久化已上传文件的数据
if "file_data" not in st.session_state:
    st.session_state["file_data"] = {}

# 允许同时上传多个文件
uploaded_files = st.file_uploader(
    "上传一个或多个 JSON / JSONL 文件 (可多选)",
    type=["json", "jsonl"],
    accept_multiple_files=True,
)

# 解析并存储文件
if uploaded_files:
    for file in uploaded_files:
        if file.name in st.session_state["file_data"]:
            # 已解析过，跳过
            continue
        file_type = file.name.split(".")[-1].lower()
        try:
            if file_type == "json":
                data = json.load(file)
                if isinstance(data, list):
                    rows = data
                else:
                    # dict 或其他结构，视为单行
                    rows = [data]
            elif file_type == "jsonl":
                rows = []
                for line in file.readlines():
                    try:
                        rows.append(json.loads(line))
                    except Exception:
                        # 解析失败的行以原始字符串存储
                        rows.append({"error": "解析失败", "raw": line.decode("utf-8", "ignore")})
            else:
                rows = []
            st.session_state["file_data"][file.name] = rows
        except Exception as e:
            st.error(f"文件 {file.name} 解析失败: {e}")

# 如果已经有文件数据，显示索引选择器并展示结果
if st.session_state["file_data"]:
    # 计算所有文件中最大长度
    max_len = max(len(rows) for rows in st.session_state["file_data"].values()) - 1
    if max_len < 0:
        max_len = 0
    index = st.number_input("选择要展示的 index（从0开始）", min_value=0, max_value=max_len, value=0, step=1)

    st.divider()
    st.subheader(f"展示所有已上传文件的第 {index} 行 / 记录：")

    for filename, rows in st.session_state["file_data"].items():
        st.markdown(f"### 📄 {filename}")
        if index < len(rows):
            st.json(rows[index])
        else:
            st.warning(f"索引 {index} 超出文件长度 (共 {len(rows)} 行)")

    st.divider()
    st.markdown("**已上传文件列表：**" + ", ".join(st.session_state["file_data"].keys()))
