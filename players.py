import re
from teams import Team


class Player:
    def __init__(self, name: str, team: Team, predict: tuple = ()):
        self.name = name
        self.team = team
        self.predict = predict

    def update_predict(self):
        with open("input.txt", 'r', encoding='cp1251') as f:
            lines = f.readlines()
        found_lines = []
        for line in lines:
            stripped = line.strip()
            match = re.match(r"^\s*\d+\.\s+(.+?)\s*\(", stripped)
            if not match:
                continue
            name_in_line = match.group(1).strip()
            if name_in_line == self.name:
                found_lines.append(stripped)
        if not found_lines:
            print(f"Прогноз для {self.name} не найден в input.txt")
            return
        last_line = found_lines[-1]
        if '(' not in last_line or ')' not in last_line:
            print(f"У {self.name} отсутствуют скобки в строке")
            return
        inline = last_line[last_line.rfind('(') + 1:last_line.rfind(')')]
        try:
            self.predict = tuple(map(int, inline.split('-')))
            print(f"Новый прогноз {self.name} - {self.predict}")
        except ValueError:
            raise ValueError("Невозможно преобразовать строку в прогноз")
