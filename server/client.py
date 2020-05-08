from __future__ import print_function

import grpc

import face_identifier_pb2_grpc
import face_identifier_pb2


def run():
  channel = grpc.insecure_channel('localhost:5002')
  stub = face_identifier_pb2_grpc.FaceIdentifierStub(channel)

  request = face_identifier_pb2.IdentifyRequest()
  request.filepath = 'out.jpg'
  response = stub.Identify(request)
  print("client received: " + repr(response))


if __name__ == '__main__':
  run()