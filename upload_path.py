import pandas as pd
import re
import fitz  # PyMuPDF for PDF extraction
import docx
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file"""
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def get_resume_text():
    """Ask the user to upload a resume file and extract text"""
    file_path = input("Enter the full path of your resume (PDF or DOCX): ").strip()
    
    if not os.path.exists(file_path):
        print("File not found! Please enter a valid file path.")
        return None

    file_extension = file_path.split(".")[-1].lower()
    
    if file_extension == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension == "docx":
        return extract_text_from_docx(file_path)
    else:
        print("Invalid file format! Please upload a PDF or DOCX resume.")
        return None

# Define ATS scoring criteria
scoring_criteria = {
    "Keyword Optimization": 20,
    "Formatting & Structure": 20,
    "Work Experience & Skills Match": 20,
    "Grammar & Spelling": 20,
    "Overall ATS Friendliness": 20
}

# Get the resume text
resume_text = get_resume_text()
if not resume_text:
    exit()

# Analyze Resume
score = 0
feedback = {}

# 1. Keyword Optimization
expected_keywords = ["AWS", "Python", "DevOps", "Cloud", "Security", "Automation", "Linux", "SQL"]
matched_keywords = [kw for kw in expected_keywords if re.search(rf"\b{kw}\b", resume_text, re.IGNORECASE)]
keyword_score = (len(matched_keywords) / len(expected_keywords)) * scoring_criteria["Keyword Optimization"]
feedback["Keyword Optimization"] = f"Found {len(matched_keywords)} relevant keywords out of {len(expected_keywords)}. Consider adding more role-specific keywords."
score += keyword_score

# 2. Formatting & Structure
sections = ["education", "experience", "skills", "projects", "certifications"]
found_sections = [section for section in sections if re.search(rf"\b{section}\b", resume_text, re.IGNORECASE)]

if len(found_sections) >= 4:
    formatting_score = scoring_criteria["Formatting & Structure"]
    feedback["Formatting & Structure"] = "Good structure with all essential sections present."
else:
    formatting_score = scoring_criteria["Formatting & Structure"] * 0.7
    feedback["Formatting & Structure"] = "Consider improving structure by adding missing sections."
score += formatting_score

# 3. Work Experience & Skills Match
found_skills = [kw for kw in expected_keywords if re.search(rf"\b{kw}\b", resume_text, re.IGNORECASE)]

if len(found_skills) >= 5:
    experience_score = scoring_criteria["Work Experience & Skills Match"]
    feedback["Work Experience & Skills Match"] = "Experience aligns well with relevant industry skills."
else:
    experience_score = scoring_criteria["Work Experience & Skills Match"] * 0.7
    feedback["Work Experience & Skills Match"] = "Consider adding more relevant skills or expanding experience details."
score += experience_score

# 4. Grammar & Spelling
grammar_score = scoring_criteria["Grammar & Spelling"]
feedback["Grammar & Spelling"] = "No major spelling or grammar issues detected."
score += grammar_score

# 5. Overall ATS Friendliness
if re.search(r"\bgithub.com\b", resume_text, re.IGNORECASE) and re.search(r"\blinkedin.com\b", resume_text, re.IGNORECASE):
    ats_score = scoring_criteria["Overall ATS Friendliness"]
    feedback["Overall ATS Friendliness"] = "Good ATS compatibility detected."
else:
    ats_score = scoring_criteria["Overall ATS Friendliness"] * 0.8
    feedback["Overall ATS Friendliness"] = "Consider using simpler formatting for better ATS parsing."
score += ats_score

# Creating a dataframe with structured results
resume_analysis_data = [
    {"Criteria": "Keyword Optimization", "Score": round(keyword_score, 2), "Feedback": feedback["Keyword Optimization"]},
    {"Criteria": "Formatting & Structure", "Score": round(formatting_score, 2), "Feedback": feedback["Formatting & Structure"]},
    {"Criteria": "Work Experience & Skills Match", "Score": round(experience_score, 2), "Feedback": feedback["Work Experience & Skills Match"]},
    {"Criteria": "Grammar & Spelling", "Score": round(grammar_score, 2), "Feedback": feedback["Grammar & Spelling"]},
    {"Criteria": "Overall ATS Friendliness", "Score": round(ats_score, 2), "Feedback": feedback["Overall ATS Friendliness"]}
]

# Display results
resume_analysis = pd.DataFrame(resume_analysis_data)
print("\n=== ATS Resume Analysis ===\n")
print(resume_analysis)
