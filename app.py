"""
🧩 لعبة الألغاز - نسخة عربية كاملة
==================================
- واجهة عربية (RTL)
- 10 مستويات (من 3x3 إلى 12x12)
- ستايل خشبي (Wood Style)
- متوافقة مع Streamlit Cloud
"""

import streamlit as st
import random
import time

# ============================================================
# إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="🧩 لعبة الألغاز",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS - ستايل خشبي + RTL
# ============================================================
WOOD_STYLE = """
<style>
/* ---------- الخط العربي ---------- */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', 'Segoe UI', sans-serif !important;
    direction: rtl;
    text-align: right;
}

/* ---------- خلفية خشبية ---------- */
.stApp {
    background:
        repeating-linear-gradient(
            90deg,
            rgba(0,0,0,0.03) 0px,
            rgba(0,0,0,0.03) 2px,
            transparent 2px,
            transparent 12px
        ),
        repeating-linear-gradient(
            0deg,
            rgba(0,0,0,0.02) 0px,
            rgba(0,0,0,0.02) 4px,
            transparent 4px,
            transparent 20px
        ),
        linear-gradient(135deg, #8B5A2B 0%, #A0522D 50%, #6B3E1F 100%);
    background-attachment: fixed;
}

/* ---------- الحاوية الرئيسية ---------- */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    background: rgba(139, 90, 43, 0.15);
    border-radius: 20px;
    backdrop-filter: blur(2px);
}

/* ---------- العنوان ---------- */
h1 {
    color: #F5DEB3 !important;
    text-align: center !important;
    text-shadow:
        2px 2px 0 #4A2C0F,
        4px 4px 8px rgba(0,0,0,0.5) !important;
    font-weight: 900 !important;
    letter-spacing: 1px;
    padding: 10px;
    background: linear-gradient(180deg, #A0522D, #6B3E1F);
    border: 4px solid #4A2C0F;
    border-radius: 15px;
    box-shadow:
        inset 0 2px 0 rgba(255,255,255,0.2),
        inset 0 -2px 0 rgba(0,0,0,0.3),
        0 8px 20px rgba(0,0,0,0.4);
}

h2, h3 {
    color: #F5DEB3 !important;
    text-align: center !important;
    text-shadow: 1px 1px 2px #000;
}

/* ---------- المقاييس (Moves / Time) ---------- */
[data-testid="stMetric"] {
    background: linear-gradient(180deg, #D2B48C, #A0522D);
    border: 3px solid #4A2C0F;
    border-radius: 12px;
    padding: 15px;
    box-shadow:
        inset 0 2px 0 rgba(255,255,255,0.3),
        inset 0 -3px 0 rgba(0,0,0,0.3),
        0 5px 15px rgba(0,0,0,0.4);
}

[data-testid="stMetricLabel"] {
    color: #3E1F0B !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    text-align: center !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 900 !important;
    text-shadow: 2px 2px 3px rgba(0,0,0,0.6) !important;
    text-align: center !important;
    font-size: 28px !important;
}

/* ---------- أزرار البطائق ---------- */
div[data-testid="stButton"] > button {
    width: 100%;
    height: 70px;
    font-size: 24px;
    font-weight: 900;
    color: #FFFFFF !important;
    background:
        radial-gradient(circle at 30% 30%, rgba(255,255,255,0.3), transparent 60%),
        linear-gradient(180deg, #D2691E 0%, #8B4513 100%);
    border: 4px solid #4A2C0F;
    border-radius: 12px;
    box-shadow:
        inset 0 3px 0 rgba(255,255,255,0.25),
        inset 0 -4px 0 rgba(0,0,0,0.3),
        0 6px 12px rgba(0,0,0,0.5);
    text-shadow: 2px 2px 3px rgba(0,0,0,0.7);
    transition: all 0.1s ease;
    padding: 0 !important;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    background:
        radial-gradient(circle at 30% 30%, rgba(255,255,255,0.4), transparent 60%),
        linear-gradient(180deg, #E07B39 0%, #A0522D 100%);
    box-shadow:
        inset 0 3px 0 rgba(255,255,255,0.3),
        inset 0 -4px 0 rgba(0,0,0,0.3),
        0 8px 16px rgba(0,0,0,0.6);
}

div[data-testid="stButton"] > button:active {
    transform: translateY(2px);
    box-shadow:
        inset 0 2px 0 rgba(0,0,0,0.3),
        0 2px 6px rgba(0,0,0,0.4);
}

/* ---------- البلاصة الخاوية ---------- */
.empty-slot {
    width: 100%;
    height: 70px;
    background: rgba(74, 44, 15, 0.6);
    border: 3px dashed #3E1F0B;
    border-radius: 12px;
    box-shadow: inset 0 4px 10px rgba(0,0,0,0.6);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ---------- أزرار التحكم ---------- */
div[data-testid="stButton"] > button[kind="secondary"] {
    height: 55px;
    font-size: 18px;
    background:
        radial-gradient(circle at 30% 30%, rgba(255,255,255,0.25), transparent 60%),
        linear-gradient(180deg, #B8860B 0%, #8B6508 100%);
    border: 3px solid #4A2C0F;
}

/* ---------- Selectbox ---------- */
[data-testid="stSelectbox"] label {
    color: #F5DEB3 !important;
    font-weight: 700 !important;
    text-shadow: 1px 1px 2px #000;
}

[data-testid="stSelectbox"] > div > div {
    background: linear-gradient(180deg, #D2B48C, #A0522D) !important;
    border: 3px solid #4A2C0F !important;
    border-radius: 10px !important;
    color: #3E1F0B !important;
    font-weight: 700 !important;
}

/* ---------- رسائل النجاح ---------- */
[data-testid="stAlert"] {
    border-radius: 15px;
    border: 4px solid #4A2C0F;
    font-weight: 700;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4);
}

/* ---------- النصوص ---------- */
p, span, label {
    color: #F5DEB3;
}

/* ---------- إخفاء عناصر Streamlit غير الضرورية ---------- */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---------- لوجو الخشب على الحواف ---------- */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 8px;
    background: linear-gradient(90deg, #4A2C0F, #8B4513, #4A2C0F);
    z-index: 999;
}
</style>
"""

