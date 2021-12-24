# ID успешной посылки 52072982


def nearest_zero(n: int, l_house: list) -> list: 
    l_rez = [0] * n
    poz = 0
    empty = False

    def calculate_distance(i: int, fwd: bool, l_house: list):
        nonlocal empty
        nonlocal poz

        if l_house[i] == 0:
            empty = True
            poz = 0
        else:
            poz += 1
            if empty:
                if fwd:
                    l_rez[i] = poz
                else:
                    if l_rez[i] == 0:
                        l_rez[i] = poz
                    elif l_rez[i] > poz:
                        l_rez[i] = poz

    for i in range(n):
        calculate_distance(i, True, l_house)

    empty = False
    for i in reversed(range(n)):
        calculate_distance(i, False, l_house)

    return(l_rez)


if __name__ == "__main__":
    n = int(input())
    list_house = list(map(int, input().split()))
    print(*nearest_zero(n, list_house))
