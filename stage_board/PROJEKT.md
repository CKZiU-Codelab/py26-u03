# Project – Stage Board

**Individual Project Brief – Week 6 · u03**

Start: Monday, 16 November 2026. Show the working program on Monday, 23 November 2026.

## The Idea

You build the results board of a rally. Three special stages, four crews, car numbers on the doors. The program reads the stage times, checks every time before it accepts it, adds a penalty for a late start, sums the stages into one total, works out the gap to the leader, orders the crews and writes the board as a text file, a CSV file and a PGM picture.

Rally classification is just arithmetic with rules — exactly the kind of arithmetic a program does better than a person at eleven at night. The rules are the project: a missing stage is not zero seconds, a late start is not the same as a slow stage, and the leader's gap is not negative.

## Why This Project Is Yours

You follow rally and you read whatever you can get your hands on, and your laptop runs Linux, so the terminal is not new to you. Timing is the part of the sport that is pure data: the cars are rows, the stages are columns, and the classification is a calculation. This project is also a fair step up from the weekly tasks, without asking you to learn a new language.

## What You Already Have

- Lists, tuples, slices, `for` and `while`.
- Conditions, logical operators, and `%s`, `%d`, `%.1f` formatting.
- `open()` inside `with`, reading a file line by line, and the `csv` module.
- The PGM format from last week: `P2`, width, height, maximum value, then the grid.

## The New Thing

Two things need a decision from you this week.

First, a person typing times makes mistakes, and the program must survive them. Find out how to:

1. Read a number that may contain a decimal point, and what raises an error when the text is not a number.
2. Keep asking for a value until it is valid, without repeating the same four lines of code.
3. Tell `12.5`, `12,5` and `12s` apart before converting anything.
4. Decide whether an empty answer means "skip" or "error", and defend the choice.

Second, an ordered board is produced by swapping rows. Find out how an insertion sort works, and why it is a good choice for a list that is almost in order.

**Write it down:** Create `notes.md` with `## The New Thing – validating a time`. Write the rule for validating one time in your own words, one example of input that must be rejected, and the one case where your rule is still too generous. Add a second heading, `## The New Thing – insertion sort`, and explain in three sentences how a card player puts a new card into an already sorted hand. That comparison is the algorithm.

## The Plan

### Milestone 1 – The board file

Create `times.csv` by hand.

1. Four crews, three stages, four columns: `car,crew,ss,time_s`.
2. One crew misses one stage — write the row with an empty time.
3. One row has a time with a comma instead of a dot, as if it came from a Polish keyboard.

### Milestone 2 – Validate before you add

Create `stage_board.py`.

1. Read the file with the `csv` module and print every row with its line number.
2. Accept only times that are numbers greater than zero and shorter than a stage can be, say under `1800` seconds.
3. Print a report for each rejected row: the line number, the crew and the reason.
4. Count accepted and rejected rows, and never let a rejected time into the totals.

### Milestone 3 – Add the stages

1. Build one row per crew, with the car number, the crew name and a total.
2. Add the accepted times of the three stages.
3. Apply the penalty rule: a crew with no time on a stage receives the slowest accepted time on that stage plus `60.0` seconds. Mark that notional time in the table, and keep the `60.0` seconds in a penalty column.
4. Print each total with one decimal place and check that the stage times plus the penalty give the total.

### Milestone 4 – The gap

1. Find the leader with a loop. Do not use `min()`.
2. Compute every gap as the crew's total minus the leader's total.
3. Print the board with the gap formatted with a leading plus sign.
4. Prove that the leader's gap is `+0.0` and that no gap is negative.

### Milestone 5 – Order and save

1. Sort the crews by total time with an insertion sort, moving whole rows, not separate values.
2. Write `results.csv` with the `csv` module and a header row, in finishing order.
3. Write `board.txt` — the same table, aligned with field widths, with the positions from `1` to `4`.
4. Read `results.csv` back and print the winner and the last crew.

