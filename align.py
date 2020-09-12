#!/usr/bin/env python3.8

import argparse
from collections import defaultdict
import sys
from corpus import AlignmentScores, ParallelCorpus
import signal
import pathlib


signal.signal(signal.SIGPIPE, signal.SIG_DFL)


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

    return parser.parse_args()


def train(corpus: ParallelCorpus) -> AlignmentScores:

    # Initialize all alignment scores to zero
    alignment_score: AlignmentScores = defaultdict(float)

    # Your code to calculate word alignment scores goes here.
    #
    # You are expected to implement IBM Model 1

    return alignment_score


def print_alignments(corpus: ParallelCorpus, alignment_score: AlignmentScores):
    """Print alignments for each parallel sentence"""
    for parallel_sentence in corpus:
        for (i, f_word) in enumerate(parallel_sentence.f):
            for (j, e_word) in enumerate(parallel_sentence.e):
                # Your code goes here
                pass


if __name__ == "__main__":
    # Parse command line arguments
    flags = parse_align_flags()

    # Construct parallel corpus from user-specified files
    parallel_corpus = ParallelCorpus(flags.f_file, flags.e_file, flags.num_sentences)

    # Calculate alignment scores using naive baseline algorithm
    baseline_alignment_scores: AlignmentScores = train(parallel_corpus)

    # Print alignments
    print_alignments(parallel_corpus, baseline_alignment_scores)
