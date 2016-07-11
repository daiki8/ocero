import random
class Search(object):
  def __init__(self, *args, **kwargs):
    raise NotImplementedError

  def next_move(self, state, player):
    '''Returns (next_state, next_move) tuple.'''
    raise NotImplementedError


class SimpleSearch(Search):
  '''A search algorithm that only looks at immediate children.'''
  def __init__(self):
    pass  # do nothing

  def next_move(self, state, player):
    next_states = [(state.move(player, move), move)
                   for move in state.next_moves(player)]
    best_score = max(next_state.score(player)
                     for (next_state, _) in next_states)
    return random.choice([(next_state, move)
                          for (next_state, move) in next_states
                          if next_state.score(player) == best_score])


class MiniMaxSearch(Search):
  '''An implementation of mini-max search algorithm for a zero-sum game.'''
  def __init__(self, max_depth=4):
    self._max_depth = max_depth
    self._player = None

  def next_move(self, state, player):
    self._cache = {}
    self._player = player
    (_, move) = self._minimax(state, player, self._max_depth)
    return (state.move(player, move), move)

  def _put(self, state, player, value):
    self._cache[(state.serialize(), player.player_id)] = value

  def _get(self, state, player):
    return self._cache.get((state.serialize(), player.player_id), None)

  def _minimax(self, state, player, depth):
    #print '_minimax run'
    '''Maximizes or minimizes the score depending on whether player is myself.

    Returns (max_score, move) if player is myself.
    Returns (min_score, move) if player is opponent.
    '''
    cached_result = self._get(state, player)
    if cached_result is not None:
      return cached_result
    myself = player == self._player
    factor = 1 if myself else -1
    if depth > 0:
      if state.win(player):
        return (factor * state.score(player), None)
      elif state.win(player.next()):
        return (-factor * state.score(player.next()), None)
      elif state.draw():
        return (0, None)
      else:
        next_states = [(state.move(player, move), move)
                       for move in state.next_moves(player)]
        #print 'next_states is ' + str(next_states)
        children = [(self._minimax(next_state,
                                   player.next(),
                                   depth - 1)[0], move)
                    for (next_state, move) in next_states]
        if myself:
          # Maximizing score
          #print 'children is ' + str(children)
          (max_score, _) = max(children)
          #print "(max_score, _) is " + str((max_score, _))
          result = random.choice(filter(lambda (s, _): s == max_score,
                                        children))
        else:
          # Minimizing score
          (min_score, _) = min(children)
          result = random.choice(filter(lambda (s, _): s == min_score,
                                        children))
        self._put(state, player, result)
        return result
    else:
      # Running out of search depth, so making a best guess.
      return (factor * state.score(player), None)
