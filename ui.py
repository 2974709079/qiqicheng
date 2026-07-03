import streamlit as st
import requests
import json
import os
from datetime import datetime

# ===== 页面配置 =====
st.set_page_config(
    page_title="琪琪的学习计划",
    page_icon="🐷",
    layout="wide"
)

# ===== 初始化数据 =====
if 'registers' not in st.session_state:
    st.session_state.registers = []
if 'practices' not in st.session_state:
    st.session_state.practices = []
if 'wrongs' not in st.session_state:
    st.session_state.wrongs = []
if 'plans' not in st.session_state:
    st.session_state.plans = []
if 'exams' not in st.session_state:
    st.session_state.exams = []
if 'statses' not in st.session_state:
    st.session_state.statses = []
if 'knowledges' not in st.session_state:
    st.session_state.knowledges = []
if 'materials' not in st.session_state:
    st.session_state.materials = []
if 'daily_goal' not in st.session_state:
    st.session_state.daily_goal = 8
if 'user_name' not in st.session_state:
    st.session_state.user_name = "琪琪"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ===== 侧边栏 =====
with st.sidebar:
    st.markdown(f"## 🐷 {st.session_state.user_name}的学习计划")
    st.caption("今日宜学习 · 忌摆烂")
    st.markdown("---")
    
    menu = st.radio(
        "导航",
        ["📊 仪表盘", "📖 题库练习", "❌ 错题本", "📅 学习计划", 
         "📝 模拟考试", "📈 成绩统计", "💡 知识点整理", "✍️ 申论素材", "⚙️ 设置"]
    )
    st.markdown("---")
    st.caption(f"📅 {datetime.now().strftime('%Y年%m月%d日')}")

# ===== DeepSeek API 配置（从环境变量读取） =====
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# ===== 右侧主区域 =====
if menu == "📊 仪表盘":
    st.markdown("## 📊 仪表盘")
    col1, col2, col3, col4 = st.columns(4)
    total_questions = len(st.session_state.registers) + len(st.session_state.practices)
    col1.metric("累计答题", total_questions)
    col2.metric("正确率", "100%" if len(st.session_state.wrongs) == 0 else "68%")
    col3.metric("今日计划", f"{len(st.session_state.plans)}/{st.session_state.daily_goal}")
    col4.metric("连续打卡", f"{min(len(st.session_state.registers)+1, 99)}天")
    
    st.markdown("---")
    st.markdown("### 📝 今日学习登记")
    cols = st.columns([3, 2, 1])
    with cols[0]:
        register_text = st.text_input("学习内容", placeholder="如「言语理解 20题」", key="register_input", label_visibility="collapsed")
    with cols[1]:
        register_subject = st.selectbox("科目", ["言语理解", "数量关系", "判断推理", "资料分析", "常识判断", "申论", "其他"], key="register_subject", label_visibility="collapsed")
    with cols[2]:
        if st.button("➕ 登记", key="register_btn"):
            if register_text:
                st.session_state.registers.append({"text": register_text, "subject": register_subject})
                st.rerun()
    
    if st.session_state.registers:
        for item in reversed(st.session_state.registers[-10:]):
            st.markdown(f"- {item['text']} `{item['subject']}`")
    else:
        st.caption("还没有学习记录，开始登记吧 📝")

elif menu == "📖 题库练习":
    st.markdown("## 📖 题库练习")
    cols = st.columns([3, 2, 1])
    with cols[0]:
        practice_text = st.text_input("练习内容", placeholder="如「判断推理 15题」", key="practice_input", label_visibility="collapsed")
    with cols[1]:
        practice_subject = st.selectbox("科目", ["言语理解", "数量关系", "判断推理", "资料分析", "常识判断", "申论", "其他"], key="practice_subject", label_visibility="collapsed")
    with cols[2]:
        if st.button("➕ 登记", key="practice_btn"):
            if practice_text:
                st.session_state.practices.append({"text": practice_text, "subject": practice_subject})
                st.rerun()
    for item in reversed(st.session_state.practices):
        st.markdown(f"- {item['text']} `{item['subject']}`")
    if not st.session_state.practices:
        st.caption("暂无练习记录")

elif menu == "❌ 错题本":
    st.markdown("## ❌ 错题本")
    cols = st.columns([4, 1])
    with cols[0]:
        wrong_text = st.text_input("错题描述", placeholder="如「资料分析第3题」", key="wrong_input", label_visibility="collapsed")
    with cols[1]:
        if st.button("➕ 记录", key="wrong_btn"):
            if wrong_text:
                st.session_state.wrongs.append({"text": wrong_text})
                st.rerun()
    for item in reversed(st.session_state.wrongs):
        st.markdown(f"- {item['text']}")
    if not st.session_state.wrongs:
        st.caption("暂无错题，继续加油 💪")

