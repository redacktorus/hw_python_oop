class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    COEFF_CAL_1 = 18
    COEFF_CAL_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        calories = ((self.COEFF_CAL_1 * super().get_mean_speed()
                     - self.COEFF_CAL_2)
                    * self.weight) / (self.M_IN_KM
                                      * (self.duration
                                         * self.MIN_IN_H))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CAL_1 = 0.035
    COEFF_CAL_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height


    def get_spent_calories(self) -> float:
        """Калории ходьбы"""
        calories = ((self.COEFF_CAL_1
                     * self.weight
                     + (super().get_mean_speed() ** 2 // self.height)
                     * self.COEFF_CAL_2 * self.weight)
                    * (self.duration * self.MIN_IN_H))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_CAL_1 = 1.1
    COEFF_CAL_2 = 2
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Скорость плавания"""
        mean_speed = (self.length_pool
                      * self.count_pool) / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Калории плавания"""
        calories = \
            (super().get_mean_speed()
             + self.COEFF_CAL_1) \
            * self.COEFF_CAL_2 \
            * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    package = {'SWM': Swimming,
               'RUN': Running,
               'WLK': SportsWalking}
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
        training = read_package(workout_type, data)
        main(training)
