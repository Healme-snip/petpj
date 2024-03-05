"""Реализация классов для хранения данных в виде таблицы"""

from random import randint
from typing import Union


class Matrix:
    """Класс для хранения матрицы"""
    def __init__(
        self,
        h: int | None = None,
        w: int | None = None,
        args: list[list[int | float]] | None = None,
    ) -> None:
        self.body: list[list[int | float]]
        self.a: int | None
        self.b: int | None
        if h and w:
            self.h = h
            self.w = w
            self.zeros()
        elif not (h and w) and args:
            self.body = args
            self.h = len(self.body)
            self.w = len(self.body[0])

    def zeros(self) -> None:
        """Создание матрицы нулей"""
        self.body = [[0 for _ in range(self.w)] for _ in range(self.h)]

    def rand_mat(self, h: int, w: int, a: int, b: int) -> "Matrix":
        """Создание матрицы случайных чисел"""
        self.h = h
        self.w = w
        self.a = a
        self.b = b
        self.body = [
            [randint(a, b) for _ in range(self.w)]
            for _ in range(self.h)
        ]
        return self

    def range_mat(self, h: int = None, w: int = None, a: int = None, b: int = None) -> 'Matrix':
        """Создание матрицы с заданными параметрами"""
        self.h = h
        self.w = w
        self.a = a
        self.b = b
        self.body = [
            [i] for i in range(a, b)
        ]
        return self

    # def form_mat(self, h, w, a, b, random: bool = False)

    def transpose(self) -> None:
        """Транспонирование матрицы"""
        self.body = [
            [self.body[i][j] for i in range(self.h)]
            for j in range(self.w)
        ]

    def mean(self) -> float | int:
        """Среднее значение всех элементов матрицы"""
        return sum([sum(row) for row in self.body]) / (self.h * self.w)

    def __add__(self, other: "Matrix") -> "Matrix":
        if self.h != other.h or self.w != other.w:
            raise ValueError("Таблицы не одинакого размера!")
        arr = Matrix(self.h, self.w)
        for i in range(self.h):
            for j in range(self.w):
                arr.body[i][j] = self.body[i][j] + other.body[i][j]
        return arr

    def __mul__(self, other: "Matrix") -> "Matrix":
        if self.w != other.h:
            raise ValueError("Неправильные размеры матриц!")
        result = Matrix(self.h, other.w)
        for i in range(self.h):
            for j in range(other.w):
                for k in range(self.w):
                    result.body[i][j] += self.body[i][k] * other.body[k][j]
        return result

    def __floordiv__(self, other: "Matrix") -> "Matrix":
        if self.h != other.h or self.w != other.w:
            raise ValueError("Таблицы не одинакого размера!")
        arr = Matrix(self.h, self.w)
        for i in range(self.h):
            for j in range(self.w):
                arr.body[i][j] = self.body[i][j] // other.body[i][j]
        return arr

    def __div__(self, other: "Matrix") -> "Matrix":
        if self.h != other.h or self.w != other.w:
            raise ValueError("Таблицы не одинакого размера!")
        arr = Matrix(self.h, self.w)
        for i in range(self.h):
            for j in range(self.w):
                arr.body[i][j] = self.body[i][j] / other.body[i][j]
        return arr

    def __str__(self) -> str:
        mx = "["
        for row in self.body:
            mx += f"{row},\n"
        return mx[:-2] + "]"


class Series:
    """Класс для хранения столбца данных"""

    def __init__(self, key: str, matrix: Matrix) -> None:
        self.key: str = key
        self.matrix: Matrix = matrix

    def mean(self) -> float | int:
        """Среднее значение всех элементов столбца"""
        return self.matrix.mean()

    def __str__(self) -> str:
        mx = f"{self.key}\n["
        for row in self.matrix.body:
            mx += f"{row},\n"
        return mx[:-2] + "]"


class DataFrame:
    """Класс для хранения таблицы данных"""

    def __init__(self, *series_list: Series) -> None:
        """Инициализация таблицы данных"""
        self.body: tuple[Series, ...] = series_list

    def keys(self) -> list[str | None]:
        """Возвращает список ключей"""
        return [series.key for series in self.body]

    def values(self) -> list[Matrix]:
        """Возвращает список значений"""
        return [series.matrix for series in self.body]

    def apnd(self, *other: Series) -> None:
        """Добавляет новый столбец в таблицу"""
        self.body += other

    def __str__(self) -> str:
        ser_mat = Matrix().range_mat(
            a=0,
            b=min([len(i.body) for i in self.values()])
        )
        ser_id = Series('ID', ser_mat)
        self.body = (ser_id,) + self.body
        s = "\t".join([s.key for s in self.body])
        s += "\n"
        for i in range(len(self.body[0].matrix.body)):
            row = [str(series.matrix.body[i]) for series in self.body]
            if i < 5 or i == (len(self.body[0].matrix.body) - 1):
                s += "\t".join(row) + "\n"
            elif i == 5:
                s += "...\n"
        return s

    def __getattr__(self, attr: str) -> str:
        return f"{attr} не существует"

    def __getitem__(self, key: str) -> Union[Series, None]:
        """Возвращает столбец по ключу"""
        if key in self.keys():
            for series in self.body:
                if series.key == key:
                    return series
        else:
            raise KeyError(f"{key} is not exist")
        return None

    def __setitem__(self, key: str, value: Matrix) -> None:
        """Добавляет новый столбец в таблицу"""
        if key in self.keys():
            raise KeyError(f"{key} is already exist")
        self.apnd(Series(key, value))


if __name__ == "__main__":
    m1 = Matrix().rand_mat(5, 1, 0, 10)
    s1 = Series("Type 1", m1)
    df = DataFrame(s1)
    m2 = Matrix().rand_mat(10, 10, 0, 10)
    df['Type 2'] = m2
    print(df)
