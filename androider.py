from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch

class VanWythoffGameApp(App):
    def build(self):
        self.l = 0
        self.r = 0
        self.player_first = False  # Изначально компьютер ходит первым
        self.losing_positions = self.generate_losing_positions()

        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.pile_label = Label(text="Установите начальные размеры стопок (максимум 100 каждая):", size_hint=(1, 0.1))
        self.root.add_widget(self.pile_label)

        self.pile_input = TextInput(hint_text="Формат: Л,П", size_hint=(1, 0.1), multiline=False)
        self.root.add_widget(self.pile_input)

        self.set_piles_button = Button(text="Установить стопки", size_hint=(1, 0.1))
        self.set_piles_button.bind(on_press=self.set_piles)
        self.root.add_widget(self.set_piles_button)

        self.first_move_label = Label(text="Выберите, кто ходит первым:", size_hint=(1, 0.1))
        self.root.add_widget(self.first_move_label)

        self.first_move_switch = Switch(active=False)  # По умолчанию, компьютер ходит первым
        self.first_move_switch.bind(active=self.on_first_move_switch_active)
        self.root.add_widget(self.first_move_switch)

        self.game_area = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.left_pile_label = Label(text="Левая: 0", size_hint=(0.5, 1))
        self.right_pile_label = Label(text="Правая: 0", size_hint=(0.5, 1))
        self.game_area.add_widget(self.left_pile_label)
        self.game_area.add_widget(self.right_pile_label)
        self.root.add_widget(self.game_area)

        self.move_input = TextInput(hint_text="Ваш ход (например, 2Л, 3П, 5О)", size_hint=(1, 0.1), multiline=False)
        self.root.add_widget(self.move_input)

        self.make_move_button = Button(text="Сделать ход", size_hint=(1, 0.1))
        self.make_move_button.bind(on_press=self.make_move)
        self.root.add_widget(self.make_move_button)

        self.status_label = Label(text="", size_hint=(1, 0.1))
        self.root.add_widget(self.status_label)

        return self.root

    def on_first_move_switch_active(self, instance, value):
        # Если переключатель включен, игрок ходит первым, если выключен - компьютер
        self.player_first = value

    def generate_losing_positions(self):
        q = []
        for i in range(100):
            x = int(i * ((1 + 5 ** 0.5) / 2))  # Золотое сечение
            y = x + i
            q.append((x, y))
        return q

    def is_losing_position(self, l, r):
        return (l, r) in self.losing_positions or (r, l) in self.losing_positions

    def set_piles(self, instance):
        try:
            l, r = map(int, self.pile_input.text.split(","))
            if 0 <= l <= 100 and 0 <= r <= 100:
                self.l = l
                self.r = r
                self.update_pile_labels()
                self.status_label.text = "Игра началась."
                if not self.player_first:
                    self.computer_move()
                    if self.l == 0 and self.r == 0:
                        self.status_label.text = "Компьютер победил!"
            else:
                self.show_popup("Некорректный ввод! Размеры стопок должны быть от 0 до 100.")
        except ValueError:
            self.show_popup("Некорректный формат ввода. Используйте: Л,П")

    def update_pile_labels(self):
        self.left_pile_label.text = f"Левая: {self.l}"
        self.right_pile_label.text = f"Правая: {self.r}"

    def make_move(self, instance):
        if self.l == 0 and self.r == 0:
            self.show_popup("Игра окончена! Начните новую игру.")
            return

        move = self.move_input.text.strip()
        if not move:
            self.show_popup("Введите корректный ход.")
            return

        parsed_move = self.parse_move(move)
        if not parsed_move:
            self.show_popup("Некорректный формат хода. Используйте: например, 2Л, 3П, 5О.")
            return

        num, pile = parsed_move
        if self.validate_move(num, pile):
            self.apply_move(num, pile)
            if self.l == 0 and self.r == 0:
                self.status_label.text = "Вы победили!"
                return

            self.computer_move()
            if self.l == 0 and self.r == 0:
                self.status_label.text = "Компьютер победил!"
        else:
            self.show_popup("Некорректный ход.")

    def parse_move(self, move_str):
        try:
            num = int(move_str[:-1])
            pile = move_str[-1].upper()
            if pile in ('Л', 'П', 'О'):
                return num, pile
            return None
        except (ValueError, IndexError):
            return None

    def validate_move(self, num, pile):
        if pile == 'Л' and 0 < num <= self.l:
            return True
        elif pile == 'П' and 0 < num <= self.r:
            return True
        elif pile == 'О' and 0 < num <= self.l and num <= self.r:
            return True
        return False

    def apply_move(self, num, pile):
        if pile == 'Л':
            self.l -= num
        elif pile == 'П':
            self.r -= num
        elif pile == 'О':
            self.l -= num
            self.r -= num
        self.update_pile_labels()

    def computer_move(self):
        for i in range(min(self.l, self.r) + 1):
            if self.is_losing_position(self.l - i, self.r - i):
                self.apply_move(i, 'О')
                self.status_label.text = f"Компьютер берет {i} из обеих стопок."
                return
        for i in range(1, self.l + 1):
            if self.is_losing_position(self.l - i, self.r):
                self.apply_move(i, 'Л')
                self.status_label.text = f"Компьютер берет {i} из левой стопки."
                return
        for i in range(1, self.r + 1):
            if self.is_losing_position(self.l, self.r - i):
                self.apply_move(i, 'П')
                self.status_label.text = f"Компьютер берет {i} из правой стопки."
                return
        if self.l > 0:
            self.apply_move(1, 'Л')
            self.status_label.text = "Компьютер берет 1 из левой стопки."
        elif self.r > 0:
            self.apply_move(1, 'П')
            self.status_label.text = "Компьютер берет 1 из правой стопки."

    def show_popup(self, message):
        popup = Popup(title="Ошибка", content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

if __name__ == "__main__":
    VanWythoffGameApp().run()