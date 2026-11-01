
import streamlit as st
from datetime import datetime


def render_audio_recorder():

    st.markdown("### 🎙 Interview Answer Recorder")

    question = st.selectbox(
        "Choose an interview question",
        [
            "Tell me about yourself.",
            "Describe a challenging project.",
            "How do you handle conflict?",
            "What is your biggest professional achievement?",
            "Why should we hire you?",
            "Explain a technical problem you solved."
        ]
    )

    st.info(question)

    audio = st.audio_input(
        "Record your interview answer",
        key="interview_recording"
    )

    if audio:

        st.success("Audio recorded successfully.")

        st.audio(audio)

        st.download_button(
            "Download Recording",
            data=audio.getvalue(),
            file_name=(
                f"interview_{datetime.now():%Y%m%d_%H%M%S}.wav"
            ),
            mime="audio/wav"
        )

        st.session_state.last_audio = audio.getvalue()

        st.caption(
            "Audio capture is working. Connect a speech-to-text "
            "service to obtain a transcript."
        )

    return question, audio
