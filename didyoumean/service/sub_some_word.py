import re

dict_eng_to_thai = {
    "a": "ฟ",
    "A": "ฤ",
    "b": "ิ",
    "B": "ฺ",
    "c": "แ",
    "C": "ฉ",
    "d": "ก",
    "D": "ฏ",
    "e": "ำ",
    "E": "ฎ",
    "f": "ด",
    "F": "โ",
    "g": "เ",
    "G": "ฌ",
    "h": "้",
    "H": "็",
    "i": "ร",
    "I": "ณ",
    "j": "่",
    "J": "๋",
    "k": "า",
    "K": "ษ",
    "l": "ส",
    "L": "ศ",
    "m": "ท",
    "M": "?",
    "n": "ื",
    "N": "์",
    "o": "น",
    "O": "ฯ",
    "p": "ย",
    "P": "ญ",
    "q": "ๆ",
    "Q": "๐",
    "r": "พ",
    "R": "ฑ",
    "s": "ห",
    "S": "ฆ",
    "t": "ะ",
    "T": "ธ",
    "u": "ี",
    "U": "๊",
    "v": "อ",
    "V": "ฮ",
    "w": "ไ",
    "W": '"',
    "x": "ป",
    "X": ")",
    "y": "ั",
    "Y": "ํ",
    "z": "ผ",
    "Z": "(",
    "4": "ภ",
    "5": "ถ",
    "6": "ุ",
    "^": "ู",
    "7": "ึ",
    "8": "ค",
    "9": "ต",
    "0": "จ",
    "-": "ข",
    "=": "ช",
    "\\": "ฃ",
    "|": "ฅ",
    "'": "ง",
    ";": "ว",
    ":": "ซ",
    "[": "บ",
    "{": "ฐ",
    "]": "ล",
    ",": "ม",
    "<": "ฒ",
    "/": "ฝ",
    "?": "ฦ",
    ".": "ใ",
    ">": "ฬ",
    "1": "ๅ",
}


def karan_pattern(
    text: str,
) -> str:  # subtitle some vowel with karan example นิ์ -> น์ or น์ิ -> น์
    if re.search(r"[ก-ฮ๐-๙][ะัาำิีึืุูเแโใไๅํ็่้๊๋ฯฺๆ์ํ๎]์", text) and not re.search("ดิ์|ติ์", text):
        text = re.sub(r"[ะัาำิีึืุูเแโใไๅํ็่้๊๋ฯฺๆ์ํ๎]์", "์", text)
    elif re.search(r"์[ะัาำิีึืุูๅํ็่้๊๋ฯฺๆ์ํ๎]", text):
        text = re.sub(r"์[ะัาำิีึืุูๅํ็่้๊๋ฯฺๆ์ํ๎]", "์", text)
    else:
        text = text
    return text


def sub_word(txt: str) -> str:
    test = txt
    test = re.sub(r" +", " ", test)
    # test = re.sub(r"-+", "-",test)
    test = re.sub(r" ำ| า", "ำ", test)
    test = re.sub(r"พระราดบัญญัติ", "พระราชบัญญัติ", test)
    return test


def sub_mispell_typing(test_string: str) -> str:
    for i in test_string:
        if i in dict_eng_to_thai.keys():
            test_string = test_string.replace(i, dict_eng_to_thai[i])
    return test_string


def eng_to_thai(test_string: str) -> str:
    if list(dict_eng_to_thai.keys())[
        list(dict_eng_to_thai.values()).index(test_string)
    ][0].isdigit():
        return list(dict_eng_to_thai.keys())[
            list(dict_eng_to_thai.values()).index(test_string)
        ][0]
    return test_string
