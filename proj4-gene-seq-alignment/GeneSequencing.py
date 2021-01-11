#!/usr/bin/python3

#from PyQt5.QtCore import QLineF, QPointF



import math
import time

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

    def __init__( self ):
        pass

# This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
# handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
# how many base pairs to use in computing the alignment
    def align( self, sequences, table, banded, align_length ):
        self.banded = banded
        self.MaxCharactersToAlign = align_length
        results = []

        for i in range(len(sequences)):
            jresults = []
            for j in range(len(sequences)):
                if j < i:
                   s = {}
                else:
###################################################################################################
# your code should replace these three statements and populate the three variables: score, alignment1 and alignment2

                    # Comparing itself
                    if i == j:
                        score = max(-3*align_length, -3*len(sequences[i]))
                        alignment1 = 'self'
                        alignment2 = 'self'
                    # Comparing with artificial sequences
                    elif (i == 0 and j != 1) or (i == 1 and j != 0):
                        score = float('inf')
                        alignment1 = 'No alignment possible'
                        alignment2 = 'No alignment possible'
                    else:
                        sequence_i_length = len(sequences[i])
                        sequence_j_length = len(sequences[j])
                        # Initialize the arrays
                        if align_length > sequence_i_length:
                            if align_length > sequence_j_length:
                                matrix_distance = [[0 for column in range(sequence_i_length + 1)] for row in range(sequence_j_length + 1)]
                                matrix_path = [['' for column in range(sequence_i_length + 1)] for row in range(sequence_j_length + 1)]
                        else:
                            matrix_distance = [[0 for column in range(align_length + 1)] for row in range(align_length + 1)]
                            matrix_path = [['' for column in range(align_length + 1)] for row in range(align_length + 1)]

                        # Filling out the first row
                        for k in range(len(matrix_distance[0])):
                            if banded:
                                if k > 3:
                                    matrix_distance[0][k] = float('inf')
                            else:
                                matrix_distance[0][k] = k * INDEL
                            matrix_path[0][k] = 'r'

                        # Filling out the first column
                        for k in range(len(matrix_distance)):
                            if banded:
                                if k > 3:
                                    matrix_distance[k][0] = float('inf')
                            else:
                                matrix_distance[k][0] = k*5
                            matrix_path[k][0] = 't'
                        matrix_path[0][0] = ''

                        for count in range(1, len(matrix_distance)):
                            if banded:
                                if count - 3 > 0:
                                    start = count - 3
                                else:
                                    start = 0
                                if count + 4 < len(matrix_distance[0]):
                                    finish = count + 4
                                else:
                                    finish = len(matrix_distance[0])
                            else:
                                start = 1
                                finish = len(matrix_distance[0])

                            # loop through and calcuate each value and find the minimum cost, filling out the matrix
                            # path matrix keeps track of which direction it came from
                            # Would take at most O(mn) time and space
                            for index in range(start, finish):
                                diagonal = matrix_distance[count-1][index-1] + self.get_difference(sequences[i], sequences[j], count-1, index-1)
                                right = matrix_distance[count-1][index] + INDEL
                                top = matrix_distance[count][index-1] + INDEL

                                min_val = min(right, top, diagonal)

                                matrix_distance[count][index] = min_val
                                if min_val == diagonal:
                                    matrix_path[count][index] = 'd'
                                elif min_val == top:
                                    matrix_path[count][index] = 't'
                                elif min_val == right:
                                    matrix_path[count][index] = 'r'

                        # Assign alignments using backtrace
                        # Would take O(mn) time and space
                        alignment1, alignment2 = self.get_string_alignment(matrix_path, sequences[i], sequences[j])
                        score = matrix_distance[-1][-1]
                        #if i == 2 and j == 9:
                        #    print(alignment1)
                        #    print(alignment2)

###################################################################################################
                    s = {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
                    table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
                    table.repaint()
                jresults.append(s)
            results.append(jresults)
        return results

    def get_string_alignment(self, matrix_path, sequence_i, sequence_j):
        path = ''
        i_final = ''
        j_final = ''
        j,k = -1,-1

        # Should start at the bottom right corner and backtrace
        # Find if it was from diagonal, from the above, and from right, and backtrace appropriately
        while matrix_path[j][k] != '':
            path = path + matrix_path[j][k]
            if matrix_path[j][k] == 'd':
                j = j - 1
                k = k - 1
            elif matrix_path[j][k] == 'r':
                k = k - 1
            elif matrix_path[j][k] == 't':
                j = j - 1
        # Each -1th item
        path = path[::-1]
        index_r, index_c = 0,0
        for i in range(len(path)):
            if path[i] == 't':
                i_final += '-'
            else:
                i_final += sequence_i[index_r]
                index_r = index_r + 1
            if path[i] == 'r':
                j_final += '-'
            else:
                j_final += sequence_j[index_c]
                index_c = index_c + 1
        return i_final, j_final


    # return -3 if match, 1 if sub
    # Would take O(1) time and constant space
    def get_difference(self, seqeunce_i, sequence_j, count, index):
        if seqeunce_i[index] == sequence_j[count]:
            return MATCH
        return SUB