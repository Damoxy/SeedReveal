import streamlit as st
import random
from datetime import datetime
from google_sheets import get_worksheet

# --- 1. Player and Code Setup ---
all_players = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry",
    "Ivy", "Jack", "Karen", "Leo", "Mona", "Nate", "Olivia", "Paul"
]

player_codes = {
    "Alice": "1234", "Bob": "2345", "Charlie": "3456", "Diana": "4567",
    "Eve": "5678", "Frank": "6789", "Grace": "7890", "Henry": "8901",
    "Ivy": "9012", "Jack": "0123", "Karen": "1111", "Leo": "2222",
    "Mona": "3333", "Nate": "4444", "Olivia": "5555", "Paul": "6666"
}

# --- 2. Seed Setup ---
all_seeds = [f"{chr(i)}{j}" for i in range(ord('A'), ord('H') + 1) for j in (1, 2)]

if "shuffled_seeds" not in st.session_state:
    st.session_state.shuffled_seeds = all_seeds.copy()
    random.shuffle(st.session_state.shuffled_seeds)

# --- 3. Load from Google Sheet ---
sheet = get_worksheet()
records = sheet.get_all_records()

try:
    assignments = {row["Player"]: row["Seed"] for row in records}
except KeyError as e:
    st.error(f"❌ Google Sheet is missing column: {e}")
    st.stop()

taken_seeds = set(assignments.values())
available_players = [p for p in all_players if p not in assignments]

# --- 4. Title ---
st.title("🏆 Knockout Cup Draw")

# --- 5. Current Seed Status with Locked icons ---
st.subheader("🎲 Current Seed Status")

cols = st.columns(8)
for idx, seed in enumerate(st.session_state.shuffled_seeds):
    col = cols[idx % 8]
    with col:
        if seed in taken_seeds:
            # Taken seeds: show seed disabled normally
            col.button(seed, key=f"readonly_{seed}", disabled=True)
        else:
            # Not taken seeds: show locked icon disabled (blurred look)
            col.button("🔒", key=f"locked_{seed}", disabled=True)

# --- 6. Authentication ---
st.subheader("🔐 Enter to Choose Your Tile")

selected_player = st.selectbox("👤 Select your name:", [""] + available_players)
access_code = st.text_input("🔑 Enter your access code:", type="password")

if st.button("✅ Submit"):
    if not selected_player:
        st.warning("Please select your name.")
    elif access_code != player_codes.get(selected_player):
        st.warning("❌ Incorrect access code.")
    elif selected_player in assignments:
        st.success(f"✅ You have already been seeded to **{assignments[selected_player]}**.")
    else:
        st.session_state.verified_player = selected_player
        st.rerun()

# --- 7. Tile selection after verification ---
if "verified_player" in st.session_state:
    player = st.session_state.verified_player

    if player in assignments:
        st.success(f"✅ You have already been seeded to **{assignments[player]}**.")
    else:
        st.success(f"✅ Welcome {player}! Please select your seed:")
        cols = st.columns(8)

        for idx, seed in enumerate(st.session_state.shuffled_seeds):
            col = cols[idx % 8]
            with col:
                if seed in taken_seeds:
                    st.button(seed, key=f"select_disabled_{seed}", disabled=True)
                else:
                    if st.button("🔒", key=f"{player}_{seed}"):
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        sheet.append_row([player, seed, timestamp])
                        st.success(f"🎯 You have been seeded to **{seed}**!")
                        st.rerun()


