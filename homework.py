from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Формирует текст сообщения."""
        text_training_type_ru = 'Тип тренировки'
        text_duration_ru = 'Длительность'
        text_distance_ru = 'Дистанция'
        text_mean_spead_ru = 'Ср. скорость'
        text_calories_ru = 'Потрачено ккал'

        return (f'{text_training_type_ru}: {self.training_type}; '
                f'{text_duration_ru}: {self.duration:.3f} ч.; '
                f'{text_distance_ru}: {self.distance:.3f} км; '
                f'{text_mean_spead_ru}: {self.speed:.3f} км/ч; '
                f'{text_calories_ru}: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return message


class Running(Training):
    """Тренировка: бег."""

    KOEF_CAL_1 = 18
    KOEF_CAL_2 = 20

    def get_spent_calories(self) -> float:
        """Бег: расход калорий."""
        speed = self.get_mean_speed()
        speed_based_calc = (self.KOEF_CAL_1 * speed) - self.KOEF_CAL_2
        cal_rate = speed_based_calc * self.weight / self.M_IN_KM
        minutes = self.duration * self.MIN_IN_H
        calories = cal_rate * minutes
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KOEF_CAL_1 = 0.035
    KOEF_CAL_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Спортивная ходьба: расход калорий."""
        square_speed = super().get_mean_speed() ** 2
        speed_based_calc = (square_speed
                            // self.height
                            * self.KOEF_CAL_2
                            * self.height)
        weight_based_calc = self.KOEF_CAL_1 * self.weight
        cal_rate = speed_based_calc + weight_based_calc
        minutes = self.duration * self.MIN_IN_H
        calories = cal_rate * minutes
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    KOEF_CAL_1 = 1.1
    KOEF_CAL_2 = 2
    LEN_STEP = 1.38

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: int,
            count_pool: int,) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Плавание: скорость."""
        pool = self.length_pool * self.count_pool
        mean_speed = pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Плавание: расход калорий."""
        speed = self.get_mean_speed()
        calories = (speed + self.KOEF_CAL_1) * self.KOEF_CAL_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    package = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    return package[workout_type](*data)


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
        try:
            training = read_package(workout_type, data)
            main(training)
        except KeyError:
            print('Неизвестный тип тренировки. :(')
