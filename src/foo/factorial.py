# recursively calculates the factorial
def calculate_factorial(x: int) -> int:
    if x < 0:
        raise ValueError("input int must be positive")
    if x <= 1:
        return 1
    else:
        return x*calculate_factorial(x-1)