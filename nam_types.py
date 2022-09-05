import sys, types as pytypes

def _nilP(exp):   return exp is None
def _trueP(exp):  return exp is True
def _falseP(exp): return exp is False

class List(list):
    def __add__(self, rhs): return List(list.__add__(self, rhs))
def _list(*vals): return List(vals)
def _listP(exp):  return type(exp) == List

class Atom(str): pass
def _atom(str):  return Atom(str)
def _atomP(exp): return type(exp) == Atom

class Symbol(str): pass
def _symbol(str):  return Symbol(str)
def _symbolP(exp): return type(exp) == Symbol
