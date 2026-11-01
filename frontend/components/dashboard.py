
import streamlit as st
from styles import section_title
from components.visualizer import score_breakdown


def render_dashboard(result=None, dark=False, ai_analysis=None):

    st.title("📊 Dashboard")

    st.markdown(
        section_title("Resume match overview"),
        unsafe_allow_html=True
    )

    if result is None:
        st.info("Upload a resume and job description to see the analysis.")
        return

    score = result.get("score")
    scores = result.get("scores", {})
    first, second, third = st.columns(3)
    first.metric("ATS match", f"{score}%" if score is not None else "Not scored")
    second.metric("Matched skills", len(result.get("matched_skills", [])))
    third.metric("Missing skills", len(result.get("missing_skills", [])))
    st.caption(result.get("explanation", "Scores are heuristic indicators."))
    if ai_analysis:
        if ai_analysis.get("status") == "success":
            analysis = ai_analysis["analysis"]
            provider = ai_analysis.get("provider", "AI").title()
            st.markdown("### AI resume analysis")
            st.caption(
                f"Structured analysis from {provider}. See Resume Report "
                "for the full analysis and quoted evidence."
            )
            st.write(analysis["overall_assessment"])
            with st.expander("AI strengths, gaps, and recommendations"):
                strengths, gaps = st.columns(2)
                with strengths:
                    st.markdown("**Strengths**")
                    for item in analysis["strengths"]:
                        st.markdown("- " + item)
                with gaps:
                    st.markdown("**Gaps**")
                    for item in analysis["gaps"]:
                        st.markdown("- " + item)
                st.markdown("**Recommendations**")
                for item in analysis["recommendations"]:
                    st.markdown("- " + item)
        elif ai_analysis.get("status") == "unavailable":
            st.warning(
                "AI analysis unavailable: "
                + ai_analysis.get("error", "Provider unavailable.")
            )

    st.plotly_chart(
        score_breakdown(scores, dark),
        use_container_width=True,
        config={"displayModeBar": False},
    )
