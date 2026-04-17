import pdfplumber
import pandas as pd

def extract_colleges_from_pdf(pdf_file):
    colleges = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                lines = text.split("\n")

                for line in lines:
                    # Basic filter (customize based on your PDF format)
                    if "College" in line or "Engineering" in line:
                        colleges.append(line.strip())

    # Remove duplicates
    colleges = list(set(colleges))

    return pd.DataFrame(colleges, columns=["College Name"])
