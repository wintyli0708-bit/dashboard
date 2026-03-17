import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- 1. 页面配置 ----------------
st.set_page_config(page_title="CEO 经营驾驶舱", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    .metric-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); border-left: 6px solid #2ECC71; }
</style>
""", unsafe_allow_html=True)

st.title("🏹 家装公司经营数据分析看板 (2026)")

# ---------------- 2. 数据处理引擎 (核心逻辑) ----------------
@st.cache_data
def load_and_process(files):
    # 初始化一个字典存储各阶段指标
    data_pool = {}
    
    for file in files:
        df = pd.read_excel(file)
        fname = file.name
        
        # A. 逻辑：提取签约 (根据 计入签约业绩日期)
        if "签约" in fname or "销售合同" in fname:
            df['日期'] = pd.to_datetime(df['计入签约业绩日期'])
            data_pool['签约'] = df
            
        # B. 逻辑：提取回款 (根据 回款业绩日期)
        elif "回款" in fname or "账单" in fname:
            df['日期'] = pd.to_datetime(df['回款业绩日期'])
            data_pool['回款'] = df
            
        # C. 逻辑：提取确收 (处理 26年x月实际)
        elif "产值" in fname or "确收" in fname:
            # 找到包含 "26年" 的列，转为纵向数据
            month_cols = [c for c in df.columns if "26年" in str(c) and "实际" in str(c)]
            df_melted = df.melt(id_vars=['地区', '项目推广名'], value_vars=month_cols, var_name='月份描述', value_name='确收金额')
            # 简单转换月份：例如 "26年1月实际" -> 2026-01-01
            df_melted['日期'] = pd.to_datetime(df_melted['月份描述'].str.extract(r'(\d+)月')[0].apply(lambda x: f"2026-{x}-01"))
            data_pool['确收'] = df_melted

    return data_pool

# ---------------- 3. 侧边栏及上传 ----------------
with st.sidebar:
    st.header("📊 数据中心")
    uploaded_files = st.file_uploader("上传 Excel 文件", accept_multiple_files=True, type=['xlsx'])
    
    if uploaded_files:
        st.success(f"已加载 {len(uploaded_files)} 个报表")
        # 实际演示中，如果没上传，我们会用模拟数据；如果上传了，就用真实逻辑
        # 这里为了演示，我们假设您已经上传并处理
        # (此处省略具体过滤代码，逻辑同前一条回复)

st.info("💡 请先在左侧上传 Excel 文件：分项目签约、认购未签约、账单台账、产值确收报表")

# ---------------- 4. 占位：如果没上传显示样例 ----------------
if not uploaded_files:
    st.warning("等待数据上传中... 下方展示结构示例")
    # (这里可以放一些 Mock 数据展示样式)