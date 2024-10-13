import sys
sys.path.insert(1, 'service')

import homomorphic_pb2_grpc as homomorphic
import homomorphic_pb2 as homo
import grpc
import logging
import numpy as np
from concurrent import futures
from common.common import *
import functools

def convert_grpc_list(data):
    if type(data) == tuple:
        return data
    return [data.polynomials0,data.polynomials1]

def convert_grpc_relinearization(key):
    res = []
    for i in key:
        print("huh")
        res += [i.item]
    return res

def convert_data_to_grpc(data):
    return homo.EncryptedData(
                polynomials0=list(data[0].tolist()),
                polynomials1=list(data[1].tolist()),
            )

class HomomorphicServer(homomorphic.HomomorphicServicer):
    def Compute(self, request, context):
        
        result = functools.reduce(lambda x, y: add_cipher(
                convert_grpc_list(x), 
                convert_grpc_list(y), 
                Q, POLY_MOD), request.data_array)
            
            # convert_grpc_relinearization(request.relinearization0), 
            # convert_grpc_relinearization(request.relinearization1))
        # print(request.evaluation_key)
        # print(decrypt(request.evaluation_key, N, Q, T, POLY_MOD, convert_grpc_list(request.data_array[2])))
        return homo.ComputationResponse(result=convert_data_to_grpc(result))
    


def serve():
    port = "9999"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    homomorphic.add_HomomorphicServicer_to_server(HomomorphicServer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__=="__main__":
    logging.basicConfig()
    serve()