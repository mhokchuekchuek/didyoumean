from pythainlp.corpus.tnc import word_freqs


def get_word_freq() -> dict:
    return {word: word_freq for word, word_freq in word_freqs()}
