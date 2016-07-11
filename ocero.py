# -*- coding; utf-8 -*-
import random
from game import Player
from game import State
from search import MiniMaxSearch

class Ocero(State):
    _EMPTY = -1
    _WALL = 3
    _vec8 = (-11, -10, -9, -1, 1, 9, 10, 11)
    pass_count = [0, 0]

    def __init__(self, board=None):
        if board is not None:
            self._board = board
        else:
            self._board = [self._EMPTY] * 100
            self._board[0:10] = self._board[90:100] = [self._WALL] * 10
            for i in xrange(10):
                self._board[i*10] = self._board[i*10-1] = self._WALL
            self._board[44] = self._board[55] = 0
            self._board[45] = self._board[54] = 1
        self._score = None

    def valid_reversible(self, player, next_move):
        if 0 <= next_move < 100 and self._board[next_move] == self._EMPTY:
            for i in self._vec8:
                current = next_move
                flag1 = flag2 = False
                if self._board[current + i] == player.next_player.player_id:
                    flag1 = True
                    while self._board[current + i] == player.next_player.player_id:
                        current = current + i
                    if self._board[current + i] == player.player_id:
                        flag2 = True
                else:
                    continue
                if flag1 == True and flag2 == True:
                    return True
        else:
            return False

    def reverse(self, player, next_move):
        if 0 <= next_move < 100 and self._board[next_move] == self._EMPTY:
            reverseList = []
            reverseList.append(next_move)
            for i in self._vec8:
                x = []
                current = next_move + i
                while self._board[current] == player.next_player.player_id:
                    x.append(current)
                    current = current + i
                if self._board[current] == player.player_id and len(x) is not 0:
                    reverseList.extend(x)
            return reverseList


    def valid_move(self, player, next_move):
        if self.valid_reversible(player, next_move) == True and 0 <= next_move < 100 and self._board[next_move] == self._EMPTY:
            return True
        else:
            return False

    def next_moves(self, player):
        valid_move_list = [i for i in range(100) if self.valid_move(player, i)]
        if len(valid_move_list) == 0:
            return ['pass']
        else:
            return valid_move_list

    def move(self, player, i):
        if i == 'pass':
            return Ocero(self._board)
        else:
            #print 'check move'
            assert 0 <= i < 100#check range
            assert self._board[i] == self._EMPTY#check empty
            assert self.valid_move(player, i)#check reverse
            #print 'update board'
            reverseList = self.reverse(player, i)
            nextBoard = [player.player_id if j in reverseList else self._board[j] for j in range(100)]
            return Ocero(nextBoard)

    def win(self, player):
        #print 'self._board is ' + str(self._EMPTY not in self._board)
        #print 'player is ' + str(player.player_id)
        if state.next_moves(player)[0] == 'pass':
           self.pass_count[player.player_id] = 1
        else:
            self.pass_count[player.player_id] = 0
        #print 'self.pass_count is ' + str(self.pass_count)
        return all(i == 1 for i in self.pass_count) or self._EMPTY not in self._board and self._board.count(player.player_id) > self._board.count(player.next_player.player_id)

    def draw(self):
        return self._EMPTY not in self._board


    def score(self, player):
        if self._score is None:
            if self.win(player):
                self._score = 100
            else:
                self._score = 2 * self._board.count(player.player_id)
                self._score = self._score + 2 * len(state.next_moves(player))
                if state.next_moves(player) == 'pass':
                    self._score = self._score - 50
        return self._score


    def serialize(self):
        return tuple(self._board)


    def __str__(self):
        s = {-1: ' ',  # empty
             0: 'o',  # player 0
             1: 'x',  # player 1
             3: '*',  # wall
             }
        sep = '-+-+-+-+-+-+-+-+-+-'
        rows = ['%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (s[self._board[i]],
                              s[self._board[i + 1]],
                              s[self._board[i + 2]],
                              s[self._board[i + 3]],
                              s[self._board[i + 4]],
                              s[self._board[i + 5]],
                              s[self._board[i + 6]],
                              s[self._board[i + 7]],
                              s[self._board[i + 8]],
                              s[self._board[i + 9]]) for i in range(0, 100, 10)]
        return '\n'.join([rows[0], sep, rows[1], sep, rows[2], sep, rows[3], sep, rows[4], sep, rows[5], sep, rows[6], sep, rows[7], sep, rows[8], sep, rows[9]])

def read_move(state, player):
    while True:
        n = raw_input('Enter your move (1-100): ')
        if n.isdigit():
            n = int(n) - 1
            if state.valid_move(player, n):
                print 'n is ' + str(n)
                return n
        print 'n is ' + str(n)
        print 'try again'

if __name__ == '__main__':
    players = [Player(0, 'human'), Player(1, 'computer')]
    players[0].next_player = players[1]
    players[1].next_player = players[0]
    player = players[0]
    state = Ocero()
    search_algorithm = MiniMaxSearch()
    print state
    while True:
        print 'now player is ' + str(player.player_id)
        print state.next_moves(player)
        if player.player_name == 'human':
            #state = state.move(player, read_move(state, player))
            move = random.choice(state.next_moves(player))
            print 'human move is ' + str(move)
            state = state.move(player, move)
        else:
            (state, move) = search_algorithm.next_move(state, player)
            #print "%s's move: %d" % (str(player).title(), move + 1)
        print state
        if state.win(player):
            print '%s wins!' % str(player).title()
            break
        elif state.draw():
            print 'Draw'
            break
        else:
            player = player.next()