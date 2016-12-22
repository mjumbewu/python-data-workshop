## Getting set up

### Verify your Python version

Open a terminal to ensure that you have an appropriate version of Python. On a
Mac, the application you want to run is called *Terminal*. On Windows, run
*Cmd*.

Once you're in the terminal, type `python -V`. You should get something like the
following:

```bash
$ python3 -V
# Python 3.5.2
```

If instead you see something like `Python 2.7.11` or `2.` anything, then try
running `python3 -V`. If that shows you a version of Python 3, then just be sure
to use `python3` wherever you see `python` in this exercise.

If you have Python 2 installed but no Python 3, then download the latest
Python 3 from https://www.python.org/downloads/.

### Using the REPL

There are two general ways that you can run Python code:

1. From within a file called a "module", which we'll come back to, or
2. Through the Python REPL.

The REPL, which stands for Read-Evaluate-Print Loop, comes in handy for trying
out quick snippets of code. We're going to start out there.

In a terminal, run `python`. You should see something like this:

```bash
$ python3
# Python 3.5.2 (default, Nov 17 2016, 17:05:23)
# [GCC 5.4.0 20160609] on linux
# Type "help", "copyright", "credits" or "license" for...
>>>
```

Try out a few expressions. For example, `1 + 2`, or `'a' + 'b'`. In both of
these cases, `1`, `2`, `'a'`, and `'b'` are literal values, meaning that the
values are literally what you see. We can also use variables and in the REPL.

```python
>>> 1 + 2
3
>>> 'a' + 'b'
'ab'
```

### Variables

There are a few ways that a variable can get set in Python that we're going to
be concerned with. One is directly. Try this in the Python REPL:

```python
>>> x = 3
>>> x + 2
5
```

Makes sense?

We can also loop over things:

```python
>>> for number in range(0, 5):
...    number + 5
...
5
6
7
8
9
```

We will come back to more about loops later cause they're great. For now, notice
Python's syntax for functions and blocks (indentation matters).

### Reading from files

Using Python, we can open files for reading or writing. By default, Python will
just open files to read from. First, download the CSV file linked from
https://www.opendataphilly.org/dataset/voting/turnout/resource/62730fc8-1186-44c9-a3d1-51059e17b436
into a folder. In your terminal, open a REPL in the same folder. In the REPL,
try this:

```python
>>> infile = open("voting/turnout.csv")
```

If you have your own data to work with, you can open that file instead. Bear in
mind though that this exercise is going to expect data in CSV format.

Let's read the file as a CSV file.

```python
import csv
infile = open("voting/turnout.csv")
rowiter = csv.reader(infile)  
header = next(rowiter)
rows = list(rowiter)
```

We'll go through this line-by-line.

```python
import csv
```

Basic CSV handling is part of the Python standard library, and is available
through the `csv` module.

Most of the Python functionality that you're going to use comes from some
module. These modules exist somewhere on your computer. In fact, you can find
out where any module is by going into the Python REPL and typing something like
this:

```python
>>> import csv
>>> csv.__file__
'/usr/lib/python3.5/csv.py'
```

Check out that file. If you're new to Python it probably won't all make sense
yet, but the style of Python in these modules is generally consistent with best
practices in Python. So, after you have a little more familiarity with the
language, it's a pretty significant advantage to have most of the standard
library available for perusal in Python.

Next line:

```python
infile = open("voting/turnout.csv")
```

Here, we make the contents of the CSV file available for reading, *but we do not
read it yet*. We are simply announcing our intention to work with the file and
obtaining a reference to its location on disk (or over the network as the case
may be). We are then storing that reference in a variable named `infile`. The
name of that variable doesn't matter; we could have called it `waffle`. I just
like `infile` because it's a file we're reading input from.

We make the reference available with the `open` function. This is a built-in
function in Python. You pass it the path to the file that you want to read, and
it gives you back a reference to that file. You can also use `open` to open a
file for writing, but it requires an additional argument.

