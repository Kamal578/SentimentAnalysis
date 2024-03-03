import numpy as np
import json
import re

VOCAB_SIZE = 16385  # Pre-defined vocabulary size from the tokenizer documentation

non_latin_letters = {'ç': 'c', 'ə': 'e', 'ı': 'i', 'ğ': 'g', 'ö': 'o', 'ş': 's', 'ü': 'u', 'ch': 'c', 'sh': 's',
                     'gh': 'g'}

common_words = [
    'men', 'sen', 'o', 'biz', 'siz', 'onlar', 'ne', 'kim', 'hara', 'niye', 'nece', 'hansi', 'ne vaxt', 'sonra',
    'eger', 'heqiqeten', 'lakin', 'cunki', 'bu', 'ki', 'butun', 've', 'ya', 'veya', 'amma', 'yoxsa', 'ancag', 'sadece',
    'qisa', 'uzun', 'kicik', 'boyuk', 'ora', 'bura', 'sag', 'sol', 'salam', 'bele', 'cox', 'az', 'e', 'bir', 'her'
]

suffixes = [
    'lar', 'ler', 'larin', 'lerin', 'mis', 'mak', 'mek', 'liq', 'luq',
    'acaq', 'eceq', 'ma', 'm', 'am', 'em', 'ar', 'er', 'araq', 'ereq', 'arak', 'erek', 'ca', 'ce', 'ci', 'cu', 'da',
    'de', 'dan', 'den', 'di', 'diq', 'dir', 'du', 'duq', 'dur', 'duk', 'dur', 'ib', 'ici', 'il', 'inci', 'uncu',
    'istan', 'is', 'in', 'la', 'le', 'las', 'les', 'liq', 'luq', 'luk', 'maq', 'mek', 'mis', 'mus', 'n', 'nci', 'ncu',
    's', 'ub', 'ucu', 'ul', 'ustan', 'us', 'ub', 'ucu', 'y',
    'cil', 'dar', 'der', 'an', 'en', 'gec', 'kar', 'kes', 'ken', 'la', 'le', 'las', 'les', 'lik', 't', 'ma', 'me',
    'nan', 'nen', 'ova', 'ov', 'sen', 'san', 'siniz', 'sul', 'sunas',
]

emojis = [
    '👍', '👎', '👌', '🙃', '😉', '❤️', '🖤', '💔', '💕', '💖', '💗', '💘', '💙', '💚', '💛', '💜', '💝', '💞', '💟',
    '💠', '🤗', '🤔', '🤣', '🤤', '🤥', '🤦', '🤧', '🤨', '🤩', '🤪', '🤫', '🤬', '🤭', '🤮', '🤯', '🤰', '🤱', '🤲',
    '🎉', '😡', '🥰'
]


def replace_non_latins(text: str) -> str:
    """
    Replace non-latin azerbaijani letters with their latin counterparts
    """
    pattern = re.compile('|'.join(map(re.escape, non_latin_letters.keys())))
    return pattern.sub(lambda m: non_latin_letters[m.group(0)], text)


def remove_punctuation(text: str) -> str:
    """
    Remove punctuation from the text
    """
    # Replace hyphens with spaces to avoid concatenation of words
    text = text.replace('-', ' ')
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    return text.translate(str.maketrans('', '', punctuation))


def remove_common_words(text: str) -> str:
    """
    Remove common words from the text
    """
    return ' '.join([word for word in text.split() if word not in common_words])


def preprocess_text(text: str) -> str:
    """
    Preprocess the text by converting it to lowercase, replacing non-latin letters with their latin counterparts,
    removing non-alphabetic characters and removing common words
    :param text: input text
    :return: preprocessed text
    """
    text = text.lower()
    text = replace_non_latins(text)
    text = remove_punctuation(text)
    text = remove_common_words(text)
    return text if text else None


def tokenize_text(text: str) -> np.ndarray:
    """
    Tokenize the text by removing grammatical suffixes, considering roots and lexical suffixes as separate tokens
    :param text: input text
    :return: array of tokens
    """
    tokens = []
    for word in text.split():
        morphemes = []  # Morphemes of the word
        for suffix in suffixes:
            if word.endswith(suffix):
                # Remove grammatical suffix
                word = word[:-len(suffix)]
        for emoji in emojis:
            if emoji in word:
                morphemes.append(emoji)
                word = word.replace(emoji, '')
        if word and word not in common_words:
            morphemes.append(word)  # Add root as a separate token

        # Reverse the order of morphemes to get the correct order
        morphemes = morphemes[::-1]
        tokens.extend(morphemes)

    return np.array(tokens)


class Tokenizer:
    def __init__(self):
        self.vocab_size = 0
        self.vocab = {}
        self.corpus = []

    def fit(self, texts):
        """
        Fit the tokenizer on the given texts
        :param texts: text corpus
        :type texts: iterable of strings
        :return: None
        """
        for text in texts:
            tokens = tokenize_text(text)
            self.corpus.append(tokens)
            for token in tokens:
                if token not in self.vocab.keys():
                    self.vocab[token] = self.vocab_size + 1
                    self.vocab_size += 1

    def transform(self, texts) -> list:
        """
        Transform the given texts to tokenized form
        :param texts: input texts
        :return: tokenized texts
        """
        tokenized_texts = []
        for text in texts:
            tokens = tokenize_text(text)
            tokenized_text = [self.vocab[token] for token in tokens if token in self.vocab.keys()]
            tokenized_texts.append(tokenized_text)
        return tokenized_texts

    def transform_single(self, text: str) -> np.ndarray:
        """
        Transform a single text to tokenized form
        :param text: input text
        :return: tokenized text
        """
        tokens = tokenize_text(text)
        tokenized_text = [self.vocab[token] for token in tokens if token in self.vocab.keys()]
        return np.array(tokenized_text)

    def token_counts(self):
        """
        Count the number of occurrences of each token in the corpus
        """
        counts = {token: 0 for token in self.vocab.keys()}
        for tokens in self.corpus:
            for token in tokens:
                try:
                    counts[token] += 1
                except KeyError:
                    pass  # Ignore tokens not in the vocabulary
        return counts

    def _reindex_vocab(self):
        """
        Reindex the vocabulary after removing tokens
        """
        new_vocab = {}
        for i, token in enumerate(self.vocab.keys()):
            new_vocab[token] = i + 1
        self.vocab = new_vocab

    def remove_rare_tokens(self, min_count: int):
        """
        Remove tokens with occurrences less than the given minimum count from the vocabulary
        :param min_count: the minimum count for the tokens
        :return: None
        """
        token_counts = self.token_counts()
        for token, count in token_counts.items():
            if count < min_count:
                del self.vocab[token]
                self.vocab_size -= 1
        self._reindex_vocab()

    def keep_top_k(self, k: int):
        """
        Keep only the top k tokens in the vocabulary
        :param k: number of tokens to keep
        :return: None
        """
        token_counts = self.token_counts()
        sorted_tokens = sorted(token_counts, key=token_counts.get, reverse=True)
        for token in sorted_tokens[k:]:
            del self.vocab[token]
            self.vocab_size -= 1
        self._reindex_vocab()

    def save(self, path: str):
        """
        Save the vocabulary to the given path
        """
        with open(path, 'w') as f:
            f.write(json.dumps(self.vocab))

    def load(self, path: str):
        """
        Load the vocabulary from the given path
        """
        with open(path, 'r') as f:
            self.vocab = json.loads(f.read())
            self.vocab_size = len(self.vocab)
            self._reindex_vocab()
        return self