word = input('Enter a word: ')
reverse_word=''.join(word[::-1])
if word == reverse_word:
    print(word + ' is palindrome')
else:
    print(word + ' is not a palindrome')