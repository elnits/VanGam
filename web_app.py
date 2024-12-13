from flask import Flask, render_template, request, redirect, url_for
import math

def generate_q_values():
    q = []
    x = (1 + math.sqrt(5)) / 2
    y = 1 + 1 / x
    for i in range(100):
        q.append((int(i * x), int(i * y)))
    return q

def determine_computer_move(q, l, r):
    # Если оба стека пусты, игра завершена
    if l == 0 and r == 0:
        return 0, None

    # Проверить, есть ли текущая позиция в списке "проигрышных позиций" (q)
    for (q_l, q_r) in q:
        if l == q_l and r == q_r:
            # Если позиция является проигрышной, выбираем безопасный ход
            if l > r:
                return 1, 'L'  # Уменьшить больший стек
            else:
                return 1, 'R'

    # Проверка, какой ход приведёт к позиции, где игрок выиграет
    potential_moves = []
    for (q_l, q_r) in q:
        # Проверим все возможные ходы:
        # Уменьшить только левую кучу
        if q_l <= l and q_r == r:
            potential_moves.append(('L', l - q_l))

        # Уменьшить только правую кучу
        if q_r <= r and q_l == l:
            potential_moves.append(('R', r - q_r))

        # Уменьшить обе кучи (оба стека одновременно)
        if q_l <= l and q_r <= r and (l - q_l == r - q_r):
            potential_moves.append(('B', l - q_l))

    # Если не найдено подходящей стратегии, сделать безопасный ход
    if potential_moves:
        # Рассмотрим все возможные ходы и выберем тот, который не приведет к выигрышному ходу игрока
        for move, num in potential_moves:
            if move == 'L' and num <= l:
                # Уменьшаем левую кучу
                new_l, new_r = l - num, r
                if new_l == 0 and new_r == 0:  # если это приведет к победе игрока
                    continue  # пропускаем этот ход
                return num, 'L'

            if move == 'R' and num <= r:
                # Уменьшаем правую кучу
                new_l, new_r = l, r - num
                if new_l == 0 and new_r == 0:  # если это приведет к победе игрока
                    continue  # пропускаем этот ход
                return num, 'R'

            if move == 'B' and num <= min(l, r):
                # Уменьшаем обе кучи
                new_l, new_r = l - num, r - num
                if new_l == 0 and new_r == 0:  # если это приведет к победе игрока
                    continue  # пропускаем этот ход
                return num, 'B'

    # Если не найдено безопасного хода, делаем случайный (или фиксированный) ход
    if l > r:
        return 1, 'L'
    else:
        return 1, 'R'

def process_move(l, r, num, pile):
    if pile == 'L':
        l -= num
    elif pile == 'R':
        r -= num
    elif pile == 'B':
        l -= num
        r -= num
    return l, r

app = Flask(__name__)
q_values = generate_q_values()

game_data = {
    "left": 0,
    "right": 0,
    "message": "",
    "instructions_shown": False,
    "winner": None,
    "turn": "player"
}

@app.route('/')
def index():
    return render_template('index.html', game_data=game_data)

@app.route('/start', methods=['POST'])
def start_game():
    global game_data
    left = int(request.form['left'])
    right = int(request.form['right'])
    first_turn = request.form['first_turn']
    game_data = {
        "left": left,
        "right": right,
        "message": "Game started!",
        "instructions_shown": False,
        "winner": None,
        "turn": first_turn
    }

    # Если первый ход за компьютером, сразу переходим к ходу компьютера
    if first_turn == 'computer':
        return redirect(url_for('computer_move'))

    return redirect(url_for('index'))

@app.route('/move', methods=['POST'])
def player_move():
    global game_data
    move = request.form['move'].strip().upper()
    if len(move) < 2 or not move[:-1].isdigit() or move[-1] not in ('L', 'R', 'B'):
        game_data["message"] = "Invalid move format! Use a number followed by L, R, or B."
        return redirect(url_for('index'))

    num = int(move[:-1])
    pile = move[-1]

    if (pile == 'L' and num > game_data['left']) or \
       (pile == 'R' and num > game_data['right']) or \
       (pile == 'B' and (num > game_data['left'] or num > game_data['right'])):
        game_data["message"] = "Invalid move! You can't remove more matches than available."
        return redirect(url_for('index'))

    game_data['left'], game_data['right'] = process_move(game_data['left'], game_data['right'], num, pile)

    if game_data['left'] == 0 and game_data['right'] == 0:
        game_data['winner'] = 'player'
        game_data['message'] = "Congratulations, you win!"
        return redirect(url_for('index'))

    game_data['turn'] = 'computer'
    return redirect(url_for('computer_move'))

@app.route('/computer_move')
def computer_move():
    global game_data

    if game_data['turn'] != 'computer':
        return redirect(url_for('index'))

    num, pile = determine_computer_move(q_values, game_data['left'], game_data['right'])
    game_data['left'], game_data['right'] = process_move(game_data['left'], game_data['right'], num, pile)
    game_data['message'] = f"Computer takes {num}{pile}."

    if game_data['left'] == 0 and game_data['right'] == 0:
        game_data['winner'] = 'computer'
        game_data['message'] += " Sorry, you lose!"
        return redirect(url_for('index'))

    game_data['turn'] = 'player'
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)