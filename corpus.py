from typing import List, MutableMapping, Tuple, Union
from sys import maxsize

# Define type alias for AlignmentScores
AlignmentScores = MutableMapping[Tuple[int, int], float]


class Vocabulary:

    def __init__(self, name: str):
        self._name: str = name
        self._int2str: List[str] = list()
        self._str2int: MutableMapping[str, int] = dict()

    def __getitem__(self, word: str) -> int:
        if isinstance(word, str):
            if word in self._str2int:
                return self._str2int[word]
            else:
                i = len(self._int2str)
                self._str2int[word] = i
                self._int2str.append(word)
                return i
        # elif isinstance(word, int):
        #     if word < 0 or word >= len(self._int2str):
        #         raise IndexError
        #     else:
        #         return self._int2str[word]
        else:
            raise TypeError

    def __str__(self):
        return f"{self._name} Vocabulary"

    def __repr__(self):
        return f"Vocabulary(name={self._name}, size={len(self)})"

    def __len__(self):
        return len(self._int2str)

    def __iter__(self):
        return iter(range(len(self)))


class ParallelSentence:

    def __init__(self, f: str, e: str):
        # Store words as integers rather than strings
        self.f: List[int] = [ParallelCorpus.f_vocab[f] for f in f.strip().split()]
        self.e: List[int] = [ParallelCorpus.e_vocab[e] for e in e.strip().split()]


class ParallelCorpus:

    e_vocab = Vocabulary(name="English")
    f_vocab = Vocabulary(name="French")

    def __init__(self, f_filename: str, e_filename: str, num_sentences: int = maxsize):

        self.parallel_sentences = [ParallelSentence(*sentence_pair) for sentence_pair in
                                   list(zip(open(f_filename), open(e_filename)))[:num_sentences]]

    def __getitem__(self, index):
        return self.parallel_sentences[index]

    def __iter__(self):
        return iter(self.parallel_sentences)

    def __len__(self):
        return len(self.parallel_sentences)