Note that, while this is the way we're going to be opening files for this
exercise, there is a "safer" construct through which to do so in Python called
a [context manager](https://jeffknupp.com/blog/2016/03/07/python-with-context-managers/).
And opening files within a context manager when possible is certainly the more
correct way to do it. However, I don't recommend doing so if you don't know why,
and for most cases, this way is sufficient. Just know that, if you ever run into
an error like "Too many files open", it's because you have dangling file
references and it's time to start closing your files and learning about context
managers.

Next line:

```python
rowiter = csv.reader(infile)
```

We are creating another variable here called `rowiter`, but bear in mind again
that it doesn't matter what we call the variable on the left side. We could have
called it `syrup` and it would be fine.

Here, we're creating a CSV reader object for the file reference we created
earlier. In the `csv` module there's a function called `reader`. This function,
when called with a file-like object (that's language you'll see often:
"file-like object"; it just means a thing that has the same set of functions
that a file reference object has) returns a new object that you can use to loop
or iterate through the rows in the file.

Which brings us to the next line, which is where things get interesting:

```python
header = next(rowiter)
```

`rowiter` is a type of Python object called an "iterator". A Python iterator is
an object that refers to a specific position in some collection of data. In this
case that underlying collection of data is the rows in our CSV file. You can
call the built-in Python function `next` on any iterator object to item within
the collection that the iterator is currently pointing to.

Maybe best explained through illustration (alpha & beta)

The ability to work with CSV in this iterative way is one of the things that
makes the format so powerful in spite of its conceptual simplicity.

A file reference object as obtained by `open` is also an iterator. In one REPL,
run the following:

```python
>>> infile = open("voting/turnout.csv")
>>> line = next(infile)
>>> line
```

And in another, compare it against this:

```python
>>> import csv
>>> infile = open("voting/turnout.csv")
>>> rowiter = csv.reader(infile)
>>> header = next(rowiter)
>>> header
```

The first gives you a string of text. The most basic thing that a CSV `reader`
does for you is parse lines of text into structured data -- from an unstructured
set of letters and symbols to a demarcated set of data. With the former, all the
data is there and available, but it's not organized into data structures that
are most useful to us. If you wanted to find the heading of the second column,
you'd have to look for all the characters between the first and second commas,
strip off surrounding quotes if there are any, ensure that the commas you found
weren't between any quotes, deal with character encoding and escaping, etc. All
of that is entirely tractable, but if we had to do it every time we wanted to
read from a CSV file our scripts would get out of hand.

So, row-by-row, the CSV reader parses the CSV file. Which brings us to the last
line in our script:

```python
rows = list(rowiter)
```

What we see here is really a shorthand for something we recognize from before.
There are other ways we can write this:

```python
rows = []
while True:
    try:
        row = next(rowiter)
        rows.append(row)
    except StopIteration:
        break
# ==========
rows = []
for row in rowiter:
    rows.append(row)
# ==========
rows = [row for row in rowiter]
# ==========
rows = list(rowiter)
```

In short, it loops the iterator over all the items remaining in the collection
and adds them to a list. We're storing that list in a variable named `rows`.

### Cleaning & transforming data

Let's say we are using the voter turnout data and we want to get rid of all of
the columns aside from precinct, political party, and voter turnout count, since
the others are entirely redundant. There are a few ways we could do this. The
last one will be the right way, but we'll get there incrementally.

In other words, so far we've being creating statements similar to the following
SQL pseudo-statement:

```sql
SELECT *
  FROM voting/turnout
```

Instead, we're going to be selective about the columns we use, so we'll create
something more like the following:

```sql
SELECT Precinct_Code, Political_Party, Voter_Count
  FROM voting/turnout
```

Starting from the code we had before:

```python
import csv
infile = open("voting/turnout.csv")
rowiter = csv.reader(infile)
header = next(rowiter)
rows = list(rowiter)
```

If we print out the `header` row, we can see that we want to keep the 3rd, 5th,
and 6th columns (we're choosing the precinct code over the full description for
the sake of brevity). So, in our code we can create a new set of rows like so:

```python
cleanrows = []
for row in rows:
    cleanrows.append([row[2], row[4], row[5]])
```

Or, more succinctly:

```python
cleanrows = [
    [row[2], row[4], row[5]]
    for row in rows
]
```

However, someone reading this code has no idea what columns 2, 4, and 5 are
(remember that Python has 0-based indexing). For clarity and other reasons,
Python provides another type of CSV reader that allows us to refer to named
columns: the `DictReader`. Here's how our code looks if we use it:

```python
import csv
infile = open("voting/turnout.csv")
rowiter = csv.DictReader(infile)
rows = list(rowiter)
cleanrows = [
    {
        'Precinct Code': row['Precinct Code'],
        'Political Party': row['Political Party'],
        'Voter Count': row['Voter Count'],
    }
    for row in rows
]
```

> NOTE: The above code differs from what we did in the workshop in two ways:
> first, it uses a **list comprehension** (as does the code block above), which
> is, sometimes, a more compact and more efficient way of creating a new
> collection from some iterable object. Something more similar to what we did
> in the workshop is:
>
> ```python
cleanrows = []
for oldrow in rows:
    newrow = {'Precinct Code':   oldrow['Precinct Code'],
              'Political Party': oldrow['Political Party'],
              'Voter Count':     oldrow['Voter Count']}
    cleanrows.append(newrow)
```
>
> Second, in this example we are creating a dictionary instead of a list. This
> is because I am preparing the data to be used with a `csv.DictWriter`, which
> is a CSV writer that corresponds to the `csv.DictReader`. It writes rows from
> dictionaries instead of from lists.
>
> Compare this code to what we wrote in class (*_02_cut.py*).

Less succinct, but much more explicit. Notice we no longer have the statement
`header = next(rowiter)`. That's because the `DictReader` automatically treats
the header row specially (that's how it knows what name to attach to each value
in a row).

Now, the precinct code is actually a single string concateated (i.e., smooshed
together) from the ward and division. It may be more useful to us to have these
two values in their own columns. So, we can further modify our clean rows:

```python
for row in cleanrows:
    code = row.pop('Precinct Code')
    ward, div = code[:2], code[2:]
    row['Ward'] = ward
    row['Div'] = div
```

Let's go row-by-row again. By this point, we kinda get what the first row means,
so we'll start with the second:

```python
code = row.pop('Precinct Code')
```

In this case we are modifying each row in the original list of rows. Remember,
in this case, since we used a `DictReader`, each of our rows is a Python `dict`
so `row` is just a dictionary. Every `dict` has a function on it called `pop`
which will remove the item corresponding to the given key and return the value
of that item. Here we save that value in a variable called `code`.

> NOTE: Remember that this line is retrieving the value of the "Precinct Code"
> field and removing the field from the data in one step, where as in the
> workshop code (see *_03_split.py*) we did these as separate steps: one where
> we did `code = oldrow[0]` (because our rows were `list` objects, not `dict`
> objects), and later we omitted the first (zero-th) element from the row when
> creating a new row by saying `newrow = oldrow[1:] + [ward, div]`.

Next line:

```python
ward, div = code[:2], code[2:]
```

This is a Python shorthand for setting multiple values at once. It's equivalent
to saying:

```python
ward = code[:2]
div  = code[2:]
```

The stuff on the right side of the equals signs are there for getting specific
portions of strings. The first statement says, "give me the first 2 characters
in the string", and the second says, "give me all the characters in the string
after the second character". Both of these use slice notation (i.e., they're
taking slices of a string), which we can dig in to later if we need.

