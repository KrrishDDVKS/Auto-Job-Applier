
import re
from docx import Document

def extract_resume_data(file_path):

    # Read text from DOCX
    doc = Document(file_path)

    text = "\n".join(
        paragraph.text for paragraph in doc.paragraphs
    )

    # Also extract text from tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text += "\n" + cell.text

    # Extract email
    email_match = re.search(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        text
    )
    email = email_match.group(0) if email_match else ""

    # Extract phone number
    phone_match = re.search(
        r'(?<!\d)(?:\+1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}(?!\d)',
        text
    )
    phone = phone_match.group(0) if phone_match else ""

    # # Extract ZIP code (US)
    # zip_match = re.search(
    #     r'\b\d{5}(?:-\d{4})?\b',
    #     text
    # )
    # zip_code = zip_match.group(0) if zip_match else ""

    # # Extract US state
    # states = {
    #     "Alabama": "AL", "Alaska": "AK",
    #     "Arizona": "AZ", "Arkansas": "AR",
    #     "California": "CA", "Colorado": "CO",
    #     "Connecticut": "CT", "Delaware": "DE",
    #     "Florida": "FL", "Georgia": "GA",
    #     "Hawaii": "HI", "Idaho": "ID",
    #     "Illinois": "IL", "Indiana": "IN",
    #     "Iowa": "IA", "Kansas": "KS",
    #     "Kentucky": "KY", "Louisiana": "LA",
    #     "Maine": "ME", "Maryland": "MD",
    #     "Massachusetts": "MA", "Michigan": "MI",
    #     "Minnesota": "MN", "Mississippi": "MS",
    #     "Missouri": "MO", "Montana": "MT",
    #     "Nebraska": "NE", "Nevada": "NV",
    #     "New Hampshire": "NH", "New Jersey": "NJ",
    #     "New Mexico": "NM", "New York": "NY",
    #     "North Carolina": "NC", "North Dakota": "ND",
    #     "Ohio": "OH", "Oklahoma": "OK",
    #     "Oregon": "OR", "Pennsylvania": "PA",
    #     "Rhode Island": "RI", "South Carolina": "SC",
    #     "South Dakota": "SD", "Tennessee": "TN",
    #     "Texas": "TX", "Utah": "UT",
    #     "Vermont": "VT", "Virginia": "VA",
    #     "Washington": "WA", "West Virginia": "WV",
    #     "Wisconsin": "WI", "Wyoming": "WY"
    # }

    # state = ""

    # for name, abbreviation in states.items():
    #     pattern = rf'\b(?:{re.escape(name)}|{abbreviation})\b'
    #     if re.search(pattern, text, re.IGNORECASE):
    #         state = name
    #         break

    # Extract name (assumes first non-empty line is the name)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    full_name = lines[0] if lines else ""

    # Remove common titles
    full_name = re.sub(
        r'^(Mr\.|Mrs\.|Ms\.|Dr\.)\s+',
        '',
        full_name,
        flags=re.IGNORECASE
    )

    name_parts = full_name.split()

    first_name = name_parts[0] if name_parts else ""
    last_name = name_parts[-1] if len(name_parts) > 1 else ""

    # Create JSON
    result = {
        "First name": first_name,
        "Last name": last_name,
        "email": email,
        "Phone": phone,
        "State": "Georgia",  # Placeholder for state extraction
        "Zip": "30060"  # Placeholder for ZIP code extraction
    }

    return result