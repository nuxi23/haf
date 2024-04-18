import re
import os
from collections import deque
import turtle as t
import subprocess

envstack = deque()
returnstack = deque()

quotes = {'{'} # add more later? maybe rethink commenting

#put the primitivies in some kind of logical groupings / order
primitives = {'+','-','*','mod','/'} #math
primitives.update({'gt','lt','eq'}) #comparison
primitives.update({'prin1','.','input','cls'}) #I/O
primitives.update({'ifte','while'}) #control
primitives.update({'dup','drop','swap','over','rot','>r','r@','r>','clearstack','reverse','depth','stack','litstack'}) #stack manipulation
primitives.update({'sed','len','mid','&','chr','ord'}) #strings
primitives.update({'exec','inline'}) #system interface
primitives.update({'describe','words','userdict','eval','bind','unbind','candr','bye'})
primitives.update({'fwd','left','right','color','up','down','pos','cs','setpos','teleport','home','penup','pendown','showturtle','hideturtle','bgcolor','circle'}) #turtle graphics


dictionary = { # here come the built-in words
'.'           :      'prin1 10 chr prin1',
'`'           :      'swap bind',
'cons'        :      '{} swap & &',
'car'         :      'candr swap drop',
'cdr'         :      'candr drop',
'if'          :      '{} ifte',
'quote'       :      '123 chr swap 125 chr & &',
'.d'          :      'describe .',
'.l'          :      'litstack .',
'.s'          :      'stack .',
'.u'          :      'userdict .',
'.w'          :      'words .'
}

def main():
       while True:
              read()

def read():
        prompt = str(len(envstack)) + '>'
        readline = input(prompt)
        evaluate(readline)

def matchquotes(line):
      depth = 0          
      pos = 0
      for element in line:
            if element == '{':
                  depth += 1
            if element == '}':
                  depth -= 1
            if depth == 0:
                  break
            pos += 1
      return pos

def evaluate(readline):
    while len(readline) > 0:
        if readline[:1] in quotes: #do we have a quote?
                pos = matchquotes(readline)
                envstack.append(readline[1:(pos)]) #once we've found the full, nested quote, stick it on the stack
                readline = readline[(pos + 1):].strip() 
        else:
                token, separator, readline = readline.partition(' ')    
                parse(token) #why is this even its own function? Because I said so, that's why.

def parse(token): 
    if token.lower() in dictionary: #I expressly let you re-bind over top of primitives
           evaluate(dictionary[token.lower()]) #token has been defined, do its thing
    elif token.lower() in primitives: #token is a primitive, execute the primitive
           evaluateprimitive(token.lower())
    else: envstack.append(token) #neither dictionary nor primitive be. On the stack I go.

