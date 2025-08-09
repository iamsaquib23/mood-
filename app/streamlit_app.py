import os
from typing import List

import streamlit as st

from app.agent.content_generator import TeachingPlan, generate_teaching_content
from app.ppt.ppt_builder import build_powerpoint


st.set_page_config(page_title="Surgery Teaching Deck Generator", page_icon="🩺", layout="wide")

st.title("🩺 General Surgery Teaching Deck Generator")

with st.sidebar:
    st.header("Settings")
    presenter_name = st.text_input("Presenter name", placeholder="Prof. Jane Doe")
    affiliation = st.text_input("Affiliation", placeholder="Dept. of General Surgery")

    st.subheader("LLM Provider")
    openai_key_input = st.text_input("OpenAI API Key", type="password", help="Optional. If omitted, deterministic fallback content is used.")
    if openai_key_input:
        os.environ["OPENAI_API_KEY"] = openai_key_input

    openai_model = st.text_input("Model (OpenAI)", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

    st.subheader("Output")
    preferred_slide_count = st.number_input("Preferred total slides", min_value=8, max_value=80, value=24, step=1)

st.subheader("Session Details")
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("Topic", placeholder="Acute cholecystitis")
    audience_level = st.selectbox("Audience level", ["MBBS/Medical students", "Interns", "Residents (Junior)", "Residents (Senior)", "Fellows"], index=2)
with col2:
    duration_minutes = st.number_input("Duration (minutes)", min_value=15, max_value=180, value=45, step=5)
    objectives_raw = st.text_area("Learning objectives (one per line)", value="Define the condition and epidemiology\nOutline diagnostic approach\nDiscuss operative and non-operative management\nRecognize complications and postoperative care\nApply guideline-based decision-making")

st.subheader("Sections to include")
sections = [
    "Introduction",
    "Relevant anatomy",
    "Pathophysiology",
    "Clinical assessment",
    "Investigations",
    "Imaging",
    "Management",
    "Operative steps",
    "Complications",
    "Postoperative care",
    "Case vignette",
    "Key takeaways",
    "MCQs",
]
section_cols = st.columns(3)
selected_sections: List[str] = []
for i, section in enumerate(sections):
    with section_cols[i % 3]:
        if st.checkbox(section, value=True):
            selected_sections.append(section)

if st.button("Generate Deck", type="primary"):
    with st.spinner("Generating content..."):
        learning_objectives = [line.strip() for line in objectives_raw.splitlines() if line.strip()]
        plan = TeachingPlan(
            topic=topic or "General Surgery Topic",
            audience_level=audience_level,
            duration_minutes=int(duration_minutes),
            learning_objectives=learning_objectives,
            include_sections=selected_sections,
            slide_count_hint=int(preferred_slide_count),
            model=openai_model.strip() if openai_model else None,
        )
        content = generate_teaching_content(plan)

    st.success("Content generated")

    st.subheader("Outline Preview")
    st.write(f"**Title**: {content.get('title')}")
    for idx, slide in enumerate(content.get("slides", []), start=1):
        st.markdown(f"**{idx}. {slide.get('title','Untitled')}**")
        for b in slide.get("bullets", [])[:5]:
            st.markdown(f"- {b}")

    with st.spinner("Building PowerPoint..."):
        ppt_path = build_powerpoint(
            content,
            presenter_name=presenter_name.strip() or None,
            affiliation=affiliation.strip() or None,
        )

    st.success("PPTX ready")
    with open(ppt_path, "rb") as f:
        st.download_button(
            label="Download PPTX",
            data=f,
            file_name=os.path.basename(ppt_path),
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

st.divider()

st.caption(
    "Note: This tool assists with drafting teaching material. Review for accuracy, add institutional policies, and complete citations before use in teaching.")