st.markdown(WOOD_STYLE, unsafe_allow_html=True)


# ============================================================
# منطق اللعبة
# ============================================================
class PuzzleBoard:
    """لوحة اللغز - المسؤولة عن الحالة والحركات"""

    def __init__(self, size=3):
        self.size = size
        self.reset()
        self.shuffle()

    def reset(self):
        total = self.size * self.size
        self.board = list(range(1, total)) + [0]
        self.empty_index = len(self.board) - 1

    def get_neighbors(self, idx):
        row, col = idx // self.size, idx % self.size
        neighbors = []
        if row > 0:
            neighbors.append(idx - self.size)
        if row < self.size - 1:
            neighbors.append(idx + self.size)
        if col > 0:
            neighbors.append(idx - 1)
        if col < self.size - 1:
            neighbors.append(idx + 1)
        return neighbors

    def shuffle(self):
        # حركات عشوائية صحيحة = اللغز دايماً قابل للحل
        for _ in range(self.size * self.size * 60):
            neighbors = self.get_neighbors(self.empty_index)
            n = random.choice(neighbors)
            self.board[self.empty_index], self.board[n] = (
                self.board[n], self.board[self.empty_index],
            )
            self.empty_index = n
        if self.is_solved():
            self.shuffle()

    def try_move(self, idx):
        if idx == self.empty_index:
            return False
        if idx in self.get_neighbors(self.empty_index):
            self.board[self.empty_index], self.board[idx] = (
                self.board[idx], self.board[self.empty_index],
            )
            self.empty_index = idx
            return True
        return False

    def is_solved(self):
        return self.board == list(range(1, self.size * self.size)) + [0]


# ============================================================
# إدارة المستويات (10 مستويات)
# ============================================================
LEVELS = [
    {"id": 1,  "size": 3,  "name": "المستوى 1 - مبتدئ (3×3)",     "emoji": "🟢"},
    {"id": 2,  "size": 3,  "name": "المستوى 2 - سريع (3×3)",       "emoji": "🟢"},
    {"id": 3,  "size": 4,  "name": "المستوى 3 - سهل (4×4)",        "emoji": "🟡"},
    {"id": 4,  "size": 4,  "name": "المستوى 4 - متوسط (4×4)",      "emoji": "🟡"},
    {"id": 5,  "size": 5,  "name": "المستوى 5 - تحدٍ (5×5)",       "emoji": "🟠"},
    {"id": 6,  "size": 5,  "name": "المستوى 6 - صعب (5×5)",        "emoji": "🟠"},
    {"id": 7,  "size": 6,  "name": "المستوى 7 - خبير (6×6)",       "emoji": "🔴"},
    {"id": 8,  "size": 7,  "name": "المستوى 8 - محترف (7×7)",      "emoji": "🔴"},
    {"id": 9,  "size": 8,  "name": "المستوى 9 - أسطوري (8×8)",     "emoji": "🟣"},
    {"id": 10, "size": 10, "name": "المستوى 10 - وحشي (10×10)",    "emoji": "⚫"},
]

LEVEL_MAP = {lvl["id"]: lvl for lvl in LEVELS}


# ============================================================
# إدارة الحالة (Session State)
# ============================================================
def init_state():
    if "level_id" not in st.session_state:
        st.session_state.level_id = 1
    if "moves" not in st.session_state:
        st.session_state.moves = 0
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    if "elapsed" not in st.session_state:
        st.session_state.elapsed = 0
    if "game" not in st.session_state:
        _new_game(st.session_state.level_id)
    if "win_shown" not in st.session_state:
        st.session_state.win_shown = False


