import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="心跳包实时监控",
    page_icon="🫀",
    layout="wide"
)
st.title("🫀 心跳包序号监控系统")

# --- 2. 模拟数据生成函数 ---
# 如果你有真实数据源（如CSV文件或API），可以替换这个函数
def generate_mock_data(num_points=20):
    # 模拟时间序列（最近的时间在最后）
    times = [datetime.now() - pd.Timedelta(seconds=i*5) for i in range(num_points)][::-1]
    # 模拟序号（假设正常递增，模拟网络抖动时的丢包或乱序）
    base_seq = int(time.time()) % 10000  # 使用当前时间戳做基础，保证每次运行序号不同
    sequences = np.random.randint(0, 5, size=num_points) + base_seq + np.arange(num_points)
    return pd.DataFrame({"时间": times, "序号": sequences})

# --- 3. 创建占位符用于动态更新 ---
# 使用 st.empty() 创建一个容器，后续的图表会在这里更新
chart_placeholder = st.empty()

# --- 4. 读取历史数据 ---
if "history_df" not in st.session_state:
    st.session_state.history_df = pd.DataFrame(columns=["时间", "序号"])

# 生成新数据
new_df = generate_mock_data(num_points=10)

# 更新历史数据
st.session_state.history_df = pd.concat([st.session_state.history_df, new_df]).reset_index(drop=True)

# --- 5. 绘制折线图 ---
st.subheader("📈 心跳包序号趋势")
st.line_chart(st.session_state.history_df.set_index("时间")["序号"])

# 显示数据表格
st.subheader("📋 最新数据")
st.dataframe(st.session_state.history_df.tail())

# --- 6. 刷新逻辑 ---
if st.button("手动刷新"):
    st.experimental_rerun()

# 自动刷新（每5秒刷新一次，注意：Streamlit Cloud 不推荐使用）
# time.sleep(5)
# st.experimental_rerun()
