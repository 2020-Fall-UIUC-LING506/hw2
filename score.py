#!/usr/bin/env python
import argparse
from collections import namedtuple
import sys
from typing import Tuple
import pathlib

AlignmentScores = namedtuple('AlignmentScores', ['precision', 'recall', 'aer'])


def parse_score_flags() -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description='Score word alignments against a gold standard')
    parser.add_argument("-f", "--f_file",
                        type=str,
                        default=f"{pathlib.Path(__file__).parent.absolute()}/data/hansards.f",
                        help="Path to sentence-aligned French side of the parallel corpus")
    parser.add_argument("-e", "--e_file",
                        type=str,
                        default=f"{pathlib.Path(__file__).parent.absolute()}/data/hansards.e",
                        help="Path to sentence-aligned English side of the parallel corpus")
    parser.add_argument("-s", "--score_alignments",
                        type=str,
                        default="-",
                        help="Path to word alignments file to be scored")
    parser.add_argument("-g", "--gold_alignments",
                        type=str,
                        default=f"{pathlib.Path(__file__).parent.absolute()}/data/hansards.a",
                        help="Path to gold-standard word alignments file")
    parser.add_argument("-n", "--num_display",
                        type=int,
                        default=sys.maxsize,
                        help="Number of alignments to display")
    return parser.parse_args()


def score(*, f_data: str, e_data: str, a_data: str, g_data: str, n: int) -> AlignmentScores:
    (size_a, size_s, size_a_and_s, size_a_and_p) = (0.0, 0.0, 0.0, 0.0)
    a_file = sys.stdin if (a_data == "-") else open(a_data)
    for (sentence_number, (f, e, g, a)) in enumerate(zip(open(f_data), open(e_data), open(g_data), a_file)):
        f_words = f.strip().split()
        e_words = e.strip().split()

        sure = set([tuple(map(int, x.split("-"))) for x in filter(lambda x: x.find("-") > -1, g.strip().split())])
        possible = set([tuple(map(int, x.split("?"))) for x in filter(lambda x: x.find("?") > -1, g.strip().split())])
        alignment = set([tuple(map(int, x.split("-"))) for x in a.strip().split()])

        size_a += len(alignment)
        size_s += len(sure)
        size_a_and_s += len(alignment & sure)
        size_a_and_p += len(alignment & possible) + len(alignment & sure)

        if sentence_number < n:
            sys.stdout.write(f"  Alignment {sentence_number}  KEY: ( ) = guessed, * = sure, ? = possible\n")
            sys.stdout.write("  ")
            for _ in e_words:
                sys.stdout.write("---")
            sys.stdout.write("\n")
            for (i, f_i) in enumerate(f_words):  # type: Tuple[int, str]
                sys.stdout.write(" |")
                for (j, e_j) in enumerate(e_words):  # type: Tuple[int, str]
                    (left, right) = ("(", ")") if (i, j) in alignment else (" ", " ")
                    point = "*" if (i, j) in sure else "?" if (i, j) in possible else " "
                    sys.stdout.write(f"{left}{point}{right}")
                sys.stdout.write(f" | {f_i}\n")
            sys.stdout.write("  ")
            for _ in e_words:
                sys.stdout.write("---")
            sys.stdout.write("\n")
            for k in range(max(map(len, e_words))):
                sys.stdout.write("  ")
                for word in e_words:
                    letter = word[k] if len(word) > k else " "
                    sys.stdout.write(f" {letter} ")
                sys.stdout.write("\n")
            sys.stdout.write("\n")

    return AlignmentScores(precision=size_a_and_p / size_a,
                           recall=size_a_and_s / size_s,
                           aer=1 - ((size_a_and_s + size_a_and_p) / (size_a + size_s)))


if __name__ == "__main__":
    try:
        flags = parse_score_flags()
        scores = score(f_data=flags.f_file,
                       e_data=flags.e_file,
                       a_data=flags.score_alignments,
                       g_data=flags.gold_alignments,
                       n=flags.num_display)
        sys.stdout.write(f"Precision = {scores.precision}\nRecall = {scores.recall}\nAER = {scores.aer}\n")
    except BrokenPipeError:
        pass

