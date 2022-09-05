import sys
import core, reader, printer, nam_types as types
from env import Env

def EVAL(sexp, env):
    le = False
    while True:
        #print("EVAL ", printer._pr_str(sexp))
        while env.find(sexp):
            #print("-- rule", printer._pr_str(sexp))
            if types._listP(sexp):
                right = env.get(sexp)
                #print("---- right", printer._pr_str(right))
                left  = env.get_left(right)
                locs  = []

                #print("===", left, right)
                for i in range(len(left)):
                    if types._symbolP(left[i]):
                        locs.append([left[i], sexp[i]])
                if locs:
                    env = Env(env)
                    for loc in locs:
                        env.set(loc[0], loc[1])
                sexp = right
                #break
            else:
                sexp = env.get(sexp)

        if not types._listP(sexp):
            return sexp

        a0 = sexp[0]

        if "rule" == a0:
            res1, res2 = EVAL(sexp[1], env), EVAL(sexp[2], env)
            return env.set(res1, res2)
        elif "quote" == a0:
            return sexp[1]
        elif "local" == a0:
            a1 = sexp[1]
            lr = EVAL(a1[0], env)
            rr = EVAL(a1[1], env)

            sexp = sexp[2]
            env  = Env(env)
            env.set(lr, rr)
        elif "filler" == a0:
            a1 = sexp[1]
            return types._symbol(a1)
        elif not le:
            #print("----------------------------------------------")
            sexp = types._list(*map(lambda a: EVAL(a, env), sexp))
            le = True
        elif callable(a0):
            args = types._list(*map(lambda a: EVAL(a, env), sexp[1:]))
            sexp = a0(*args)

        else:
            return sexp

env = Env()
for rule in core.syms:
    env.set(rule[0],rule[1])
    
def REP(str):
    return printer._pr_str(EVAL(reader.read_str(str), env))

print(REP("(rule (if 0 (filler true-body) (filler false-body)) false-body)"))
print(REP("(rule (if 1 (filler true-body) (filler false-body)) true-body)"))

print(REP("(if 1 да нет)"))
print(REP("(if 0 да нет)"))

#print(REP("(rule x (quote (- 10 5)))"))
#print(REP("x"))

print(REP("(rule ((filler x) inf+ (filler y)) (+ x y))"))
print(REP("(10 inf+ 20)"))

#print(REP("(rule (quote (factorial 0)) 1)"))
#print(REP("(rule (factorial (filler x)) (quote (* x (factorial (- x 1)))))"))
#print(REP("(rule x 3)"))

#print(REP("(rule (while (filler cond) (filler body)) (quote (rule (while 1 (filler lala) (while cond body)))))"))

#print(REP("(rule x 5)"))
#print(REP("(while x (rule x (- x 1)))"))

#print("----------------------------------------------")

#print(REP("(factorial (- x 1))"))

#print(REP("(+ 1 (+ 2 (+ 3 4)))"))
#print(REP("(* 3 (* 2 (* 1 1)))"))
