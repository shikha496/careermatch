
import streamlit as st

from styles import section_title, skill_chips
from components.visualizer import match_gauge


def render_resume_report(result, dark=False, ai_analysis=None):

    if result is None:
        st.info("Run resume analysis to see the detailed report.")
        return

    if ai_analysis:
        if ai_analysis.get("status") == "success":
            analysis = ai_analysis["analysis"]
            st.markdown("### AI resume analysis")
            st.caption(
                "Structured analysis from " + ai_analysis.get("provider", "AI")
                + "; verify all suggestions against your original resume."
            )
            st.write(analysis["overall_assessment"])
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
            if analysis["evidence"]:
                with st.expander("Quoted resume evidence"):
                    for item in analysis["evidence"]:
                        st.markdown("> " + item["quote"])
                        st.caption(item["relevance"])
        elif ai_analysis.get("status") == "unavailable":
            st.warning("AI analysis unavailable: " + ai_analysis.get("error", "Provider unavailable."))

    score = result["score"]

    left, right = st.columns(
        [0.8, 2.2],
        gap="medium"
    )

    # LEFT MATCH RATE PANEL
    with left:

        with st.container(border=True):

            st.markdown("### Match Rate")

            if score is not None:

                st.plotly_chart(
                    match_gauge(score, dark),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )

                if score >= 80:
                    st.success("Strong match")
                elif score >= 60:
                    st.warning("Moderate match")
                else:
                    st.error("Low match")

            else:
                st.warning("Score unavailable")

            st.divider()

            categories = [
                ("Skills", result["scores"]["skills"]),
                ("Experience", result["scores"]["experience"]),
                ("Education", result["scores"]["education"]),
                ("Keywords", result["scores"]["keywords"]),
                ("Structure", result["scores"]["structure"])
            ]

            for label, value in categories:

                if value is None:
                    st.caption(label + ": Not evaluated")
                    continue

                st.caption(label)

                st.progress(
                    max(0, min(100, value)) / 100
                )

                st.caption(f"{value}%")

    # RIGHT REPORT PANEL
    with right:

        tab1, tab2 = st.tabs(
            ["Resume Report", "Job Description Analysis"]
        )

        with tab1:

            st.markdown(
                """
                <div class="info-banner">
                    ⚡ <b>ATS-Specific Analysis</b><br>
                    Review your resume's searchable content,
                    required skills and experience evidence.
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### Searchability")

            for label, passed in result["checks"].items():

                icon = "🟢" if passed else "🔴"

                st.markdown(
                    f"{icon} **{label.title()}**"
                )

            st.divider()

            st.markdown("### Hard Skills & Technical Skills")

            skill_chips(
                result["matched_skills"],
                "matched"
            )

            st.markdown("### Missing Skills")

            skill_chips(
                result["missing_skills"],
                "missing"
            )

            st.divider()

            st.markdown("### Experience Analysis")

            st.info(result["experience_note"])

            st.markdown("### Education Analysis")

            st.info(result["education_note"])

            st.divider()

            st.markdown("### Evidence for Matched Skills")

            for skill, evidence_list in result["evidence"].items():

                with st.expander(skill):

                    for item in evidence_list:
                        st.write(
                            f'Line {item["line"]}: {item["text"]}'
                        )

            st.markdown("### Possible Related Evidence")

            st.caption(
                "These are semantic suggestions, not confirmed skill matches."
            )

            for skill, evidence_list in result[
                "possible_evidence"
            ].items():

                with st.expander(
                    f"Review evidence for {skill}"
                ):

                    for item in evidence_list:
                        st.write(item["text"])
                        st.caption(
                            f"Similarity: {item['similarity']:.3f} — "
                            "Manual verification required"
                        )

        with tab2:

            st.markdown("### Required Skills")

            skill_chips(
                result["required_skills"],
                "neutral"
            )

            st.markdown("### Skills Found in Resume")

            skill_chips(
                result["resume_skills"],
                "matched"
            )

            st.markdown("### Skills Not Detected")

            skill_chips(
                result["missing_skills"],
                "missing"
            )
