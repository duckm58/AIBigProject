import datetime

import ai_lib.ai_io as ai_io
import ai_lib.ai_helper as ai_helper


class AlgorithmPart3:
    NAME = 'AlgorithmPart3'
    PREVIOUS = {
        1: [0],
        2: [1],
        3: [0],
        4: [0, 1, 2, 3],
        5: [2, 4],
        6: [3, 4],
        7: [4, 6],
        8: [4, 5, 7]
    }

    def __init__(self, inputs):
        self.inputs = inputs  # a list of n inputs
        self.results = []  # a list of n results

        # START: Find freq_dict for each input in inputs
        self.freq_dicts = []
        for i in self.inputs:
            self.freq_dicts.append(ai_helper.get_frequency_dict(i))
        # END

    def heuristic(self, state, index):
        score = 0

        # START: Find a list of remaining letters (letters that are not in 'state')
        letters_left = self.inputs[index][:]
        for letter in state:
            letters_left.remove(letter)
        # END

        len_state = len(state)

        if len_state == 2:
            for letter in letters_left:
                if ai_io.has_meaning(state[0], state[1], letter):
                    score += 0.001
        elif len_state == 3:
            # check the first row
            if not ai_io.has_meaning(state[0], state[1], state[2]):
                return 0
            else:
                score += 0.001
#                for letter in letters_left:
#                    now_score = score
#                    for j in AlgorithmPart3.PREVIOUS[len_state]:
#                        try:
#                            score += self.freq_dicts[index][state[j] + letter] / 10
#                        except Exception:
#                            score = now_score  # reset score
#                            break
#                if score == 0.001:
                    # there is no letter in letters_left that can go in the next position
#                    return 0
        elif len_state == 4:
            score += 0.001
#            for letter in letters_left:
#                now_score = score
#                for j in AlgorithmPart3.PREVIOUS[len_state]:
#                    try:
#                        score += self.freq_dicts[index][state[j] + letter] / 10
#                    except Exception:
#                        score = now_score  # reset score
#                        break
#            if score == 0.001:
                # there is no letter in letters_left that can go in the next position
#                return 0
        elif len_state == 5:
            for letter in letters_left:
                if ai_io.has_meaning(state[3], state[4], letter):
                    score += 0.001
        elif len_state == 6:
            # check the second row
            if not ai_io.has_meaning(state[3], state[4], state[5]):
                return 0
            else:
                for letter in letters_left:
                    if ai_io.has_meaning(state[0], state[3], letter):
                        score += 0.002
        elif len_state == 7:
            # check the first column and the right-left diagonal
            if (not ai_io.has_meaning(state[0], state[3], state[6])
                or not ai_io.has_meaning(state[2], state[4], state[6])):
                return 0
            else:
                for letter in letters_left:
                    if ai_io.has_meaning(state[1], state[4], letter):
                        score += 0.004
        elif len_state == 8:
            # check the second column
            if not ai_io.has_meaning(state[1], state[4], state[7]):
                return 0
            else:
                for letter in letters_left:
                    if (ai_io.has_meaning(state[2], state[5], letter)
                        and ai_io.has_meaning(state[0], state[4], letter)
                        and ai_io.has_meaning(state[6], state[7], letter)):
                        score += 10
        elif len(state) == 9:
            # check the third column, the third row and the left-right diagonal
            if (not ai_io.has_meaning(state[2], state[5], state[8])
                or not ai_io.has_meaning(state[0], state[4], state[8])
                or not ai_io.has_meaning(state[6], state[7], state[8])):
                return 0
            else:
                score += 10

        return score

    def execute(self, trace, pause):
        # Loop through all inputs in 'inputs' list
        for i in range(len(self.inputs)):
            num_of_states = 0
            start_time = datetime.datetime.now()

            if ai_helper.check_all(self.inputs[i]):
                # the input is the result already
                end_time = datetime.datetime.now()
                time = int((end_time - start_time).total_seconds() * 1000)
                self.results.append((self.inputs[i], 1, time))
                continue

            L = []  # a list of all states

            # START: Insert all letter in self.inputs[i] into L
            # this is where initial states are created
            for letter in self.inputs[i]:
                # get frequency of 'letter'
                freq = self.freq_dicts[i][letter]
                
                # insert (letter, freq) into L and keep L sorted
                if (letter, freq) not in L:
                    for j in range(len(L)):
                        if freq > L[j][1]:
                            L.insert(j, (letter, freq))
                            break
                    else:
                        L.append((letter, freq))
            # END

            while True:
                if len(L) == 0:
                    # can not find the result
                    self.results.append("None")
                    break

                current_state = L.pop(0)[0]
                
                # increment number of states
                num_of_states += 1

                if len(current_state) == 9:
                    # Found the result
                    end_time = datetime.datetime.now()
                    time = int((end_time - start_time).total_seconds() * 1000)
                    self.results.append((current_state, num_of_states, time))
                    break

                # START: Find a list of remaining letters (letters that are not in current_state)
                letters_left = self.inputs[i][:]
                for letter in current_state:
                    letters_left.remove(letter)
                # END

                if trace:
                    next_states = []

                for letter in letters_left:
                    next_state = current_state + letter
                    h_next = self.heuristic(next_state, i)  # the heuristic value of 'next_state'
                    if h_next == 0:
                        # skip the state if its heuristic value is 0
                        continue

                    # START: Insert 'next_state' into L and keep L sorted
                    if (next_state, h_next) not in L:
                        for j in range(len(L)):
                            if h_next > L[j][1]:
                                L.insert(j, (next_state, h_next))
                                break
                        else:
                            L.append((next_state, h_next))
                    # END

                    if trace:
                        next_states.append("H({}) = {}".format(next_state, h_next))

                if trace:
                    print("Current state: {}".format(current_state))
                    print("Depth: {}".format(len(current_state)))
                    print("Next states:")
                    for state in L:
                        print(state)
                    if pause:
                        try:
                            next = raw_input("Next?")
                        except:
                            next = input("Next?")

