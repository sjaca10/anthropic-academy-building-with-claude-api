def greeting():
  print("Hi there!")


def calculate_pi(digits=5):
    """Calculate pi to the given number of decimal digits.

    Uses the Nilakantha series:
        pi = 3 + 4/(2*3*4) - 4/(4*5*6) + 4/(6*7*8) - ...

    The series alternates, so the true value always lies between two
    consecutive partial sums. We iterate until the terms are far smaller
    than the last requested digit, then round to `digits` places.
    """
    if digits < 0:
        raise ValueError("digits must be non-negative")

    tolerance = 10 ** -(digits + 3)

    total = 3.0
    sign = 1
    n = 2
    while True:
        term = 4.0 / (n * (n + 1) * (n + 2))
        total += sign * term
        if term < tolerance:
            break
        sign = -sign
        n += 2

    return round(total, digits)


if __name__ == "__main__":
    greeting()
    print(calculate_pi())
