from dataclasses import dataclass

from typing import List, Dict, Union, Type, Tuple


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {"%.3f" % self.duration} ч.; '
                f'Дистанция: {"%.3f" % self.distance} км; '
                f'Ср. скорость: {"%.3f" % self.speed} км/ч; '
                f'Потрачено ккал: {"%.3f" % self.calories}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_M: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError("Метод не переопределяется у наследника!")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_FOR_WEIGHT: float = 0.035
    COEF_FOR_SPEED: float = 0.029
    KMH_IN_MS: float = 0.278
    SM_IN_M: int = 100

    def __init__(self, action: int, duration: float, weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        duration_in_min: float = self.duration * self.H_IN_M
        height_in_meter: float = self.height / self.SM_IN_M
        speed_in_ms: float = self.get_mean_speed() * self.KMH_IN_MS
        return (self.COEF_FOR_WEIGHT * self.weight
                + (speed_in_ms ** 2 / height_in_meter) * self.COEF_FOR_SPEED
                * self.weight) * duration_in_min


class Swimming(Training):
    """Тренировка: плавание."""

    COEF_FOR_SPEED: float = 1.1
    LEN_STEP: float = 1.38
    CONST_2: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool) / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.COEF_FOR_SPEED) * self.CONST_2 * self.weight
                * self.duration)


list_of_types = Tuple[int, float, float]


def read_package(workout_type: str, data: List[list_of_types]) -> Training:
    """Прочитать данные полученные от датчиков."""

    dict_class: Dict[str, Type[Union[Swimming, Running, SportsWalking]]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in dict_class:
        return dict_class[workout_type](*data)
    else:
        print("Нет такого типа треннировки")


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
