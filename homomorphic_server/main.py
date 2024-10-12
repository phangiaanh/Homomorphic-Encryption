import sys
sys.path.insert(1, 'service')

import homomorphic_pb2_grpc as homomorphic
import homomorphic_pb2 as homo
import grpc
import logging
from concurrent import futures


class HomomorphicServer(homomorphic.HomomorphicServicer):
    def Compute(self, request, context):
        print('something')
        return homo.ComputationResponse()
    


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