alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

for x in range(len(alphabet)):
    alphabet.append(alphabet[x])

message = input('Entrez votre message crypté : ')
clef = int(input('Entrez votre clef : '))

def chiffrage_lettre(lettre, alphabet, clef):
    for i in range(len(alphabet)):
        if lettre == ' ':
            return ' '
        elif alphabet[i]==lettre:
            return str(alphabet[i-clef])
    return '?'

message_chiffre = str()

for lettre in message:
    message_chiffre += chiffrage_lettre(lettre, alphabet, clef)

print(message_chiffre)