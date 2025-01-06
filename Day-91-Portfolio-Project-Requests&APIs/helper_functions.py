from dotenv import load_dotenv
import os
import PyPDF2
from tkinter import filedialog
from elevenlabs.client import ElevenLabs

load_dotenv()
el_api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key = el_api_key,
)

def select_file():
    file_path = filedialog.askopenfilename(
        title = "Select a PDF File",
        filetypes = (("PDF files", "*pdf"), ("All files", "*.*"))
    )

    if file_path:
        return file_path
    else:
        print("No file selected")
        return None
    
def pdf_to_text(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def text_to_speech(text):
    response = client.text_to_speech.convert(
        voice_id = "pNInz6obpgDQGcFmaJgB",
        output_format = "mp3_22050_32",
        text = text,
        model_id = "eleven_turbo_v2_5"
    )
    return response

def choose_save_path(title):
    save_file_path = filedialog.asksaveasfilename(
        defaultextension = ".mp3",
        filetypes = [("MP3 files", ".mp3"), ("All files", "*.*")],
        initialfile = f"{title}.mp3",
        title = "Save audio file as"
    )

    if save_file_path:
        return save_file_path
    else:
        print("No save path selected")
        return None

def save_file(save_path, response):
    with open(save_path, "wb") as file:
        for chunk in response:
            if chunk:
                file.write(chunk)
    return print("New audio file was saved successfully")