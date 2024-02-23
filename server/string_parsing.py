"""
Here are 10 practice problems related to string parsing in Python, ranging from beginner to more advanced levels. They cover various aspects of string manipulation, including basic operations, string methods, regular expressions, and JSON parsing.

Beginner
--------
Reverse a String 
Write a function that takes a string as input and returns the string reversed.

Count Vowels
Write a function that counts and returns the number of vowels (a, e, i, o, u) in a given string.

Palindrome Checker
Write a function that checks whether a given string is a palindrome (reads the same forward and backward, ignoring spaces, punctuation, and case).

Find and Replace
Given a string, write a function that replaces all occurrences of "Python" with "Java" and returns the modified string.

Intermediate
-------------
First Non-Repeated Character
Write a function that finds and returns the first non-repeated character in a string. If there is no such character, return None.

Word Frequency Counter
Given a sentence, write a function that counts the frequency of each word and returns a dictionary with words as keys and their frequencies as values.

Acronym Generator
Write a function that takes a string (representing a phrase) and returns the acronym of that phrase. For example, "As Soon As Possible" should return "ASAP".

CamelCase to snake_case Converter
Write a function that converts a string from CamelCase to snake_case."""

# reverse string
sample_string = "hello how are you"
reversed_string = sample_string[::-1]  # [start:stop:step]
print("reverse: " + reversed_string)

# count vowels
vowels = set(["a", "e", "i", "o", "u"])
sample_string = "hello how are you"  # should have seven vowels
vowel_counter = 0
for letter in sample_string:
    if letter in vowels:
        vowel_counter += 1
print("num vowels: ", vowel_counter)

# palindrome Checker
not_palindrome = "this is not a palindrome"
palindrome = "racecar"
print("not palindrome:", not_palindrome == not_palindrome[::-1])
print("palindrome:", palindrome == palindrome[::-1])

# Find and Replace
sample_string = "I love to code in python but sometimes python is hard"
replacement = sample_string.replace(
    "python", "java", 2
)  # params in order: old, new, count
print(replacement)

# Word Frequency Counter
sample_string = "I love to code in python but sometimes python is hard"
split_string = sample_string.split(" ")  # Split the string
frequency_table = dict()
for word in split_string:
    if word in frequency_table:
        frequency_table[word] += 1
    else:
        frequency_table[word] = 1
print(frequency_table)

# Acronym Generator
acronym_string = "central processing unit"
split_acronym = acronym_string.split(" ")
acronym = ""
for word in split_acronym:
    acronym += word[0].upper()  # to do lower -> .lower() method
print("acronym:", acronym)

# CamelCase to snake_case Converter
sample_string = "HelloWorld"


def camel_to_snake(input: str):
    snake = ""
    for index, letter in enumerate(input): # enumerate loop gives index then letter
        print(index, letter)
        if index != 0 and letter.isupper():
            snake += f"_{letter.lower()}"
        else:
            snake += letter.lower()
    print(snake)


camel_to_snake("ThisIsCamel")
