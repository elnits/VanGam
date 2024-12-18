def is_valid_input(input_str):
    try:
        a, b = map(int, input_str.split(","))
        return 0 <= a <= 100 and 0 <= b <= 100
    except ValueError:
        return False

def parse_move(move_str):
    if len(move_str) < 2:
        return None
    num = move_str[:-1]
    pile = move_str[-1].upper()
    if not num.isdigit() or pile not in ('L', 'R', 'B'):
        return None
    return int(num), pile

def generate_losing_positions():
    q = []
    for i in range(100):
        x = int(i * ((1 + 5 ** 0.5) / 2))  # Golden ratio
        y = x + i
        q.append((x, y))
    return q

def is_losing_position(l, r, losing_positions):
    return (l, r) in losing_positions or (r, l) in losing_positions

def computer_move(l, r, losing_positions):
    # Если куча одинаковая, пробуем забрать все спички из обеих куч.
    if l == r:
        # Если после забирания всех спичек не будет проигрышной позиции
        if not is_losing_position(l - l, r - r, losing_positions):  # Проверка на проигрышную позицию после забора всех спичек
            return l, 'B'  # Берем все спички из обеих куч

    # Иначе пытаемся найти проигрышную позицию, забирая одинаковое количество из обеих куч
    for i in range(1, min(l, r) + 1):
        if is_losing_position(l - i, r - i, losing_positions):
            return i, 'B'  # Берем одинаковое количество из обеих куч

    # Если не нашли выигрыша при одинаковых количествах, пробуем забрать из одной кучки
    for i in range(1, l + 1):
        if is_losing_position(l - i, r, losing_positions):
            return i, 'L'  # Берем только из левой кучи

    for i in range(1, r + 1):
        if is_losing_position(l, r - i, losing_positions):
            return i, 'R'  # Берем только из правой кучи

    # Если нет выигрыша, делаем случайный допустимый ход
    if l > 0:
        return 1, 'L'
    if r > 0:
        return 1, 'R'
    return 0, 'B'

def van_wythoff_game():
    # Print the title with exact spacing
    print("                        VANGAM")
    print("                  CREATIVE COMPUTING")
    print("                MORRISTOWN, NEW JERSEY")
    print("\n" * 3, end="")

    print("VAN WYTHOFF'S GAME: DO YOU WANT INSTRUCTIONS ", end="")
    b = input().strip().upper()
    if b.startswith('Y'):
        print("YOU ARE TO CREATE TWO PILES OF MATCHES, EACH CONTAINING 100 OR LESS.")
        print("YOU PLAY ALTERNATELY WITH ME, AND OUR MOVES CONSIST OF:")
        print("          (A) TAKING AWAY 1 OR MORE MATCHES FROM ONE PILE ONLY, OR")
        print("          (B) TAKING AWAY THE SAME NUMBER FROM EACH PILE.")
        print("THE ONE WHO TAKES AWAY THE LAST MATCH OF ALL WINS.")
        print("ENTER YOUR MOVES IN THIS MANNER:")
        print("          2L - (2 LEFT) TAKE TWO FROM LEFT PILE")
        print("          3R - (3 RIGHT) TAKE THREE FROM RIGHT PILE")
        print("          5B - (5 BOTH) TAKE FIVE FROM EACH PILE")

    losing_positions = generate_losing_positions()

    while True:
        print("\nDESIRED PILE SIZES (NUMBER,NUMBER):", end=" ")
        piles_input = input().strip()
        if not is_valid_input(piles_input):
            print("INVALID INPUT. PLEASE ENTER TWO NUMBERS BETWEEN 0 AND 100.")
            continue
        l, r = map(int, piles_input.split(","))
        break

    print("DO YOU WANT TO GO FIRST ", end="")
    b = input().strip().upper()
    player_first = b.startswith('Y')

    while l > 0 or r > 0:
        print(f"                          LEFT  {l:<5} RIGHT  {r:<5}")
        if player_first:
            while True:
                print("YOUR MOVE:", end=" ")
                move = input().strip()
                parsed_move = parse_move(move)
                if not parsed_move:
                    print("IMPROPER ENTRY, STOP FOOLING AROUND.")
                    continue
                num, pile = parsed_move
                if pile == 'L' and 0 < num <= l:
                    l -= num
                    break
                elif pile == 'R' and 0 < num <= r:
                    r -= num
                    break
                elif pile == 'B' and 0 < num <= l and num <= r:
                    l -= num
                    r -= num
                    break
                print("INVALID MOVE. TRY AGAIN.")
        else:
            num, pile = computer_move(l, r, losing_positions)
            if pile == 'L':
                l -= num
            elif pile == 'R':
                r -= num
            elif pile == 'B':
                l -= num
                r -= num
            print(f"I TAKE: {num}{pile}")

        if l == 0 and r == 0:
            if player_first:
                print("CONGRATULATIONS. YOU ARE A VERY CLEVER VAN WYTHOFF'S GAMESMAN.")
            else:
                print("SORRY - I WIN. DON'T FEEL BADLY - I'M AN EXPERT.")
            break

        player_first = not player_first

    print("DO YOU WANT TO PLAY AGAIN ", end="")
    b = input().strip().upper()
    if b.startswith('Y'):
        van_wythoff_game()

if __name__ == "__main__":
    van_wythoff_game()

