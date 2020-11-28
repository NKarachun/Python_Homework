# Problem Set 2, hangman.py
# Name: Anastasia Karachun
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    word = set(secret_word)
    letters = set(letters_guessed)
    if word == word & letters:
        return True
    return False



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word = set(secret_word)
    letters = set(letters_guessed)
    guessed_letters = word & letters
    str = ''
    for i in secret_word:
        if i in guessed_letters:
            str += i
        else:
            str += '_ '
    return str



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = string.ascii_lowercase
    for i in letters_guessed:
        if i in alphabet:
            alphabet = alphabet.replace(i, '')
    return alphabet
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    full_alphabet = string.ascii_lowercase
    letters_guessed = []
    vowels = ['a', 'i', 'e', 'o', 'u']
    l = len(secret_word)
    warnings = 3
    guess = 6
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', l, 'letters long.')
    print('You have', warnings, 'warnings left.')
    while guess > 0:
        alphabet = get_available_letters(letters_guessed)
        print('-------------')
        if is_word_guessed(secret_word, letters_guessed):
            number = len(set(secret_word))
            total_score = guess * number
            print('Congratulations, you won!')
            print('Your total score for this game is:', total_score)
            break
        else:
            if warnings != 0:
                is_correct = True
            else:
                is_correct = False
            print('You have', guess, 'guesses left.')
            print('Available letters:', alphabet)

            def check(letter):
                nonlocal warnings
                nonlocal guess
                nonlocal is_correct
                nonlocal vowels
                if warnings != 0:
                    if len(letter) != 1 and letter[0] in full_alphabet:
                        warnings -= 1
                        print('Oops! You should enter only one letter. You have', warnings, 'warnings left:', end=' ')
                        is_correct = False
                        return 0
                    elif letter not in full_alphabet:
                        warnings -= 1
                        print('Oops! That is not a valid letter. You have', warnings, 'warnings left:', end=' ')
                        is_correct = False
                        return 0
                    elif letter in letters_guessed:
                        warnings -= 1
                        print("Oops! You've already guessed that letter. You have", warnings, "warnings left:", end=' ')
                        is_correct = False
                        return 0
                else:
                    if len(letter) != 1 and letter[0] in full_alphabet:
                        print('Oops! You should enter only one letter.', end=' ')
                    elif letter not in full_alphabet:
                        print('Oops! That is not a valid letter.', end=' ')
                    elif letter in letters_guessed:
                        print("Oops! You've already guessed that letter.", end=' ')

                    if letter in vowels:
                        guess -= 2
                    else:
                        guess -= 1
                    print('You have no warnings left, so you lose one guess.', end=' ')
                    is_correct = False

            letter = input('Please guess a letter:').lower()
            if warnings != 0 or letter not in alphabet:
                check(letter)
            elif letter in alphabet:
                is_correct = True

            letters_guessed.append(letter)
            if letter in secret_word and is_correct:
                print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
            elif is_correct:
                print("Oops! That letter is not in the word: ", get_guessed_word(secret_word, letters_guessed))
                if letter in vowels:
                    guess -= 2
                else:
                    guess -= 1
            else:
                print(get_guessed_word(secret_word, letters_guessed))

    else:
        print('-----------')
        print('Sorry, you ran out of guesses. The word was', secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(' ', '')
    if len(my_word) == len(other_word):
        for i in range(len(other_word)):
            q = len(my_word) - 1
            count = 0
            if other_word[i] != my_word[i] and my_word[i] != '_':
                return False
            while q >= 0 and my_word[i] != '_':
                if my_word[i] == other_word[q]:
                    count += 1
                    if count == 1:
                        temp = q
                    elif count > 1 and my_word[q] != my_word[temp]:
                        return False
                q -= 1
        return True
    return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    ls = []
    for i in wordlist:
        if match_with_gaps(my_word, i):
            ls.append(i)
            print(i, end=' ')
    if len(ls) == 0:
        print('No matches found')


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    full_alphabet = string.ascii_lowercase
    letters_guessed = []
    vowels = ['a', 'i', 'e', 'o', 'u']
    l = len(secret_word)
    warnings = 3
    guess = 6
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', l, 'letters long.')
    print('You have', warnings, 'warnings left.')
    while guess > 0:
        alphabet = get_available_letters(letters_guessed)
        print('-------------')
        if is_word_guessed(secret_word, letters_guessed):
            number = len(set(secret_word))
            total_score = guess * number
            print('Congratulations, you won!')
            print('Your total score for this game is:', total_score)
            break
        else:
            if warnings != 0:
                is_correct = True
            else:
                is_correct = False
            print('You have', guess, 'guesses left.')
            print('Available letters:', alphabet)

            def check(letter):
                nonlocal warnings
                nonlocal guess
                nonlocal is_correct
                nonlocal vowels
                if warnings != 0:
                    if len(letter) != 1 and letter[0] in full_alphabet:
                        warnings -= 1
                        print('Oops! You should enter only one letter. You have', warnings, 'warnings left:', end=' ')
                        is_correct = False
                        return 0
                    elif letter not in full_alphabet:
                        if letter == '*':
                            print('Possible word matches are:', end=' ')
                            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                            is_correct = True
                        else:
                            warnings -= 1
                            print('Oops! That is not a valid letter. You have', warnings, 'warnings left:', end=' ')
                            is_correct = False
                        return 0
                    elif letter in letters_guessed:
                        warnings -= 1
                        print("Oops! You've already guessed that letter. You have", warnings, "warnings left:", end=' ')
                        is_correct = False
                        return 0
                else:
                    if len(letter) != 1 and letter[0] in full_alphabet:
                        print('Oops! You should enter only one letter.', end=' ')
                    elif letter not in full_alphabet:
                        if letter == '*':
                            print('Possible word matches are:', end=' ')
                            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                        else:
                            print('Oops! That is not a valid letter.', end=' ')
                    elif letter in letters_guessed:
                        print("Oops! You've already guessed that letter.", end=' ')

                    if letter in vowels:
                        guess -= 2
                        print('You have no warnings left, so you lose one guess.', end=' ')
                    elif letter == '*':
                        pass
                    else:
                        guess -= 1
                        print('You have no warnings left, so you lose one guess.', end=' ')
                    is_correct = False

            letter = input('Please guess a letter:').lower()
            if warnings != 0 or letter not in alphabet:
                check(letter)

            letters_guessed.append(letter)
            if letter in secret_word and is_correct:
                print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
            elif is_correct:
                if letter == '*':
                    print()
                else:
                    print("Oops! That letter is not in the word: ", get_guessed_word(secret_word, letters_guessed))
                    if letter in vowels:
                        guess -= 2
                    elif letter == '*':
                        pass
                    else:
                        guess -= 1
            else:
                print(get_guessed_word(secret_word, letters_guessed))

    else:
        print('-----------')
        print('Sorry, you ran out of guesses. The word was', secret_word)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############

    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
