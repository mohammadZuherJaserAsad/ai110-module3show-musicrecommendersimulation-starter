"""Streamlit UI for the Music Recommender Simulation."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from src.recommender import load_songs, recommend_songs

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VibeMatch 1.0 – Music Recommender",
    page_icon="🎵",
    layout="centered",
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🎵 VibeMatch 1.0")
st.subheader("A content-based music recommender simulation")
st.markdown(
    "Tell us your taste and we'll rank the best matching songs from our catalog."
)
st.divider()

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_songs():
    return load_songs("data/songs.csv")

songs = get_songs()

# ── Sidebar – User Preferences ────────────────────────────────────────────────
st.sidebar.header("🎧 Your Taste Profile")

genres = sorted(set(s["genre"] for s in songs))
moods  = sorted(set(s["mood"]  for s in songs))

favorite_genre  = st.sidebar.selectbox("Favorite Genre",  genres, index=genres.index("pop") if "pop" in genres else 0)
favorite_mood   = st.sidebar.selectbox("Favorite Mood",   moods,  index=moods.index("happy") if "happy" in moods else 0)
target_energy   = st.sidebar.slider("Target Energy (0 = calm, 1 = high)", 0.0, 1.0, 0.8, step=0.05)
likes_acoustic  = st.sidebar.toggle("I prefer acoustic sounds 🎸", value=False)
top_k           = st.sidebar.slider("Number of recommendations", 1, len(songs), 5)

user_prefs = {
    "genre":        favorite_genre,
    "mood":         favorite_mood,
    "energy":       target_energy,
    "likes_acoustic": likes_acoustic,
}

# ── Recommendations ───────────────────────────────────────────────────────────
st.markdown("### 🏆 Top Recommendations")

recommendations = recommend_songs(user_prefs, songs, k=top_k)

if not recommendations:
    st.info("No songs found. Try adjusting your preferences.")
else:
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**#{rank} — {song['title']}** by *{song['artist']}*")
                st.caption(
                    f"Genre: `{song['genre']}` · Mood: `{song['mood']}` · "
                    f"Energy: `{song['energy']}` · Acousticness: `{song['acousticness']}`"
                )
                st.markdown(f"💡 _{explanation}_")
            with col2:
                st.metric("Score", f"{score:.1f}")

# ── Divider + Catalog ─────────────────────────────────────────────────────────
st.divider()
with st.expander("📂 View Full Song Catalog"):
    import pandas as pd
    df = pd.DataFrame(songs)
    st.dataframe(df, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("AI110 – Module 3 Project · Content-based filtering simulation · 10-song catalog")
