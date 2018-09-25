#!/usr/bin/env python3

"""
Simple implementation of A* algorithm to solve 8 Puzzle.
It uses the sum of Manhattan distance of each number compared to where it should be in the puzzle as heuristic method.
"""
__author__ = "Rafael Telles"


class State(object):
    def __init__(self, s, moves):
        self.s = tuple(s)
        self.moves = moves

    def expand(self):
        states = []
        zero_index = self.s.index(0)
        if zero_index >= 3:  # can go up
            new_state = list(self.s)
            new_state[zero_index] = new_state[zero_index - 3]
            new_state[zero_index - 3] = 0
            new_moves = self.moves + '^'
            states.append(State(new_state, new_moves))
        if zero_index < 6:  # can go down
            new_state = list(self.s)
            new_state[zero_index] = new_state[zero_index + 3]
            new_state[zero_index + 3] = 0
            new_moves = self.moves + 'v'
            states.append(State(new_state, new_moves))
        if zero_index % 3 > 0:  # can go left
            new_state = list(self.s)
            new_state[zero_index] = new_state[zero_index - 1]
            new_state[zero_index - 1] = 0
            new_moves = self.moves + '<'
            states.append(State(new_state, new_moves))
        if zero_index % 3 <= 1:  # can go right
            new_state = list(self.s)
            new_state[zero_index] = new_state[zero_index + 1]
            new_state[zero_index + 1] = 0
            new_moves = self.moves + '>'
            states.append(State(new_state, new_moves))
        return states

    def print(self):
        print("|{}|{}|{}|\n"
              "|{}|{}|{}|\n"
              "|{}|{}|{}|".format(*self.s))

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        return self.s == other.s

    def __repr__(self):
        return "State({}), h={}, path={}".format(self.s, heuristic(self), self.moves)


def heuristic(state):
    h = 0
    for i, n in enumerate(state.s):
        h += abs(int(n / 3) - int(i / 3)) + abs(n % 3 - i % 3)
    return h


def cost(state):
    return heuristic(state) + len(state.moves)


def pop_best(states):
    list_states = list(states)
    list_states.sort(key=cost)
    best_state = list_states[0]
    states.remove(best_state)

    return best_state


# Algorithm got from https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable/
def check_solvable(state):
    state = list(state)
    state.remove(0)

    inversions = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[j] > state[i]:
                inversions += 1

    return inversions % 2 == 0


def solve(states):
    visited = set()
    while True:
        if not states:
            raise Exception("Busca falhou!")

        best_state = pop_best(states)
        visited.add(best_state.s)

        h = heuristic(best_state)
        if h == 0:
            return best_state

        if len(best_state.moves) > 31:  # The hardest 8 Puzzle state takes 31 moves.
            continue

        new_states = best_state.expand()
        states |= set([s for s in new_states if s.s not in visited])


if __name__ == "__main__":
    import random

    while True:
        state_s = list(range(9))
        random.shuffle(state_s)

        if check_solvable(state_s):
            state = State(state_s, "")
            state.print()
            print("Solving...")
            solution = solve({state})

            print("Solved! {} moves: {}".format(len(solution.moves), solution.moves))
            print()
