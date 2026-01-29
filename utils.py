# utils.py (Corrected)
import pandas as pd
import json
from docx import Document
import io
from gtts import gTTS, gTTSError # Import gTTSError

def create_txt(text):
    """Creates a text file in memory."""
    return io.StringIO(text)

def create_json(source_file, text):
    """Creates a JSON file in memory."""
    data = {"source_file": source_file, "extracted_text": text}
    return io.StringIO(json.dumps(data, indent=4))

def create_csv(source_file, text):
    """Creates a CSV file in memory."""
    df = pd.DataFrame([{"source_file": source_file, "extracted_text": text}])
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

def create_excel(source_file, text):
    """Creates an Excel file in memory."""
    output = io.BytesIO()
    df = pd.DataFrame([{"source_file": source_file, "extracted_text": text}])
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Extraction')
    output.seek(0)
    return output

def create_docx(text):
    """Creates a DOCX file in memory."""
    document = Document()
    document.add_paragraph(text)
    output = io.BytesIO()
    document.save(output)
    output.seek(0)
    return output

def create_mp3(text):
    """Creates an MP3 file in memory, handling connection errors."""
    if not text.strip():
        return None
    
    try:
        output = io.BytesIO()
        tts = gTTS(text=text, lang="en")
        tts.write_to_fp(output)
        output.seek(0)
        return output
    # except gTTSError:
    #     # If there's a connection error, return None
    #     print("gTTS connection failed. Skipping MP3 generation.")
    #     return None
    except Exception as e:
        print("MP3 generation error:", e)
        return None