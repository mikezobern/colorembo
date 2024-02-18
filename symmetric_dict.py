class SymmetricDict:
    def __init__(self):
        self._data = set()

    def add_line(self, dot_name_1, dot_name_2):
        line = tuple(sorted([dot_name_1, dot_name_2]))
        self._data.add(line)

    def get_lines(self, dot_name):
        return {dot for line in self._data for dot in line if dot != dot_name}

# Пример использования
symmetric_dict = SymmetricDict()

symmetric_dict.add_line("dot1", "dot2")
symmetric_dict.add_line("dot2", "dot3")

print(symmetric_dict.get_lines("dot1"))  # Вывод: {'dot2'}
print(symmetric_dict.get_lines("dot2"))  # Вывод: {'dot1', 'dot3'}