# ID успешной посылки 52077661
# Это вариант отправленный на ревью и принятый

# def init_list_game() -> list:
    # game_list = [0] * 10
    # return game_list

# def make_list_game(g_list: list, row: str) -> list:
    # for char in row:
        # if char != '.':
            # i = int(char)
            # g_list[i] += 1
    # return g_list

# def check_game(g_list: list, k: int) -> int:
    # ball = 0
    # for i in range(1, 10):
        # if g_list[i] and g_list[i] <= k:
            # ball += 1
    # return ball

# if __name__ == "__main__":
    # game_list = init_list_game()
    # k2 = int(input()) * 2
    
    # for _ in range(4):
        # row = input()
        # game_list = make_list_game(game_list, row)

    # print(check_game(game_list, k2))


# этот вариант сделан позже и вроде как более лаконичный
class GameJuggle:
    def __init__(self, size, k):
        self.k = k
        self.game_list = [0] * size

    def make_list_game(self, row):
        for char in row:
            if char != '.':
                i = int(char)
                self.game_list[i] += 1

    def check_game(self):
        ball = 0
        for i in range(1, 10):
            if self.game_list[i] and self.game_list[i] <= self.k:
                ball += 1
        return ball


if __name__ == "__main__":
    k2 = int(input()) * 2
    game = GameJuggle(10, k2)
    
    for _ in range(4):
        row = input()
        game.make_list_game(row)

    print(game.check_game())
