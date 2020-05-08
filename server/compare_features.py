import io
import scipy.spatial
from extract_faces import extract_faces
from extract_features import load_features, extract_features


def compare_features(filepath):
    bboxes, face_features = extract_features(filepath)
    names,allfeatures = load_features()    

    results = []
    for bbox,feature in zip(bboxes,face_features):    
        min = 1.0
        max = 0.0
        nearest = None
        furthest = None
        for n,f in zip(names,allfeatures):
            dist = scipy.spatial.distance.cosine(feature, f)        
            if dist < min:
                nearest = n
                min = dist
            if dist > max:
                furthest = n
                max = dist

        print(nearest, furthest)               
        results.append({'face': bbox, 'nearest': {'name': nearest, 'distance': min }, 'furthest': { 'name': furthest, 'distance': max}})

    return results


    #for face in faces:

if __name__ == '__main__':
    results = compare_features('../data/faces/matt-fun.jpg')
    print(results)


