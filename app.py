"""
🧩 Puzzle Blocks - نسخة Streamlit
=================================
لعبة بلوكات ملونة بحال Puzzle Blocks:
- اللوحة: الطول 12 × العرض 6
- بلوكات بأشكال مختلفة (L, I, O, T, S...)
- نظام Score
- ستايل خشبي عربي
"""

import streamlit as st
import random
import time

# ============================================================
# إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="🧩 Puzzle Blocks",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS - ستايل خشبي + RTL
# ============================================================
WOOD_STYLE = """
<style>
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

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
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
    padding: 12px;
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

/* ---------- المقاييس ---------- */
[data-testid="stMetric"] {
    background: linear-gradient(180deg, #D2B48C, #A0522D);
    border: 3px solid #4A2C0F;
    border-radius: 12px;
    padding: 12px;
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
    font-size: 26px !important;
}

/* ---------- أزرار ---------- */
div[data-testid="stButton"] > button {
    width: 100%;
    font-size: 18px;
    font-weight: 900;
    color: #FFFFFF !important;
    background:
        radial-gradient(circle at 30% 30%, rgba(255,255,255,0.3), transparent 60%),
        linear-gradient(180deg, #D2691E 0%, #8B4513 100%);
    border: 3px solid #4A2C0F;
    border-radius: 10px;
    box-shadow:
        inset 0 3px 0 rgba(255,255,255,0.25),
        inset 0 -4px 0 rgba(0,0,0,0.3),
        0 5px 10px rgba(0,0,0,0.5);
    text-shadow: 2px 2px 3px rgba(0,0,0,0.7);
    padding: 8px !important;
    transition: all 0.1s ease;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    background:
        radial-gradient(circle at 30% 30%, rgba(255,255,255,0.4), transparent 60%),
        linear-gradient(180deg, #E07B39 0%, #A0522D 100%);
}

div[data-testid="stButton"] > button:active {
    transform: translateY(2px);
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

/* ---------- تنبيهات ---------- */
[data-testid="stAlert"] {
    border-radius: 15px;
    border: 4px solid #4A2C0F;
    font-weight: 700;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4);
}

p, span, label {
    color: #F5DEB3;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

st.markdown(WOOD_STYLE, unsafe_allow_html=True)


# ============================================================
# ثوابت اللعبة
# ============================================================
ROWS = 12   # الطول
COLS = 6    # العرض

# ألوان البلوكات
COLORS = {
    "red":    ("#FF4D4D", "#C62828"),
    "blue":   ("#4D94FF", "#1565C0"),
    "green":  ("#4DD94D", "#2E7D32"),
    "yellow": ("#FFD24D", "#F9A825"),
    "orange": ("#FF9F4D", "#E65100"),
    "purple": ("#B84DFF", "#6A1B9A"),
    "pink":   ("#FF4DB8", "#AD1457"),
    "cyan":   ("#4DFFFF", "#00838F"),
}

COLOR_KEYS = list(COLORS.keys())

# أشكال البلوكات (إحداثيات نسبية)
SHAPES = {
    "I2":  [(0, 0), (0, 1)],
    "I3":  [(0, 0), (0, 1), (0, 2)],
    "I4":  [(0, 0), (0, 1), (0, 2), (0, 3)],
    "O":   [(0, 0), (0, 1), (1, 0), (1, 1)],
    "L":   [(0, 0), (1, 0), (2, 0), (2, 1)],
    "J":   [(0, 1), (1, 1), (2, 1), (2, 0)],
    "T":   [(0, 0), (0, 1), (0, 2), (1, 1)],
    "S":   [(0, 1), (0, 2), (1, 0), (1, 1)],
    "Z":   [(0, 0), (0, 1), (1, 1), (1, 2)],
    "Tiny":[(0, 0)],
    "Line2V": [(0, 0), (1, 0)],
}

SHAPE_NAMES = list(SHAPES.keys())


# ============================================================
# توليد البلوكات
# ============================================================
def random_block():
    """توليد بلوك عشوائي."""
    shape_key = random.choice(SHAPE_NAMES)
    color_key = random.choice(COLOR_KEYS)
    cells = SHAPES[shape_key]
    return {
        "shape": shape_key,
        "color": color_key,
        "cells": cells,
    }


def blocks_to_grid(block):
    """تحويل البلوك لمصفوفة صغيرة للعرض."""
    cells = block["cells"]
    if not cells:
        return []
    max_r = max(c[0] for c in cells) + 1
    max_c = max(c[1] for c in cells) + 1
    grid = [[None for _ in range(max_c)] for _ in range(max_r)]
    for (r, c) in cells:
        grid[r][c] = block["color"]
    return grid


# ============================================================
# منطق اللوحة
# ============================================================
def new_board():
    return [[None for _ in range(COLS)] for _ in range(ROWS)]


def can_place(board, block, row, col):
    """هل يمكن وضع البلوك في (row, col)؟"""
    for (dr, dc) in block["cells"]:
        r, c = row + dr, col + dc
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            return False
        if board[r][c] is not None:
            return False
    return True


def place_block(board, block, row, col):
    """وضع البلوك على اللوحة."""
    for (dr, dc) in block["cells"]:
        r, c = row + dr, col + dc
        board[r][c] = block["color"]


def clear_lines(board):
    """مسح الصفوف والأعمدة الممتلئة، وإرجاع عدد المسوح."""
    cleared = 0
    # الصفوف
    for r in range(ROWS):
        if all(board[r][c] is not None for c in range(COLS)):
            for c in range(COLS):
                board[r][c] = None
            cleared += 1
    # الأعمدة
    for c in range(COLS):
        if all(board[r][c] is not None for r in range(ROWS)):
            for r in range(ROWS):
                board[r][c] = None
            cleared += 1
    return cleared


def score_for_clear(cleared):
    """حساب النقاط."""
    if cleared == 0:
        return 0
    # نقاط متزايدة
    return cleared * 100 + (cleared - 1) * 50


def can_place_anywhere(board, block):
    """هل يمكن وضع البلوك في أي مكان؟"""
    for r in range(ROWS):
        for c in range(COLS):
            if can_place(board, block, r, c):
                return True
    return False


# ============================================================
# إدارة الحالة
# ============================================================
def init_state():
    if "board" not in st.session_state:
        st.session_state.board = new_board()
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "high_score" not in st.session_state:
        st.session_state.high_score = 0
    if "blocks" not in st.session_state:
        st.session_state.blocks = [random_block() for _ in range(3)]
    if "selected_block" not in st.session_state:
        st.session_state.selected_block = 0
    if "game_over" not in st.session_state:
        st.session_state.game_over = False


def reset_game():
    st.session_state.board = new_board()
    st.session_state.score = 0
    st.session_state.blocks = [random_block() for _ in range(3)]
    st.session_state.selected_block = 0
    st.session_state.game_over = False
    st.session_state.win_shown = False


def refill_blocks():
    """إعادة تعبئة 3 بلوكات جديدة."""
    st.session_state.blocks = [random_block() for _ in range(3)]
    st.session_state.selected_block = 0


def check_game_over():
    """هل انتهت اللعبة؟"""
    board = st.session_state.board
    for block in st.session_state.blocks:
        if can_place_anywhere(board, block):
            return False
    return True


# ============================================================
# رسم البلوك الصغير (HTML)
# ============================================================
def render_small_block(block, selected=False):
    """رسم بلوك صغير بـ HTML."""
    grid = blocks_to_grid(block)
    if not grid:
        return ""

    border = "4px solid #FFD24D" if selected else "2px solid #4A2C0F"
    size = 26

    html = f"""
    <div style="
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 6px;
        background: rgba(74,44,15,0.4);
        border-radius: 8px;
        border: {border};
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.5);
    ">
    """
    for row in grid:
        html += "<div style='display:flex;'>"
        for cell in row:
            if cell is None:
                html += f"<div style='width:{size}px;height:{size}px;'></div>"
            else:
                light, dark = COLORS[cell]
                html += f"""
                <div style="
                    width:{size}px;height:{size}px;
                    background: radial-gradient(circle at 30% 30%, {light}, {dark});
                    border: 2px solid #4A2C0F;
                    border-radius: 4px;
                    box-shadow: inset 0 1px 0 rgba(255,255,255,0.4),
                                inset 0 -2px 0 rgba(0,0,0,0.3);
                    margin: 1px;
                    box-sizing: border-box;
                "></div>
                """
        html += "</div>"
    html += "</div>"
    return html


# ============================================================
# رسم اللوحة
# ============================================================
def render_board():
    board = st.session_state.board

    # حجم الخلايا حسب عرض الشاشة - نستخدم table
    cell_size = 42

    html = """
    <div style="
        display: flex;
        justify-content: center;
        padding: 12px;
        background: linear-gradient(135deg, #5C3317, #3E1F0B);
        border-radius: 15px;
        border: 5px solid #4A2C0F;
        box-shadow:
            inset 0 4px 15px rgba(0,0,0,0.6),
            0 8px 25px rgba(0,0,0,0.5);
        margin: 10px auto;
        width: fit-content;
    ">
    <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 4px;">
    """

    for r in range(ROWS):
        for c in range(COLS):
            val = board[r][c]
            if val is None:
                bg = "rgba(74,44,15,0.5)"
                border = "2px solid #3E1F0B"
                shadow = "inset 0 2px 6px rgba(0,0,0,0.5)"
                extra = ""
            else:
                light, dark = COLORS[val]
                bg = f"radial-gradient(circle at 30% 30%, {light}, {dark})"
                border = "2px solid #4A2C0F"
                shadow = (
                    "inset 0 2px 0 rgba(255,255,255,0.4), "
                    "inset 0 -3px 0 rgba(0,0,0,0.3), "
                    "0 2px 4px rgba(0,0,0,0.4)"
                )
                extra = "border-radius:6px;"

            html += f"""
            <div style="
                width:{cell_size}px;
                height:{cell_size}px;
                background: {bg};
                border: {border};
                border-radius: 6px;
                box-shadow: {shadow};
                {extra}
            "></div>
            """

    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# واجهة المستخدم
# ============================================================
def render_header():
    st.markdown("# 🧩 Puzzle Blocks")
    st.markdown(
        "<p style='text-align:center; color:#F5DEB3; font-size:15px;"
        " text-shadow:1px 1px 2px #000;'>"
        "اختر بلوكاً، ثم اختر صفاً وعموداً لوضعه — املأ الصفوف والأعمدة لمسحها!"
        "</p>",
        unsafe_allow_html=True,
    )


def render_stats():
    col1, col2, col3 = st.columns(3)
    col1.metric("🏆 النقاط", st.session_state.score)
    col2.metric("⭐ أفضل نتيجة", st.session_state.high_score)

    filled = sum(
        1 for row in st.session_state.board for cell in row if cell is not None
    )
    total = ROWS * COLS
    col3.metric("📦 ممتلئ", f"{filled}/{total}")


def render_block_selector():
    st.markdown("### 🎨 البلوكات المتاحة")

    cols = st.columns(3)
    for i, block in enumerate(st.session_state.blocks):
        with cols[i]:
            selected = (i == st.session_state.selected_block)
            html = render_small_block(block, selected)
            st.markdown(html, unsafe_allow_html=True)
            label = "✅ مختار" if selected else "اختر"
            if st.button(label, key=f"select_{i}", use_container_width=True):
                st.session_state.selected_block = i
                st.rerun()


def render_placement_controls():
    """اختيار الصف والعمود للوضع."""
    if not st.session_state.blocks:
        return

    block = st.session_state.blocks[st.session_state.selected_block]
    board = st.session_state.board

    st.markdown("### 📍 مكان الوضع")

    # الصفوف اللي يمكن فيها الوضع
    valid_rows = list(range(ROWS))
    valid_cols = list(range(COLS))

    col1, col2 = st.columns(2)
    with col1:
        row = st.selectbox(
            "الصف (من فوق)",
            valid_rows,
            format_func=lambda x: f"صف {x + 1}",
            key="row_select",
        )
    with col2:
        col = st.selectbox(
            "العمود (من اليمين)",
            valid_cols,
            format_func=lambda x: f"عمود {x + 1}",
            key="col_select",
        )

    can = can_place(board, block, row, col)

    if can:
        st.success(f"✅ يمكن وضع البلوك في ({row + 1}, {col + 1})")
    else:
        st.warning(f"❌ لا يمكن وضع البلوك في ({row + 1}, {col + 1})")

    if st.button(
        "📍 ضع البلوك هنا",
        use_container_width=True,
        type="primary",
        disabled=not can,
    ):
        place_block(board, block, row, col)
        # احذف البلوك من القائمة
        st.session_state.blocks.pop(st.session_state.selected_block)
        st.session_state.selected_block = max(0, st.session_state.selected_block - 1)

        # مسح الخطوط
        cleared = clear_lines(board)
        if cleared > 0:
            gained = score_for_clear(cleared)
            st.session_state.score += gained
            st.session_state.last_gain = gained
            st.session_state.last_cleared = cleared
        else:
            st.session_state.last_gain = 0
            st.session_state.last_cleared = 0

        # تعبئة بلوكات جديدة إذا خلصو
        if not st.session_state.blocks:
            refill_blocks()

        # التحقق من انتهاء اللعبة
        if check_game_over():
            st.session_state.game_over = True

        st.rerun()


def render_controls():
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 لعبة جديدة", use_container_width=True):
            reset_game()
            st.rerun()

    with col2:
        if st.button("💡 تبديل البلوكات", use_container_width=True):
            refill_blocks()
            st.rerun()


def render_game_over():
    if st.session_state.game_over:
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score

        st.error(
            f"💀 **انتهت اللعبة!**\n\n"
            f"🏆 النقاط: **{st.session_state.score}**\n\n"
            f"⭐ أفضل نتيجة: **{st.session_state.high_score}**"
        )
        if st.button("🎮 ابدأ من جديد", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()


def render_last_action():
    """عرض آخر نتيجة مسح."""
    if st.session_state.get("last_gain", 0) > 0:
        cleared = st.session_state.get("last_cleared", 0)
        gained = st.session_state["last_gain"]
        st.success(
            f"✨ مسحت **{cleared}** خطوط! حصلت على **+{gained}** نقطة!"
        )
        st.session_state.last_gain = 0


def render_footer():
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#D2B48C; font-size:13px;"
        " text-shadow:1px 1px 2px #000;'>"
        "🪵 Puzzle Blocks — طول 12 × عرض 6 — نسخة Streamlit"
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
    render_last_action()
    render_board()
    render_block_selector()

    if not st.session_state.game_over:
        render_placement_controls()

    render_controls()
    render_game_over()
    render_footer()


if __name__ == "__main__":
    main()