def evaluateprimitive(token): # re-order to match above
    try:
        if token == "+":
                arg1 = envstack.pop()
                arg2 = envstack.pop()
                try:
                     envstack.append(str(int(arg2) + int(arg1)))
                except:
                       envstack.append('0') #replace with flexible false?
        elif token == "-":
                arg1 = envstack.pop()
                arg2 = envstack.pop()
                try:
                     envstack.append(str(int(arg2) - int(arg1)))
                except:
                       envstack.append('0')
        elif token == "*":
                arg1 = envstack.pop()
                arg2 = envstack.pop()
                try:
                     envstack.append(str(int(arg2) * int(arg1)))
                except:
                       envstack.append('0')
        elif token == "mod":
                arg1 = envstack.pop()
                arg2 = envstack.pop()
                try:
                     envstack.append(str(int(arg2) // int(arg1)))
                except:
                       envstack.append('0')
        elif token == "/":
                arg1 = envstack.pop()
                arg2 = envstack.pop()
                try:
                     envstack.append(str(int(arg2) / int(arg1)))
                except:
                       envstack.append('0')
        elif token == "gt":
                arg1 = int(envstack.pop())
                arg2 = int(envstack.pop())
                if arg2 > arg1:
                       arg3 = '1'           # truth values should really come from setfalse
                else:
                       arg3 = '0'
                envstack.append(arg3)
        elif token == "lt":
                arg1 = int(envstack.pop())
                arg2 = int(envstack.pop())
                if arg2 < arg1:
                       arg3 = '1'
                else:
                       arg3 = '0'
                envstack.append(arg3)
        elif token == "eq":
                arg1 = envstack.pop()
                arg2 = envstack.pop()
                try:
                     envstack.append(str(int(arg2) == int(arg1)))
                except:
                       envstack.append('0')
        elif token == "prin1":
              print(envstack.pop(),end='')
        elif token == "&":
               arg1 = envstack.pop()
               arg2 = envstack.pop()
               envstack.append(arg2 + arg1)
        elif token == "eval":
              evaluate(envstack.pop())
        elif token == "cls":
              os.system('cls')
        elif token == "bind":
              arg1 = envstack.pop()
              arg2 = envstack.pop()
              dictionary[arg2] = arg1
        elif token == "unbind":
               arg1 = envstack.pop()
               try:
                      del dictionary[arg1]
               except: pass
        elif token == "dup":
              arg1 = envstack.pop()
              envstack.append(arg1)
              envstack.append(arg1)
        elif token == "drop":
              envstack.pop()
        elif token == "drop":
              envstack.reverse()
        elif token == "swap":
              arg1 = envstack.pop()
              arg2 = envstack.pop()
              envstack.append(arg1)
              envstack.append(arg2)
        elif token == "exec":
              arg1 = envstack.pop()
              proc = subprocess.Popen(arg1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
              o, e = proc.communicate()
              envstack.append(o.decode('ascii'))
        elif token == "inline":
              arg1 = envstack.pop()
              envstack.append(eval(arg1))
        elif token == "chr":
              arg1 = envstack.pop()
              envstack.append(chr(int(arg1)))
        elif token == "str":
              arg1 = envstack.pop()
              envstack.append(str(ord(arg1)))
        elif token == "ifte":
               arg1 = envstack.pop()
               arg2 = envstack.pop()
               arg3 = envstack.pop()
               if arg3 != '0': #replace with definable false
                      evaluate(arg2)
               else:
                      evaluate(arg1)
        elif token == "while":
              arg1 = envstack.pop()
              arg2 = envstack.pop()
              while arg2 !='0': #replace with definable false
                     envstack.append(arg2)
                     returnstack.append(arg1)
                     evaluate(arg1)
                     arg1 = returnstack.pop()
                     arg2 = envstack.pop()
        elif token == "over":
               arg1 = envstack.pop()
               arg2 = envstack.pop()
               envstack.append(arg2)
               envstack.append(arg1)
               envstack.append(arg2)
        elif token == "rot":
               arg1 = envstack.pop()
               arg2 = envstack.pop()
               arg3 = envstack.pop()
               envstack.append(arg2)
               envstack.append(arg1)  
               envstack.append(arg3)
        elif token == "candr":
                arg1 = envstack.pop()
                if arg1[:1] in quotes:
                        pos = matchquotes(arg1)
                        envstack.append(arg1[(pos + 1):].strip()) #push cdr
                        envstack.append(arg1[1:(pos)]) #push car
                else:
                       arg1, arg2 = arg1.split(maxsplit=1)
                       envstack.append(arg2)
                       envstack.append(arg1)
        elif token == ">r":
              arg1 = envstack.pop()
              returnstack.append(arg1)
        elif token == "r@":
              arg1 = returnstack.pop()
              returnstack.append(arg1)
              envstack.append(arg1)
        elif token == "r>":
              arg1 = returnstack.pop()
              envstack.append(arg1)
        elif token == "clearstack":
               envstack.clear()
        elif token == "input":
               input(arg1)
               envstack.append(arg1)
        elif token == "quote":
               arg1 = envstack.pop()
               envstack.append("{" + arg1 + "}")
        elif token =="depth":
               arg1 = len(envstack)
               envstack.append(str(arg1))
        elif token =="mid":
               arg1 = envstack.pop()
               arg2 = envstack.pop()
               arg3 = envstack.pop()
               try:
                     envstack.append(arg3[int(arg2):int(arg2) + int(arg1)])
               except:
                     envstack.append('')
               
        elif token =="len":
               arg1 = envstack.pop()
               envstack.append(str(len(arg1)))  
        elif token == "describe":
               arg1 = envstack.pop()
               if arg1.lower() in dictionary:
                      envstack.append(dictionary[arg1.lower()])
               else:
                      envstack.append(arg1)
        elif token == "sed":
               arg1 = envstack.pop()
               arg2 = envstack.pop()
               arg3 = envstack.pop()
               envstack.append(re.sub(arg2,arg1,arg3))
        elif token == "userdict":
               envstack.append(' '.join(dictionary.keys()))
        elif token == "words":
               envstack.append(' '.join(primitives) + ' ' + ' '.join(dictionary.keys()))
        elif token == "stack":
               arg1 = ' '.join(map(str, envstack))
               envstack.append(arg1)
        elif token == 'litstack':
               arg1 = ' '.join(f'{{{item}}}' for item in envstack)
               envstack.append(arg1)
       #ups, lc, and, or not, xor
        elif token == "bye":
              quit()

#turtle graphics!
        elif token == "fwd":
                arg1 = int(envstack.pop())
                t.forward(arg1)
        elif token == "left":
                arg1 = int(envstack.pop())
                t.left(arg1)
        elif token == "right":
                arg1 = int(envstack.pop())
                t.right(arg1)
        elif token == "up":
                t.up()  
        elif token == "down":
                t.down() 
        elif token == "cs":
                t.clearscreen()  
        elif token == "color":
                arg1 = envstack.pop()
                t.color(arg1)
        elif token == "pos":
                envstack.append(t.pos())
        elif token == "setpos":
               arg1 = int(envstack.pop())
               arg2 = int(envstack.pop())
               t.setpos(arg2,arg1)
        elif token == "teleport":
               arg1 = int(envstack.pop())
               arg2 = int(envstack.pop())
               t.teleport(arg2,arg1)
        elif token == "home":
               t.home()
        elif token =="penup":
               t.penup()
        elif token =="pendown":
               t.pendown()
        elif token =="showturtle":
               t.showturtle()
        elif token =="hideturtle":
               t.hideturtle
        elif token =="circle":
               arg1 = int(envstack.pop())
               t.circle(arg1)
        elif token =="bgcolor":
               arg1=envstack.pop()
               t.bgcolor(arg1)

                                                                         
        else:
               print("oops")
    except IndexError:
        print("Stack Underflow")


if __name__ == "__main__":

    main()
