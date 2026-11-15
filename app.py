import random
from datetime import datetime
import streamlit as st
from questions import QUESTIONS

# ページ基本設定（スマホ対応）
st.set_page_config(
    page_title="人間の理解 第3章 演習＆模擬試験",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# カスタムCSS（押しやすいボタンスタイル、ルビの調整、提出票デザイン）
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px 16px;
        margin-bottom: 8px;
    }
    ruby {
        font-size: 1.15em;
        line-height: 2.0;
    }
    rt {
        font-size: 0.6em;
        color: #555;
    }
    .question-box {
        background-color: #f8fafc;
        border-left: 5px solid #2563eb;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 1.15em;
        line-height: 2.2;
    }
    .report-card {
        background-color: #f1f5f9;
        border: 1px solid #cbd5e1;
        padding: 18px;
        border-radius: 10px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if "mode" not in st.session_state:
    st.session_state.mode = "menu"
if "exam_questions" not in st.session_state:
    st.session_state.exam_questions = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []

# 受講生情報（共通ヘッダー・折りたたみ）
with st.expander("👤 学生情報（提出用）", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        student_class = st.text_input("クラス名", value="25A")
    with col2:
        student_id = st.text_input("学籍番号", placeholder="92594999")
    student_name = st.text_input("氏名", placeholder="ヤグラ タロウ")

ruby_toggle = st.toggle("ふりがな（ルビ）を表示する", value=True)

# -----------------
# 1. メインメニュー画面
# -----------------
if st.session_state.mode == "menu":
    st.title("📚 人間の理解 第3章")
    st.subheader("チームマネジメント 練習問題＆模擬試験")
    st.caption("全118問の中から、学習方法に合わせてモードを選択してください。")

    st.write("---")
    st.markdown("### 🎯 模擬試験モード")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if st.button("⏱️ ミニ模試（ランダム10問）"):
            st.session_state.exam_questions = random.sample(QUESTIONS, 10)
            st.session_state.mode = "quiz"
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.rerun()
    with col_m2:
        if st.button("🔥 本格模試（ランダム25問）"):
            st.session_state.exam_questions = random.sample(QUESTIONS, 25)
            st.session_state.mode = "quiz"
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.rerun()

    st.write("---")
    st.markdown("### 📖 節別 練習問題モード")
    units = [
        (1, "第1節 介護実践マネジメント (全25問)"),
        (2, "第2節1・2項 集団力学とPM理論 (全22問)"),
        (3, "第2節3項 リーダーシップと連携 (全24問)"),
        (4, "第3節 人材育成・自己研鑽 (全25問)"),
        (5, "第4節 組織目標と経営管理 (全22問)"),
    ]
    for u_id, u_label in units:
        if st.button(f"📘 {u_label}"):
            filtered = [q for q in QUESTIONS if q["unit"] == u_id]
            st.session_state.exam_questions = filtered
            st.session_state.mode = "quiz"
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.rerun()

    if st.button("🌐 全118問を一気に演習する"):
        st.session_state.exam_questions = list(QUESTIONS)
        st.session_state.mode = "quiz"
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.user_answers = []
        st.rerun()

# -----------------
# 2. 問題出題画面
# -----------------
elif st.session_state.mode == "quiz":
    q_list = st.session_state.exam_questions
    idx = st.session_state.current_q

    if idx < len(q_list):
        q = q_list[idx]
        st.progress((idx) / len(q_list), text=f"第 {idx + 1} 問 / 全 {len(q_list)} 問（{q['unit_title']}）")

        q_text = q["question_ruby"] if ruby_toggle else q["question_plain"]
        
        st.markdown(f"""
        <div class="question-box">
            <span style="font-size:0.85em; color:#64748b; font-weight:bold;">【問 {idx + 1} / {q['q_number']}】</span><br>
            {q_text}
        </div>
        """, unsafe_allow_html=True)

        # 4つの選択肢
        for opt_idx, opt in enumerate(q["options"], 1):
            if st.button(f"{opt_idx}. {opt}", key=f"q_{idx}_opt_{opt_idx}"):
                is_correct = (opt_idx == q["answer"])
                if is_correct:
                    st.session_state.score += 1
                st.session_state.user_answers.append({
                    "q_num": idx + 1,
                    "code": q["q_number"],
                    "question": q["question_plain"],
                    "selected": opt,
                    "correct": q["options"][q["answer"] - 1],
                    "is_correct": is_correct,
                    "explanation": q["explanation"]
                })
                st.session_state.current_q += 1
                st.rerun()
    else:
        st.session_state.mode = "result"
        st.rerun()

# -----------------
# 3. 成績サマリー・提出画面
# -----------------
elif st.session_state.mode == "result":
    q_list = st.session_state.exam_questions
    total = len(q_list)
    score = st.session_state.score
    rate = round((score / total) * 100, 1)

    st.balloons()
    st.success("🎉 演習が終了しました！お疲れ様でした。")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric(label="あなたの得点", value=f"{score} / {total} 問")
    with col_s2:
        st.metric(label="正答率", value=f"{rate}%", delta="合格水準" if rate >= 70 else "要復習")

    # 提出用テキスト作成
    now_str = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    report_text = f"""【課題提出：人間の理解 第3章 演習結果】
-----------------------------------
■ 受講生情報
・クラス：{student_class}
・学籍番号：{student_id}
・氏名：{student_name}
・実施日時：{now_str}

■ 成績サマリー
・得点：{score} / {total} 問（正答率：{rate}％）
・判定：{"合格水準達成（70％以上）" if rate >= 70 else "復習推奨"}
-----------------------------------
■ 間違えた問題と振り返り
"""
    wrong_count = 0
    for item in st.session_state.user_answers:
        if not item["is_correct"]:
            wrong_count += 1
            report_text += f"\n【問{item['q_num']}】(No.{item['code']})\n"
            report_text += f"・あなたの解答：{item['selected']}\n"
            report_text += f"・正解：{item['correct']}\n"
            report_text += f"・解説：{item['explanation']}\n"
    if wrong_count == 0:
        report_text += "\n全問正解でした！素晴らしい理解度です。\n"

    st.subheader("📋 教員への提出用テキスト")
    st.info("下の枠内のテキストを全選択してコピーし、Google Classroomやメール、Forms等に貼り付けて提出してください。")
    st.text_area("提出用テキスト（コピー用）", value=report_text, height=260)

    # 見直しアコーディオン
    with st.expander("🔍 全問の正誤と解説を確認する"):
        for item in st.session_state.user_answers:
            icon = "✅" if item["is_correct"] else "❌"
            st.markdown(f"**{icon} 問{item['q_num']}: {item['question']}**")
            st.caption(f"選んだ答え: {item['selected']} ｜ 正解: {item['correct']}")
            st.markdown(f"💡 *解説: {item['explanation']}*")
            st.write("---")

    if st.button("🔄 メインメニューに戻る"):
        st.session_state.mode = "menu"
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.user_answers = []
        st.rerun()
