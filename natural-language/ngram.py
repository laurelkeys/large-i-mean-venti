print(["condescendences"[i:i+2] for i in range(len("condescendences")-1)])
s = "Two roads diverged in a yellow wood, And sorry I"
s = s.split(" ")
s = [' '.join(s[i:i+5]) for i in range(len(s) - 4)]
print(s)
print(list(map(lambda x: len(x.split(' ')), s)))

def ngram_to_next_dict(src, order, model={}):
    src += '$'
    for i in range(len(src) - order):
        ngram = tuple(src[i : i+order])
        next = src[i + order]
        try: 
            model[ngram].append(next)
        except: 
            model[ngram] = [next]
    return model