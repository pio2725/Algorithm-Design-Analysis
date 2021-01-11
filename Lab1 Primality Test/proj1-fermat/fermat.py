import random


def prime_test(N, k):
    # This is the main function connected to the Test button. You don't need to touch it.
    return run_fermat(N,k), run_miller_rabin(N,k)

def mod_exp(x, y, N):
    # You will need to implement this function and change the return value.

    if y == 0:
        return 1

    # Recursively call mod_exp function with y divided by 2 rounding down.
    z = mod_exp(x, (y//2), N)

    if y % 2 == 0:  # when y is even
        return (z**2) % N
    else:
        return (x*(z**2)) % N

def fprobability(k):
    # You will need to implement this function and change the return value.
    # Fermat's test returns YES when N is not prime: p(fail) <= (1/2^k), so p(success) = 1 - p(fail)
    return 1 - 1/(2**k)

def mprobability(k):
    # You will need to implement this function and change the return value.
    # Miller-Rabin test passes when N is not prime : p(fail) <= (1/4^k), so p(success) = 1 - p(fail)
    return 1 - 1/(4**k)

def run_fermat(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likely want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.

    # If N is 2, it is prime
    if N == 2:
        return 'prime'

    for i in range(1, k+1):
        # Create random number to test
        random_number = random.randint(1, N - 1)
        if mod_exp(random_number, N-1, N) != 1:
            return 'composite'
    return 'prime'




def run_miller_rabin(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likely want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.

    # Return 'prime' when N is 2
    if N == 2:
        return 'prime'

    # K tests
    for i in range(1, k+1):
        # Pick a random number 1 <= a < N
        random_number = random.randint(1, N-1)

        # Initial test
        if mod_exp(random_number, N - 1, N) != 1:
            return 'composite'

        # Initial test passed, compute the sequence and find the first value that is not equal to 1
        y = (N - 1) / 2
        compute_sequence = True
        while compute_sequence:
            value = mod_exp(random_number, y, N)
            if value != 1:
                if (value + 1) != N:  # value is not -1
                    return 'composite'
                else:
                    break  # Passed the test, move on

            if y % 2 != 0:
                compute_sequence = False  # Can't square root anymore
            else:
                y = y / 2

    return 'prime'





