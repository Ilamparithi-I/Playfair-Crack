from collections import Counter
import json



matrix = [['H', 'Z', 'U', 'G', 'S'], ['R', 'O', 'A', 'V', 'X'], ['I', 'W', 'Q', 'F', 'Y'], ['D', 'P', 'L', 'T', 'B'], ['N', 'E', 'M', 'C', 'K']]
cipher = "DGYHMVELRQHCMOIHNPPAMVMQHNMRDFREQMDOKZGKAXNOVUZPZNECRLLHYXMELVUQQDNOPVMZPMXYGXVPNOHZFHUDFHGDDHSTZRQRHDUKGHDQCQRQDGRMNIZESLDQMVKHLVPCONDOKZMELVDFOCWRMRDGRMGBFNMBRMPLXZPCPRCIVMKPARXEMVBADQCHDSRWRMYHEMXMQXUAUBQNMQQINORMLRDQWCPACHPNEANVVLQWDGDNMOGYAOAZVNAEUAHDBFPWAMBHMVONQURQAOFDWXWVHAONHYPNCDXYGBFNMBRM"

with open('data.json', 'r') as json_file:
    loaded_data = json.load(json_file)

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
            
def decrypt_playfair_and_display(matrix):
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
    return plaintext

print (decrypt_playfair_and_display(matrix))