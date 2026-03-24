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

# --- 2. 模拟数据生成函数（每次只生成1条，避免卡顿）---
def generate_mock_data():
    current_time = datetime.now()
    base_seq = int(time.time()) % 10000
    # 模拟正常递增的序号，带微小抖动
    seq = base_seq + np.random.randint(0, 3)
    return pd.DataFrame({"时间": [current_time], "序号": [seq]})

# --- 3. 初始化历史数据 ---
if "history_df" not in st.session_state:
    st.session_state.history_df = pd.DataFrame(columns=["时间", "序号"])
    # 首次加载时生成5条初始数据，避免空图表
    for _ in range(5):
        st.session_state.history_df = pd.concat(
            [st.session_state.history_df, generate_mock_data()],
            ignore_index=True
        )

# --- 4. 手动刷新时添加新数据 ---
if st.button("🔄 手动刷新获取新数据", type="primary"):
    new_df = generate_mock_data()
    st.session_state.history_df = pd.concat(
        [st.session_state.history_df, new_df],
        ignore_index=True
    )
    # 限制最多保留50条数据，防止图表卡顿
    st.session_state.history_df = st.session_state.history_df.tail(50)

# --- 5. 绘制图表（先判断数据是否为空）---
st.subheader("📈 心跳包序号趋势")
if not st.session_state.history_df.empty:
    st.line_chart(
        st.session_state.history_df.set_index("时间")["序号"],
        use_container_width=True
    )
else:
    st.info("正在生成初始数据，请稍候...")

# --- 6. 显示最新数据表格 ---
st.subheader("📋 最新数据")
st.dataframe(
    st.session_state.history_df.tail(10),
    use_container_width=True,
    hide_index=True
)
