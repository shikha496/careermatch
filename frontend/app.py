
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from styles import apply_theme, page_header, section_title

from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.resume_report import render_resume_report
from components.audio_recorder import render_audio_recorder

from components.visualizer import (
    performance_radar,
    category_donut
)

from api_client import analyze_resume as request_ai_resume_analysis
from api_client import generate_questions, interview_chat
from services.ats_analyzer import analyze_ats
from services.interview_evaluator import evaluate_transcript
from services.parser import ResumeParser
from services.star_enhancer import generate_star_answer


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Career Match AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

DEFAULTS = {
    "theme": "Light",
    "page": "Career Match AI",
    "resume_text": "",
    "resume_filename": "",
    "job_description": "",
    "analysis": None,
    "ai_analysis": None,
    "star_result": None,
    "interview_result": None,
    "interview_history": [],
    "generated_questions": None,
    "coach_response": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# THEME AND SIDEBAR
# --------------------------------------------------

st.markdown(apply_theme(st.session_state.theme), unsafe_allow_html=True)

selected_page = render_sidebar()

if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

dark = st.session_state.theme == "Dark"


# --------------------------------------------------
# CAREER MATCH AI
# --------------------------------------------------

if st.session_state.page == "Career Match AI":

    st.markdown(
        page_header(
            "Career Match AI",
            "Intelligent resume analysis and job compatibility."
        ),
        unsafe_allow_html=True
    )

    # Upload and job description

    left, right = st.columns(
        [1, 1],
        gap="large"
    )

    with left:

        with st.container(border=True):

            st.markdown(section_title("📄 Upload Your Resume"), unsafe_allow_html=True)

            uploaded = st.file_uploader(
                "Upload PDF, DOCX or TXT",
                type=["pdf", "docx", "txt"],
                key="resume_upload"
            )

            if uploaded:

                if st.button(
                    "Extract Resume",
                    use_container_width=True
                ):

                    try:

                        with st.spinner(
                            "Extracting resume content..."
                        ):

                            resume_text = ResumeParser.parse(
                                uploaded.getvalue(), uploaded.name
                            )
                            parsed = {
                                "text": resume_text,
                                "filename": uploaded.name,
                                "words": len(resume_text.split()),
                            }

                            st.session_state.resume_text = parsed["text"]
                            st.session_state.resume_filename = parsed["filename"]
                            st.session_state.analysis = None
                            st.session_state.ai_analysis = None

                        st.success(
                            f"Extracted {parsed['words']} words."
                        )

                    except Exception as error:
                        st.error(str(error))

            if st.session_state.resume_text:

                st.success(
                    f"Loaded: {st.session_state.resume_filename}"
                )

                st.caption(
                    f"{len(st.session_state.resume_text.split())} words extracted"
                )

                with st.expander("Preview extracted resume"):
                    st.text(
                        st.session_state.resume_text[:4000]
                    )

    with right:

        with st.container(border=True):

            st.markdown(section_title("💼 Target Job Description"), unsafe_allow_html=True)

            jd = st.text_area(
                "Paste the complete job description",
                value=st.session_state.job_description,
                height=230,
                placeholder=(
                    "Paste responsibilities, qualifications, "
                    "technical skills and experience requirements..."
                )
            )

            st.session_state.job_description = jd

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:

        if st.button(
            "🔍 Analyze Resume & Generate Report",
            use_container_width=True
        ):

            if not st.session_state.resume_text:
                st.error("Please upload and extract your resume.")

            elif not st.session_state.job_description.strip():
                st.error("Please enter a job description.")

            else:

                try:

                    with st.spinner(
                        "Analyzing skills, requirements and evidence..."
                    ):

                        result = analyze_ats(
                            st.session_state.resume_text,
                            st.session_state.job_description
                        )

                        st.session_state.analysis = result
                        try:
                            st.session_state.ai_analysis = request_ai_resume_analysis(
                                st.session_state.resume_text.encode("utf-8"),
                                "resume.txt",
                                st.session_state.job_description,
                            )
                        except Exception as ai_error:
                            st.session_state.ai_analysis = {
                                "status": "unavailable",
                                "error": str(ai_error),
                            }

                    st.success("Analysis completed.")
                    st.rerun()

                except Exception as error:
                    st.error(f"Analysis failed: {error}")

    with col2:

        if st.button(
            "Clear Analysis",
            use_container_width=True
        ):

            st.session_state.analysis = None
            st.session_state.ai_analysis = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    render_dashboard(
        st.session_state.analysis,
        dark,
        st.session_state.ai_analysis,
    )


# --------------------------------------------------
# RESUME REPORT
# --------------------------------------------------

elif st.session_state.page == "Resume Report":

    st.markdown(
        page_header(
            "Resume Report",
            "Detailed ATS compatibility, skill gaps and evidence."
        ),
        unsafe_allow_html=True
    )

    render_resume_report(
        st.session_state.analysis,
        dark,
        st.session_state.ai_analysis,
    )


# --------------------------------------------------
# INTERVIEW IQ
# --------------------------------------------------

elif st.session_state.page == "Interview IQ":

    st.markdown(
        page_header(
            "Interview IQ",
            "Practice interview responses and evaluate your answers."
        ),
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs([
        "Interview Practice",
        "Performance Analytics"
    ])

    with tab1:

        left, right = st.columns(
            [1.2, 0.8],
            gap="large"
        )

        with left:

            with st.container(border=True):

                question, audio = render_audio_recorder()

        with right:

            with st.container(border=True):

                st.markdown(section_title("Interview Preparation"), unsafe_allow_html=True)

                role = st.text_input(
                    "Target role",
                    value="Backend Developer",
                    key="interview_role",
                )

                category = st.selectbox(
                    "Interview Type",
                    [
                        "Technical",
                        "HR",
                        "Behavioral",
                        "Managerial"
                    ]
                )

                difficulty = st.select_slider(
                    "Difficulty",
                    ["Beginner", "Intermediate", "Advanced"]
                )

                st.markdown("### Preparation Checklist")

                st.checkbox("Research the company")
                st.checkbox("Prepare project examples")
                st.checkbox("Practice STAR answers")
                st.checkbox("Prepare questions")

                st.caption(
                    f"{category} interview | {difficulty}"
                )

                if st.button("Generate 5 AI questions"):
                    try:
                        with st.spinner("Generating interview questions..."):
                            generated = generate_questions(role, category, difficulty)
                        st.session_state.generated_questions = generated
                    except Exception as error:
                        st.error("Question generation failed: " + str(error))

                if st.session_state.generated_questions:
                    generated = st.session_state.generated_questions
                    st.caption("Generated with " + generated["provider"])
                    st.text(generated["questions"])

        st.divider()

        st.markdown(section_title("Evaluate Interview Transcript"), unsafe_allow_html=True)

        transcript = st.text_area(
            "Paste your transcribed interview answer",
            height=180,
            placeholder="Paste the actual transcript here..."
        )

        if st.button(
            "Evaluate Interview Answer",
            use_container_width=True
        ):

            if not transcript.strip():

                st.warning(
                    "Enter an interview transcript first."
                )

            else:

                try:

                    result = evaluate_transcript(transcript)

                    st.session_state.interview_result = result

                    st.session_state.interview_history.append(
                        result
                    )

                    st.success("Transcript evaluation completed.")

                except ValueError as error:
                    st.error(str(error))

        result = st.session_state.interview_result

        if result:

            st.markdown("### Interview Feedback")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Heuristic Score",
                f'{result["overall_score"]}/100'
            )

            c2.metric(
                "Word Count",
                result["word_count"]
            )

            c3.metric(
                "Action Signals",
                result["action_signals"]
            )

            for feedback in result["feedback"]:
                st.info(feedback)

            st.caption(result["disclaimer"])

        with st.expander("Ask the AI interview coach"):
            coach_prompt = st.text_area(
                "What would you like help with?",
                placeholder="Ask for interview preparation or feedback on an answer.",
                key="coach_prompt",
            )
            if st.button("Ask coach"):
                if not coach_prompt.strip():
                    st.warning("Enter a question for the coach.")
                else:
                    try:
                        with st.spinner("Getting coaching advice..."):
                            st.session_state.coach_response = interview_chat(
                                coach_prompt,
                                role=st.session_state.get("interview_role"),
                            )
                    except Exception as error:
                        st.error("AI coach unavailable: " + str(error))
            if st.session_state.coach_response:
                st.caption(
                    "Response from "
                    + st.session_state.coach_response["provider"]
                )
                st.write(st.session_state.coach_response["answer"])

    with tab2:

        history = st.session_state.interview_history

        if history:

            latest = history[-1]

            st.metric(
                "Latest heuristic score",
                f'{latest["overall_score"]}/100'
            )

            scores = {
                "Answer Structure": latest["overall_score"],
                "Action Signals": min(
                    100, latest["action_signals"] * 20
                ),
                "Result Signals": min(
                    100, latest["result_signals"] * 25
                )
            }

            st.plotly_chart(
                performance_radar(scores, dark),
                use_container_width=True
            )

            st.caption(
                "These are transcript-based heuristic indicators, "
                "not validated communication or confidence scores."
            )

        else:

            st.info(
                "Complete an interview transcript evaluation "
                "to see your analytics."
            )


# --------------------------------------------------
# AI STAR ENHANCER
# --------------------------------------------------

elif st.session_state.page == "AI STAR Enhancer":

    st.markdown(
        page_header(
            "AI STAR Enhancer",
            "Structure real professional experiences into interview answers."
        ),
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown(section_title("✨ STAR Answer Builder"), unsafe_allow_html=True)

        situation = st.text_area(
            "1. Situation",
            placeholder="What was the background or challenge?",
            height=100
        )

        task = st.text_area(
            "2. Task",
            placeholder="What were you responsible for?",
            height=100
        )

        action = st.text_area(
            "3. Action",
            placeholder="What did you personally do?",
            height=100
        )

        result_text = st.text_area(
            "4. Result",
            placeholder="What happened? Include real measurable outcomes.",
            height=100
        )

        if st.button(
            "✨ Generate STAR Answer",
            use_container_width=True
        ):

            try:

                star = generate_star_answer(
                    situation,
                    task,
                    action,
                    result_text
                )

                st.session_state.star_result = star

            except ValueError as error:

                st.warning(str(error))

    if st.session_state.star_result:

        st.markdown("### Your STAR Answer")

        answer = st.session_state.star_result["answer"]

        st.text_area(
            "Generated answer",
            value=answer,
            height=250
        )

        st.caption(
            f"Word count: {st.session_state.star_result['word_count']}"
        )

        st.download_button(
            "Download STAR Answer",
            data=answer,
            file_name="star_answer.txt",
            mime="text/plain"
        )

        st.info(
            "This version structures your original content. "
            "Connect an LLM for intelligent rewriting and "
            "personalized interview feedback."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#94A3B8;font-size:11px">
        Career Match AI & Interview IQ |
        Professional Career Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)
