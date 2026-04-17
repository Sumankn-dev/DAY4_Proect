import requests
from bs4 import BeautifulSoup
import re

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    snippets = []
    for g in soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd"):
        snippets.append(g.get_text())

    return " ".join(snippets)


def enrich_college(college_name):
    data = {
        "College Name": college_name,
        "NAAC": "",
        "NBA": "",
        "NIRF": "",
        "Year": "",
        "Type": "",
        "Ownership": ""
    }

    text = google_search(college_name + " NAAC NBA NIRF ranking established type")

    # NAAC
    if "A++" in text:
        data["NAAC"] = "A++"
    elif "A+" in text:
        data["NAAC"] = "A+"
    elif "A" in text:
        data["NAAC"] = "A"

    # NBA
    if "NBA accredited" in text:
        data["NBA"] = "Yes"

    # NIRF
    match = re.search(r"NIRF.*?(\d{1,3})", text)
    if match:
        data["NIRF"] = match.group(1)

    # Year
    year_match = re.search(r"(established|founded)\s*(in)?\s*(\d{4})", text, re.I)
    if year_match:
        data["Year"] = year_match.group(3)

    # Type
    if "autonomous" in text.lower():
        data["Type"] = "Autonomous"
    elif "visvesvaraya technological university" in text.lower():
        data["Type"] = "VTU"
    elif "deemed to be university" in text.lower():
        data["Type"] = "University"

    # Ownership
    if "government" in text.lower():
        data["Ownership"] = "Government"
    elif "private" in text.lower():
        data["Ownership"] = "Private"

    return data
