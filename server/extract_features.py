import os
import pickle
from keras_vggface.vggface import VGGFace
from keras.layers import GlobalAveragePooling2D, GlobalMaxPooling2D, Concatenate
from keras.engine import Model
from extract_faces import extract_all_faces, extract_faces
import numpy as np

FEATURES = 'names_and_features.p'
MODEL = None

def load_model():    
    global MODEL
    if MODEL is None:
        MODEL = VGGFace(model='senet50', include_top=False, input_shape=(224, 224, 3), pooling=None)
        output = MODEL.get_layer('add_16').output
        ## output = MODEL.layers[-1].output
        x1 = GlobalAveragePooling2D()(output)
        x2 = GlobalMaxPooling2D()(output)
        x = Concatenate()([x1,x2])
        MODEL = Model(MODEL.input, x)
        MODEL.summary()

    return MODEL

def extract_all_features():
    model = load_model()
    names,faces = extract_all_faces()

    features = []
    for face in faces:
        print('face shape', face.shape)
        f = model.predict(face)
        print('features shape', f.shape)
        avg = np.average(f, axis=0)
        print('avg shape', avg.shape)
        features.append( avg )
    return (names, features)
    
def extract_features(filepath):
    
    boxes,faces = extract_faces(filepath)
    model = load_model()

    features = []
    bboxes = []
    
    for box,face in zip(boxes,faces):
        print('extracting features from face')
        bboxes.append(np.average(box, axis=0))
        features.append( np.average(model.predict(face), axis=0 ) )
    return (bboxes, features)

def load_features():
    if os.path.exists(FEATURES):
        return pickle.load(open(FEATURES, 'rb'))
    else:
        print('Features file does not exist! Creating it now!')
        names, features = extract_all_features()
        with open(FEATURES,'wb') as f: pickle.dump((names,features), f)
        return (names, features)

if __name__ == "__main__":
    #bboxes,features = extract_features('../data/faces/dustin-smile.jpg')
    #print(bboxes[0].shape, features[0].shape)
    names, features = extract_all_features()
    with open(FEATURES,'wb') as f: pickle.dump((names,features), f)

    