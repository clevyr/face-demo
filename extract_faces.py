import os
import mtcnn
from PIL import Image
import numpy as np

extractor = mtcnn.MTCNN()	
def extract_all_faces(dir='data/faces', size = (224,224)):
    filenames = os.listdir(dir)

    def process_names(filepath):
        split = filepath.split('-')
        if len(split) > 2:
            return split[0] + '-' + split[1]
        return split[0]
        
    data =  np.array([extract_faces(os.path.join(dir, x)) for x in filenames if x.endswith('-smile.jpg')])
    names = [process_names(x) for x in filenames if x.endswith('-smile.jpg')]  
    return (names, data.reshape((-1,) + data.shape[2:]))
    

def extract_faces(filepath, size = (224,224), confidence=0.7):
    img = Image.open(filepath)
    data = np.asarray(img)
    
    faces = extractor.detect_faces(data)

    def process(face):
        minX, minY, width, height = face['box']
        maxX, maxY = minX + width, minY + height
        facePixels = data[minY:maxY, minX:maxX]
        faceImg = Image.fromarray(facePixels)
        faceImg = faceImg.resize(size)
        faceImg.show()
        return np.asarray(faceImg)

    return np.array([process(x) for x in faces if x['confidence'] >= confidence])
                

if __name__ == "__main__":
    data = extract_all_faces()
    print(data.shape)
    #faces = extract_faces('data/faces/dustin-smile.jpg', size=(224,224))
    #print(faces)
   

