
import scipy.spatial
from extract_faces import extract_faces
from extract_features import load_features, extract_features

def compare_features(filepath):
    feature = extract_features(filepath)[0]

    names,features = load_features()
    #print(names)
    min = 1.0
    closest = None
    for n,f in zip(names,features):
        dist = scipy.spatial.distance.cosine(feature, f)
        print(n, dist)
        if dist < min:
            closest = n
            min = dist
    
    print(closest)


    #for face in faces:

if __name__ == '__main__':
    compare_features('data/faces/ryan-fun.jpg')


