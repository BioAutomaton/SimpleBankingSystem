word = input()
for letter in word:
    if letter.isupper():
        if word[0] == letter:
            word = word.replace(letter, letter.lower())
        else:
            word = word.replace(letter, f"_{letter.lower()}")
print(word)
