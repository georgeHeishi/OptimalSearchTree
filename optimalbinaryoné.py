'''
This file file implements Optimal Binary Search on data with lines consisted of:
    frequency(number) word(string)

Where values on one line are seperated by space (' ')

This script was implemented as a solution to assigment on FEI STU course I-ADS Algorithms and data structures.
'''

__author__ = 'Juraj Lapcak'


import sys


class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None


def optimal_bst(p_table, q_table, n):
    e_table = [[0 for _ in range(n + 1)] for _ in range(n + 2)]
    w_table = [[0 for _ in range(n + 1)] for _ in range(n + 2)]
    root_table = [[0 for _ in range(n + 1)] for _ in range(n + 2)]

    for i in range(1, n + 2):
        e_table[i][i - 1] = q_table[i - 1]
        w_table[i][i - 1] = q_table[i - 1]

    for l in range(1, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            e_table[i][j] = float('inf')
            w_table[i][j] = w_table[i][j - 1] + p_table[j - 1] + q_table[j]

            for r in range(i, j + 1):
                t = e_table[i][r - 1] + e_table[r + 1][j] + w_table[i][j]

                if t < e_table[i][j]:
                    e_table[i][j] = t
                    root_table[i][j] = r

    return e_table, root_table


def calculate_p(reduced_data, freq_sum):
    '''
    Parameters:
        reduced_data -- list of tuples, with frequency >= 50_000, where first member is frequency, second word
        freq_sum    -- summary of frequencies
    Returns:
        p_table -- list of probabilities p
    '''
    p_table = list()

    for freq, _ in reduced_data:
        p_table.append(freq/freq_sum)

    return p_table


def calculate_q(data, reduced_data, freq_sum):
    '''
    Parameters:
        data -- list of tuples, where first member is frequency, second word
        reduced_data -- list of tuples, with frequency >= 50_000, where first member is frequency, second word
        freq_sum --summary of frequencies
    Return:
        q_table -- list of probabilities q
    '''
    q_table = list()

    freq_part_sum = 0
    for freq_i, _ in enumerate(data[:data.index(reduced_data[0])]):
        freq_part_sum += freq_i
    q_table.append(freq_part_sum/freq_sum)

    for i, value in enumerate(reduced_data):
        freq_part_sum = 0
        data_i = data.index(value) + 1

        if i == len(reduced_data) - 1:
            data_next_i = len(data) + 1
        else:
            data_next_i = data.index(reduced_data[i + 1])

        for freq, _ in data[data_i:data_next_i]:
            freq_part_sum += freq
        q_table.append(freq_part_sum/freq_sum)

    return q_table


def prepare_data(data_path):
    '''
    Parameters:
        data_path -- string, path to data-file
    Return:
        sorted_data -- list of tuples, where first member is frequency, second word
        sorted_reduced_data -- list of tuples, with frequency >= 50_000, where first member is frequency, second word
        freq_sum -- summary of frequencies
    '''
    reduced_data_from_file = list()
    data_from_file = list()
    freq_sum = 0
    with open(data_path, 'r') as f:
        for line in f:
            split_line = line.split()
            freq_i = int(split_line[0])
            word_i = split_line[1].strip()
            freq_sum += freq_i

            data_from_file.append((freq_i, word_i))
            if freq_i >= 50_000:
                reduced_data_from_file.append((freq_i, word_i))

    sorted_data = sorted(data_from_file, key=lambda x: x[1])
    sorted_reduced_data = sorted(reduced_data_from_file, key=lambda x: x[1])
    return sorted_data, sorted_reduced_data, freq_sum


if __name__ == "__main__":
    data, reduced_data, freq_sum = prepare_data('dictionary.txt')

    p_table = calculate_p(reduced_data, freq_sum)
    q_table = calculate_q(data, reduced_data, freq_sum)

    e_table, root_table = optimal_bst(p_table, q_table, len(reduced_data))

    print((e_table[1][len(reduced_data)]))

    # tmp_sum = 0
    # for i in q_table:
    #     tmp_sum += i
    # for i in p_table:
    #     tmp_sum += i
    # print(tmp_sum)

    # with open('data.txt', 'w') as f:
    #     for i in data:
    #         f.write(f'{i}\n')

    # with open('reduced_data.txt', 'w') as f:
    #     for i in reduced_data:
    #         f.write(f'{i}\n')

    # with open('p_table.txt', 'w') as f:
    #     for i in p_table:
    #         f.write(f'{i}\n')

    # with open('q_table.txt', 'w') as f:
    #     for i in q_table:
    #         f.write(f'{i}\n')
