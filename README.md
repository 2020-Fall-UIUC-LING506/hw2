# Word alignment

## Data

Clone [the data repo](https://github.com/2020-Fall-UIUC-LING506/data) and ensure it is within this directory.

The cloned `data` directory contains a fragment of the Canadian Hansards,
aligned by Ulrich Germann:

-`hansards.e` is the English side.

-`hansards.f` is the French side.

-`hansards.a` is the alignment of the first 37 sentences. The 
  notation i-j means the word as position i of the French is 
  aligned to the word at position j of the English. Notation 
  i?j means they are probably aligned. Positions are 0-indexed.
  

## Programs

There are three python programs here (`-h` for usage):

-`./baseline.py` aligns words.

-`./validate.py` checks that the entire dataset is aligned, and
  that there are no out-of-bounds alignment points.

-`./score.py` computes alignment error rate.

The commands work in a pipeline. For instance:

   > ./baseline.py -t 0.9 -n 1000 | ./validate.py | ./score.py -n 5


## Assignment

Your task is to implement a better word aligner. Your code (`c.py`, `b.py`, and `a.py`) 

### Rubric

To earn a **C**, you must successfully implement a word alignment algorithm in `c.py` that notably improves on the baseline.

To earn a **B**, you must successfully implement IBM Model 1 in `b.py`

To earn an **A**, you must successfully implement IBM Model 1 in `b.py` and also implement a model more powerful than IBM Model 1 (such as IBM Model 2) in `a.py`

### Additional requirements

To earn full credit, your code must follow each of the following additional requirements:

* Your code must use Python 3, not Python 2

* Your code must run with no errors using Python 3.8

* Your code must be well-documented

* Your code must use [Python type hints](https://www.python.org/dev/peps/pep-0484/). If you're new to type hints in Python, look at the provided code. My code provides examples of how and when to use type hints.

* Your code must successfully type check with no errors and no warnings using [mypy](https://mypy.readthedocs.io/en/latest/getting_started.html).

* Your code (`c.py`, `b.py`, and `a.py`) must accept the same flags as `baseline.py` (with the exception of the threshold flag - you don't need to support that). I have provided align.py as template starter code that you may use for `c.py`, `b.py`, and `a.py`
