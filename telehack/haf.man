#HAF: a halfway decent manual by Nuxi
for version .99


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
Haf's mascot: Enid, the naked mole rat




##Introduction

Welcome to Haf, the language that's half Forth, half Lisp, and half TeleBASIC, with just a smidgen of a very obscure language called Mouse.

...why?

Well, a few reasons. Nobody had made a complete language in TeleBASIC yet. I have never designed a language. And I made up something very similar during a session with chatGPT in which I wanted to prove it didn't really understand the code it was creating. The language I made up on the spot actually seemed pretty intriguing, so I decided to implement that.

After developing Haf, I was amazed to discover that many of the design decisions I thought were unique and novel already existed in concatenative languages like Factor or Cat, or most especially Postscript. Haf is really close to Postscript without, you know, all the font stuff..

Concatenative languages are a subset of functional languages. "Concatenation is composition" is the mantra. In other words, by using a stack rather than function calls with explicit arguments, a program becomes a string of chained commands, like unix pipes, but more powerful.

If there is one thing that makes Haf different from its forebears, it is that syntax is as simple as possible. Thus it is entirely, aggressively postfix, including function binding and control structures. The only components are words and the literal markers, "{" and "}"; the alternate control notations "(" and "[" are syntactic sugar for a postfix notation. This puts Haf a bit closer to Lisp, with true code-as-data homoiconicity.

OTOH, it has mutable variables. So maybe it's less like a lisp? 

Whatever. It's super fun!

##Starting out

I will assume you have familiarity with the concept of the stack, and that of a REPL environment. You type it in, the interpreter interprets as you go.

The stack in Haf consists entirely of strings. Strings are the only data type native to Haf. (BASIC, on the other hand, has string and numeric types, and this is reflected in many of the primitive words. You're on your own interms of type checking though. More on this later.)

To put something on the stack, type it, and press return:
0>A
1>1
2>Fnord

The number next to the prompt tells you the current depth of the stack. To see what is on the stack, print it with "."
2>.
Fnord
1>.
1
0>.
A

You can combine elements on a single line, separated by spaces:
0>A 1 Fnord . . .
Fnord
1
A

What if you want to put the character "." itself on the stack? Or a full sentence? To do this, you will use curly braces {}

0>{.} {} {Wumpus toods} . . .
Wumpus toods

.

NOTE: You will need to be very careful with braces (and brackets and parens, and tildes when they show up). Three things to keep in mind.
	1) They must always match. {This is a {faulty} line and will cause cause havoc.
	2) No crossing the streams. {this (is fine ~just peachy!~ if you want ())} {this ( is} not)
	3) No spaces at the end of the literal (unless you want it there for, e.g., a literal space) { } is fine, but {DUP } will cause issues if you are using recursive code


At this point you should probably type .w to see a list of all the words available to you. Commands, hereafter called words, in Haf are case-independant; cat or CAT or cAt would all work. .w will show all the words in Haf's dictionary. You can see it comes with a lot, and unless I've had a lot of time on my hands, it's in no particular order. Many should look familiar though, as they have been taken directly from TeleBASIC.

You can do math:

0>1 3 + . 
4
0>10 3 % .
1

or string manipulation:

0>{Wumpus toods} 5 RIGHT UPS .
TOODS

or th commands:

0>ls exec .
advent.gam    againstip.txt    basic.man
(rest of directory listing omitted)


Haf handliy shows you the stack depth in the prompt, but sometimes you'll want to use the depth of the stack in your code:
3>DEPTH
4>.
3

and you can clear the stack with CLEARSTACK
3>CLEARSTACK
0>

##Stack Manipulation

If you know (or have a passing familiarity with) Forth, you can probably skip this chapter.

There are five basic stack manipulation words: DUP DROP SWAP OVER ROT

Let's look at them in turn, but first we'll need to look at how to read a stack definition:

DUP (a -- aa)

this shows that DUP takes 1 element from the stack, and puts 2 back on. I will use a b c for most definitions, but will use n when basic requires a number, for instance:

+ (n n -- n)

On to the definitions:

DUP (a -- aa) - duplicates the top of the stack
DROP (a --) - removes the item at the top of the stack
SWAP (ab -- ba) - swaps top two elements of the stack
OVER (ab -- aba) - takes the element in the second position and copies it to the top of the stack
ROT (abc -- bca) - moves the item in the third position to the top of the stack

