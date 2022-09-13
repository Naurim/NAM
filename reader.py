from nam_types import (_list, _atom)

class Reader():
    def __init__(self, tokens, position=0):
        self.tokens = tokens
        self.position = position

    def next(self):
        self.position += 1
        return self.tokens[self.position-1]

    def peek(self):
        if len(self.tokens) > self.position:
            return self.tokens[self.position]
        else: return None

def make_tokenizer(tokens):
    def clos(stri):
        stokens = tokens
        acc     = []
        cache   = ''
        for x in stri:
            if x.isspace():
                if not cache: continue

                acc.append(cache)
                cache = ''
                continue
            if x in stokens:
                if cache:
                    acc.append(cache)
                    cache = ''
                acc.append(x)
                continue            
            cache += x
        if cache: acc.append(cache)
        return acc
    return clos
tokenize = make_tokenizer('()\'')

def read_atom(reader):
    token = reader.next()
    if token == "nil":     return None
    else:
        try:               return int(token)
        except ValueError: return _atom(token)

def read_list(reader):
    sexp = _list()
    token = reader.next()
     
    if token != '(': raise Exception("expected '('")

    token = reader.peek()
    while token != ')':
        if not token: raise Exception("expected ')', got EOF")
        sexp.append(read_form(reader))
        token = reader.peek()
    reader.next()
    return sexp

def read_form(reader):
    token = reader.peek()

    if token == '\'':
        reader.next()
        return _list(_atom('quote'), read_form(reader))
    
    elif token == ')': raise Exception("unexpected ')'")
    elif token == '(': return read_list(reader)
    
    else:              return read_atom(reader);

def read_str(str):
    tokens = tokenize(str)
    if len(tokens) == 0: raise Exception("Empty code")
    return read_form(Reader(tokens))
