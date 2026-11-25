from pathlib import Path

import streamlit as st


_HTML = Path(__file__).with_name("human_heart.html")


def render_human_heart(height: int = 410) -> None:
    """Render a responsive, animated anatomical heart illustration."""
    st.iframe(
        _HTML.read_text(encoding="utf-8"),
        width="stretch",
        height=height,
        tab_index=0,
        alt="Animated anatomical human heart showing the atria, ventricles, and major vessels.",
    )
