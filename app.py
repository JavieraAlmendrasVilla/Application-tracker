from langchain_ollama import ChatOllama
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import gradio as gr
import csv
import os
import time
import re

CSV_FILE = "applications.csv"

# ---------------- LLM Setup ----------------
llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0.1,
    top_k=10,
    top_p=0.1,
)

# ---------------- Define Structured Parser ----------------
schemas = [
    ResponseSchema(name="position", description="Position / Job Title"),
    ResponseSchema(name="company", description="Company name"),
    ResponseSchema(name="company_summary", description="Short summary of the company"),
    ResponseSchema(name="job_description_summary", description="Summary of the position only"),
    ResponseSchema(name="technical_skills", description="List of technical skills, comma separated"),
    ResponseSchema(name="soft_skills", description="List of soft skills, comma separated"),
    ResponseSchema(name="education", description="Education requirements")
]

parser = StructuredOutputParser.from_response_schemas(schemas)
format_instructions = parser.get_format_instructions()


# ---------------- Helper to Clean Skills ----------------
def clean_skills(skills_str):
    if isinstance(skills_str, list):
        return skills_str
    return [s.strip() for s in skills_str.split(",") if s.strip()]


# ---------------- Extract Job Data with Retry ----------------
def extract_job_data(text, max_retries=3):
    prompt = f"""
Extract the following from this job description. {format_instructions}

Job Description Text:
{text}

Instructions: 
- Always create the expected_keys "position", "company", "company_summary", "job_description_summary", 
"technical_skills", "soft_skills", "education" even if they are empty.
- Provide a 'company_summary' describing the company briefly.
- Provide 'job_description_summary' describing the position only.
- Separate skills into 'technical_skills' and 'soft_skills'.
- Technical skills are tools or technologies required for the job, like programming languages, frameworks, etc.
- Soft skills are interpersonal skills like communication, teamwork, etc.
- Make sure skill lists are valid JSON arrays (lists), not strings.
"""

    # Expected keys with safe defaults
    expected_keys = {
        "position": "",
        "company": "",
        "company_summary": "",
        "job_description_summary": "",
        "technical_skills": [],
        "soft_skills": [],
        "education": ""
    }

    for attempt in range(max_retries):
        result = llm.invoke(prompt)
        print("Raw LLM output:", result.content)

        try:
            clean_json = re.sub(r',(\s*[}\]])', r'\1', result.content)
            parsed = parser.parse(clean_json)

            # ✅ Merge with defaults so missing keys are empty
            data = {**expected_keys, **parsed}

            # Clean up lists
            data["technical_skills"] = clean_skills(data.get("technical_skills", []))
            data["soft_skills"] = clean_skills(data.get("soft_skills", []))

            return data

        except Exception as e:
            print(f"Parsing failed on attempt {attempt + 1}: {e}")
            time.sleep(0.5)

    # If all attempts fail, return empty structure
    return expected_keys


# ---------------- Write to CSV ----------------
def write_to_csv(data):
    file_exists = os.path.isfile(CSV_FILE)

    # Convert lists to strings
    tech_skills_str = ", ".join(data.get("technical_skills", [])) or ""
    soft_skills_str = ", ".join(data.get("soft_skills", [])) or ""

    # Clean fields
    row = [
        (data.get("position") or "").replace("\n", " ").strip(),
        (data.get("company") or "").replace("\n", " ").strip(),
        (data.get("company_summary") or "").replace("\n", " ").strip(),
        (data.get("job_description_summary") or "").replace("\n", " ").strip(),
        tech_skills_str,
        soft_skills_str,
        (data.get("education") or "").replace("\n", " ").strip()
    ]

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "Position",
                "Company",
                "Company Summary",
                "Job Description Summary",
                "Technical Skills",
                "Soft Skills",
                "Education"
            ])
        writer.writerow(row)


# ---------------- Full Pipeline ----------------
def process_job_text(text):
    job_data = extract_job_data(text)
    write_to_csv(job_data)
    return f"Added job posting for '{job_data.get('position')}' at '{job_data.get('company')}' to CSV."


# ---------------- Gradio Interface ----------------
iface = gr.Interface(
    fn=process_job_text,
    inputs=gr.Textbox(lines=15, placeholder="Paste the job description here..."),
    outputs=gr.Textbox(label="Status"),
    title="Job Description Extractor",
    description="Paste a job description to extract position, company, company summary, job description summary, "
                "technical skills, soft skills, and education, then automatically add it to a CSV file."
)

iface.launch()
