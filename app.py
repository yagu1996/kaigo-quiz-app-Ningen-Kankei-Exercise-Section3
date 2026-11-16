import streamlit as st
import random
import copy
from datetime import datetime
from questions import QUESTIONS

# ページ基本設定（モバイルブラウザ対応）
st.set_page_config(
    page_title="人間の理解 第3章 演習＆模擬試験",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# カスタムCSS（押しやすいタッチUI、ルビ表示最適化、提出用ブロック）
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-size: 16px;
        padding: 10px 15px;
        margin-bottom: 8px;
        text-align: left;
    }
    ruby {
        font-size: 1.15em;
        line-height: 1.8;
    }
    rt {
        font-size: 0.58em;
        color: #444;
    }
    .report-box {
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
        padding: 15px;
        border-radius: 8px;
        font-family: monospace;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------
# 選択肢の動的シャッフル関数
# -----------------
def prepare_shuffled_questions(question_list, enable_dynamic_shuffle=True):
    """
    出題時に選択肢の並び順を動的にシャッフルし、正解インデックスを自動再計算する。
    これにより位置による暗記を完全に防ぎます。
    """
    shuffled_list = []
    for q in question_list:
        q_copy = copy.deepcopy(q)
        correct_text = q_copy["options"][q_copy["answer"] - 1]
        
        if enable_dynamic_shuffle:
            random.shuffle(q_copy["options"])
            q_copy["answer"] = q_copy["options"].index(correct_text) + 1
            
        shuffled_list.append(q_copy)
    return shuffled_list

# -----------------
# セッション状態の初期化
# -----------------
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
if "exam_title" not in st.session_state:
    st.session_state.exam_title = ""

# -----------------
# タイトル・受講生プロファイル
# -----------------
st.title("📚 人間の理解 第3章")
st.caption("チームマネジメント 練習問題＆模擬試験（動的シャッフル・ルビ対応）")

with st.expander("👤 受講生情報・設定（教員提出用）", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        student_class = st.text_input("クラス", value="介護福祉科1年")
    with col2:
        student_id = st.text_input("学籍番号", placeholder="例: A123456")
    student_name = st.text_input("氏名", placeholder="例: 介護 太郎")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        ruby_toggle = st.toggle("ふりがな（ルビ）表示", value=True)
    with col_t2:
        shuffle_toggle = st.toggle("出題ごとに選択肢をシャッフル", value=True, help="ONにすると解くたびに選択肢の順序が変わり位置暗記を防ぎます")

# -----------------
# 1. メインメニュー画面
# -----------------
if st.session_state.mode == "menu":
    st.subheader("モードを選択してください")
    
    tab1, tab2 = st.tabs(["📖 節別 練習問題", "⏱️ 模擬試験モード"])
    
    with tab1:
        st.write("各節ごとにじっくり演習を行います。全118問をカバーしています。")
        sections = [
            ("第1節 介護実践マネジメント (25問)", 1),
            ("第2節 ケア展開・集団力学 (22問)", 2),
            ("第2節 チーム力最大化・リーダーシップ (24問)", 3),
            ("第3節 人材育成・自己研鑽 (25問)", 4),
            ("第4節 組織目標達成・マネジメント (22問)", 5),
            ("【全節一括演習】 全118問", 0),
        ]
        for title, u_num in sections:
            if st.button(title, key=f"sec_btn_{u_num}"):
                if u_num == 0:
                    subset = QUESTIONS
                else:
                    subset = [q for q in QUESTIONS if q["unit"] == u_num]
                
                st.session_state.exam_questions = prepare_shuffled_questions(subset, enable_dynamic_shuffle=shuffle_toggle)
                st.session_state.exam_title = title
                st.session_state.mode = "quiz"
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.user_answers = []
                st.rerun()

    with tab2:
        st.write("全範囲からランダムに抽出された本番形式のテストです。")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("📝 模擬試験（10問）", key="mock_10"):
                sample_pool = random.sample(QUESTIONS, min(10, len(QUESTIONS)))
                st.session_state.exam_questions = prepare_shuffled_questions(sample_pool, enable_dynamic_shuffle=shuffle_toggle)
                st.session_state.exam_title = "模擬試験（ランダム10問）"
                st.session_state.mode = "quiz"
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.user_answers = []
                st.rerun()
        with col_m2:
            if st.button("🎯 実戦模試（25問）", key="mock_25"):
                sample_pool = random.sample(QUESTIONS, min(25, len(QUESTIONS)))
                st.session_state.exam_questions = prepare_shuffled_questions(sample_pool, enable_dynamic_shuffle=shuffle_toggle)
                st.session_state.exam_title = "実戦模擬試験（ランダム25問）"
                st.session_state.mode = "quiz"
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.user_answers = []
                st.rerun()

# -----------------
# 2. 問題演習画面
# -----------------
elif st.session_state.mode == "quiz":
    q_list = st.session_state.exam_questions
    idx = st.session_state.current_q
    
    if idx < len(q_list):
        q = q_list[idx]
        progress_val = (idx) / len(q_list)
        st.progress(progress_val, text=f"{st.session_state.exam_title} ： 第 {idx + 1} 問 / 全 {len(q_list)} 問")
        
        # 節バッジ
        st.markdown(f"<span style='background:#e2e3e5; color:#383d41; padding:3px 8px; border-radius:4px; font-size:0.85em;'>{q['unitTitle']}</span>", unsafe_allow_html=True)
        
        # 問題文表示（ルビ切替対応）
        q_text = q["stem"] if ruby_toggle else q["stem_plain"]
        st.markdown(f"### 問 {idx + 1}")
        st.markdown(f"<div style='font-size: 1.1em; line-height: 1.8; margin-bottom: 20px;'>{q_text}</div>", unsafe_allow_html=True)
        
        st.write("▼ 最も適切な選択肢を1つ選んでください：")
        
        # 選択肢ボタン
        for opt_idx, opt in enumerate(q["options"], 1):
            if st.button(f"{opt_idx}. {opt}", key=f"q_{idx}_opt_{opt_idx}"):
                is_correct = (opt_idx == q["answer"])
                if is_correct:
                    st.session_state.score += 1
                
                st.session_state.user_answers.append({
                    "q_num": idx + 1,
                    "unit_title": q["unitTitle"],
                    "question": q["stem_plain"],
                    "selected": opt,
                    "correct": q["options"][q["answer"] - 1],
                    "is_correct": is_correct,
                    "explanation": q["explanation"]
                })
                st.session_state.current_q += 1
                st.rerun()
                
        if st.button("⏹️ 中断してメニューに戻る", type="secondary"):
            st.session_state.mode = "menu"
            st.rerun()
    else:
        st.session_state.mode = "result"
        st.rerun()

# -----------------
# 3. 成績・提出画面
# -----------------
elif st.session_state.mode == "result":
    q_list = st.session_state.exam_questions
    total = len(q_list)
    score = st.session_state.score
    rate = round((score / total) * 100, 1) if total > 0 else 0
    passed = rate >= 70.0
    
    if passed:
        st.success(f"🎉 合格水準達成！ おめでとうございます！")
    else:
        st.warning(f"⚠️ 復習が必要です。間違えた問題を確認しましょう。")
        
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("正解数", f"{score} / {total} 問")
    col_s2.metric("正答率", f"{rate} %")
    col_s3.metric("判定", "合格" if passed else "要復習")
    
    # 提出用テキスト生成
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_text = f"""【課題提出：人間の理解 第3章演習】
------------------------------------------
■ 受講生情報
・クラス　：{student_class}
・学籍番号：{student_id}
・氏名　　：{student_name}
・実施日時：{now_str}
・実施区分：{st.session_state.exam_title}

■ 成績サマリー
・得点　　：{score} / {total} 問
・正答率　：{rate} ％
・合否判定：{"合格水準達成（70％以上）" if passed else "要復習（70％未満）"}
------------------------------------------
■ 誤答の振り返り（見直し内容）
"""
    wrong_count = 0
    for item in st.session_state.user_answers:
        if not item["is_correct"]:
            wrong_count += 1
            report_text += f"\n【問{item['q_num']}】 ({item['unit_title']})\n"
            report_text += f" 問題：{item['question']}\n"
            report_text += f" あなたの回答：{item['selected']} (×)\n"
            report_text += f" 正解　　　　：{item['correct']} (◯)\n"
            report_text += f" 解説　　　　：{item['explanation']}\n"
            
    if wrong_count == 0:
        report_text += "\n素晴らしい！全問正解でした。\n"
        
    report_text += "------------------------------------------\n"
    
    st.subheader("📋 教員への提出用テキスト")
    st.info("下の枠内のテキストをコピーし、Google Classroomの課題提出欄やメールに貼り付けて提出してください。")
    st.text_area("提出テキスト（全選択してコピー）", value=report_text, height=220)
    
    # 見直しアコーディオン
    with st.expander("🔍 全問題の振り返りと解説を開く", expanded=False):
        for item in st.session_state.user_answers:
            mark = "✅ 正解" if item["is_correct"] else "❌ 不正解"
            st.markdown(f"**問{item['q_num']}. {item['question']}** 【{mark}】")
            st.write(f"- あなたの回答: {item['selected']}")
            st.write(f"- 正解: **{item['correct']}**")
            st.caption(f"解説: {item['explanation']}")
            st.divider()
            
    if st.button("🔄 もう一度挑戦する（メニューへ）", type="primary"):
        st.session_state.mode = "menu"
        st.rerun()
