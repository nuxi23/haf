# HAF: a halfway decent manual by Nuxi
### for Python version

```
       _---.      _--.,-'-\_,-"~^"-...
     ." () `"-,-"` \     //       /   ;
    /  *      \/    |   /||      \     ;
   @   \     _/    /     \\     ,-"     ;
   "!_.--. /    \/ \      |\   /        ;
        /`-.\   | .,\.,"`,/,| |        `._______
     _.-'_/`  )  )           \     \-----------,)
   ((("~` _.-'.-'           __`-.   )         //
         ((("`             (((---~"`         //
                                            U
```
Haf's mascot: Enid, the naked mole rat




## Introduction

Welcome to Haf, the language that's half Forth, half Lisp, half BASIC, and half Logo, with just a smidgen of a very obscure language called Mouse.

...why?

Well, a few reasons. I am an avid player of the game [Telehack](telehack.com) and nobody had made a complete language in its native scripting language TeleBASIC yet. Also, I have never designed a language -- knew the basics, but never really implemented anything fully, let alone designed something to my tastes. And I made up something very similar during a session with chatGPT in which I wanted to prove it didn't really understand the code it was creating. The language I made up on the spot actually seemed pretty intriguing, so I decided to implement that.

After developing Haf, I was amazed to discover that many of the design decisions I thought were unique and novel already existed in concatenative languages like Factor or most especially Postscript. Haf is really close to Postscript without, you know, all the font stuff...

Concatenative languages are a subset of functional languages. "Concatenation is composition" is the mantra. In other words, by using a stack rather than function calls with explicit arguments, a program becomes a string of chained commands: like unix pipes, but more powerful.

If there is one thing that makes Haf different from its forebears, it is that syntax is as simple as possible. Thus it is entirely, aggressively postfix, including function binding and control structures. The only components are words and the literal markers, "{" and "}"; the alternate control notations "(" and "[" are syntactic sugar for a postfix notation. This puts Haf a bit closer to Lisp, with true code-as-data homoiconicity.

OTOH, it has mutable variables. So maybe it's less like a lisp? 

Whatever. It's super fun!

## Starting out

I will assume you have familiarity with the concept of the stack, and that of a REPL environment. You type it in, the interpreter interprets as you go.

The stack in Haf consists entirely of strings. Strings are the only data type native to Haf. (Python, on the other hand, is typed, and this is affects several of the primitives. You're on your own interms of type checking though. More on this later.)

To put something on the stack, type it, and press return:
```
0>A
1>1
2>Fnord
```
The number next to the prompt tells you the current depth of the stack. To see what is on the stack, print it with "."
```
2>.
Fnord
1>.
1
0>.
A
```
You can combine elements on a single line, separated by spaces:
```
0>A 1 Fnord . . .
Fnord
1
A
```
What if you want to put the character "." itself on the stack? Or a full sentence? To do this, you will use curly braces {}
```
0>{.} {} {Foo Bar} . . .
Foo Bar

.
```
NOTE: You will need to be very careful with braces. They must always match. {This is a {faulty} line and will cause havoc.


At this point you should probably type .w to see a list of all the words available to you. Commands, hereafter called words, in Haf are case-independant; cat or CAT or cAt would all work. .w will show all the words in Haf's dictionary. You can see it comes with a lot, and unless I've had a lot of time on my hands, it's in no particular order.

You can do math:
```
0>1 3 + . 
4
0>10 3 % .
1
```
or string manipulation:
```
0>{foo bar} 3 RIGHT UPS .
BAR
```
or shell commands:
```
0>ls exec .
advent.gam    againstip.txt    basic.man
(rest of directory listing omitted)
```

Haf handliy shows you the stack depth in the prompt, but sometimes you'll want to use the depth of the stack in your code:
```
3>DEPTH
4>.
3
```
and you can clear the stack with CLEARSTACK
```
3>CLEARSTACK
0>
```
## Stack Manipulation

If you know (or have a passing familiarity with) Forth, you can probably skip this chapter.

There are five basic stack manipulation words: DUP DROP SWAP OVER ROT

Let's look at them in turn, but first we'll need to look at how to read a stack definition:
```
DUP (a -- aa)
```
this shows that DUP takes 1 element from the stack, and puts 2 back on. I will use a b c for most definitions, but will use n when basic requires a number, for instance:
```
+ (n n -- n)
```
On to the definitions:

>DUP (a -- aa) - duplicates the top of the stack
>
>DROP (a --) - removes the item at the top of the stack
>
>SWAP (ab -- ba) - swaps top two elements of the stack
>
>OVER (ab -- aba) - takes the element in the second position and copies it to the top of the stack
>
>ROT (abc -- bca) - moves the item in the third position to the top of the stack

```
0>3 DUP + .
6

0>CLEARSTACK Fiddle Dee Dee ROT . DEPTH .
Fiddle
2
```
There are actually two more, PICK and ROLL, but they are generally only used in extreme circumstances. 

>PICK (n -- a) - Choose the Nth element from the top of stack, and place at top of stack. 0 PICK is equivalent to DUP, 1 PICK is equivalent to OVER.
>
>ROLL (n -- a)
>

##Loops & conditionals

There are two conditionals, IFTE and IF:

>IFTE (a a a --) - IFTE takes three parameters, the third item on the stack is a boolean, if true, the second from the top is executed, if false, the top is executed
```
0>TRUE {{I'm the true case} .} {{I'm the false case} .} IFTE
I'm the true case
```
>IF (a a--) - IF takes two parameters, if the boolean at the top of the stack is true, the word in the second spot is executed
```
0>FALSE {{I'm the true case} .} IF
0>
```

There is only one looping command, WHILE.

>WHILE (a a--a) - While takes the element in the second position, if it is not false it executes the code in the top position, with the test value placed at the top of the stack before execution, repeating until the condition is false

```
0>10 {1 - DUP .} WHILE
9
8
7
6
5
4
3
2
1
```

```
0>TRUE {{Enter password} PRIN1 INPUT Swordfish NE} WHILE {You're in!} .
Enter password?Password
Enter password?12345
Enter password?Swordfish
You're in!
```

>PRIN1 (a --) - pops the top of the stack, prints it without a newline. Equivalent to basic PRINT FOO;
>
>NE (a a--a) - Not equal, returns a boolean value if the two are not equal

## Bind / eval

Thusfar we've done a lot of REPL interaction, but nothing persistent. Nothing that looks like a program. For that, we will need a new word: BIND

>BIND (a a --) - binds the element at the top of the stack to the name in the second position

Let's watch the behavior a bit:
```
0>THREE 3 BIND
0>three .
3
0>{ThReE} DESCRIBE .
3
```

>DESCRIBE (a -- a) - shows the value bound to the word at the top of the stack

Wait, why did that last example need braces? It's because otherwise you wouldn't get the definition of THREE, you'd get the definition of 3. This will be important later.

```
0>{THREE} 4 BIND
0>THREE .
4
```

Yeah, they're mutable. Mut 'em all you want. Also, BIND is global in scope (I may add the ability to do local scoping later). Now, what would happen if you didn't quote THREE here?
```
0>THREE 5 BIND
0>THREE .
5
```
Well. No problem then.
```
0>.U
CONS TRUE? FALSE? IF CLEARSTACK PRINTLN CAR CDR .D .S .U .L .B ` CAT THREE 4
```

>.U (--) Prints all the defined (not primitive) words in the dictionary, including built-ins

Oops. You can bind numbers, even rebind over primitives if you want (though you can't unbind them). Speaking of which, better clean up after ourselves:

```
0>{THREE} UNBIND
0>THREE .
THREE
0>{4} UNBIND
0>.U
CONS TRUE? FALSE? IF CLEARSTACK PRINTLN CAR CDR .D .S .U .L .B ` CAT
```

>UNBIND (a --) removes word at the top of the stack from the dictionary

So big deal, you've got a weird way to make variables. But wait, let's have a look at that USERDICT again. IF? CLEARSTACK? Yes, you can bind anything to a word, including code. Let's look.

```
0>{CLEARSTACK} DESCRIBE . 
DEPTH {DROP DROP DEPTH} WHILE
0>{CONS} DESCRIBE .
SWAP { } & SWAP &
```

So let's try it out. Here's a simple program:
```
0>SQUARE {DUP * } BIND
0>4 SQUARE
16
```

And another:
```
0>! {DUP 1 gt {DUP 1 - !} {1} IFTE *} bind
0>5 ! .
120
```
or tail recursively:
```
0>{!} {over 1 eq {swap drop} {over * swap 1 - swap !} IFTE} bind
0>5 ! .
120
```
You can also do shell commands via EXEC:
```
0>ls {{ls} exec} bind
0>ls
(directory listing omitted)
```
Now something a bit more elaborate:
```
0>{get-password} {{what is your secret password?} println input} bind
0>{get-mask-length} {over len over len / int 1 +} bind
0>{make-mask} {get-mask-length swap string} bind
0>{trim-mask} {over len left} bind
0>{encode} {xor} bind
0>{secure-text} {get-password make-mask trim-mask encode}  bind
```
A good Haf program is usually made of lots of tiny words. These words, when strung together, describe what your program does: get password, make mask, trim mask, encode. There's no screen editor, but by keeping them short, the input history buffer is usually suffient for editing. Just don't forget to quote the word if you're re-binding. This approach also makes it easy to add features. xor is pretty stupid as an encryption method, but it works as a placeholder. Now you can build up the encode word to nest the real method as you develop it.

It's a good idea to always quote the name of your word in a definition. That way if you are re-defining a word, it won't accidentally get executed.


There's one more concept I want to introduce, and that's EVAL.

>EVAL (a -- ?) Eval pops the stack, and then evaluates the string as if it had been typed at the command line. This is an incredibly powerful ability, that I will not go into much here. But here's some examples:
```
0>1 EVAL .
1
```
(numbers and strings always eval to themselves unless they've been bound)
```
0>{THREE BLIND MICE} EVAL . . .
MICE
BLIND
THREE

0>fnord {+} {3 4 fnord} sub EVAL .
7
```
Eval lets you treat data just like code, and vice versa. So your program can create code and then run it on the fly.
```
0>4 {SQUARE} {\*} {+} DESCRIBE SUB EVAL . ~turn square into double~
8
```
>SUB (abc -- a) regex-based replacement tool, replaces substring "a" in string "c" with substitution "b" per re.sub 



## Return stack functions

There are five more stack words to introduce (again, if you know Forth, feel free to skip this bit).

These words are a bit different than the others, because they deal with the return (or environment) stack. They go here at the end because they can be dangerous, but they're also a way to handle temporary values without binding them. The most important thing to remember is that, unlike traditional stack, *you must end the word with no changes to the return stack*. If you add an element to the return stack, you'd better remove it when you're done. In addition, they're only active locally within the current "depth" of branching, making this sort of a local stack.

>\>R (a -- ) moves an element from the stack to the return stack

>R> ( -- a) moves an element from the return stack to the stack

>R@ ( -- a) copies an element from the return stack to the stack

>N>R (a n -- ) moves n elements from the stack to the return stack

>NR> ( -- a) moves number of elements specified in the top return stack value from the return stack to the stack
```
0>ONE TWO THREE 3 (>R . R> 1 -)
THREE
TWO 
ONE
```

Here's factorial again, non-recursively

0>countdown {{dup 1 -} while} bind
0>multimultiply {{>R * R> 1 -} while} bind
0>! {dup >R countdown R> 1 - multimultiply}  bind
0>5 !
120

## CANDR (pronounced candor)

Now it's time for the Lisp fans. CANDR is a contraction of CAR AND CDR, but be careful -- it should not be confused with CADR (which is not implemented anyway). Instead, CANDR takes the CAR (sorta) and the CDR (also sorta) and puts them both on the stack. CONS, which you probably already noticed, is also present, and also (sorta) works like Lisp.

For those of you who have no idea what the above paragraph meant, let's explain.

>CANDR (a -- a a) returns the first element of the list on the top of the stack, the remainder of the list in the second spot
```
0>{{this is my nested} list} CANDR . .
this is my nested
list
```
>CAR (a -- a) returns the first element of the list as the top of the stack
```
0>{1 2 3 4} CAR .
1
```

>CDR (a -- a) returns everything but the first element of the list as the top of the stack
```
0>{1 2 3 4} CDR .
2 3 4
```

>CONS (a a -- a) combines top two elements on the stack into a list (i.e., concatenates them with a space)
```
0>FOO 
1>BAR 
2>BAZ CONS CONS .
FOO BAR BAZ
```
## Meta-stack commands, creating higher-order functions MAP and REDUCE

You already know CLEARSTACK and DEPTH, but there are a few other commands that address the stack as a unit, namely STACK and LITSTACK. These are very similar, but with one imporant difference.

>STACK (* -- *a) place the entire contents of the stack as a list on the top of the stack
>LITSTACK (* -- *a) place the entire contents of the stack as a list of quoted elements at the top of the stack

STACK is useful if you just want to quickly view what's on the stack, or quickly concatenate the whole stack. LITSTACK is more useful when you want to save the contents and restore them later.

```
0>1 2 3 {+} STACK .
1 2 3 +
0>1 2 3 {+} STACK >R CLEARSTACK >R EVAL STACK .
1 5

0>1 2 3 {+} LITSTACK .
{1} {2} {3} {+}
0>1 2 3 {+} LITSTACK >R CLEARSTACK R> EVAL STACK .
1 2 3 +
```
Let's look at some of the very powerful things we're now able to do by freezing the state of the stack, stashing it somewhere, and then bringing it back:
```
{reduce-func} {>r eval r> depth 2 - {>r >r r@ eval r> r> 1 -} while drop} bind
{reduce} {depth 2 - {>r >r litstack >r clearstack 3 nr> 2 pick 3 n>r drop reduce-func r> swap >r eval drop r>} {reduce-func} ifte} bind
```
>REDUCE (aa - a), sometimes called fold, is a common higher-order function in functional languages. It will repeatedly apply a function to (in our case) a list, accumulating until a single result is acheived. For example:
```
0>{1 2 3} {+} REDUCE .
6
```
By using the meta-stack commands, we are able to implement reduce via stack commands, as if it had its own local stack. See how it respects the original stack:
```
0>HEY THERE
2>{1 2 3} {+} REDUCE
3>.S
HEY THERE 6
```
Let's REDUCE a function to get the maximum value of a list. Our implementation of REDUCE takes two values at a time and applies the function, so this should be easy:

0>{1 2 4 5 2} {gt} REDUCE
0

Uh-oh. The greater-than function returns a binary truth value, not a result. Clearly we will need to create and bind a new word, MAX, to get the larger of two values. Except in Haf, words are just substitutions. So if we don't need to use that max function anywhere else, we can put it right in:

0>{1 2 5 4 2} {over over gt {drop} {swap drop} ifte} REDUCE .
5

There's some advanced stuff hidden in here, but for our intents and purposes, you should focus on the fact that *sometimes* you will want to create new words, *sometimes* you won't. Clarity, repetition, reuse, are all factors.

Now if you are familiar already with REDUCE or fold, you may wonder, can we create a MAP? Yep!
```
{map-func} {>r eval r@ eval r> depth 2 - {>r >r swap r@ eval swap cons r> r> 1 -} while drop} bind
{map} {depth 2 - {>r >r litstack >r clearstack 3 nr> 2 pick 3 n>r drop map-func swap >r eval drop r>} {map-func} ifte}  bind
```
>MAP (aa -- a) MAP takes a function and applies it to each element of a list. The function must take a single argument and return a single value (i.e. have a stack notation of the form (a -- a))
```
0>{1.3 3.9 5.7} {INT} MAP
1 3 5
```


## Abbreviations

There are several common abbreviated commands provided as built-ins, namely ` and the dot-commands.

>` (aa --} equivalent to BIND, but reversing the order (i.e. DEFINITION NAME). This order is often more convenient at the REPL

>.D (a --) DESCRIBE .

>.L ( -- ) LITSTACK .

>.S ( -- ) STACK .

>.U ( -- ) USERDICT .

>.W ( -- ) WORDS .


## Sample program
Here's an example of much of what we have learned in action, a simple generative grammar:
```
{count-words}
{{ } 1 1 RE 1 +} bind

{rand}
{rnd int} bind

{space-split} 
{{>R cdr R> 1 -} while} bind

{rand-word}
{count-words rand space-split car} bind

{noun-phrase}
{determiner-list dup rand-word adjective-list dup rand-word noun-list dup rand-word cons cons} bind

{sentence}
{noun-phrase verb-list dup rand-word noun-phrase cons cons} bind
{{pigeon pickle tood paperclip Kardashian}} noun-list bind
{{eats unleashes tickles hacks questions}} verb-list bind
{{a the}} determiner-list bind
{{cranky yellow happy tall stanky burbling}} adjective-list bind

0 >sentence .
a stanky Kardashian unleashes the yellow tood
```

## Full dictionary

  
```
Word		stack		etymology	definition
		    def
%		    (n n -- n)	Math		Modulo	
&		    (a a -- a)	Excel		Concatenates two strings at the top of the stack
*		    (n n -- n)	Math		Multiply
+		    (n n -- n)	Math		Add
-		    (n n -- n) 	Math		Add		
.		    (a -- )		Forth		Pops value at top of stack and prints it, with newline. Synonym for PRINTLN
.D		    (a -- )		Haf		    Prints definition of word at top of the stack. Equivalent to DESCRIBE .
.EXE        (a -- )		Haf		    Executes command in telehack without placing it on stack
.L		    ( -- )		Haf		    Prints stack contents as literals. Equivalent to LITSTACK .
.S		    ( -- )		Forth		Prints stack contents. Equivalent to STACK .
.U		    ( -- )		Haf		    Prints list of all user (non-primitive) words. Equivalent to USERDICT .
.W		    ( -- )		Forth		Prints list of all words including primitivies. Equivalent to WORDS .
/		    (n n -- n)	Math		Floating Division
LT		    (n n -- a)	Math		If arg 1 < arg 2, return TRUE, else return FALSE
EQ		    (n n -- a)	Math		If arg 1 = arg 2, return TRUE, else return FALSE
GT		    (n n -- a)	Math		If arg 1 > arg 2, return TRUE, else return FALSE
>R		    (n -- )		Forth		Move value at top of stack to return stack
^		    (n n -- n)	Math		Exponentation
`		    (a a -- )	Haf		    Bind arg1 to arg2.
AND		    (a a -- a)	THBAS		Bitwise AND
APPEND      (a -- )		Haf		    Opens working file for appending with name referenced at top of stack
ASC
ATN
B64E 
B64D
BIN
BIND	    (a a -- )	Haf		    Bind arg2 to arg1
BYE		    ( -- )		Basic    	Quit haf
CANDR	    (a -- a a)	Lisp		Return first element of list at top of stack, followed by remainder of list
CAR		    (a -- a)	Lisp		Return first element of list
CAT		    (a a -- a)	Unix		concatenate arg1 and arg2 with newline between
CDR		    (a -- a)	Lisp		Remove first element of list
CHAR		(n -- a)	Basic		Put character equivalent of arg1 on top of stack
CINT		(a -- a)	Basic		Closest Int
CLEARSTACK	(a+ -- )	Forth		Empties data stack
CLOSE		( -- )		Haf		Closes working file
COLOR
CONS		(a a -- a)	Lisp		Combines two elements into a single list
COS 
CSNG
DEFGROUP
DEPTH		( -- a)		Forth		Returns depth of stack before word is run
DESCRIBE	( -- a)		Lisp		Returns definition of word (user words only)
DIR
DROP		(a -- )		Forth		Discards element at top of stack
DUP		    (a -- a a)	Forth		Duplicates element at top of stack
EMIT		(a -- )		Forth		Prints single character represented by unicode value at top of stack
EOF
EQ		    (a a -- a)	Lisp		If arg1 and arg2 are the same, return TRUE else return FALSE
EVAL		(a -- )		Lisp		Execute element at top of stack as if entered at command line
EXEC		(a -- )		THBAS		Pass arg1 to TELEHACK, return value goes to top of stack
EXP
FALSE		(-- a)		Lisp		Return False
FALSE?		(a -- a)	Lisp		If value at top of stack is false, return true
FETCH		(a -- a)	Haf		    Read from file at line number at top of stack
GMTIME
HASADMIN
HASBADGE 
HASLOGIN 
HASROOT 
HASSYSOP 
HEIGHT
HELP		( -- )				    Print help screen
HEX
HOSTNAME
IF		    (a a -- )	Haf		    If arg1 is true, eval arg2
IFTE		(a a a -- )	Haf		    If arg1 is true, eval arg2 else eval arg3
INKEY
INPUT
INSTR
INT
LEFT 
LEN 
LITSTACK	( -- a)		Haf		    Return contents of stack as literals
LOCALTIME 
LOG 
LOG10 
MD5BASE64
MD5HEX
MID 
MODEM
MOVETO    	(x y --)	Postscript	Move cursor to x, y
N>R		    (n --)		Forth		Move n elements (not including n) to the return stack
NE		    (a a -- a)	Lisp		If arg1 and arg2 are different, return TRUE else return FALSE
NETSTAT
NEW		    (--)		THBAS		Restores environment to original state
NINT
NR>		    (n --)		Forth		Move n elements from the return stack to the data stack
NOT
OCT
OPEN    	(a --)		Haf		    Opens working file with name referenced at top of stack
OVER		(a a -- a a a)	Forth   Copy element in second postion to top of stack
OR
PEEK 
PICK        (n -- a)    Forth       Copies element at stack position n to top of stack
PLAN
POKE 
POLKEY 
PORT 
POS
PRIN1		(a --)		Lisp		Prints top of stack without a newline. Equivalent to basic PRINT FOO;
QUOTE		(a -- a)	Lisp		Quotes top of stack by adding a set of curly braces
R>		    ( -- a)		Forth		Move element at top of return stack to data stack
R@		    ( -- a)		Forth		Copy element at top of return stack to data stack
R2D
READ    	( -- a)		Haf		    Read one line from open file and put at top of stack
RE 
RE$ 
REC
REV
RIGHT 
RND
ROT		(a a a -- a a a)Forth	    Move element in 3rd position to top of stack
SCRATCH		(a -- )		THBAS	    Remove file at top of stack, prompt for confirmation
SSCRATCH	(a -- )		THBAS	    Remove file at top of stack silently
SED
SELECT		(a -- a)	SQL		    Get line from file at row# specified at top of stack
SETTRUE		(a -- )		Haf		    Make value at top of stack the new value of TRUE
SETFALSE	(a -- )		Haf		    Make value at top of stack the new value of FALSE
SGN 
SIN 
SLEEP 
SQR 
STACK		( -- a)		Forth		Put contents of stack as a single list on the top of the stack
STRING
SWAP		(a a -- a a)Forth		Swap top two elements of stack
SYSLEVEL
TAN
TIM 
TIME 
TIMER 
TYP
TRUE		(a -- a)	Lisp		Returns TRUE
TRUE?		(a -- a)	Lisp		If value at top of stack is true, return true, else return false
UNBIND		(a --)		Haf		    Remove binding from element at top of stack
UPS 
USER 
USERDICT	(-- a)		Haf		    Put list of all user words(non-primitives) at top of stack
WIDTH
WHILE
WORDS		(-- a)		Forth		Put list of all words, including primtives at top of stack. Synonym for DICT
WRITE		(a --)		Haf		    Writes top of stack to open file
