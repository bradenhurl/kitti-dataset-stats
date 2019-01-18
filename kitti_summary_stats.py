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
    gta_classes, gta_obj_counts, gta_obj_images = getDatasetStats(data_dir)

    dataset_dir = '/home/bradenhurl/Kitti/'
    data_dir = dataset_dir + label_dir
    classes, obj_counts, obj_images = getDatasetStats(data_dir)

    #Output txt file as latex table
    with open(output_file, 'w+') as f:
        for class_str in gta_classes:
            writeLine(f, class_str, gta_classes, gta_obj_counts, gta_obj_images, classes, obj_counts, obj_images)

        for class_str in classes:
            if class_str not in gta_classes:
                writeLine(f, class_str, gta_classes, gta_obj_counts, gta_obj_images, classes, obj_counts, obj_images)

def writeLine(f, class_str, gta_classes, gta_obj_counts, gta_obj_images,
              classes, obj_counts, obj_images):
    inGTA = class_str in gta_classes
    gta_idx = -1
    if inGTA:
        gta_idx = gta_classes.index(class_str)
    inKitti = class_str in classes
    class_idx = -1
    if inKitti:
        class_idx = classes.index(class_str)

    gta_count = 'NA'
    kitti_count = 'NA'
    gta_avg = 'NA'
    kitti_avg = 'NA'
    if inGTA:
        gta_count = gta_obj_counts[gta_idx]
        gta_avg = "{:.2f}".format(gta_obj_counts[gta_idx] / gta_obj_images[gta_idx])
    if inKitti:
        kitti_count = obj_counts[class_idx]
        kitti_avg = "{:.2f}".format(obj_counts[class_idx] / obj_images[class_idx])
    f.write("{} & {} & {} & {} & {}\\\\\n".format(class_str,
                                                kitti_count,
                                                gta_count,
                                                kitti_avg,
                                                gta_avg
                                                ))

def getDatasetStats(data_dir):
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
    for file in os.listdir(data_dir):
        sys.stdout.write("\rProcessing index {} / {}".format(
            file_idx + 1, num_files))
        sys.stdout.flush()
        filepath = data_dir + '/' + file
        contains = []
        if os.stat(filepath).st_size != 0:
            idx = int(os.path.splitext(file)[0])
            if idx < 40000:
                continue
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
                #if obj.type == 'Pedestrian':
                    #max_dist = max(max_dist, dist)
                #if dist < 80:
                class_idx = classes.index(obj.type)
                obj_counts[class_idx] = obj_counts[class_idx] + 1
                #elif obj.type == 'Pedestrian':
                #    print(obj.t[0], obj.t[1], obj.t[2])
                #    print(dist, idx)
        
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
    for idx in range(40000,50000)
        sys.stdout.write("\rProcessing index {} / {}".format(
            idx + 1 - startIdx, endIdx - startIdx))
        sys.stdout.flush()
        filepath = data_dir + '/' + "{:06d}.txt"
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