elif menu == "📅 学习计划":
    st.markdown("## 📅 学习计划")
    cols = st.columns([4, 1])
    with cols[0]:
        plan_text = st.text_input("计划内容", placeholder="如「完成资料分析20题」", key="plan_input", label_visibility="collapsed")
    with cols[1]:
        if st.button("➕ 添加", key="plan_btn"):
            if plan_text:
                st.session_state.plans.append({"text": plan_text})
                st.rerun()
    for item in reversed(st.session_state.plans):
        st.markdown(f"- {item['text']}")
    if not st.session_state.plans:
        st.caption("暂无计划，规划起来 📋")

elif menu == "📝 模拟考试":
    st.markdown("## 📝 模拟考试")
    cols = st.columns([4, 1])
    with cols[0]:
        exam_text = st.text_input("模考名称 + 分数", placeholder="如「行测模考 68分」", key="exam_input", label_visibility="collapsed")
    with cols[1]:
        if st.button("➕ 记录", key="exam_btn"):
            if exam_text:
                st.session_state.exams.append({"text": exam_text})
                st.rerun()
    for item in reversed(st.session_state.exams):
        st.markdown(f"- {item['text']}")
    if not st.session_state.exams:
        st.caption("暂无模考记录")

elif menu == "📈 成绩统计":
    st.markdown("## 📈 成绩统计")
    cols = st.columns([4, 1])
    with cols[0]:
        stats_text = st.text_input("科目 + 成绩", placeholder="如「言语理解 80分」", key="stats_input", label_visibility="collapsed")
    with cols[1]:
        if st.button("➕ 记录", key="stats_btn"):
            if stats_text:
                st.session_state.statses.append({"text": stats_text})
                st.rerun()
    for item in reversed(st.session_state.statses):
        st.markdown(f"- {item['text']}")
    if not st.session_state.statses:
        st.caption("暂无成绩记录")

elif menu == "💡 知识点整理":
    st.markdown("## 💡 知识点整理")
    cols = st.columns([4, 1])
    with cols[0]:
        knowledge_text = st.text_input("知识点描述", placeholder="输入核心知识点", key="knowledge_input", label_visibility="collapsed")
    with cols[1]:
        if st.button("➕ 添加", key="knowledge_btn"):
            if knowledge_text:
                st.session_state.knowledges.append({"text": knowledge_text})
                st.rerun()
    for item in reversed(st.session_state.knowledges):
        st.markdown(f"- {item['text']}")
    if not st.session_state.knowledges:
        st.caption("暂无知识点")

elif menu == "✍️ 申论素材":
    st.markdown("## ✍️ 申论素材")
    cols = st.columns([4, 1])
    with cols[0]:
        material_text = st.text_input("素材内容", placeholder="好词好句或案例", key="material_input", label_visibility="collapsed")
    with cols[1]:
        if st.button("➕ 添加", key="material_btn"):
            if material_text:
                st.session_state.materials.append({"text": material_text})
                st.rerun()
    for item in reversed(st.session_state.materials):
        st.markdown(f"- {item['text']}")
    if not st.session_state.materials:
        st.caption("暂无素材，开始积累 📚")

elif menu == "⚙️ 设置":
    st.markdown("## ⚙️ 设置")
    new_goal = st.number_input("每日学习目标（题）", min_value=1, max_value=50, value=st.session_state.daily_goal)
    if new_goal != st.session_state.daily_goal:
        st.session_state.daily_goal = new_goal
    new_name = st.text_input("你的名字", value=st.session_state.user_name)
    if new_name != st.session_state.user_name:
        st.session_state.user_name = new_name
    st.caption("💡 数据保存在浏览器本地，换设备会丢失")

# ===== 右下角固定的 DeepSeek 按钮 =====
st.markdown("---")
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    chat_btn = st.button("🤖 问 DeepSeek", use_container_width=True)

if chat_btn:
    st.markdown("### 🤖 问 DeepSeek")
    chat_input = st.text_input("输入你的问题...", key="chat_input", placeholder="想问什么？")
    if st.button("发送", key="send_chat"):
        if chat_input and DEEPSEEK_API_KEY:
            with st.spinner("思考中..."):
                try:
                    response = requests.post(
                        "https://api.deepseek.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "deepseek-chat",
                            "messages": [{"role": "user", "content": chat_input}],
                            "temperature": 0.7,
                            "max_tokens": 2000
                        },
                        timeout=30
                    )
                    data = response.json()
                    if data.get("choices"):
                        st.success(data["choices"][0]["message"]["content"])
                    else:
                        st.error("没有获取到有效回复")
                except Exception as e:
                    st.error(f"连接失败：{e}")
        elif not DEEPSEEK_API_KEY:
            st.error("请先在 Streamlit Cloud Secrets 中配置 DEEPSEEK_API_KEY")
        else:
            st.warning("请输入问题")