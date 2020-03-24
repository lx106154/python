import random


def encrypt(message, N, E):
    message_lst = list()
    for i in range(len(message)):
        message_lst.append(ord(message[i]))
    for i, j in enumerate(message_lst):
        message_lst[i] = (j ** E) % N
    return message_lst


def decrypt(encrypted_message, N, D):
    decrypted_list = list()
    for i, j in enumerate(encrypted_message):
        decrypted_list.append(chr((j ** D) % N))
    message = ''.join(decrypted_list)
    return message


def is_prime(P):
    if P > 1:
        for i in range(2, P//2):
            if P % i == 0:
                return False
        else:
            return True
    else:
        return False


def get_primes_in_range(low, high):
    primes = list()
    for i in range(low, high):
        if is_prime(i):
            primes.append(i)
    return primes


def get_prime_divisors(N):
    divisors = list()
    for i in get_primes_in_range(1, N+1):
        if N % i == 0:
            divisors.append(i)
    return divisors


def generate_key():
    P, Q = random.sample(get_primes_in_range(130, 300), 2)
    N = P * Q
    X = (P - 1) * (Q - 1)
    E = 2
    while any(item in get_prime_divisors(E) for item in get_prime_divisors(X)):
        E = E + 1
    D = 2
    while (D * E - 1) % X != 0:
        D = D + 1
    print("The keys are here: N =", N, "E =", E, "D =", D)
    return (N, E, D)

NED = generate_key()
message = "Hello World"
message_encrypted = encrypt(message, NED[0], NED[1])
print(message_encrypted)
message_decrypted = decrypt(message_encrypted, NED[0], NED[2])
print(message_decrypted)
