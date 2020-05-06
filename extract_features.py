import os
import pickle
from keras_vggface.vggface import VGGFace
from extract_faces import extract_all_faces, extract_faces

FEATURES = 'names_and_features.p'

def load_model():
    return VGGFace(model='senet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')

def extract_all_features():
    model = load_model()
    names,faces = extract_all_faces()
    return (names, model.predict(faces))


def extract_features(filepath):
    faces = extract_faces(filepath)
    model = load_model()
    return model.predict(faces)

def load_features():
    if os.path.exists(FEATURES):
        return pickle.load(open(FEATURES, 'rb'))
    else:
        print('Features file does not exist! Creating it now!')
        names, features = extract_all_features()
        with open(FEATURES,'wb') as f: pickle.dump((names,features), f)
        return (names, features)

if __name__ == "__main__":
    names, features = extract_all_features()
    with open(FEATURES,'wb') as f: pickle.dump((names,features), f)

    