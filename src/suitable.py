from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from typing import List
import ollama
import re
from docx import Document

class Skill(BaseModel):
    name: str
    aliases: List[str] = Field(default_factory=list)


class SkillsResponse(BaseModel):
    technical_skills: List[Skill]
    tools_and_frameworks: List[Skill]
    methodologies: List[Skill]
    soft_skills: List[Skill]



def generate_skills(job_title: str):

    prompt = f"""
    You are an expert technical recruiter.

    Generate the most relevant skills for this job title:

    Job Title: {job_title}

    Categorize skills into:
    1. Technical skills
    2. Tools and frameworks
    3. Methodologies

    Requirements:
    - Generate 20-30 relevant skills.
    - Include common abbreviations as aliases.
    - Avoid duplicate skills.
    - Focus on industry-relevant skills.
    - Return structured output matching the schema.
    """

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=SkillsResponse.model_json_schema()
    )

    skills = SkillsResponse.model_validate_json(
        response["message"]["content"]
    )

    return skills


def extract_job_description(driver):
    # Get complete rendered HTML
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    # Remove unnecessary HTML elements
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    # Extract readable text
    return soup.get_text(separator="\n", strip=True)


def extract_resume_text(file_path):
           
        doc = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )


def extract_skills(text, skills):

    found_skills = []

    for skill in skills:

        patterns = [
            skill.name,
            *skill.aliases
        ]

        for pattern in patterns:

            regex = (
                r"(?<!\w)"
                + re.escape(pattern).replace(r"\ ", r"\s+")
                + r"(?!\w)"
            )

            if re.search(
                regex,
                text,
                re.IGNORECASE
            ):

                found_skills.append(skill.name)
                break

    return list(set(found_skills))


def calculate_match(jd_skills, resume_skills):

    jd_set = set(jd_skills)
    resume_set = set(resume_skills)

    matched = jd_set.intersection(resume_set)

    missing = jd_set - resume_set

    extra = resume_set - jd_set

    if not jd_set:
        score = 0
    else:
        score = (
            len(matched) / len(jd_set)
        ) * 100

    return {
        "match_score": round(score, 2),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "additional_skills": sorted(extra)
    }