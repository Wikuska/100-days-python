import tkinter
from helper_functions import select_file, pdf_to_text, text_to_speech, choose_save_path, save_file

root = tkinter.Tk()
root.attributes('-topmost', True) 
root.iconify()

print("Welcome in tts converter!")
print("Choose file to convert: ")

file_path = select_file()
if file_path:
    print(f"Choosen file: {file_path}")
    text = pdf_to_text(pdf_path = file_path)
    see_text = input("Would you like to see extracted text before converting it? Y/N: ").upper()
    if see_text == "Y":
        print(text)
    response = text_to_speech(text = text)
    title = input("Enter new file name: ")
    save_file_path = choose_save_path(title)
    if save_file_path:
        save_file(save_file_path, response)
root.destroy()
