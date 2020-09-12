#!/usr/bin/env python3.8

import argparse
import sys
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
import pathlib

def parse_validate_flags() -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description='Validate word alignments for a sentence-aligned parallel corpus')
    parser.add_argument("-f", "--f_file",
                        type=str,
                        default=f"{pathlib.Path(__file__).parent.absolute()}/data/hansards.f",
                        help="Path to sentence-aligned French side of the parallel corpus")
    parser.add_argument("-e", "--e_file",
                        type=str,
                        default=f"{pathlib.Path(__file__).parent.absolute()}/data/hansards.e",
                        help="Path to sentence-aligned English side of the parallel corpus")

    return parser.parse_args()


def validate(f_filename: str, e_filename: str):
    f_data = open(f_filename)
    e_data = open(e_filename)

    for (n, (f, e, a)) in enumerate(zip(f_data, e_data, sys.stdin)):
        size_f = len(f.strip().split())
        size_e = len(e.strip().split())
        try:
            alignment = set([tuple(map(int, x.split("-"))) for x in a.strip().split()])
            for (i, j) in alignment:
                if i >= size_f or j > size_e:
                    sys.stderr.write(f"WARNING: Sentence {n}, point ({i},{j}) is not a valid link\n")
                pass
        except Exception:
            sys.stderr.write(f"ERROR line {n} is not formatted correctly:\n  {a}")
            sys.stderr.write("Lines can contain only tokens \"i-j\", where i and j are integer indexes " +
                             "into the French and English sentences, respectively.\n")
            sys.exit(1)
        try:
            sys.stdout.write(a)
        except BrokenPipeError:
            return

    warned = False
    for a in sys.stdin:
        if not warned:
            sys.stderr.write("WARNING: alignment file is longer than parallel corpus\n")
            warned = True
        try:
            sys.stdout.write(a)
        except BrokenPipeError:
            return

    try:
        if next(f_data):
            sys.stderr.write("WARNING: parallel corpus is longer than alignment file\n")
    except StopIteration:
        pass


if __name__ == "__main__":

    try:
        flags = parse_validate_flags()
        validate(flags.f_file, flags.e_file)
    except BrokenPipeError:
        pass
