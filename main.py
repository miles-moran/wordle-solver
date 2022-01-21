import json
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
        # print(word)
        for l in word:
            if (l not in counted):
                score += letters[l]
            else:
                score += letters[l] * .3
            counted.append(l)
        rankings.append({
            'word': word,
            'score': round(score, 2)
        })
    rankings.sort(key=lambda x: x['score'], reverse=True)
    return rankings

def filterWords(words, greens, yellows, grays):
    filtered1 = []
    filtered2 = []
    for i in range(len(greens)):
        green = greens[i]
        if green != '':
            yellows[i] = []

    for word in words:
        add = True
        for gray in grays:
            if gray in word['word'] and gray != '':
                add = False
        for yellow in yellows:
            for y in yellow:
                if y not in word['word']:
                    add = False
        if add == True:
            filtered1.append(word)

    for word in filtered1:
        add = True
        for i in range(5):
            letter = word['word'][i]
            green = greens[i]
            if green != '':
                if letter != green:
                    add = False
            yellow = yellows[i]
            for y in yellow:
                if y == letter:
                    add = False
        if add == True:
            filtered2.append(word)

    return filtered2

#frequency of 5 letter words not all words


words = getWords()
greens = ['', '', '', '', '']
yellows = [[''], [''], [''], [''], ['']]
grays = []

# print(len(filterWords(words, greens, yellows, grays)))

#ROBOT 215 4/6
# greens = ['', 'o', '', 'o', '']
# yellows = [['t'], ['t', 'r'], ['o', 't'], [''], ['r']]
# grays = ['a', 'n', 'e', 'i', 's', 'm']

#ROBOT 163 5/6
# greens = ['', 'r', 'o', 'v', 'e']
# yellows = [[''], [''], [''], ['r'], ['']]
# grays = ['a', 't', 'n', 's', 'h', 'd', 'g']

# greens = ['', 'r', 'i', 'n', '']
# yellows = [['r', 'g'], [''], [''], [''], ['']]
# grays = ['a', 't', 'o', 'e', 'u', 's', 'd']

#HORSE 165 3/6
# greens = ['', 'o', '', '', 'e']
# yellows = [[''], [''], ['o'], ['s'], ['']]
# grays = ['a', 't', 'n', 'h', 'r']

#CHEAT 166 4/6
# greens = ['', '', '', '', '']
# yellows = [['a', 't', 'h'], ['t', 'e', 'a'], ['a', 't'], ['e'], ['e']]
# grays = ['o', 'n', 'r', 's', 'd']

#GRIME 167 5/6
# greens = ['', 'r', 'i', 'm', 'e']
# yellows = [[''], [''], [''], ['r'], ['']]
# grays = ['a', 't', 'o', 'n', 's', 'h', 'p', 'd', 'c']

# greens = ['', '', '', 'e', '']
# yellows = [['h', 's'], ['e', 'h'], ['r'], ['r'], ['e', 's']]
# grays = ['a', 't', 'o', 'n', 'i']

#double letter, one gray, one yellow

# filtered = filterWords(words, greens, yellows, grays)
# pprint(filtered)

# pprint(filtered[:50])

# print(len(filtered))


def solve(solution):
    greens = ['', '', '', '', '']
    yellows = [[], [], [], [], []]
    grays = []
    answer = None
    suggestions = getWords()
    counter = 1
    while answer == None:
        counter += 1

        suggestions = filterWords(suggestions, greens, yellows, grays)
        if len(suggestions) == 1:
            answer = suggestions[0]
        guess = suggestions[0]['word']

        for i in range(5):
            letter = guess[i]
            if letter not in solution:
                grays.append(letter)
                continue
            if letter == solution[i]:
                greens[i] = letter
            else:
                yellows[i].append(letter)
        
    return counter


words = []
with open('five-letter-words.json', "r") as fw:
    words = json.load(fw)

guesses = 0
puzzles = 0
for word in words['words'][:500]:
    score = solve(word)
    guesses += score
    puzzles += 1


print('guess average')
print(guesses / puzzles)





    

