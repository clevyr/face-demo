import os
import io
import scipy.spatial
from extract_faces import extract_faces
from extract_features import load_features, extract_features
import sys
import numpy as np

# extract the facial features from the specified filepath 
# and compare each extracted set of features to
# the saved employee features.  Find the employee 
# that matches closest and the employee that is furthest.
def compare_features(filepath):
    bboxes, face_features = extract_features(filepath)
    if len(bboxes) == 0:
        return []
    names, allfeatures = load_features()        
    results = []
    for bbox,feature in zip(bboxes,face_features):    
        min = sys.float_info.max
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
        results.append({'face': bbox, 'nearest': {'name': nearest, 'distance': min }, 'furthest': { 'name': furthest, 'distance': max}})

    return results


    #for face in faces:

if __name__ == '__main__':
    success = 0
    fail = 0
    failed = []
    def process_names(filepath):
        split = filepath.split('-')
        if len(split) > 2:
            return split[0] + '-' + split[1]
        return split[0]

    filenames = [x for x in os.listdir('../data/faces') if x.endswith('-fun.jpg')]
    names = [process_names(x) for x in filenames]  

    for name, filename in zip(names,filenames):
        print(name)
        result = compare_features(os.path.join('../data/faces', filename))
        if len(result) ==0:
            continue
        if result[0]['nearest']['name'] == name: 
            success += 1 
        else: 
            fail += 1
            failed.append(name)
    

    print(success,fail, failed)