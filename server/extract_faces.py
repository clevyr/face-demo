import os
import mtcnn
from PIL import Image
import numpy as np
import io
import random

EXPANSION = 0.0
JITTER = 5
SAMPLES = 1
ANGLE = 10

EXTRACTOR = None
def load_extractor():
    global EXTRACTOR
    if EXTRACTOR is None:
        EXTRACTOR = mtcnn.MTCNN()
    return EXTRACTOR

def extract_all_faces(dir='../data/faces', size = (224,224)):
    filenames = os.listdir(dir)

    def process_names(filepath):
        split = filepath.split('-')
        if len(split) > 2:
            return split[0] + '-' + split[1]
        return split[0]
        
    data =  np.array([extract_faces(os.path.join(dir, x))[1] for x in filenames if x.endswith('-smile.jpg')])
    names = [process_names(x) for x in filenames if x.endswith('-smile.jpg')]  
    data = data.reshape((-1,) + data.shape[2:])
    return (names, data)
    

def extract_faces(filepath, size = (224,224), confidence=0.85, jitter=False):
    print('extracting face from image.')
    img = Image.open(filepath).convert('RGB')
    data = np.asarray(img)
    extractor = load_extractor()
    faces = extractor.detect_faces(data)

    results = []
    for face in faces:
        bboxes = []
        pixels = []
        if face['confidence'] < confidence:
            print('face confidence too low!', face['confidence'])
            continue
        for i in range(SAMPLES):
            minX, minY, width, height = face['box']                
            maxX, maxY = minX + width, minY + height
            # width = int(width * EXPANSION)
            # height = int(height * EXPANSION)
            # minX = max(0, minX - width)
            # minY = max(0, minY - height)
            # maxX = min(img.width, maxX + width)
            # maxY = min(img.height, maxY + height)
            if jitter:
                minX += random.randrange(-JITTER, JITTER)
                minY += random.randrange(-JITTER, JITTER)
                maxX += random.randrange(-JITTER, JITTER)
                maxY += random.randrange(-JITTER, JITTER)
            minX = max(0, minX)
            minY = max(0, minY)
            maxX = min(img.width, maxX)
            maxY = min(img.height, maxY)
            facePixels = data[minY:maxY, minX:maxX]
            faceImg = Image.fromarray(facePixels)
            faceImg = faceImg.resize(size)
            #faceImg = faceImg.rotate(random.uniform(-ANGLE, ANGLE))
            #faceImg.show()
            bboxes.append((minX / img.width, minY / img.height, maxX / img.width,  maxY / img.height))
            pixels.append(np.asarray(faceImg))
        results.append({ 'bboxes' : np.array(bboxes), 'pixels' : np.array(pixels)})
            #return (np.array( minX / img.width, minY / img.height, maxX / img.width,  maxY / img.height), np.asarray(faceImg))    

    print('num faces: ', len(results))
    return ( np.array([x['bboxes'] for x in results]), np.array([x['pixels'] for x in results]))
    # bboxes (x1,y1,x2,y2) & pixels
    #return (np.array([ x[0] for x in results ]), np.array([ x[1] for x in results ]))
                

if __name__ == "__main__":
    #data = extract_all_faces()
    #print(data.shape)
    faces = extract_faces('../data/faces/dustin-smile.jpg', size=(224,224))
   

