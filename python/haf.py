import re
import math
import os
from collections import deque
import turtle as t
import subprocess

envstack = deque()
returnstack = deque()

quotes = {'{'} # add more later? maybe rethink commenting

#put the primitivies in some kind of logical groupings / order
primitives = {'+','-','*','%','/'} #math
primitives.update({'gt','lt','eq'}) #comparison
primitives.update({'ifte','while'}) #control
primitives.update({'drop','swap','>r','r@','r>','n>r','nr>'}) #stack manipulation
primitives.update({'sed','mid','&'}) #strings
primitives.update({'exec','inline'}) #system interface
primitives.update({'describe','bind','unbind','candr'})


dictionary = { # here come the built-in words
'.'           :      'prin1 10 chr prin1',
'`'           :      'swap bind',
'abs'         :      'abs( swap & )  & inline', #python has eval, so we can go hog-wild
'bye'         :      'quit() inline',
'cons'        :      '{} swap & &',
'cat'         :      '10 chr swap & &',
'car'         :      'candr swap drop',
'cdr'         :      'candr drop',
'chr'         :      'chr(int( swap & )) & inline',
'clearstack'  :      'envstack.clear() inline drop',
'cls'         :      'os.system("cls") inline drop',
'dup'         :      '>r r@ r>',
'eval'        :      'evaluate(envstack.pop()) inline drop',
'emit'        :      'chr prin1',
'if'          :      '{} ifte',
'input'       :      'input() inline',
'int'         :      'math.floor( swap & ) & inline',
'left'        :      '0 swap mid',
'len'         :      'len(envstack) inline',
'litstack'    :      '{" ".join(f"{{{item}}}" for item in envstack)} inline',
'ord'         :      'chr(int( swap & )) & inline',
'prin1'       :      'print(envstack.pop(),end="") inline drop',
'quote'       :      '123 chr swap 125 chr & &',
'over'        :      '1 pick',
'pick'        :      'dup >r envstack.rotate( swap & ) & inline drop dup r> swap >r -1 * envstack.rotate( swap & ) & inline drop r>',
'reverse'     :      'envstack.reverse() inline drop',
'roll'        :      'dup >r envstack.rotate( swap & ) & inline drop r> swap >r -1 * envstack.rotate( swap & ) & inline drop r>',
'rot'         :      '2 roll',
'stack'       :      '{" ".join(map(str, envstack))} inline',
'userdict'    :      '{" ".join(dictionary.keys())} inline',
'words'       :      '{" ".join(primitives) + " " + " ".join(dictionary.keys())} inline',
'r>'          :      '1 nr>',
'>r'          :      '1 n>r',
'.d'          :      'describe .',
'.l'          :      'litstack .',
'.s'          :      'stack .',
'.u'          :      'userdict .',
'.w'          :      'words .',
't.fwd'       :      't.forward(int(envstack.pop())) inline drop',
't.left'      :      't.left(int(envstack.pop())) inline drop',
't.right'     :      't.right(int(envstack.pop())) inline drop',
't.circle'    :      't.right(int(envstack.pop())) inline drop',
't.color'     :      't.color(envstack.pop()) inline drop',
't.bgcolor'   :      't.color(envstack.pop()) inline drop',
't.up'        :      't.up() inline drop',
't.down'      :      't.down() inline drop',
't.home'      :      't.home() inline drop',
't.showturtle':      't.showturtle() inline drop',
't.cls'       :      't.clearscreen() inline drop',
't.hideturle' :      't.hideturtle() inline drop',
't.pos'       :      't.pos() inline',
't.setpos'    :      't.setpos( roll & , & swap & ) & inline drop',
't.teleport'  :      't.teleport( roll & , & swap & ) & inline drop'
}

def main():
       while True:
              readline = input(str(len(envstack)) + '>')
              evaluate(readline)

def matchquotes(line):
      depth = pos = 0
      for element in line:
            if element == '{': depth += 1
            if element == '}': depth -= 1
            if depth == 0: break
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
                if token.lower() in dictionary: #I expressly let you re-bind over top of primitives
                     evaluate(dictionary[token.lower()]) #token has been defined, do its thing
                elif token.lower() in primitives: #token is a primitive, execute the primitive
                     evaluateprimitive(token.lower())
                else: envstack.append(token) #neither dictionary nor primitive be. On the stack I go.

def evaluateprimitive(token): # re-order to match above
    try:
        if token == "+":
                try:
                     envstack.append(str(int(envstack.pop()) + int(envstack.pop())))
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
                try:
                     envstack.append(str(int(envstack.pop()) * int(envstack.pop())))
                except:
                       envstack.append('0')
        elif token == "%":
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
        elif token == "&":
               arg1 = envstack.pop()
               arg2 = envstack.pop()
               envstack.append(arg2 + arg1)
        elif token == "bind":
              arg1 = envstack.pop()
              arg2 = envstack.pop()
              dictionary[arg2.lower()] = arg1
        elif token == "unbind":
               arg1 = envstack.pop()
               try:
                      del dictionary[arg1]
               except: pass
        elif token == "drop":
              envstack.pop()
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
              envstack.append(str(eval(arg1)))
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
        elif token == "n>r":
              arg1 = envstack.pop()
              for i in range(int(arg1)):
                     arg2 = envstack.pop()         
                     returnstack.append(arg2)
        elif token == "r@":
              arg1 = returnstack.pop()
              returnstack.append(arg1)
              envstack.append(arg1)
        elif token == "nr>":
              arg1 = envstack.pop()
              for i in range(int(arg1)):
                     arg2 = returnstack.pop()
                     envstack.append(arg2)
        elif token =="mid":
               arg1 = envstack.pop()
               arg2 = envstack.pop()
               arg3 = envstack.pop()
               try:
                     envstack.append(arg3[int(arg2):int(arg2) + int(arg1)])
               except:
                     envstack.append('')
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
                                                                         
        else:
               print("oops")
    except IndexError:
        print("Stack Underflow")


if __name__ == "__main__":

    main()