### Milestone 6 – The stage map

1. Create `stages.pgm`: one row of blocks per stage, one block per crew.
2. Give each block a gray value that depends on the crew's position on that stage — fastest darkest, for example.
3. Draw a notional time in a different shade from a real time, and say in `notes.md` why the difference must be visible.
4. Print the same map to the terminal with digits or letters and compare it with the CSV file.

## Example

```text
Reading times.csv
  line 2  12  Kowalski / Nowak    SS1   412.7   accepted
  line 3  12  Kowalski / Nowak    SS2   398.1   accepted
  line 4  17  Wiśniewski / Duda   SS2    12,9   rejected: comma is not a decimal point
  line 5  23  Mazur / Lis         SS3            rejected: empty time, notional time + penalty

10 rows accepted, 2 rows rejected

board.txt
Pos Car Crew                 SS1    SS2    SS3  Pen   Total    Gap
 1   7  Zieliński / Kot    401.2  395.8  410.3  0.0  1207.3   +0.0
 2  12  Kowalski / Nowak   412.7  398.1  405.9  0.0  1216.7   +9.4
 3  17  Wiśniewski / Duda  418.4  428.9* 430.1 60.0  1337.4 +130.1
 4  23  Mazur / Lis        421.0  428.9  430.1* 60.0  1340.0 +132.7
* slowest accepted time of the stage, plus the 60 s penalty

Saved results.csv (4 rows)
Saved stages.pgm (32x24)
```

The numbers are an example. Your file decides your numbers.

## Requirements

- One program, `stage_board.py`, started from the terminal with `python3 stage_board.py`.
- Every time is validated before conversion; a rejected value never reaches a total.
- The penalty rule is applied in one place, and a notional time is marked in the table and explained under it.
- The leader is found and the gaps are computed with loops, not with `min()`.
- The sort moves whole rows, so that a crew never loses its car number.
- `results.csv` is written with the `csv` module and has a header row.
- `stages.pgm` has a correct header, one block per crew and stage, and a shade that separates a notional time from a real one.

## Files

```text
stage_board/
├── times.csv
├── stage_board.py
├── results.csv
├── board.txt
├── stages.pgm
├── notes.md
└── check.py
```

Commit the whole directory to your repository and push it before the Monday session. A directory that exists only on your laptop cannot be checked.

Run `python3 check.py` in the project directory before you commit. It reads the files your program produced, not your code, and prints one line per requirement.


## How It Will Be Checked

- Rejected rows are listed with line numbers and reasons, and the totals do not change when they are fixed.
- The sum of the stage times plus the penalty equals the total for every crew.
- The gaps are measured against the leader of the whole rally, not against the previous crew.
- The finishing order in `results.csv` matches `board.txt`.
- Every block in `stages.pgm` can be traced to one cell in `results.csv`.
- You can explain your validation rule and your sort without the editor open.

**Hint:** Keep the three stage times in three separate columns of the row until the moment you compute the total. A missing time is not `0.0` — if you convert it to zero, the penalty rule and the gap rule stop agreeing with each other.

**Additional challenge:** Add a second classification for one stage only, and print the two boards side by side in the terminal. Then add a `--stage 2` style option — ask for the stage number with `input()` instead of a command-line argument, and say in `notes.md` which of the two ways you would prefer if you wrote this program for other people.

## Suggested Learning Resources

- [Errors and exceptions – what `ValueError` means](https://docs.python.org/3/tutorial/errors.html)
- [The `float()` constructor and numeric types](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)
- [The `csv` module – reading and writing tabular data](https://docs.python.org/3/library/csv.html)
- [Netpbm – description of the PGM format](https://netpbm.sourceforge.net/doc/pgm.html)

**Final goal:** By the end of this project, you should have a program that validates raw times, applies penalty rules, computes a classification with gaps, orders it by moving whole rows, and writes the result as CSV, text and a PGM picture — using loops, conditions, lists and file handling from the first five weeks.
