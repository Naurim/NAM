import nam_types as types

def _pr_str(obj):
    if types._listP(obj):
        return "(" + " ".join(map(lambda e: _pr_str(e), obj)) + ")"
    elif types._nilP(obj):
        return "nil"
    else:
        return obj.__str__()
