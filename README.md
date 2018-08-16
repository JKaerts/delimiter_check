# DelimiterCheck

This short script arose from a need to check my LaTeX-files for consistent parentheses, brackets and braces.
Since a typesetting engine should allow for prose with unbalanced delimiters, you should check everything manually or let your editor handle it.
This script was written to ease the labour.

## Usage

In a command line, simply enter

```
python DelimiterCheck.py -i textfile.txt
```

Supposing the text file contained

```
[a
(b
{c
}d
)e
(f
]g
```

you will get the following output.

```
Unclosed opening delimiter [ at line 1
Unclosed opening delimiter ( at line 6
Superfluous closing delimiter ] at line 7
```

The script knows that the two curly braces on lines 3 and 4 cancel.
With them out of the way, the parentheses on lines 2 and 5 can also cancel.
Finally, we are left with the delimiter structure `[(]` and this structure will not be reduced further, generating the three messages.
This is by design. I do not want overlapping hierarchies.

## How do I break the rules (in LaTeX)?

Of course in LaTeX there are sometimes reasons for wanting unbalanced delimiters.
Some examples are:
 * a system of equations being preceded by a single curly brace,
 * intervals with excluded endpoints are often denoted as `[a,b[` or `[a,b)`,
 * in numbered lists you might want the labels to be `a)`, `b)`, `c)`, etc.

My solutions to these problems are as follows:
 * LaTeX includes commands `\lbrace`, `\rbrace`, `\lbrack` and `\rbrack` for braces and square brackets.
   These commands will not be picked up by the script so you can use these in places where you explicitly need only one of a pair.
   This solves the first problem and part of the second problem.
 * Similar commands `\lparen` and `\rparen` exist in the package `mathtools`.
 * Using these six commands with a package like `enumitem` allows you to solve the third problem.

## How do I extend the rules?

It is possible to add your own set of delimiters to the program.
To do so you need to edit the code in one place.
Suppose I want the script to also check if every `\langle` has a matching `\rangle`.
To this end I need to add them to `delimiter_dictionary` (which matches opening delimiters to their closing counterpart).
It will now look like this:

```
delimiter_dictionary = {r'(': r')',
                        r'{': r'}',
                        r'[': r']',
                        r'\langle': r'\rangle'}
```

The use of raw strings is simply to make it less painful to get LaTeX-commands right
