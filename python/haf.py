import re
from collections import deque
import turtle as t
import subprocess

envstack = deque()
returnstack = deque()
primitives = {'+','-','*','mod','/'} #math
primitives.update({'gt','lt','eq'}) #comparison
primitives.update({'.','describe','stack','litstack','words','sed','userdict','len','mid','depth','quote','&','eval','bind','unbind','dup','drop','swap','over','rot','>r','r@','r>','clearstack','candr','exec','inline','ifte','while','bye'}) #unsorted :)
primitives.update({'fwd','left','right','color','up','down','pos','cs','setpos','teleport','home','penup','pendown','showturtle','hideturtle','bgcolor','circle'}) #turtle graphics
#put the primitivies in some kind of logical groupings / order
quotes = {'{'} # add more later? maybe rethink commenting
dictionary = {}

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
                parse(token)

def parse(token): 
    if token.lower() in dictionary: #I expressly let you re-bind over top of primitives
           evaluate(dictionary[token.lower()])
    elif token.lower() in primitives:
           evaluateprimitive(token.lower())
    else: envstack.append(token)

def evaluateprimitive(token): # order these more logicially
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
                       arg3 = 1
                else:
                       arg3 = 0
                envstack.append(str(arg3))
        elif token == "lt":
                arg1 = int(envstack.pop())
                arg2 = int(envstack.pop())
                if arg2 < arg1:
                       arg3 = 1
                else:
                       arg3 = 0
                envstack.append(str(arg3))
        elif token == "eq":
                arg1 = envstack.pop()
                arg2 = envstack.pop()
                try:
                     envstack.append(str(int(arg2) == int(arg1)))
                except:
                       envstack.append('0')
        elif token == ".":
              print(envstack.pop())
        elif token == "&":
               arg1 = envstack.pop()
               arg2 = envstack.pop()
               envstack.append(arg2 + arg1)
        elif token == "eval":
              evaluate(envstack.pop())
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
