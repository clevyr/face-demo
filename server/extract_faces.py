import os
import mtcnn
from PIL import Image
import numpy as np
import io
import random

TOO_SMALL = 0.025
EXTRACTOR = None

#load up the MTCNN extractor if we haven't already loaded it
def load_extractor():
    global EXTRACTOR
    if EXTRACTOR is None:
        EXTRACTOR = mtcnn.MTCNN()
    return EXTRACTOR

#extract all bounding box and face pixels from the specified file
def extract_faces(filepath, size = (224,224), confidence=0.75, jitter=False):
    print('extracting face from image.')

    #open the file as an image and convert it to RGB, if necessary
    img = Image.open(filepath).convert('RGB')
    #convert the image to a numpy array
    data = np.asarray(img)

    #load the MTCNN face extractor & extract faces
    extractor = load_extractor()
    faces = extractor.detect_faces(data)

    bboxes = []
    pixels = []

    #order faces by MTCNN 'confidence' score, descending
    for face in sorted(faces, key=lambda x: x['confidence'], reverse=True):
        # skip any faces with too low 'confidence' score
        if face['confidence'] < confidence:
            print('face confidence too low!', face['confidence'])
            continue
        minX, minY, width, height = face['box']    
        maxX, maxY = minX + width, minY + height
  
        #clamp the values since sometimes the bbox can go outside the image for some reason
        minX = max(0, minX)
        minY = max(0, minY)      
        maxX = min(img.width, maxX)
        maxY = min(img.height, maxY)
        #skip any faces that are too small
        if width/img.width < TOO_SMALL:
            print('face too small!')
            continue
        
        #print(minX, maxX, minY, maxY, (img.width, img.height))    
        #get the pixels from the image corresponding to the MTCNN bounding box & resize them.
        facePixels = data[minY:maxY, minX:maxX]
        faceImg = Image.fromarray(facePixels)
        faceImg = faceImg.resize(size)

        #normalize the bounding box coordinates to 0 -> 1 range
        bboxes.append( (minX / img.width, minY / img.height, maxX / img.width,  maxY / img.height) )
        pixels.append( np.asarray(faceImg) )
              
    return ( np.array(bboxes), np.array(pixels))

# extract all face data (bounding boxes and face pixels) from files in the specified directory
def extract_all_faces(dir='../data/faces', size = (224,224)):
    filenames = os.listdir(dir)

    def process_names(filepath):
        split = filepath.split('-')
        if len(split) > 2:
            return split[0] + '-' + split[1]
        return split[0]
    
    # get only the 'normal' employee photos, extract face data & the employee names
    data =  np.array([extract_faces(os.path.join(dir, x))[1] for x in filenames if x.endswith('-smile.jpg')])
    names = [process_names(x) for x in filenames if x.endswith('-smile.jpg')]  
    data = data.reshape((-1,) + data.shape[2:])
    return (names, data)
             

if __name__ == "__main__":
    #data = extract_all_faces()
    #print(data.shape)
    faces = extract_faces('../data/faces/dustin-smile.jpg', size=(224,224))
   