The next two lines go together:

```python
row['Ward'] = ward
row['Div'] = div
```

These lines are adding new fields into the row -- `'Ward'` and `'Div'`.

### Aggregating & summarizing data

Generally, when aggregating, you'll want to group by some small set of fields
(often just one) and do some calculation over all the rows that share the same
value in that field.

We're going to do something similar to the following SQL:

```sql
SELECT Ward, SUM(Dem) AS Sum_Dem, SUM(Rep) AS Sum_Rep, SUM(Total) AS Sum_Total
  FROM voting/turnout
GROUP BY Ward
```

```python
summary = {}
for row in rows:
    ward = row['Ward']
    if ward not in summary:
        summary[ward] = {'Sum_Dem': 0, 'Sum_Rep': 0, 'Sum_Total': 0}
    summary[ward]['Sum_Dem'] += int(row['Dem'])
    summary[ward]['Sum_Rep'] += int(row['Rep'])
    summary[ward]['Sum_Total'] += int(row['Total'])
```

### Writing data

So far we have just been working with data in memory. We can also write to
files, but we're going to write to standard out instead.

```python
import csv
import sys
writer = csv.DictWriter(sys.stdout, fieldnames=rowiter.fieldnames)
writer.writeheader()
writer.writerows()
```

### Working with multiple datasets

### Other modules and tools

* For GIS
  - Prerequisites are GEOS, GDAL, Proj4; libspatialindex for rtree
  - shapely for working with spatial objects
* For Databases
  - datum
* For HTTP/APIs
  - requests
* petl and pandas