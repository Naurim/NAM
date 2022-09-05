from nam_types import _listP, _symbolP
class Env():
    def __init__(self, outer=None):
        self.rules = []
        self.outer = outer or None

    def search(self, key):
        if _listP(key):
            for rule in self.rules:
                rl = rule[0]
                lk = len(key)
                if lk == len(rl):
                    for i in range(lk):
                        if (not _symbolP(rl[i])) and (key[i] != rl[i]):
                            break
                    else:
                        return rule[1]
                elif key == rl: return rule[1]
            return False
        else:
            for rule in self.rules:
                if key == rule[0]: return rule[1]
    def left(self, key):
        for rule in self.rules:
            if key == rule[1]: return rule[0]

    def find(self, key):
        if self.search(key): return self
        elif self.outer:     return self.outer.find(key)
        else:                return None
    def find_left(self, key):
        if self.left(key): return self
        elif self.outer:   return self.outer.find(key)
        else:              return None

    def set(self, rl, rr):
        rule = [rl, rr]
        self.rules.append(rule)
        return rl

    def get(self, key):
        env = self.find(key)
        if not env: raise Exception(key, " not found")
        return env.search(key)
    def get_left(self, key):
        env = self.find_left(key)
        if not env: raise Exception(key, " not found")
        return env.left(key)

