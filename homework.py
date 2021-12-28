from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.'
                    )

    def get_message(self) -> str:
        """Получить информацию о тренировке."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
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

    COEF_CAL_1: int = 18
    COEF_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        """Бег: расход калорий."""
        speed: float = self.get_mean_speed()
        speed_based_calc: float = (self.COEF_CAL_1 * speed) - self.COEF_CAL_2
        cal_rate: float = speed_based_calc * self.weight / self.M_IN_KM
        minutes: float = self.duration * self.MIN_IN_H
        calories: float = cal_rate * minutes
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_CAL_1: float = 0.035
    COEF_CAL_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Спортивная ходьба: расход калорий."""
        square_speed: float = self.get_mean_speed() ** 2
        speed_based_calc: float = (square_speed
                                   // self.height
                                   * self.COEF_CAL_2
                                   * self.height)
        weight_based_calc: float = self.COEF_CAL_1 * self.weight
        cal_rate: float = speed_based_calc + weight_based_calc
        minutes: int = self.duration * self.MIN_IN_H
        calories: float = cal_rate * minutes
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    COEF_CAL_1: float = 1.1
    COEF_CAL_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: int,
            count_pool: int,) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Плавание: скорость."""
        pool: int = self.length_pool * self.count_pool
        mean_speed: float = pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Плавание: расход калорий."""
        speed: float = self.get_mean_speed()
        calories: float = (
                        (speed + self.COEF_CAL_1)
                        * self.COEF_CAL_2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    packages = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    return packages[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: str = training.show_training_info()
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
