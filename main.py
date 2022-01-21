import json
from pickle import TRUE
from pprint import pprint

#rank words

def getWords():
    words = []
    letters = []
    rankings = []
    with open('five-letter-words.json', "r") as fw:
        words = json.load(fw)
    with open('letter-distribution.json', 'r') as fl:
        letters = json.load(fl)
    for word in words['words']:
        score = 0
        counted = []
        print(word)
        for l in word:
            if (l not in counted):
                score += letters[l]
            else:
                score += letters[l] * 0
            counted.append(l)
        rankings.append({
            'word': word,
            'score': round(score, 2)
        })
    rankings.sort(key=lambda x: x['score'], reverse=True)
    return rankings

def filterWords(words, greens, yellows, grays):
    filtered = []
    for i in range(len(greens)):
        green = greens[i]
        if green != '':
            yellows[i] = []

    for word in words:
        add = True
        for i in range(5):
            letter = word['word'][i]
            if letter in grays:
                break
            green = greens[i]
            if green != '':
                if letter != green:
                    add = False
            yellow = yellows[i]
            for y in yellow:
                if y == letter:
                    add = False
        if add == True:
            filtered.append(word)

    return filtered

#frequency of 5 letter words not all words


words = getWords()
# greens = ['', '', '', '', '']
# yellows = [[''], [''], [''], [''], ['']]
# grays = [[''], [''], [''], [''], ['']]

greens = ['', '', '', '', '']
yellows = [[''], [''], [''], [''], ['']]
grays = ['']

filtered = filterWords(words, greens, yellows, grays)
# pprint(filtered)

pprint(filtered[:50])

print(len(filtered))


    

