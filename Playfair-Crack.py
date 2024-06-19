from collections import Counter
import random
import json
import copy
import math


cipher = "DGYHMVELRQHCMOIHNPPAMVMQHNMRDFREQMDOKZGKAXNOVUZPZNECRLLHYXMELVUQQDNOPVMZPMXYGXVPNOHZFHUDFHGDDHSTZRQRHDUKGHDQCQRQDGRMNIZESLDQMVKHLVPCONDOKZMELVDFOCWRMRDGRMGBFNMBRMPLXZPCPRCIVMKPARXEMVBADQCHDSRWRMYHEMXMQXUAUBQNMQQINORMLRDQWCPACHPNEANVVLQWDGDNMOGYAOAZVNAEUAHDBFPWAMBHMVONQURQAOFDWXWVHAONHYPNCDXYGBFNMBRM"

possibleKeyChars = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','K','L','Z','X','C','V','B','N','M']


maxScore = -100000
maxMatrix = []

with open('data.json', 'r') as json_file:
    loaded_data = json.load(json_file)


def generate_playfair_matrix(key):
    matrix = []
    for char in key:
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, len(matrix), 5)]

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
            
def decrypt_playfair_and_display(matrix, iterCount, score):
    plaintext = ""
    pairs = [cipher[i:i+2] for i in range(0, len(cipher), 2)]

    for pair in pairs:
        row1, col1 = find_position(matrix, pair[0])
        row2, col2 = find_position(matrix, pair[1])
        if row1 == row2:
            plaintext += matrix[row1][(col1-1)%5] + matrix[row2][(col2-1)%5]
        elif col1 == col2:
            plaintext += matrix[(row1-1)%5][col1] + matrix[(row2-1)%5][col2]
        else:
            plaintext += matrix[row1][col2] + matrix[row2][col1]
    print("After iteration " + str(iterCount))
    print (matrix)
    print (plaintext)
    print (score)

def decrypt_playfair_and_score(matrix):
    # decrypting 
    
    plaintext = ""
    pairs = [cipher[i:i+2] for i in range(0, len(cipher), 2)]

    for pair in pairs:
        row1, col1 = find_position(matrix, pair[0])
        row2, col2 = find_position(matrix, pair[1])
        if row1 == row2:
            plaintext += matrix[row1][(col1-1)%5] + matrix[row2][(col2-1)%5]
        elif col1 == col2:
            plaintext += matrix[(row1-1)%5][col1] + matrix[(row2-1)%5][col2]
        else:
            plaintext += matrix[row1][col2] + matrix[row2][col1]
    
    # Scoring
    substrings = [plaintext[i:i+4] for i in range(len(plaintext)-3)]
    frequency_dict = dict(Counter(substrings))
    score = 0
    for i in frequency_dict:
        if (i in loaded_data):
            score = score + frequency_dict[i]*loaded_data[i]
        else:
            score = score + frequency_dict[i]*loaded_data["FLOOR"]

    return score

while(True):        
    parent = random.sample(possibleKeyChars, 25)
    parentMatrix = generate_playfair_matrix(parent)
    parentScore = decrypt_playfair_and_score(parentMatrix)
    Temperature = 28
    iteration = 0
    while(Temperature > 0):
        counter = 0
        while(counter < 10000):
            random_number =random.randint(1, 50)
            childMatrix = copy.deepcopy(parentMatrix)
            if (random_number == 1):
                # flip matrix across NW-SE axis
                childMatrix = [list(reversed(row)) for row in reversed(childMatrix)]
            elif (random_number == 2):
                # flip matrix top to bottom
                childMatrix = list(reversed(childMatrix))
            elif (random_number == 3):
                # flip matrix left to right
                childMatrix = [list(reversed(row)) for row in childMatrix]
            elif (random_number == 4):
                # swap two rows chosen at random 
                row1 = random.randint(0, 4)
                row2 = random.randint(0, 4)
                childMatrix = copy.deepcopy(childMatrix)
                childMatrix[row1], childMatrix[row2] = childMatrix[row2], childMatrix[row1]
            elif (random_number == 5):
                # swap two columns chosen at random
                col1 = random.randint(0, 4)
                col2 = random.randint(0, 4)
                for i in range(len(childMatrix)):
                    childMatrix[i][col1], childMatrix[i][col2] = childMatrix[i][col2], childMatrix[i][col1]
            else:
                # swap any two values chosen at random
                row1 = random.randint(0, 4)
                col1 = random.randint(0, 4)
                row2 = random.randint(0, 4)
                col2 = random.randint(0, 4)
                childMatrix[row1][col1], childMatrix[row2][col2] = childMatrix[row2][col2], childMatrix[row1][col1]
            childScore = decrypt_playfair_and_score(childMatrix)
            diff = (parentScore - childScore)
            if (diff < 0):
                parentMatrix = childMatrix
                parentScore = childScore
            else:
                probability = 1 / math.exp(diff/Temperature)
                randNum = random.random()
                if (probability > randNum):
                    parentMatrix = childMatrix
                    parentScore = childScore
                else:
                    if (counter % 1000 == 0): 
                        print(counter, Temperature)
                    counter = counter + 1
            if (childScore > maxScore):
                maxScore = childScore
                maxMatrix = childMatrix
        iteration = iteration + 1      
        decrypt_playfair_and_display(maxMatrix, iteration, maxScore)
        Temperature = Temperature - 0.5