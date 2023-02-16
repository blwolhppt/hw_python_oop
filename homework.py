class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float, distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return f'Тип тренировки: {self.training_type}; ' \
               f'Длительность: {"%.3f" % self.duration} ч.; Дистанция: {"%.3f" % self.distance} км; ' \
               f'Ср. скорость: {"%.3f" % self.speed} км/ч; Потрачено ккал: {"%.3f" % self.calories}.'


class Training:
    """Базовый класс тренировки."""

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.M_IN_KM = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        LEN_STEP = 0.65
        distance: float = self.action * LEN_STEP / self.M_IN_KM
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
        return InfoMessage(type(self).__name__, self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
        CALORIES_MEAN_SPEED_SHIFT: float = 1.79
        cal_run: float = ((CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                           + CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM * self.duration * 60)
        return cal_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int, duration: float, weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
        CALORIES_MEAN_SPEED_SHIFT: float = 0.029
        cal_walk: float = ((CALORIES_MEAN_SPEED_MULTIPLIER * self.weight + ((self.get_mean_speed()) / 1000 ** 2 /
                                                                            (
                                                                                        self.height / 100)) * CALORIES_MEAN_SPEED_SHIFT * self.weight) * self.duration * 60)
        return cal_walk


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self, action: int, duration: float, weight: float, length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed: float = self.length_pool * self.count_pool / self.duration / self.M_IN_KM
        return speed

    def get_spent_calories(self) -> float:
        SDWIG_SPEED: float = 1.1
        cal_swim: float = (self.get_mean_speed() + SDWIG_SPEED) * 2 * self.weight * self.duration
        return cal_swim


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
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

