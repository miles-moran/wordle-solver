import json
from pprint import pprint

def recurse(guesses, solutions, r = {}):
    for guess in guesses:
        g = guess['word']
        if g not in r:
            r[g] = {}
        for solution in solutions:
            s = solution['word']
            feedback = {
                "greens": ['', '', '', '', ''],
                "yellows": [[], [], [], [], []],
                "grays": []
            }
            attempt = getFeedback(s, g, feedback)['f']
            filtered = filterGuesses(guesses, attempt)
            if s != g:
                r[g] = recurse(filtered, filtered, r[g])
    return r

def getGuesses():
    guesses = []
    t = []
    with open('guess-pool-2.json', "r") as fw:
        guesses = json.load(fw)['words']
    for g in guesses:
        t.append(str(g))
    return t

def getSolutions():
    guesses = []
    t = []
    with open('solution-pool.json', "r") as fw:
        guesses = json.load(fw)['words']
    for g in guesses:
        t.append(str(g))
    return t

def getWeights():
    weights = []
    with open('letter-distribution.json', "r") as fw:
        weights = json.load(fw)
    return weights

def getSuggestions(guesses, weights, dr = -1):
    suggestions = []
    for word in guesses:
        score = 0
        counted = []
        for l in word:
            if (l not in counted):
                score += weights[l]
            else:
                score += weights[l] * dr
            counted.append(l)
        suggestions.append({
            'word': word,
            'score': round(score, 2)
        })
    suggestions.sort(key=lambda x: x['score'], reverse=True)
    return suggestions

def filterGuesses(guesses, feedback):
    filtered1 = []
    filtered2 = []
    for i in range(len(feedback['greens'])):
        green = feedback['greens'][i]
        if green != '':
           feedback['yellows'][i] = []

    for word in guesses:
        add = True
        for gray in feedback['grays']:
            if gray in word['word'] and gray != '':
                add = False
        for yellow in feedback['yellows']:
            for y in yellow:
                if y not in word['word']:
                    add = False
        if add == True:
            filtered1.append(word)

    for word in filtered1:
        add = True
        for i in range(5):
            letter = word['word'][i]
            green = feedback['greens'][i]
            if green != '':
                if letter != green:
                    add = False
            yellow = feedback['yellows'][i]
            for y in yellow:
                if y == letter:
                    add = False
        if add == True:
            filtered2.append(word)
    return filtered2

def getFeedback(solution, guess, possibles, guesses, feedback = {
        "greens": ['', '', '', '', ''],
        "yellows": [[], [], [], [], []],
        "grays": []
     }):
    a = {
        "colors": ['', '', '', '', ''],
        "guess": guess,
        "possibles": possibles,
        "guesses": guesses
    }
    for i in range(5):
        letter = guess[i]
        if letter not in solution:
            feedback['grays'].append(letter)
            a["colors"][i] = 'gray'
            continue
        if letter == solution[i]:
            feedback['greens'][i] = letter
            a["colors"][i] = 'green'
        else:
            feedback['yellows'][i].append(letter)
            a["colors"][i] = 'yellow'
    return {
        "a": a,
        "f": feedback
    }

def getUniqueLettersLeft(possibles, feedback):
    greens = feedback['greens']
    yellows = feedback['yellows'][0] + feedback['yellows'][1] + feedback['yellows'][2] + feedback['yellows'][3] + feedback['yellows'][4]
    left = {}
    # print(yellows)
    # print('----', left)
    for word in possibles:
        w = word['word']

        for l in w:
            if (l not in greens) and (l not in yellows):
                if (l not in left):
                    left[l] = 0
                left[l] += 1
    return left

def findEliminators(left, guesses, elims, th):
    eliminators = []
    for guess in guesses:
        s = 0
        e = []
        g = guess['word']
        for l in left:
            if l in g:
                e.append(l)
                s += left[l]
        if len(e) > th and g not in elims:
            eliminators.append({
                'word': g,
                'e': e,
                'score': s
            })
    eliminators.sort(key=lambda x: (len(x['e']), x['score']), reverse=True)
    return eliminators
            

def attempt(solution, guesses, solutions, th):
    feedback = {
        "greens": ['', '', '', '', ''],
        "yellows": [[], [], [], [], []],
        "grays": []
    }
    answer = None
    attempts = []
    elims = []
    while answer == None:
        possibles = filterGuesses(solutions, feedback)
        guess = ''
        elims = [] 
        if len(possibles) == 0:
            answer = None
            return
        else:
            guess = possibles[0]['word']
            left = getUniqueLettersLeft(possibles, feedback)
            eliminators = findEliminators(left, guesses, elims, th)
            elims = eliminators
            if len(eliminators) > 0:
                guess = eliminators[0]['word']
                elims.append(guess)
        fb = getFeedback(solution, guess, possibles, elims, feedback)
        if guess == solution:
            answer = guess
        attempts.append(fb["a"])
    return attempts

def solve(solution, th=4):
    weightedGuesses = getSuggestions(getGuesses() + getSolutions(), getWeights()) 
    weightedSolutions = getSuggestions(getSolutions(), getWeights())
    attempts = attempt(solution, weightedGuesses, weightedSolutions, th)
    if attempts is None:
        print('FAILED TO FIND A WORD RETRYING WITH LARGER POOL')
        attempts = attempt(solution, weightedGuesses, weightedGuesses, th)
   
    return attempts

