# haf
## A toy concatenative language

Haf was first developed in TeleBASIC, the native language of [Telehack](https://telehack.com). It is so named because it is half Forth, half Lisp, and half BASIC (and now in the Python version, half Logo!). Initial development was done pretty naively, as I didn't know anything of concatenative languages other than Forth. It ended up being both fairly useful as a scripting tool, and just plain fun to play around with. Early versions were "BASIC-ier" as I initially thought it might be fun to try and port it to a Microsoft BASIC, but I have since adopted more modern features for performance sake.

## Python version

The Python version was born when my 11 year old took an interest in the Telehack version. They had never really expressed any interest in computing, but asked some questions as to what I was doing. So I explained a few things like the stack. That prompted further interest, and later discussion of quoting and binding. This way of programming seemed completely natural to them (it does me too, I should add). So I have decided to create a version in Python that adds, among other things, turtle graphics. We'll see where further exploration takes us!

Additionally, as far as I know, there has not yet been the concatenative language equivalent of [(How to Write a (Lisp) Interpreter (in Python))](https://norvig.com/lispy.html). Due to dropping colon definitions (among other things), Haf has an incredibly simple parser, providing a good jumping in point for people curious about how they work. The code as such is deliberately pretty wordy (maybe too wordy?).

**n.b.** Until I get a chance to work on a Python version, the TeleBASIC manual should mostly work, although not all commands are implmented, and none of the alternate bracket types '(', '[' or even '~' are implmented. There is, however, one major difference:

**I have swapped the way Bind works**. Code tends to be more readable when you put the name of the function first, so:
>{dup *} double bind

is now
>double {dup *} bind

Until I implement either builtins or a standard library, I would highly suggest binding the backquote to work the old way, thusly:
>` {swap bind} bind

## TODO

- well, some error handling would be nice. Probably work on that first. 
- and a manual, also, too.
- implement more of the primitives from TeleHaf
- comments, though I may change the syntax for them
- add either builtins or a standard library
- remove unneccesary primitives (they were primitives in TeleHaf due to performance issues)
- file handling of some sort (was never thrilled with the TeleHaf version)
