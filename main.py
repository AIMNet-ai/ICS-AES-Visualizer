#!/usr/bin/python

from pprint import pprint

from constants import round_constants
from constants import sbox

matrix_size = 4


def hex_to_matrix(hex_array):
    matrix = []
    for i in range(16):
        if i % matrix_size == 0:
            matrix.append([hex_array[i]])
        else:
            matrix[int(i / 4)].append(hex_array[i])
    return matrix


def text_to_hex(text):
    hex_array = []
    for char in text:
        hex_array.append(ord(char))
    return hex_array


def shift_matrix(matrix):
    for i in range(matrix_size):
        matrix[i] = matrix[i][-i:] + matrix[i][:-i]
    return matrix


def key_expansion(key_matrix):
    round_keys = [key_matrix]
    round_key = key_matrix[:]
    for r in range(0, 10):
        new_key = round_key.copy()
        last = round_key[3]
        new_key[3] = round_last(new_key[3], r)
        new_key[0] = xor_matrix(new_key[0], new_key[3])
        new_key[1] = xor_matrix(new_key[1], new_key[0])
        new_key[2] = xor_matrix(new_key[2], new_key[1])
        new_key[3] = xor_matrix(last, new_key[2])
        round_key = new_key
        round_keys += [new_key]
    return round_keys


def xor_matrix(first, second):
    first = first.copy()
    for i in range(4):
        first[i] = first[i] ^ second[i]
    return first


def round_last(round_key, r):
    # Shift bottom row
    last_column = round_key[1:] + round_key[:1]

    # Byte substitution (sbox uses hex representation as index)
    for column in range(matrix_size):
        last_column[column] = sbox[last_column[column]]

    # Adding round constant
    last_column[0] = last_column[0] ^ round_constants[r]
    return last_column


test_key = text_to_hex("Thats my Kung Fu")
test_text = text_to_hex("Two One Nine Two")

pprint(hex_to_matrix(test_key))
print("\n\n")
pprint(key_expansion(hex_to_matrix(test_key)))