def _new_game(level_id):
    lvl = LEVEL_MAP[level_id]
    st.session_state.game = PuzzleBoard(lvl["size"])
    st.session_state.moves = 0
    st.session_state.start_time = time.time()
    st.session_state.elapsed = 0
    st.session_state.win_shown = False


def change_level(new_level_id):
    if new_level_id != st.session_state.level_id:
        st.session_state.level_id = new_level_id
        _new_game(new_level_id)
        st.rerun()


# ============================================================
# رسم الواجهة
# ============================================================
def render_header():
    st.markdown("# 🧩 لعبة الألغاز الخشبية")
    st.markdown(
        "<p style='text-align:center; color:#F5DEB3; font-size:16px;"
        " text-shadow:1px 1px 2px #000;'>"
        "حرّك المربعات حتى ترتّبها من 1 إلى الأخير — استعمل الفأرة أو اللمس"
        "</p>",
        unsafe_allow_html=True,
    )


def render_stats():
    game = st.session_state.game
    elapsed = st.session_state.elapsed
    if not game.is_solved() and st.session_state.moves > 0:
        elapsed = int(time.time() - st.session_state.start_time)
        st.session_state.elapsed = elapsed

    minutes = elapsed // 60
    seconds = elapsed % 60

    col1, col2, col3 = st.columns(3)
    col1.metric("🔄 الحركات", st.session_state.moves)
    col2.metric("⏱️ الوقت", f"{minutes:02d}:{seconds:02d}")
    col3.metric("🎯 المستوى", f"{st.session_state.level_id} / 10")


def render_level_selector():
    st.markdown("### 🎚️ اختر المستوى")
    options = [lvl["id"] for lvl in LEVELS]

    def fmt(i):
        lvl = LEVEL_MAP[i]
        return f"{lvl['emoji']} {lvl['name']}"

    selected = st.selectbox(
        "المستويات (من 1 إلى 10)",
        options=options,
        index=options.index(st.session_state.level_id),
        format_func=fmt,
        label_visibility="collapsed",
    )
    if selected != st.session_state.level_id:
        change_level(selected)


def render_board():
    game = st.session_state.game
    size = game.size

    # حجم الخط حسب حجم اللوحة
    font_size = max(12, min(24, 90 // size))

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    for r in range(size):
        cols = st.columns(size, gap="small")
        for c in range(size):
            idx = r * size + c
            val = game.board[idx]

            with cols[c]:
                if val == 0:
                    st.markdown(
                        "<div class='empty-slot'></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    clicked = st.button(
                        str(val),
                        key=f"tile_{idx}_{st.session_state.level_id}",
                        use_container_width=True,
                    )
                    if clicked:
                        if game.try_move(idx):
                            st.session_state.moves += 1
                            st.rerun()


def render_controls():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔀 خلط جديد", use_container_width=True, type="secondary"):
            _new_game(st.session_state.level_id)
            st.rerun()

    with col2:
        if st.button("🔄 إعادة المحاولة", use_container_width=True, type="secondary"):
            _new_game(st.session_state.level_id)
            st.rerun()

    with col3:
        if st.button("💡 حل تلقائي", use_container_width=True, type="secondary"):
            game = st.session_state.game
            game.reset()
            st.session_state.elapsed = int(time.time() - st.session_state.start_time)
            st.session_state.moves = 0
            st.rerun()


def render_win():
    game = st.session_state.game
    if game.is_solved() and st.session_state.moves > 0:
        elapsed = int(time.time() - st.session_state.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60

        if not st.session_state.win_shown:
            st.balloons()
            st.session_state.win_shown = True

        st.success(
            f"🎉 **مبروك!** حلّيت المستوى {st.session_state.level_id} بنجاح!\n\n"
            f"🔄 الحركات: **{st.session_state.moves}**  |  "
            f"⏱️ الوقت: **{minutes:02d}:{seconds:02d}**"
        )

        if st.session_state.level_id < 10:
            if st.button(
                f"➡️ الانتقال للمستوى {st.session_state.level_id + 1}",
                type="primary",
                use_container_width=True,
            ):
                change_level(st.session_state.level_id + 1)
        else:
            st.info("🏆 أنت بطل! ختمتي جميع المستويات العشرة!")


def render_footer():
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#D2B48C; font-size:13px;"
        " text-shadow:1px 1px 2px #000;'>"
        "🪵 صنع بحب — لعبة الألغاز الخشبية · 10 مستويات · Streamlit"
        "</p>",
        unsafe_allow_html=True,
    )


# ============================================================
# التشغيل
# ============================================================
def main():
    init_state()
    render_header()
    render_stats()
    render_level_selector()
    render_board()
    render_controls()
    render_win()
    render_footer()


if __name__ == "__main__":
    main()
