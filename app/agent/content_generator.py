import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass
class TeachingPlan:
    topic: str
    audience_level: str
    duration_minutes: int
    learning_objectives: List[str]
    include_sections: List[str]
    slide_count_hint: Optional[int] = None
    model: Optional[str] = None


class OpenAIClient:
    def __init__(self, api_key: Optional[str]) -> None:
        self.api_key = api_key
        self.api_base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate_json(self, system_prompt: str, user_prompt: str, model: Optional[str] = None, max_tokens: int = 2000, temperature: float = 0.4) -> Dict[str, Any]:
        if not self.is_available():
            raise RuntimeError("OpenAI API key not set")
        effective_model = model or self.model
        url = f"{self.api_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": effective_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        data = response.json()
        raw = data["choices"][0]["message"]["content"].strip()
        return _coerce_json_from_text(raw)


def _coerce_json_from_text(text: str) -> Dict[str, Any]:
    # Extract JSON object from text that may include pre/postamble
    match = re.search(r"\{[\s\S]*\}", text)
    candidate = match.group(0) if match else text
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        # Last resort: try to fix common issues
        candidate = candidate.replace("\n", " ")
        candidate = re.sub(r",\s*\}", "}", candidate)
        return json.loads(candidate)


def build_system_prompt() -> str:
    return (
        "You are an assistant for a Professor of General Surgery. "
        "You design evidence-informed teaching slide content that is accurate, concise, and clinically practical. "
        "Always include clear learning objectives, structured slides, suggested figures or diagrams, and speaker notes when appropriate. "
        "Use current surgical guidelines and best practices, but DO NOT fabricate citations. Provide placeholders like '[Add citation: ...]'. "
        "Output strictly a compact JSON object matching the requested schema."
    )


def build_user_prompt(plan: TeachingPlan) -> str:
    sections_csv = ", ".join(plan.include_sections)
    objectives = "\n".join(f"- {o}" for o in plan.learning_objectives)
    slide_hint = f"Preferred total slides: {plan.slide_count_hint}." if plan.slide_count_hint else ""
    return (
        f"Topic: {plan.topic}\n"
        f"Audience level: {plan.audience_level}\n"
        f"Duration (minutes): {plan.duration_minutes}\n"
        f"Learning objectives:\n{objectives}\n"
        f"Include sections: {sections_csv}\n"
        f"{slide_hint}\n\n"
        "Return JSON with keys: 'title', 'slides' (array), 'references' (array).\n"
        "Each slide item: { 'title': str, 'bullets': [str], 'speakerNotes': str (optional), 'figureSuggestion': str (optional) }.\n"
        "Avoid markdown; keep text plain. Limit bullets per slide to 5."
    )


def generate_teaching_content(plan: TeachingPlan) -> Dict[str, Any]:
    client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(plan)

    if client.is_available():
        try:
            result = client.generate_json(system_prompt, user_prompt, model=plan.model)
            return _ensure_minimum_schema(result, plan)
        except Exception:
            # Fall back if API errors
            pass

    # Deterministic fallback
    return _fallback_content(plan)


def _ensure_minimum_schema(data: Dict[str, Any], plan: TeachingPlan) -> Dict[str, Any]:
    title = data.get("title") or f"{plan.topic} — General Surgery Teaching Session"
    slides = data.get("slides") or []
    references = data.get("references") or []

    # Basic normalization
    normalized_slides: List[Dict[str, Any]] = []
    for slide in slides:
        normalized_slides.append({
            "title": str(slide.get("title", "Untitled"))[:120],
            "bullets": [str(b) for b in (slide.get("bullets") or [])][:5],
            "speakerNotes": str(slide.get("speakerNotes", ""))[:2000],
            "figureSuggestion": str(slide.get("figureSuggestion", ""))[:500],
        })

    if not normalized_slides:
        return _fallback_content(plan)

    return {
        "title": title,
        "slides": normalized_slides,
        "references": [str(r) for r in references][:12],
    }


def _fallback_content(plan: TeachingPlan) -> Dict[str, Any]:
    default_sections = plan.include_sections or [
        "Introduction",
        "Relevant anatomy",
        "Pathophysiology",
        "Clinical assessment",
        "Investigations",
        "Management",
        "Operative steps",
        "Complications",
        "Postoperative care",
        "Key takeaways",
        "MCQs",
        "References",
    ]
    title = f"{plan.topic} — Teaching Session"

    slides: List[Dict[str, Any]] = []
    slides.append({
        "title": f"{plan.topic}: Objectives",
        "bullets": plan.learning_objectives[:5],
        "speakerNotes": "Review objectives with learners and gauge baseline knowledge.",
        "figureSuggestion": "Simple objectives list layout",
    })

    for section in default_sections:
        if section.lower() == "references":
            continue
        slides.append({
            "title": f"{plan.topic}: {section}",
            "bullets": [
                "Define scope and key terms",
                "Summarize most important clinical points",
                "Emphasize decision-making and safety",
                "Include pearls/pitfalls",
                "Point to evidence or guidelines",
            ],
            "speakerNotes": f"Provide concise teaching points for {section.lower()}.",
            "figureSuggestion": "Box diagram or flowchart where relevant",
        })

    slides.append({
        "title": "Key Takeaways",
        "bullets": [
            "Prioritize early recognition of red flags",
            "Standardize perioperative pathways",
            "Know indications and contraindications",
            "Prevent and manage complications",
            "Local guidelines and resources",
        ],
        "speakerNotes": "Close with actionable summary and resources.",
        "figureSuggestion": "Summary icons",
    })

    references = [
        "[Add citation: Relevant surgical society guideline, year]",
        "[Add citation: Standard textbook chapter]",
        "[Add citation: Landmark RCT or meta-analysis]",
    ]

    return {"title": title, "slides": slides, "references": references}


__all__ = [
    "TeachingPlan",
    "generate_teaching_content",
]