0>3 DUP + .
6

0>CLEARSTACK Fiddle Dee Dee ROT . DEPTH .
Fiddle
2

There are actually two more, PICK and ROLL, but they are generally only used in extreme circumstances. So extreme I've yet to implement ROLL, you you're stuck with PICK.

PICK (n -- a) - Choose the Nth element from the top of stack, and place at top of stack. 0 PICK is equivalent to DUP, 1 PICK is equivalent to OVER. On error, PICK returns an empty string.

##Loops & conditionals

There are two different ways to represent both loops and conditionals. First we will look at the "pure" postfix method.

There are two conditionals, IFTE and IF:

IFTE (a a a --) - IFTE takes three parameters, the third item on the stack is a boolean, if true, the second from the top is executed, if false, the top is executed

0>TRUE {{I'm the true case} .} {{I'm the false case} .} IFTE
I'm the true case

IF (a a--) - IF takes two parameters, if the boolean at the top of the stack is true, the word in the second spot is executed
>FALSE {{I'm the true case} .} IF
(nothing happens)

There is only one looping command, WHILE.

WHILE (a a--a) - While takes the element in the second position, if it is not false it executes the code in the top position, with the test value placed at the top of the stack before execution, repeating until the condition is false
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

0>TRUE {{Enter password} PRIN1 INPUT Swordfish NE} WHILE {You're in!} .
Enter password?Password
Enter password?12345
Enter password?Swordfish
You're in!

PRIN1 (a --) - pops the top of the stack, prints it without a newline. Equivalent to basic PRINT FOO;
NE (a a--a) - Not equal, returns a boolean value if the two are not equal

As I mentioned previously, I've added a bit of syntactic sugar by way of alternate notation. Square brackets [] can denote a conditional:
0>TRUE [{Only display if true} .]
Only display if true

Parentheses denote a loop:
0>10 (1 - DUP .)
9
8
7
6
5
4
3
2
1

##Bind / eval

Thusfar we've done a lot of REPL interaction, but nothing persistent. Nothing that looks like a program. For that, we will need a new word: BIND

BIND (a a --) - binds the second element to the name at the top of the stack

Let's watch the behavior a bit:
0>3 THREE BIND
0>three .
3
0>{ThReE} DESCRIBE .
3

DESCRIBE (a -- a) - shows the value bound to the word at the top of the stack

Wait, why did that last example need braces? It's because otherwise you wouldn't get the definition of THREE, you'd get the definition of 3. This will be important later.

0>4 {THREE} BIND
0>THREE .
4

Yeah, they're mutable. Mut 'em all you want. Also, BIND is global in scope (I may add the ability to do local scoping later). Now, what would happen if you didn't quote THREE here?
0>5 THREE BIND
0>THREE .
5

Well. No problem then.

0>.U
CONS TRUE? FALSE? IF CLEARSTACK PRINTLN CAR CDR .D .S .U .L .B ` CAT THREE 4

.U (--) Prints all the defined (not primitive) words in the dictionary, including built-ins

Oops. You can bind numbers, even rebind over primitives if you want (though you can't unbind them). Speaking of which, better clean up after ourselves:

0>{THREE} UNBIND
0>THREE .
THREE
0>{4} UNBIND
0>.U
CONS TRUE? FALSE? IF CLEARSTACK PRINTLN CAR CDR .D .S .U .L .B ` CAT

UNBIND (a --) removes word at the top of the stack from the dictionary

So big deal, you've got a weird way to make variables. But wait, let's have a look at that USERDICT again. IF? CLEARSTACK? Yes, you can bind anything to a word, including code. Let's look.


0>{CLEARSTACK} DESCRIBE . 
~a+ --~ DEPTH {DROP DROP DEPTH} WHILE
0>{CONS} DESCRIBE .
~a a -- a~ SWAP { } & SWAP &


So let's try it out. Here's a simple program:
0>{~n -- n~ DUP * } SQUARE BIND
0>4 SQUARE
16

~ ... ~ , in case you didn't realize, denotes comments. It's always a very good idea to put the stack notation in your comments for future reference. Why ~~ and not () like in Forth? Because nested parens are easier to parse, so I saved them for loops. Also, [], (), and ~~ were the elements borrowed from Mouse, a language, and book that was my first introduction to how interpreters worked.

And another:

0>{~n -- n~ DUP 1 > {DUP 1 - !} {1} IFTE *} ! bind
0>5 ! .
120

or tail recursively:
0>{~n -- n~ over 1 eq {swap drop} {over * swap 1 - swap !} IFTE} {!} bind
0>5 ! .
120

You can also do shell commands via EXEC:
0>{~a --~ exec dup len 1 - left .}} ! bind ~gets rid of trailing newline~
0>{~ --~ {cls} !} cls bind
0>cls
(clears screen)

0>{~a -- a~ {chess /move=} swap & operator cons !} {ch} bind
0>d5d7 ch
(chess program output omitted}

Now something a bit more elaborate:

0>{~ -- a~ {what is your secret password?} println input} get-password bind
0>{~a a -- n~ over len over len / int 1 +} get-mask-length bind
0>{~a -- a~ get-mask-length swap string} make-mask bind
0>{~ a a -- a~ over len left} trim-mask bind
0>{~a a -- a~ xor} encode bind
0>{~a -- a~ get-password make-mask trim-mask encode} secure-text bind

A good Haf program is usually made of lots of tiny words. These words, when strung together, describe what your program does: get password, make mask, trim mask, encode. There's no screen editor, but by keeping them short, the input history buffer is usually suffient for editing. Just don't forget to quote the word if you're re-binding. This approach also makes it easy to add features. xor is pretty stupid as an encryption method, but it works as a placeholder. Now you can build up the encode word to nest the real method as you develop it.

Also, there is a limit to how many words you can have in a single program. Nesting words within words allows you to have more complicated programs.


There's one more concept I want to introduce, and that's EVAL.

EVAL (a -- ?) Eval pops the stack, and then evaluates the string as if it had been typed at the command line. This is an incredibly powerful ability, that I will not go into much here. But here's some examples:

0>1 EVAL .
1

(numbers and strings always eval to themselves unless they've been bound)

0>{THREE BLIND MICE} EVAL . . .
MICE
BLIND
THREE

0>{3 4 fnord} fnord {+} gi SED EVAL .
7

Eval lets you treat data just like code, and vice versa. So your program can create code and then run it on the fly.

0>4 {SQUARE} DESCRIBE {\*} {+} {} gi SED EVAL . ~turn square into double~
8

SED (abcd -- a) regex-based replacement tool, replaces substring "b" in string "a" with substitution "c"according to options "d" per TH_SED$ in thbas. see also RE, RE$



##Return stack functions

There are five more stack words to introduce (again, if you know Forth, feel free to skip this bit).

These words are a bit different than the others, because they deal with the return (or environment) stack. They go here at the end because they can be dangerous, but they're also a way to handle temporary values without binding them. The most important thing to remember is that, unlike traditional stack, *you must end the word with no changes to the return stack*. If you add an element to the return stack, you'd better remove it when you're done. In addition, they're only active locally within the current "depth" of branching, making this sort of a local stack.

>R (a -- ) moves an element from the stack to the return stack
R> ( -- a) moves an element from the return stack to the stack
R@ ( -- a) copies an element from the return stack to the stack
N>R (a n -- ) moves n elements from the stack to the return stack
NR> ( -- a) moves number of elements specified in the top return stack value from the return stack to the stack

0>ONE TWO THREE 3 (>R . R> 1 -)
THREE
TWO 
ONE


Here's factorial again, non-recursively

0>{~n -- 1 ... n~ (dup 1 -)} countdown bind
0>{~n ... n -- n~ (>R * R> 1 -)} multimultiply bind
0>{~n -- n~ dup >R countdown R> 1 - multimultiply} ! bind
0>5 !
120

##CANDR (pronounced candor)

Now it's time for the Lisp fans. CANDR is a contraction of CAR AND CDR, but be careful -- it should not be confused with CADR (which is not implemented anyway). Instead, CANDR takes the CAR (sorta) and the CDR (also sorta) and puts them both on the stack. CONS, which you probably already noticed, is also present, and also (sorta) works like Lisp.

For those of you who have no idea what the above paragraph meant, let's explain.

CANDR (a -- a a) returns the first element of the list on the top of the stack, the remainder of the list in the second spot

0>{{this is my nested} list} CANDR . .
{this is my nested}
list

CAR (a -- a) returns the first element of the list as the top of the stack
0>{1 2 3 4} CAR .
1


CDR (a -- a) returns everything but the first element of the list as the top of the stack
0>{1 2 3 4} CDR .
2 3 4

CONS (a a -- a) combines top two elements on the stack into a list (i.e., concatenates them with a space)
0>FOO 
1>BAR 
2>BAZ CONS CONS .
FOO BAR BAZ

## Meta-stack commands, creating higher-order functions MAP and REDUCE

You already know CLEARSTACK and DEPTH, but there are a few other commands that address the stack as a unit, namely STACK and LITSTACK. These are very similar, but with one imporant difference.

STACK (* -- *a) place the entire contents of the stack as a list on the top of the stack
LITSTACK (* -- *a) place the entire contents of the stack as a list of quoted elements at the top of the stack

STACK is useful if you just want to quickly view what's on the stack, or quickly concatenate the whole stack. LITSTACK is more useful when you want to save the contents and restore them later.

0>1 2 3 {+} STACK .
1 2 3 +
0>1 2 3 {+} STACK >R CLEARSTACK >R EVAL STACK .
1 5

0>1 2 3 {+} LITSTACK .
{1} {2} {3} {+}
0>1 2 3 {+} LITSTACK >R CLEARSTACK >R EVAL STACK .
1 2 3 +

Let's look at some of the very powerful things we're now able to do by freezing the state of the stack, stashing it somewhere, and then bringing it back:

{>r eval r> depth 2 - {>r >r r@ eval r> r> 1 -} while drop} {reduce-func} bind
{depth 2 - {>r >r litstack >r clearstack 3 nr> 2 pick 3 n>r drop reduce-func r> swap >r eval drop r>} {reduce-func} ifte} {reduce} bind ~the last drop is due to a bug~

REDUCE (aa - a), sometimes called fold, is a common higher-order function in functional languages. It will repeatedly apply a function to (in our case) a list, accumulating until a single result is acheived. For example:

0>{1 2 3} {+} REDUCE .
6

By using the meta-stack commands, we are able to implement reduce via stack commands, as if it had its own local stack. See how it respects the original stack:

0>HEY THERE
2>{1 2 3} {+} REDUCE
3>.S
HEY THERE 6

Let's REDUCE a function to get the maximum value of a list. Our implementation of REDUCE takes two values at a time and applies the function, so this should be easy:

0>{1 2 4 5 2} {>} REDUCE
0

Uh-oh. The greater-than function returns a binary truth value, not a result. Clearly we will need to create and bind a new word, MAX, to get the larger of two values. Except in Haf, words are just substitutions. So if we don't need to use that max function anywhere else, we can put it right in:

0>{1 2 5 4 2} {over over > {drop} {swap drop} ifte} REDUCE .
5

There's some advanced stuff hidden in here, but for our intents and purposes, you should focus on the fact that *sometimes* you will want to create new words, *sometimes* you won't. Clarity, repetition, reuse, are all factors.

Now if you are familiar already with REDUCE or fold, you may wonder, can we create a MAP? Yep!

{>r eval r@ eval r> depth 2 - {>r >r swap r@ eval swap cons r> r> 1 -} while drop} {map-func} bind
{depth 2 - {>r >r litstack >r clearstack 3 nr> 2 pick 3 n>r drop map-func swap >r eval drop r>} {map-func} ifte} {map} bind ~last drop is due to a bug~

MAP (aa -- a) MAP takes a function and applies it to each element of a list. The function must take a single argument and return a single value (i.e. have a stack notation of the form (a -- a)

0>{1.3 3.9 5.7} {INT} MAP
{1 3 5}

0>{yes I could have done this example without map by treating it as a string} {UPS} MAP .
YES I COULD HAVE DONE THIS EXAMPLE WITHOUT MAP BY TREATING IT AS A STRING

0>{{3 4 +} {8 9 *}} {EVAL -1 *} MAP
-7 -72


##Abbreviations

There are several common abbreviated commands provided as built-ins, namely ` and the dot-commands.

` (a --} equivalent to BIND, and quicker to type
.D (a --) DESCRIBE .
.L ( -- ) LITSTACK .
.S ( -- ) STACK .
.U ( -- ) USERDICT .
.W ( -- ) WORDS .


## Sample program
Here's an example of much of what we have learned in action, a simple generative grammar:

{{ } 1 1 RE 1 +} count-words bind
{rnd int} rand bind
{(>R cdr R> 1 -)} {space-split} bind
{count-words rand space-split car} rand-word bind
{determiner-list dup rand-word adjective-list dup rand-word noun-list dup rand-word cons cons} noun-phrase bind
{noun-phrase verb-list dup rand-word noun-phrase cons cons} sentence bind
{{pigeon pickle tood paperclip Kardashian}} noun-list bind
{{eats unleashes tickles hacks questions}} verb-list bind
{{a the}} determiner-list bind
{{cranky yellow happy tall stanky burbling}} adjective-list bind

0 >sentence .
a stanky Kardashian unleashes the yellow tood


## One Liners

{.+? swap & .+ & {} 1 re$ .} {grep} ` ~only finds first occurrence of a pattern, though~
2024561111 (1 + dup dial swap cons exec .) ~wardialler~
{{rlogin} swap cons exec .} {rlogin} `
{{{{@} swap cons exec .} {@} `} @ rot gi sed eval} {cmdarg} ` ~macro to create commands with arguments as above~
{0 userdict (candr dup describe swap { : } & swap  & .)} {describe-all} ` ~show all currently bound words and definitions~


## File handling 

Haf accepts a single filename as a command line argument to be loaded and excecuted as if typed in at the prompt. e.g.,
haf relshell.haf

Haf, for now, only handles one open file at a time.  Future versions may change file-handling. But in the version on pub there are the following commands:

OPEN (a --) Opens working file with name referenced at top of stack
CLOSE ( -- ) Closes working file
APPEND (a -- ) Opens working file for appending with name referenced at top of stack
WRITE (a --) Writes top of stack to open file
READ ( -- a) Read one line from open file and put at top of stack
UPDATE (a a--) put record second from top in file row # delcared at top of stack
SELECT (a -- a) get line from row # specified at top of stack


if you want to build in a method to save and load words, you could use something like this:

0>{dup describe quote swap cons {bind} cons write} save-word `
0>{read eval} load-word `

0>backup.haf open
0>{square} save-word
0>close
0>backup.haf append
0>{save-word} save-word
0>close 

QUOTE (a -- a) put literal markers {} around item at top of the stack. Needed e.g., to overcome greedy evaluation

## Full dictionary

  

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
<		    (n n -- a)	Math		If arg 1 < arg 2, return TRUE, else return FALSE
=		    (n n -- a)	Math		If arg 1 = arg 2, return TRUE, else return FALSE
>		    (n n -- a)	Math		If arg 1 > arg 2, return TRUE, else return FALSE
>R		    (n -- )		Forth		Move value at top of stack to return stack
^		    (n n -- n)	Math		Exponentation
`		    (a a -- )	Haf		    Bind arg1 to arg2. Synonym for BIND
AND		    (a a -- a)	THBAS		Bitwise AND
APPEND      (a -- )		Haf		    Opens working file for appending with name referenced at top of stack
ASC
ATN
B64E 
B64D
BIN
BIND	    (a a -- )	Haf		    Bind arg1 to arg2. Synonym for `
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
TH_TIME
TIM 
TIME 
TIMER 
TYP
TRUE		(a -- a)	Lisp		Returns TRUE
TRUE?		(a -- a)	Lisp		If value at top of stack is true, return true, else return false
UUD 
UUE 
UNBIND		(a --)		Haf		    Remove binding from element at top of stack
UPDATE		(a a-- )	SQL		    Store text at second position at line # of file specified at top of stack
UPS 
USER 
USERDICT	(-- a)		Haf		    Put list of all user words(non-primitives) at top of stack
WIDTH
WHILE
WORDS		(-- a)		Forth		Put list of all words, including primtives at top of stack. Synonym for DICT
WRITE		(a --)		Haf		    Writes top of stack to open file
