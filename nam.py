import sys
import core, reader, printer, nam_types as types
from env import Env

def EVAL(sexp, env):
    le = False
    while True:
        #print("EVAL ", printer._pr_str(sexp))
        while env.find(sexp):
            #print("-- rule", printer._pr_str(sexp))
            le = False
            if types._listP(sexp):
                right = env.get(sexp)
                left  = env.get_left(right)
                locs  = []

                #print("====", printer._pr_str(left), printer._pr_str(right))
                for i in range(len(left)):
                    if types._symbolP(left[i]):
                        locs.append([left[i], EVAL(sexp[i], env)])
                if locs:
                    env = Env(env)
                    for loc in locs:
                        env.set(loc[0], loc[1])
                sexp = right
            else:
                sexp = env.get(sexp)
                
        #else: print("---- replaced", printer._pr_str(sexp))
        if not types._listP(sexp):
            return sexp

        a0 = sexp[0]

        if "rule" == a0:
            return env.set(EVAL(sexp[1], env), EVAL(sexp[2], env))
        elif "global" == a0:
            return env.set_glob(EVAL(sexp[1], env), EVAL(sexp[2], env))
        elif "local" == a0:
            a1   = sexp[1]
            sexp = sexp[2]
            env  = Env(env)
            env.set(EVAL(a1[0], env), EVAL(a1[1], env))
        elif "quote" == a0:
            return sexp[1]
        elif "filler" == a0:
            return types._symbol(sexp[1])
        elif not le:
            #print("==============================================")
            sexp = types._list(*map(lambda a: EVAL(a, env), sexp))
            le = True
        elif callable(a0):
            sexp = a0(*sexp[1:])
            le = False

        else: return sexp

env = Env()
for rule in core.syms:
    env.set_glob(rule[0],rule[1])
    
def REP(str):
    return printer._pr_str(EVAL(reader.read_str(str), env))

# if-else
print(REP("(rule (if 1 (filler true-body) (filler false-body)) \
                 true-body)"))
print(REP("(rule (if 0 (filler true-body) (filler false-body)) \
                 false-body)"))

print(REP("(if 1 да нет)"))
print(REP("(if 0 да нет)"))

# custom sintaxis, infix +
print(REP("(rule ((filler x) inf+ (filler y)) \
                 '(+ x y))"))
print(REP("(10 inf+ 20)"))

# recursion, does not work
#print(REP("(rule (factorial (filler x)) \
#                 '(* x (factorial (- x 1))))"))
#print(REP("(rule '(factorial 0) 1)"))

#print("----------------------------------------------")

#print(REP("(factorial 1)"))

# loop, does not work
#print(REP("(rule (while (filler cond) (filler body))  \
#                 '(rule (while 1 (filler lala)) \
#                        (while cond body)))"))

#print("----------------------------------------------")

#print(REP("(rule x 5)"))
#print(REP("(while x (rule 'x (- x 1)))"))

#print(REP("(+ 1 (+ 2 (+ 3 4)))"))
#print(REP("(* 3 (* 2 (* 1 1)))"))
