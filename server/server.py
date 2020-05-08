
from concurrent import futures
import logging
import grpc
import time
import os
import face_identifier_pb2
import face_identifier_pb2_grpc

from compare_features import compare_features
from extract_faces import load_extractor
from extract_features import load_model

#os.environ['KMP_DUPLICATE_LIB_OK']='True'

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class FaceIdentifier(face_identifier_pb2_grpc.FaceIdentifierServicer):
                            

    def Identify(self, request, context):

        # loop over the predicted scores and class labels
        result = compare_features(request.filepath)
        response = face_identifier_pb2.IdentifyReply()
        response.nearest.name = result['nearest']['name']
        response.nearest.distance = result['nearest']['distance']
        response.furthest.name = result['furthest']['name']
        response.furthest.distance = result['furthest']['distance']
        return response
    def IdentifyImage(self, request_iterator, context):
        

        imageBytes = b''

        for chunk in request_iterator:
            imageBytes = imageBytes + chunk.image

        
        import io
                
        #test = file.read()
        #print(len(test))       
        # loop over the predicted scores and class labels
        results = compare_features(io.BytesIO(imageBytes))

        response = face_identifier_pb2.IdentifyReply()
        for result in results:
            item = response.results.add()                  
            minX,minY,maxX,maxY = result['face']
            item.boundingBox.minX = minX
            item.boundingBox.minY = minY
            item.boundingBox.maxX = maxX
            item.boundingBox.maxY = maxY
            item.nearest.name = result['nearest']['name']
            item.nearest.distance = result['nearest']['distance']
            item.furthest.name = result['furthest']['name']
            item.furthest.distance = result['furthest']['distance']
        
        
        return response

def serve():
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    face_identifier_pb2_grpc.add_FaceIdentifierServicer_to_server(FaceIdentifier(), server)
    server.add_insecure_port('127.0.0.1:5002')
    server.start()
    #load_model()
    #load_extractor()
    #server.wait_for_termination()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()