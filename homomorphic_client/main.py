import sys
sys.path.insert(1, 'service')

import argparse
import logging
import grpc
import homomorphic_pb2_grpc as homomorphic
import homomorphic_pb2 as homo
import numpy as np
from common.common import *

parser = argparse.ArgumentParser()
parser.add_argument('--data', nargs='+', type=int)
parser.add_argument('--op')



def convert_data_to_grpc(data, pk):
    res = []
    for i in data:
        ct1 = encrypt(pk, N, Q, T, POLY_MOD, i)
        res += [homo.EncryptedData(
                polynomials0=list(ct1[0].tolist()),
                polynomials1=list(ct1[1].tolist()),
            )]
    return res

def convert_grpc_to_data(encrypted_data):
    return [encrypted_data.polynomials0, encrypted_data.polynomials1]

def convert_relinearization_to_grpc(key):
    res = []
    for i in key:
        res += [homo.ItemArray(
            item=i
        )]
    return res

def run():
    args = parser.parse_args()
    pk, sk = keygen(N, Q, POLY_MOD)

    # rlk0_v1, rlk1_v1 = evaluate_keygen_v1(sk, N, Q, T, POLY_MOD, STD)
    # print(rlk0_v1)
    # print(rlk1_v1)

    with grpc.insecure_channel("localhost:9999") as channel:
        stub = homomorphic.HomomorphicStub(channel)
        response = stub.Compute(homo.ComputationRequest(
            data_array=convert_data_to_grpc(args.data, pk),
            operation=args.op,
            # relinearization0=convert_relinearization_to_grpc(rlk0_v1),
            # relinearization1=convert_relinearization_to_grpc(rlk1_v1),
        ))
    print("Total number after decryption: ")
    # print(response.result)
    decrypted_ct3 = decrypt(sk, N, Q, T, POLY_MOD, convert_grpc_to_data(response.result))
    print(decrypted_ct3)

if __name__=="__main__":
    logging.basicConfig()
    run()
    
