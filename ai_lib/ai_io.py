import re
import random


# read 2 given files once when this module is imported
with open('ai_lib/3_letters_dictionary') as open_file:
    letters_dict = open_file.read()

with open('ai_lib/bigram_frequence_list') as open_file:
    freq_list = open_file.read()

def create_input(num_of_input):
    """
    Input: Number of inputs need to create
    Output: Print randomly created inputs to "input" file
    """
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    inputs = []
    for k in range(num_of_input):
        letters = ''
        for i in range(9):
            letters += random.choice(alphabet)
        inputs.append(letters)

    open_file = open("input", 'w')
    for i in inputs:
        open_file.write(i + "\n")

def read_input():
    """
    Output: a list of 2D list of letters
    """
    with open("input") as open_file:
        data = open_file.read()

    data = data.split()
    inputs = []
    for line in data:
        inputs.append([line[0:3], line[3:6], line[6:9]])
    return inputs 

def has_meaning(*letters):
    """
    Input: a tuple of 3 letters named 'letters'
    Output: True if it has a meaning, False otherwise
    """
    word = ''.join(letters)

    if re.search(word, letters_dict, re.I) == None:
        return False
    else:
        return True

def get_frequency(*letters):
    """
    Input: a tuple of 2 letters named 'letters'
    Output: the frequency of those in the dictionary
    """
    pair = ' '.join(letters)

    line = re.search(pair + r'\s0[\d.]*', freq_list, re.I).group()

    return float(line[4:])

def print_results(results, file_name):
    """
    Input: a list of strings of letters
    Output: write to file_name file as a string of 9 letters
    """
    open_file = open(file_name, 'w')

    for result in results:
        open_file.write(str(result) + "\n")

def read_file(file_name):
    """
    Output: a list of input
        Each input is list of 9 letter
    """
    with open(file_name) as open_file:
        data = open_file.read()

    data = data.split()
    inputs = []
    for line in data:
        inputs.append(list(line))
    return inputs 