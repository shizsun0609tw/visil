import json
import numpy as np
import sys

# command example: python processing/outputprocessing.py processing_results=123123

in_path = "results.json"
out_path_folder = "processing/"
out_path_prefix = "processing_results_"
out_path_suffix = ".json"

for arg in sys.argv:
    if "processing_results=" in arg:
        out_path_suffix = arg.split("processing_results=")[1] + out_path_suffix

in_file = open(in_path, 'r')
out_file = open(out_path_folder + out_path_prefix + out_path_suffix, 'w')

data = json.load(in_file)
out_data = []

for video in data.keys():
    video_similarity = sorted(data[video].items(), key = lambda x:x[1], reverse = True)
    video_similarity = list((x, y) for x, y in video_similarity)[:3]

    out_data.append([video, video_similarity])

out_data.sort(key = lambda x:(x[1][0][1], x[1][1][1], x[1][2][1]), reverse=True)
json.dump(out_data, out_file, indent = 1)

in_file.close()
out_file.close()