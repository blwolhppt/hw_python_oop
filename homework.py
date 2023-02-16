class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return f'Тип тренировки: {self.training_type}; ' \
               f'Длительность: {"%.3f" % self.duration} ч.; ' \
               f'Дистанция: {"%.3f" % self.distance} км; ' \
               f'Ср. скорость: {"%.3f" % self.speed} км/ч; ' \
               f'Потрачено ккал: {"%.3f" % self.calories}.'


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_M = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

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
        cal_run: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                          / self.M_IN_KM * self.duration * 60)
        return cal_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_1: float = 0.035
    CALORIES_MEAN_SPEED_2: float = 0.029
    KMH_IN_MS: float = 0.278
    SM_IN_M: int = 100

    def __init__(self, action: int, duration: float, weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        dur_min = self.duration * self.H_IN_M
        h_met = self.height / self.SM_IN_M
        speed_ms = self.get_mean_speed() * self.KMH_IN_MS
        return (self.CALORIES_MEAN_SPEED_1 * self.weight
                + (speed_ms ** 2 / h_met) * self.CALORIES_MEAN_SPEED_2
                * self.weight) * dur_min


class Swimming(Training):
    """Тренировка: плавание."""

    sdwig_speed: float = 1.1
    LEN_STEP: float = 1.38
    CONST_2 = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool) / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed()
                + self.sdwig_speed) * self.CONST_2 * self.weight \
            * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dict_class = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return dict_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
