from pathlib import Path

import streamlit as st


_HTML = Path(__file__).with_name("heart_globe.html")


def render_heart_globe(height: int = 410) -> None:
    """Render the Earth image inside a glowing, animated heart silhouette."""
    st.iframe(
        _HTML.read_text(encoding="utf-8"),
        width="stretch",
        height=height,
        tab_index=0,
        alt="Earth texture glowing inside a heart-shaped globe, with softly twinkling stars.",
    )
