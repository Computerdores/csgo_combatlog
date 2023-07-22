class GameStateManager:
    def __init__(self):
        self.map = Map()
        self.player = Player()
        self._round_phase = ""
        self._bomb = None
    
    def apply_round_phase(self, phase: str):
        if self._round_phase != phase:
            self._round_phase = phase
    
    def apply_bomb(self, bomb_state: str):
        if self._bomb != bomb_state:
            self._bomb = bomb_state

class Team:
    def __init__(self):
        self._score = None
        self._name = None
        self._consecutive_losses = None
        self._remaining_timeouts = None
        self._matches_won = None
    
    def apply_score(self, score: int):
        if self._score != score:
            self._score = score
    
    def apply_name(self, name: str):
        if self._name != name:
            self._name = name
    
    def apply_consecutive_losses(self, losses: int):
        if self._consecutive_losses != losses:
            self._consecutive_losses = losses
    
    def apply_timeouts_remaining(self, timeouts: int):
        if self._remaining_timeouts != timeouts:
            self._remaining_timeouts = timeouts
    
    def apply_matches_won_this_series(self, wins: int):
        if self._matches_won != wins:
            self._matches_won = wins

class Map:
    def __init__(self):
        self._round_wins = []

        self._mode = None
        self._name = None
        self._phase = None
        self._round = None

        self.team_ct = Team()
        self.team_t  = Team()

        self._num_matches_to_win_series = -1
        self._current_spectators = -1
        self._souveniers_total = -1
    
    def apply_round_win(self, round: int, result: str):
        assert round >= 0

        if round >= len(self._round_wins):
            for _ in range(round - len(self._round_wins) + 1):
                self._round_wins.append(None)
        
        if self._round_wins[round] != result:
            self._round_wins[round] = result
        
    def apply_mode(self, mode: str):
        if self._mode != mode:
            self._mode = mode
    
    def apply_name(self, name: str):
        if self._name != name:
            self._name = name
    
    def apply_phase(self, phase: str):
        if self._phase != phase:
            self._phase = phase
    
    def apply_round(self, round: int):
        if self._round != round:
            self._round = round
    
    def apply_num_matches_to_win_series(self, num_matches: int):
        if self._num_matches_to_win_series != num_matches:
            self._num_matches_to_win_series = num_matches
    
    def apply_current_spectators(self, spectators: int):
        if self._current_spectators != spectators:
            self._current_spectators = spectators
    
    def apply_souveniers_total(self, souveniers: int):
        if self._souveniers_total != souveniers:
            self._souveniers_total = souveniers

class Player:
    pass