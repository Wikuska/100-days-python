from morse_dict import morse_dict

def text_to_morse(text):
    try:
        translated = ""
        for char in text:
            if char == ' ':
                morse_char = '       '
            else:
                morse_char = (morse_dict[char] + "   ")
            translated += morse_char
        return print(f"Translated text:\n{translated}")
    except KeyError as char:
        return print(f"Invalid key: {char}")

go_on = True
print('MORSE CODE TRANSLATOR')
while go_on:
    print("\nPlease use english alphabet!")
    to_translate = input("What would you like to translate?: ").upper()
    text_to_morse(to_translate)
    translate_more = input("Would you like to translate something else? y/n: ").lower()
    if translate_more == "n":
        go_on = False
