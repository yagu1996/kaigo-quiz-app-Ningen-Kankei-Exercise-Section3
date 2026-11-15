import random
from datetime import datetime
import streamlit as st

# ページ基本設定（スマホ対応）
st.set_page_config(
    page_title="人間の理解 第3章 演習＆模擬試験",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# カスタムCSS（スマホ向け押しやすいボタン・ルビスタイル）
st.markdown(
    """
<style>
    .stButton>button { width: 100%; border-radius: 8px; font-size: 16px; margin-bottom: 8px; }
    ruby { font-size: 1.15em; }
    rt { font-size: 0.6em; color: #555; }
    .report-box { background-color: #f8f9fa; border: 1px solid #ddd; padding: 15px; border-radius: 8px; }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------
# 問題データ（抜粋・例）
# -----------------
QUESTIONS = [
    {
        "id": 1,
        "section": "第1節",
        "question_ruby": "<ruby>介護<rt>かいご</rt></ruby>サービスには<ruby>物質的<rt>ぶっしつてき</rt></ruby>な「かたち」が<ruby>存在<rt>そんざい</rt></ruby>しないという<ruby>特性<rt>とくせい</rt></ruby>を<ruby>何<rt>なん</rt></ruby>というか。",
        "question_plain": "介護サービスには物質的な「かたち」が存在しないという特性を何というか。",
        "options": ["無形性", "不可分性", "品質の変動性", "消滅性"],
        "answer": 1,
        "explanation": "介護サービスは形のない「無形性」をもちます。",
    },
    {
        "id": 2,
        "section": "第1節",
        "question_ruby": "<ruby>介護<rt>かいご</rt></ruby>サービスの<ruby>提供<rt>ていきょう</rt></ruby>（<ruby>生産<rt>せいさん</rt></ruby>）と<ruby>利用<rt>りよう</rt></ruby>（<ruby>消費<rt>しょうひ</rt></ruby>）が<ruby>同時<rt>どうじ</rt></ruby>に<ruby>行<rt>おこな</rt></ruby>われ、<ruby>切<rt>き</rt></ruby>り<ruby>離<rt>はな</rt></ruby>すことができない<ruby>特性<rt>とくせい</rt></ruby>を<ruby>何<rt>なん</rt></ruby>というか。",
        "question_plain": "介護サービスの提供（生産）と利用（消費）が同時に行われ、切り離すことができない特性を何というか。",
        "options": [
            "均質性",
            "不可分性（同時性）",
            "永続性",
            "独立性",
        ],
        "answer": 2,
        "explanation": "生産と消費が同時に起こることを「不可分性（同時性）」といいます。",
    },
    # ※ここに作成済みの全問題を登録（全118問）
]

# セッション状態の初期化
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []
if "mode" not in st.session_state:
    st.session_state.mode = "menu"
if "exam_questions" not in st.session_state:
    st.session_state.exam_questions = []

# -----------------
# 画面表示ロジック
# -----------------
st.title("📚 人間の理解 第3章")
st.caption("チームマネジメント 練習問題＆模擬試験アプリ")

# 受講生情報入力（提出用）
with st.expander("👤 受講生情報（提出用）", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        student_class = st.text_input("クラス", value="介護福祉科1年")
    with col2:
        student_id = st.text_input("学籍番号", placeholder="A123456")
    student_name = st.text_input("氏名", placeholder="介護 太郎")
    ruby_toggle = st.toggle("ふりがな（ルビ）を表示する", value=True)

# 1. メインメニュー画面
if st.session_state.mode == "menu":
    st.subheader("モードを選択してください")
    if st.button("📖 節別 練習問題（全問演習）"):
        st.session_state.exam_questions = QUESTIONS
        st.session_state.mode = "quiz"
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.user_answers = []
        st.rerun()

    if st.button("⏱️ 模擬試験モード（ランダム10問）"):
        st.session_state.exam_questions = random.sample(
            QUESTIONS, min(10, len(QUESTIONS))
        )
        st.session_state.mode = "quiz"
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.user_answers = []
        st.rerun()

# 2. 問題解答画面
elif st.session_state.mode == "quiz":
    q_list = st.session_state.exam_questions
    idx = st.session_state.current_q

    if idx < len(q_list):
        q = q_list[idx]
        st.progress((idx) / len(q_list), text=f"第 {idx + 1} 問 / 全 {len(q_list)} 問")

        # 問題文（ルビ対応）
        q_text = q["question_ruby"] if ruby_toggle else q["question_plain"]
        st.markdown(f"#### 【問 {idx + 1}】", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size: 1.1em; line-height: 1.8;'>{q_text}</div>",
            unsafe_allow_html=True,
        )
        st.write("")

        # 選択肢ボタン
        for opt_idx, opt in enumerate(q["options"], 1):
            if st.button(f"{opt_idx}. {opt}", key=f"q_{idx}_opt_{opt_idx}"):
                is_correct = opt_idx == q["answer"]
                if is_correct:
                    st.session_state.score += 1
                st.session_state.user_answers.append({
                    "q_num": idx + 1,
                    "question": q["question_plain"],
                    "selected": opt,
                    "correct": q["options"][q["answer"] - 1],
                    "is_correct": is_correct,
                    "explanation": q["explanation"],
                })
                st.session_state.current_q += 1
                st.rerun()
    else:
        st.session_state.mode = "result"
        st.rerun()

# 3. 成績・提出画面
elif st.session_state.mode == "result":
    q_list = st.session_state.exam_questions
    total = len(q_list)
    score = st.session_state.score
    rate = round((score / total) * 100, 1)

    st.success("🎉 演習が終了しました！")
    st.metric(label="あなたの得点", value=f"{score} / {total} 問", delta=f"{rate}%")

    # 提出用テキストの生成
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_text = f"""【課題提出：人間の理解 第3章演習】
-----------------------------------
■ 受講生情報
・クラス：{student_class}
・学籍番号：{student_id}
・氏名：{student_name}
・実施日時：{now_str}

■ 成績サマリー
・得点：{score} / {total} 問（正答率：{rate}％）
・判定：{"合格水準達成" if rate >= 70 else "要復習"}
-----------------------------------
■ 誤答の振り返り
"""
    wrong_count = 0
    for item in st.session_state.user_answers:
        if not item["is_correct"]:
            wrong_count += 1
            report_text += f"\n・問{item['q_num']}: 選択「{item['selected']}」→ 正解「{item['correct']}」\n  解説: {item['explanation']}\n"
    if wrong_count == 0:
        report_text += "全問正解でした！\n"

    st.subheader("📋 教員への提出")
    st.info("下の枠内のテキストをコピーして、提出フォームやメール等に貼り付けてください。")
    st.text_area("提出用テキスト（コピー用）", value=report_text, height=220)

    if st.button("🔄 もう一度挑戦する"):
        st.session_state.mode = "menu"
        st.rerun()
