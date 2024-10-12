import sys
sys.path.insert(1, 'service')

import argparse
import logging
import grpc
import homomorphic_pb2_grpc as homomorphic
import homomorphic_pb2 as homo
import numpy as np
from numpy.polynomial import polynomial as poly

parser = argparse.ArgumentParser()
parser.add_argument('--data', nargs='+', type=int)
parser.add_argument('--op')

def polymul(x, y, modulus, poly_mod):
    """Add two polynoms
    Args:
        x, y: two polynoms to be added.
        modulus: coefficient modulus.
        poly_mod: polynomial modulus.
    Returns:
        A polynomial in Z_modulus[X]/(poly_mod).
    """
    return np.int64(
        np.round(poly.polydiv(poly.polymul(x, y) % modulus, poly_mod)[1] % modulus)
    )


def polyadd(x, y, modulus, poly_mod):
    """Multiply two polynoms
    Args:
        x, y: two polynoms to be multiplied.
        modulus: coefficient modulus.
        poly_mod: polynomial modulus.
    Returns:
        A polynomial in Z_modulus[X]/(poly_mod).
    """
    return np.int64(
        np.round(poly.polydiv(poly.polyadd(x, y) % modulus, poly_mod)[1] % modulus)
    )

def gen_binary_poly(size):
    """Generates a polynomial with coeffecients in [0, 1]
    Args:
        size: number of coeffcients, size-1 being the degree of the
            polynomial.
    Returns:
        array of coefficients with the coeff[i] being 
        the coeff of x ^ i.
    """
    return np.random.randint(0, 2, size, dtype=np.int64)


def gen_uniform_poly(size, modulus):
    """Generates a polynomial with coeffecients being integers in Z_modulus
    Args:
        size: number of coeffcients, size-1 being the degree of the
            polynomial.
    Returns:
        array of coefficients with the coeff[i] being 
        the coeff of x ^ i.
    """
    return np.random.randint(0, modulus, size, dtype=np.int64)


def gen_normal_poly(size):
    """Generates a polynomial with coeffecients in a normal distribution
    of mean 0 and a standard deviation of 2, then discretize it.
    Args:
        size: number of coeffcients, size-1 being the degree of the
            polynomial.
    Returns:
        array of coefficients with the coeff[i] being 
        the coeff of x ^ i.
    """
    return np.int64(np.random.normal(0, 2, size=size))

def keygen(size, modulus, poly_mod):
    """Generate a public and secret keys
    Args:
        size: size of the polynoms for the public and secret keys.
        modulus: coefficient modulus.
        poly_mod: polynomial modulus.
    Returns:
        Public and secret key.
    """
    sk = gen_binary_poly(size)
    a = gen_uniform_poly(size, modulus)
    e = gen_normal_poly(size)
    b = polyadd(polymul(-a, sk, modulus, poly_mod), -e, modulus, poly_mod)
    return (b, a), sk

def encrypt(pk, size, q, t, poly_mod, pt):
    """Encrypt an integer.
    Args:
        pk: public-key.
        size: size of polynomials.
        q: ciphertext modulus.
        t: plaintext modulus.
        poly_mod: polynomial modulus.
        pt: integer to be encrypted.
    Returns:
        Tuple representing a ciphertext.      
    """
    # encode the integer into a plaintext polynomial
    m = np.array([pt] + [0] * (size - 1), dtype=np.int64) % t
    delta = q // t
    scaled_m = delta * m  % q
    e1 = gen_normal_poly(size)
    e2 = gen_normal_poly(size)
    u = gen_binary_poly(size)
    ct0 = polyadd(
            polyadd(
                polymul(pk[0], u, q, poly_mod),
                e1, q, poly_mod),
            scaled_m, q, poly_mod
        )
    ct1 = polyadd(
            polymul(pk[1], u, q, poly_mod),
            e2, q, poly_mod
        )
    return (ct0, ct1)

def run():
    args = parser.parse_args()
    

    n = 2**4
    # ciphertext modulus
    q = 2**15
    # plaintext modulus
    t = 2**8
    # polynomial modulus
    poly_mod = np.array([1] + [0] * (n - 1) + [1])
    # Keygen
    pk, sk = keygen(n, q, poly_mod)
    # Encryption
    pt1, pt2 = 73, 20
    cst1, cst2 = 7, 5
    ct1 = encrypt(pk, n, q, t, poly_mod, pt1)
    ct2 = encrypt(pk, n, q, t, poly_mod, pt2)

    print("[+] Ciphertext ct1({}):".format(pt1))
    print("")
    print("\t ct1_0:", ct1[0].tolist())
    # print("\t ct1_0:", ct1[0].tolist().dtype)
    print("\t ct1_0:", type([1,2,3]))
    print("\t ct1_1:", ct1[1])
    print("\t ct1_1:", type(ct1[1]))
    print("")
    print("[+] Ciphertext ct2({}):".format(pt2))
    print("")
    print("\t ct1_0:", ct2[0])
    print("\t ct1_1:", ct2[1])
    print("")

    with grpc.insecure_channel("localhost:9999") as channel:
        stub = homomorphic.HomomorphicStub(channel)
        response = stub.Compute(homo.ComputationRequest(
            data_array=list([homo.EncryptedData(
                polynomials0=list(ct1[0].tolist()),
                polynomials1=list([1,2,3]),
            )]),
        ))
    print("Greeter client received: " + response.message)

if __name__=="__main__":
    logging.basicConfig()
    run()
    
