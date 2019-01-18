import os
import numpy as np
import math
import sys
from wavedata.tools.obj_detection import obj_utils

#Set this index to exit after this many files
exit_idx = -1

def main():
    #INPUTS
    #dataset_dir = 'E:/data/object/label_2'
    label_dir = '/object/training/label_2'
    output_file = '/media/bradenhurl/hd/dataset_stats.txt'

    dataset_dir = '/home/bradenhurl/GTAData/'
    data_dir = dataset_dir + label_dir
    printEvery1000(data_dir)


def printEvery1000(data_dir):
    print(data_dir)
    print(os.path.abspath(obj_utils.__file__))

    #Need to change these next 2
    ped_distance_var = 0
    distance = []

    classes = []
    obj_counts = []
    obj_images = []

    #crawl through all files in the directory
    files = os.listdir(data_dir)
    num_files = len(files)
    file_idx = 0
    max_dist = 0
    startIdx = 40000
    endIdx = 50000
    for idx in range(startIdx,endIdx):
        sys.stdout.write("\rProcessing index {} / {}".format(
            idx + 1 - startIdx, endIdx - startIdx))
        sys.stdout.flush()
        filepath = data_dir + '/' + "{:06d}.txt".format(idx)
        contains = []
        if os.stat(filepath).st_size != 0:
            obj_list = obj_utils.read_labels(data_dir, idx)
            for obj in obj_list:
                x = obj.t[0]**2
                y = obj.t[1]**2
                z = obj.t[2]**2
                dist = math.sqrt(x + y + z)
                contains.append(obj.type)
                if obj.type not in classes:
                    classes.append(obj.type)
                    obj_counts.append(0)
                    obj_images.append(0)
                class_idx = classes.index(obj.type)
                obj_counts[class_idx] = obj_counts[class_idx] + 1
        
        for obj_class in classes:
            if obj_class in contains:
                class_idx = classes.index(obj_class)
                obj_images[class_idx] = obj_images[class_idx] + 1

        if idx % 1000 == 0:
            for obj_class in classes:
                if obj_class == 'Pedestrian':
                    class_idx = classes.index(obj_class)
                    print("\n{} count: {}".format(obj_class, obj_counts[class_idx]))
                    print("{} image count: {}".format(obj_class, obj_images[class_idx]))
            classes = []
            obj_counts = []
            obj_images = []
        #Update indices
        file_idx = file_idx + 1

        if file_idx == exit_idx:
            break

    return classes, obj_counts, obj_images
    print("")
    #print summary stats
    for obj_class in classes:
        class_idx = classes.index(obj_class)
        print("\n{} count: {}".format(obj_class, obj_counts[class_idx]))
        print("{} image count: {}".format(obj_class, obj_images[class_idx]))

main()