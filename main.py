from math import log, ceil
from random import random, randint
from decimal import Decimal, getcontext

# Задаем распределение вероятностей
W1_1 = 0.7
W2_1 = 1 - W1_1

W1_2 = 0.2
W2_2 = 1 - W1_2

# Какая вероятность ошибки нас устраивает
LAMBDA = 0.05

# Длина последовательностей, которыми мы кодируем слова
K = 5

# Количество итераций для тестирования найденного m
N = 100


def calc_h() -> float:
    h_1 = W1_1 * log(W1_1) + W2_1 * log(W2_1) - (W1_1 * log(W1_2) + W2_1 * log(W2_2))
    h_2 = W1_2 * log(W1_2) + W2_2 * log(W2_2) - (W1_2 * log(W1_1) + W2_2 * log(W2_1))
    return min(h_1, h_2)


def calc_math_expectation(c, inner_square=False) -> float:
    if c == 1:
        if inner_square:
            return W1_1 * (log(W1_1) - log(W1_2)) * (log(W1_1) - log(W1_2)) + W2_1 * (log(W2_1) - log(W2_2)) * (log(W2_1) - log(W2_2))
        return W1_1 * (log(W1_1) - log(W1_2)) + W2_1 * (log(W2_1) - log(W2_2))
    if c == 2:
        if inner_square:
            return W1_2 * (log(W1_2) - log(W1_1)) * (log(W1_2) - log(W1_1)) + W2_2 * (log(W2_2) - log(W2_1)) * (log(W2_2) - log(W2_1))
        return W1_2 * (log(W1_2) - log(W1_1)) + W2_2 * (log(W2_2) - log(W2_1))


def m(_lambda, k) -> int:
    def _m(c, _lambda, k) -> int:
        math_expectation = calc_math_expectation(c)

        numerator = calc_math_expectation(c, inner_square=True) - math_expectation ** 2
        denominator = ((math_expectation - calc_h() / 2) ** 2) * (1 - (1 - _lambda) ** (1 / k))
        return ceil(numerator / denominator)

    m1 = _m(1, _lambda, k)
    m2 = _m(2, _lambda, k)
    return max(m1, m2)


def calc_probability(c, m_max) -> bool:
    def twist_letter(x) -> int:
        r = random()
        if x == 1:
            if r <= W1_1:
                return 1
            return 2
        if x == 2:
            if r <= W2_2:
                return 2
            return 1


    letters = [c] * m_max  # Посылаем букву m раз
    twisted_letters = list(map(twist_letter, letters))  # Искажаем букву с определенной вероятностью

    p1 = Decimal(1)
    p2 = Decimal(1)
    for i in twisted_letters:
        if c == 1:
            if i == 1:
                p1 *= Decimal(W1_1)
                p2 *= Decimal(W1_2)
            elif i == 2:
                p1 *= Decimal(W2_1)
                p2 *= Decimal(W2_2)
        elif c == 2:
            if i == 1:
                p1 *= Decimal(W1_2)
                p2 *= Decimal(W1_1)
            elif i == 2:
                p1 *= Decimal(W2_2)
                p2 *= Decimal(W2_1)
    
    return p1 > p2


if __name__ == "__main__":
    getcontext().prec = 100000

    threshold_probability = (1 - LAMBDA) ** (1 / K)

    m_max = m(LAMBDA, K)  # Это сколько раз нам нужно посылать буквы
    print("m_max =", m_max)

    success_attempts = 0
    for i in range(N):
        if calc_probability(randint(1, 2), m_max):
            success_attempts += 1
        # print(f"#{i + 1}: P = {success_attempts / (i + 1)}")
    
    result = success_attempts / N

    print(f"Полученная вероятность: {result}\nПороговая вероятность по условию: {threshold_probability}")
    print(f"{result} > {threshold_probability} == {result > threshold_probability}")  # Должно быть True
