import unittest
from io import StringIO
from unittest.mock import patch

# Импортировать функции из вашего модуля
from main import is_valid_input, parse_move, generate_losing_positions, computer_move, van_wythoff_game

class TestVanWythoffGame(unittest.TestCase):

    def test_computer_move_empty_pile(self):
        losing_positions = generate_losing_positions()

        # Когда одна куча пуста, например, 0 и 5
        self.assertEqual(computer_move(0, 5, losing_positions), (5, 'R'))

        # Когда другая куча пуста, например, 5 и 0
        self.assertEqual(computer_move(5, 0, losing_positions), (5, 'L'))
    def test_is_valid_input(self):
        self.assertTrue(is_valid_input("50,50"))
        self.assertTrue(is_valid_input("0,0"))
        self.assertTrue(is_valid_input("100,100"))
        self.assertFalse(is_valid_input("101,50"))
        self.assertFalse(is_valid_input("-1,50"))
        self.assertFalse(is_valid_input("50"))
        self.assertFalse(is_valid_input("50,a"))

    def test_parse_move(self):
        self.assertEqual(parse_move("5L"), (5, 'L'))
        self.assertEqual(parse_move("10R"), (10, 'R'))
        self.assertEqual(parse_move("3B"), (3, 'B'))
        self.assertIsNone(parse_move("5"))
        self.assertIsNone(parse_move("L"))
        self.assertIsNone(parse_move("5Z"))
        self.assertIsNone(parse_move("abc"))

    def test_generate_losing_positions(self):
        positions = generate_losing_positions()
        self.assertIsInstance(positions, list)
        self.assertGreater(len(positions), 0)
        for x, y in positions:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

    def test_computer_move(self):
        losing_positions = generate_losing_positions()

        # Проверяем случай, когда обе кучки равны (5, 5) — должно быть (5, 'B')
        self.assertEqual(computer_move(5, 5, losing_positions), (5, 'B'))  # Теперь возвращаем 5, 'B', а не 1

        # Проверка на случай, когда левая куча пустая (1, 0) — должен быть ход из левой кучи (1, 'L')
        self.assertEqual(computer_move(1, 0, losing_positions), (1, 'L'))

        # Проверка на случай, когда правая куча пустая (0, 1) — должен быть ход из правой кучи (1, 'R')
        self.assertEqual(computer_move(0, 1, losing_positions), (1, 'R'))

    def test_computer_move(self):
        losing_positions = generate_losing_positions()

        # Тест 1: Кучи одинаковые, забираем все спички из обеих куч.
        self.assertEqual(computer_move(5, 5, losing_positions), (5, 'B'))

        # Тест 2: Нужно забрать одинаковое количество из обеих куч
        self.assertEqual(computer_move(7, 7, losing_positions), (7, 'B'))

    def test_computer_move_minimum_case(self):
        losing_positions = generate_losing_positions()

        # Тест для минимальных куч
        self.assertEqual(computer_move(1, 1, losing_positions), (1, 'B'))

        # Тест с одной кучей пустой
        self.assertEqual(computer_move(1, 0, losing_positions), (1, 'L'))
        self.assertEqual(computer_move(0, 1, losing_positions), (1, 'R'))

    def test_computer_move_win_immediately(self):
        losing_positions = generate_losing_positions()

        # Тест на немедленный выигрыш: если позиция сразу проигрышная, компьютер забирает все спички
        self.assertEqual(computer_move(2, 2, losing_positions),
                         (2, 'B'))  # Ожидаем, что компьютер заберет 2 спички из обеих куч

    def test_computer_move_all_losing_positions(self):
        losing_positions = generate_losing_positions()

        # Проверка на все проигрышные позиции. Пусть 3 и 3 — проигрышная позиция.
        self.assertEqual(computer_move(3, 3, losing_positions),
                         (3, 'B'))  # Ожидаем, что компьютер заберет все спички из обеих куч

    def test_computer_move_single_match(self):
        losing_positions = generate_losing_positions()

        # Тест с одной спичкой в куче
        self.assertEqual(computer_move(1, 1, losing_positions),
                         (1, 'B'))  # Ожидаем, что компьютер заберет все из обеих куч

        # Когда в одной куче 0 спичек, а в другой 1
        self.assertEqual(computer_move(0, 1, losing_positions),
                         (1, 'R'))  # Ожидаем, что компьютер заберет 1 из правой кучи

    def test_computer_move_empty_pile(self):
        losing_positions = generate_losing_positions()

        # Когда в левой куче нет спичек, а в правой куче есть несколько
        self.assertEqual(computer_move(0, 3, losing_positions),
                         (3, 'R'))  # Ожидаем, что компьютер заберет все 3 из правой кучи

        # Когда в правой куче нет спичек, а в левой куче есть несколько
        self.assertEqual(computer_move(4, 0, losing_positions),
                         (4, 'L'))  # Ожидаем, что компьютер заберет все 4 из левой кучи


if __name__ == "__main__":
    unittest.main()