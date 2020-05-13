import os
import pickle
from keras_vggface.vggface import VGGFace
from keras.layers import GlobalAveragePooling2D, GlobalMaxPooling2D, Concatenate
from keras.engine import Model
from extract_faces import extract_all_faces, extract_faces
import numpy as np
import tensorflow as tf

FEATURES = 'names_and_features.p'
MODEL = None

#load the 'senet50' VGGFace model and modify it slightly
def load_model():
    global MODEL
    if MODEL is None:
        MODEL = VGGFace(model='senet50', include_top=False, input_shape=(224, 224, 3), pooling=None)
        output = MODEL.get_layer('add_16').output
        x1 = GlobalAveragePooling2D()(output)
        x2 = GlobalMaxPooling2D()(output)
        x = Concatenate()([x1,x2])
        MODEL = Model(MODEL.input, x)
    return MODEL

# get all the employee faces from mtcnn and run them through our VGGFace model
# to get each employee's feature vector.
def extract_all_features():
    model = load_model()
    names,faces = extract_all_faces()
    
    return (names, model.predict(faces))

# get the bounding box & face pixels from the specified filepath and run them trhough
# the VGGFace model to get each face's feature vector.
def extract_features(filepath):
    
    bboxes,faces = extract_faces(filepath)
    model = load_model()
   
    print('extracting features from faces')       
    return (bboxes, model.predict(faces))

# load each employee's names & features from file
# create the file if it does not exist
def load_features():
    if os.path.exists(FEATURES):
        with open(FEATURES, 'rb') as f: return pickle.load(f)
    else:
        print('Features file does not exist! Creating it now!')
        names, features = extract_all_features()
        #variance = np.var(features, axis=0)
        #indices = np.argsort(variance)
        #indices = indices[::-1]#[:128]
        #features = features[:,indices]

        with open(FEATURES,'wb') as f: pickle.dump((names,features),f)#,indices), f)
        return (names, features)

if __name__ == "__main__":
    #names, features, sort = load_features()
    #print(features.shape)
    bboxes,features = extract_features('../data/faces/dustin-smile.jpg')
    print(bboxes[0].shape, features[0].shape)
    #names, features = extract_all_features()
    
    
    
    #names, features, sort = load_features()
    #test = np.array(features)    
    
    #print(variance[sort[0]: sort[5]])

    