#!/usr/bin/env python3.8

import argparse
from collections import defaultdict
import sys
from typing import MutableMapping, Tuple
from corpus import AlignmentScores, ParallelCorpus, ParallelSentence

import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
import pathlib

def parse_align_flags() -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description='Calculate word alignments from a sentence-aligned parallel corpus')
    parser.add_argument("-f", "--f_file",
                        type=str,
                        default=f"{pathlib.Path(__file__).parent.absolute()}/data/hansards.f",
                        help="Path to sentence-aligned French side of the parallel corpus")
    parser.add_argument("-e", "--e_file",
                        type=str,
                        default=f"{pathlib.Path(__file__).parent.absolute()}/data/hansards.e",
                        help="Path to sentence-aligned English side of the parallel corpus")
    parser.add_argument("-n", "--num_sentences",
                        type=int,
                        default=sys.maxsize,
                        help="Number of sentences to use for training and alignment")
    parser.add_argument("-t", "--dice_threshold",
                        type=float,
                        default=0.5,
                        help="Threshold for aligning with Dice's coefficient")

    return parser.parse_args()


def train(corpus: ParallelCorpus) -> AlignmentScores:
    """Calculate alignment scores using Dice's co-efficient.

       The use of Dice's co-efficient to calculate alignment scores is a terrible idea.
       This function should serve only as a very naive baseline.
    """
    print("\nCollecting counts...", end="", file=sys.stderr, flush=True)


    # Initialize counts of foreign words to zero
    f_count: MutableMapping[int, int] = {f_word: 0 for f_word in ParallelCorpus.f_vocab}

    # Initialize counts of English words to zero
    e_count: MutableMapping[int, int] = {e_word: 0 for e_word in ParallelCorpus.e_vocab}

    # Initialize counts of foreign-English word pairs to zero
    fe_count: AlignmentScores = defaultdict(int)

    # For each parallel sentence
    for (n, parallel_sentence) in enumerate(corpus):  # type: Tuple[int, ParallelSentence]

        # Increment the foreign word type count for each word type in the foreign sentence
        for f_word in set(parallel_sentence.f):
            f_count[f_word] += 1

        # Increment the English word type count for each word type in the English sentence
        for e_word in set(parallel_sentence.e):
            e_count[e_word] += 1

        # Increment the Foreign-English word pair count for each word type pair in the parallel sentence
        for f_word in set(parallel_sentence.f):
            for e_word in set(parallel_sentence.e):
                fe_count[(f_word, e_word)] += 1

        if n % 5000 == 0:
            print(".", end="", file=sys.stderr, flush=True)

    print("\nCalculating Dice's coefficient...", end="", file=sys.stderr, flush=True)

    # Initialize all alignment scores to zero
    alignment_score = defaultdict(float)

    # For each potentially aligned word pair, calculate its alignment score
    for (k, (f_word, e_word)) in enumerate(fe_count.keys()):

        # Here we calculate the alignment score using Dice's co-efficient.
        alignment_score[(f_word, e_word)] = 2.0 * fe_count[(f_word, e_word)] / (f_count[f_word] + e_count[e_word])

        if k % 100000 == 0:
            print(".", end="", file=sys.stderr, flush=True)

    print("\n", end="", file=sys.stderr, flush=True)

    return alignment_score


def print_alignments(corpus: ParallelCorpus, alignment_score: AlignmentScores, threshold: float):
    """Print alignments for each parallel sentence"""
    try:
        for parallel_sentence in corpus:
            for (i, f_word) in enumerate(parallel_sentence.f):
                for (j, e_word) in enumerate(parallel_sentence.e):
                    # In this naive baseline, two words are considered aligned
                    #   if their alignment score as calculated using Dice's co-efficient
                    #   meets or exceeds a user-specified threshold.
                    if alignment_score[(f_word, e_word)] >= threshold:
                        sys.stdout.write(f"{i}-{j} ")
            sys.stdout.write("\n")
    except BrokenPipeError:
        return


if __name__ == "__main__":

    try:
        # Parse command line arguments
        flags = parse_align_flags()

        # Construct parallel corpus from user-specified files
        print("Loading parallel corpus...", end="", file=sys.stderr, flush=True)
        parallel_corpus = ParallelCorpus(flags.f_file, flags.e_file, flags.num_sentences)

        # Calculate alignment scores using naive baseline algorithm
        baseline_alignment_scores: AlignmentScores = train(parallel_corpus)

        # Print alignments
        print_alignments(parallel_corpus, baseline_alignment_scores, flags.dice_threshold)

    except BrokenPipeError:
        pass
