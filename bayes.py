import re
from collections import defaultdict

def _get_words(a):
    res = [a.author]
    #yield a.author
    for w in re.split(r"[\s.,;:\!\?\(\)]+", a.title.lower()):
        #yield w
        res.append(w)
    return res

def guess(articles):
    articles = list(articles)
    classes = defaultdict(int)
    words = defaultdict(int)
    wbc = defaultdict(lambda: defaultdict(int)) # words by class

    for a in articles: #переводим метку в класс
        if a.label:
            classes[a.label] += 1

            for w in _get_words(a): #запоминаем признаки у класса 
                wbc[a.label][w] += 1 # выбираем словарь в который будет записанно слово, запоминаем сколько слово встретилось всего в отмечанном классе
                words[w] += 1 #запоминаем сколько слово встретилось всего

    for a in articles:
        if a.label:
            # возврщаем статьи без лейбла 
            pass
        else:
            probs = [] #список пар вероятность-класс

            for label, c in classes.items(): 
                p = c 
                for w in _get_words(a):
                    if w in words:
                        if w in wbc[label]:
                            p *= wbc[label][w] / words[w]
                        else:
                            p *= 0.1 / words[w]

                probs.append((p, label))

            if probs:
                yield (max(probs)[1], a) 
            else:
                yield (None, a)








