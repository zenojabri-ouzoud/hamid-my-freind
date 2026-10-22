import streamlit as st
import random

# --- منطق اللعبة (نفس المنطق اللي درناه قبيل) ---
class PuzzleBoard:
    def __init__(self, size=3):
        self.size = size
        self.reset()
        self.shuffle()

    def reset(self):
        total = self.size * self.size
        self.board = list(range(1, total)) + [0]
        self.empty_index = len(self.board) - 1

    def shuffle(self):
        for _ in range(self.size * self.size * 50):
            neighbors = self.get_neighbors(self.empty_index)
            n = random.choice(neighbors)
            self.board[self.empty_index], self.board[n] = self.board[n], self.board[self.empty_index]
            self.empty_index = n

    def get_neighbors(self, idx):
        row, col = idx // self.size, idx % self.size
        neighbors = []
        if row > 0: neighbors.append(idx - self.size)
        if row < self.size - 1: neighbors.append(idx + self.size)
        if col > 0: neighbors.append(idx - 1)
        if col < self.size - 1: neighbors.append(idx + 1)
        return neighbors

    def try_move(self, idx):
        if idx == self.empty_index: return False
        if idx in self.get_neighbors(self.empty_index):
            self.board[self.empty_index], self.board[idx] = self.board[idx], self.board[self.empty_index]
            self.empty_index = idx
            return True
        return False

    def is_solved(self):
        return self.board == list(range(1, self.size * self.size)) + [0]

# --- واجهة Streamlit ---
st.set_page_config(page_title="Puzzle Game", layout="centered")
st.title("🧩 Puzzle Game")

# إدارة الحالة (State)
if 'size' not in st.session_state:
    st.session_state.size = 3
if 'game' not in st.session_state or st.session_state.get('game_size') != st.session_state.size:
    st.session_state.game = PuzzleBoard(st.session_state.size)
    st.session_state.game_size = st.session_state.size
    st.session_state.moves = 0
if 'moves' not in st.session_state:
    st.session_state.moves = 0

# اختيار الحجم
size_choice = st.selectbox("Level", [3, 4, 5], index=st.session_state.size - 3)
if size_choice != st.session_state.size:
    st.session_state.size = size_choice
    st.rerun()

game = st.session_state.game

# عرض الإحصائيات
col1, col2 = st.columns(2)
col1.metric("Moves", st.session_state.moves)
col2.metric("Status", "Solved! 🎉" if game.is_solved() else "Playing...")

# رسم البورد (Grid) باستعمال الأزرار
for r in range(game.size):
    cols = st.columns(game.size)
    for c in range(game.size):
        idx = r * game.size + c
        val = game.board[idx]
        if val == 0:
            cols[c].write("⬜") # بلاصة خاوية
        else:
            if cols[c].button(str(val), key=f"tile_{idx}", use_container_width=True):
                if game.try_move(idx):
                    st.session_state.moves += 1
                    st.rerun()

# أزرار التحكم
if st.button("🔀 Shuffle / New Game"):
    st.session_state.game = PuzzleBoard(st.session_state.size)
    st.session_state.moves = 0
    st.rerun()

if game.is_solved():
    st.balloons()
    st.success("🎉 مبروك! حلّيتي اللعبة!")
