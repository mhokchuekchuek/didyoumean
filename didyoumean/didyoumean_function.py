import json
import re
import string
from collections import Counter
from operator import itemgetter
from typing import List

import numpy as np
from pythainlp import thai_digits, thai_letters, word_tokenize
from pythainlp.util import normalize

from didyoumean.sub_some_word import (
    eng_to_thai,
    karan_pattern,
    sub_mispell_typing,
    sub_word,
)


# spell_checking
class SpellChecker:
    def __init__(self, word_freq_path, thai_word_path):
        self.words = self._load_thai_word(thai_word_path)
        self.word_freq = self._load_word_freq_from_json(word_freq_path)
        self.vocabs = set(self.words)
        self.word_counts = Counter(self.words)
        total_words = float(sum(self.word_counts.values()))
        self.word_probas = {
            word: self.word_counts[word] / total_words for word in self.vocabs
        }

    def _load_word_freq_from_json(self, json_path: str):
        with open(json_path, "r") as f:
            json_word_freq = json.load(f)
        return {
            x: int(y)
            for x, y in json_word_freq.items()
            if y != "อ๊าาา     1\nอ๊าาา    66\nName: freq, dtype: int64"
        }

    def _load_thai_word(self, thai_word_path: str):
        with open(thai_word_path, "r") as corpus:
            words = [line.strip() for line in corpus]
        return words

    def _level_one_edits(self, word):
        letters = (
            thai_digits
            + thai_letters
            + string.ascii_lowercase
            + string.ascii_uppercase
            + string.digits
            + "."
        )
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        replaces = [l + c + r[1:] for l, r in splits if r for c in letters]
        deletes = [l + r[1:] for l, r in splits if r]
        swaps = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r) > 1]
        inserts = [l + c + r for l, r in splits for c in letters]

        return set(deletes + swaps + replaces + inserts)

    def _level_two_edits(self, word):
        return set(
            e2 for e1 in self._level_one_edits(word) for e2 in self._level_one_edits(e1)
        )

    def check(
        self, word: str
    ) -> list[tuple]:  # checkว่าหลังจากที่ทำ edit distance รอบที่ 1 และ
        if word not in self.vocabs:
            candidates = (
                self._level_one_edits(word) or self._level_two_edits(word) or [word]
            )
            valid_candidates = [w for w in candidates if w in self.vocabs]
            return sorted(
                [(c, self.word_probas[c]) for c in valid_candidates],
                key=lambda tup: tup[1],
                reverse=True,
            )
        else:
            return [(word, 0)]

    def _return_word(self, input_checking: str) -> str:  # ทำการแก้คำผิดในระดับที่เป็นคำ
        if len(self.check(input_checking)) == 1:
            return self.check(input_checking)[0][0]
        else:
            find_max = []
            sim_short = []
            for i in self.check(input_checking):
                if i[0] in self.word_freq.keys():
                    find_max.append((i[0], self.word_freq[i[0]]))
            for i in self.check(
                input_checking
            ):  # เอาไว้เช็คตัวย่อ โดยดูว่าถ้าเอาจุดออกมันมีค่าเท่ากันไหม
                if re.sub(r"\.", "", i[0]) == re.sub(r"\.", "", input_checking):
                    sim_short.append((i[0], self.word_freq[i[0]]))
                    find_max = []
            if find_max:
                return max(find_max, key=itemgetter(1))[0]
            if sim_short:
                return max(sim_short, key=itemgetter(1))[0]
            else:
                if self.check(input_checking):
                    return self.check(input_checking)[0][0]
                else:
                    return input_checking

    def _is_in_corpus(self, input_checking):
        if self.check(input_checking):
            return True
        return False

    def change_some_input(
        self, input_text: str
    ) -> str:  # เปลี่ยนคำพิมพืผิดที่พิมพ์จาก eng เป็นไทย เช่น dlm=. แก้เป็น กสทช.
        input_tranform = []
        check_in_split = input_text.split(" ")
        for i in check_in_split:
            if sub_mispell_typing(i) != i and not self.check_file_name(input_text):
                words = [
                    eng_to_thai(word) if len(word) == 1 else word
                    for word in word_tokenize(sub_mispell_typing(i), engine="attacut")
                ]
                if len([word for word in words if self._is_in_corpus(word)]) == len(
                    words
                ):
                    split_1 = "".join(
                        [
                            self._return_word(word)
                            if self._is_in_corpus(word)
                            and not re.match(
                                "[ !#$%&'()*+,\-./:;<=>?@[\]^_`{|}~]", word
                            )
                            and len(word) > 1
                            else word
                            for word in words
                        ]
                    )
                    input_tranform.append(split_1)
                else:
                    input_tranform.append(i)
            else:
                input_tranform.append(i)

        return " ".join(
            [
                self._return_word(word)
                if self._is_in_corpus(word)
                and not re.match("[ !#$%&'()*+,\-./:;<=>?@[\]^_`{|}~]", word)
                and len(word) > 1
                else word
                for word in input_tranform
            ]
        )

    def check_file_name(self, input_checking: str) -> List[str]:
        if re.search(r"\.[a-zA-Z].+[a-zA-Z]|\)[a-zA-Z].+[a-zA-Z]", input_checking):
            return re.findall(
                r"\.[a-zA-Z].+[a-zA-Z]|\)[a-zA-Z].+[a-zA-Z]", input_checking
            )
        return []

    def _normalize_file_type(self, input_checking: str) -> str:
        if self.check_file_name(input_checking):
            for i in self.check_file_name(input_checking):
                file_type = re.sub(r"\.|\)", "", i)
                if self._is_in_corpus(file_type):
                    input_checking = input_checking.replace(
                        file_type, self._return_word(file_type)
                    )
            return input_checking
        return input_checking

    def _normalize_sentence(self, input_checking: str) -> list:
        user_sentence = []
        for sentence in input_checking.split():
            if re.search("[ก-์]+", sentence) and len(sentence) > 1:
                if not re.search("[0-9]|[๐-๙]", sentence):
                    sentence = self._return_word(sentence)
                thai_words = word_tokenize(sentence, engine="attacut")
                combined_thai_word = []
                for thai_word in thai_words:
                    if (
                        len(thai_word) > 1
                        and not re.search("[๐-๙]|[0-9]", thai_word)
                        and not self.check_file_name(thai_word)
                    ):
                        combined_thai_word.append("".join(self._return_word(thai_word)))
                    else:
                        combined_thai_word.append(thai_word)
                user_sentence.append("".join(combined_thai_word))
            else:
                user_sentence.append(sentence)
        return user_sentence

    def return_word(self, input_checking: List[str]) -> str:
        input_checking = normalize(input_checking)
        input_checking = karan_pattern(input_checking)
        input_checking = sub_word(input_checking)

        if self._is_in_corpus(input_checking):
            return self._return_word(input_checking)
        else:
            input_checking = re.sub(r" +", " ", input_checking)
            input_checking = self.change_some_input(
                self._normalize_file_type(input_checking)
            )
            words = self._normalize_sentence(input_checking)
            return " ".join(words)
