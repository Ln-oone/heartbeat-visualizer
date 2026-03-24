import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import numpy as np

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="心跳包实时监控",
    page_icon="🫀",
    layout="wide"
)
st.title("🫀 心跳包序号监控系统")

# --- 2. 模拟数据生成函数 ---
def generate_mock_data():
    # 每次只生成1条新数据
    current_time = datetime.now()
    base_seq = int(time.time()) % 10000
    # 模拟递增序号
    seq = base_seq + np.random.randint(0, 3)
    return pd.DataFrame({"时间": [current_time], "序号": [seq]})

# --- 3. 初始化历史数据 ---
if "history_df" not in st.session_state:
    st.session_state.history_df = pd.DataFrame(columns=["时间", "序号"])

# --- 4. 添加新数据 ---
new_df = generate_mock_data()
st.session_state.history_df = pd.concat([st.session_state.history_df, new_df], ignore_index=True)

# 限制最多保留50条，避免数据太多卡顿
st.session_state.history_df = st.session_state.history_df.tail(50)

# --- 5. 绘图 ---
st.subheader("📈 心跳包序号趋势")
if not st.session_state.history_df.empty:
    st.line_chart(st.session_state.history_df.set_index("时间")["序号"])
else:
    st.info("正在生成第一条数据...")

# --- 6. 显示最新数据 ---
st.subheader("📋 最新数据")
st.dataframe(st.session_state.history_df.tail(10), use_container_width=True)

# --- 7. 手动刷新按钮 ---
st.divider()
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🔄 手动刷新获取新数据", type="primary"):
        st.rerun()  # 新版streamlit用st.rerun()
