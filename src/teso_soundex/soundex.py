
def letter_values(argument: str) -> str:
    letter = argument.lower()
    switcher = {
        "b" : "1",
        "f" : "1",
        "p" : "1",
        "v" : "1",
        "c" : "2", 
        "g" : "2", 
        "j" : "2", 
        "k" : "2", 
        "q" : "2", 
        "s" : "2", 
        "x" : "2", 
        "z" : "2",
        "d" : "3", 
        "t" : "3",
        "l" : "4",
        "m" : "5", 
        "n" : "5",
        "r" : "6"
    }
    return switcher.get(letter)


def convert_to_code(word: str) -> str:
    code = ""
    last_number = ""
    for letter in word:
        converted_letter = letter_values(letter)
        if last_number == converted_letter:
            continue
        last_number = converted_letter
        code += converted_letter
    if len(code) < 3:
        while len(code) != 3:
            code += "0"
    elif len(code) > 3:
        code = code[0:2]
    return code
        

def remove_letters(word: str) -> str:
    letters_to_remove = ["a", "e", "i", "o", "u", "y", "h", "w"]
    for letter in letters_to_remove:
        word = word.replace(letter, "")
    return word


def read_buffer(file_stream, buffer_size: int) -> str:
    return file_stream.read(buffer_size)


def convert_to_soundex(word: str) -> str:
    remainder = word[1:]
    remainder = remove_letters(remainder)
    remainder = convert_to_code(remainder)
    soundex_word = word[0].lower() + remainder
    return soundex_word

    
if __name__ == '__main__':
    print("Hello World")
