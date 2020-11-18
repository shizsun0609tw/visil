import json
import numpy as np

in_path = "results.json"
out_path = "processing_results.json"

in_file = open(in_path, 'r')
out_file = open(out_path, 'w')

data = json.load(in_file)
out_data = dict()

for video in data.keys():
    video_similarity = sorted(data[video].items(), key = lambda x:x[1], reverse = True)
    video_similarity = list((x, y) for x, y in video_similarity if y > 0 and x != video)

    out_data.update({video:[video_similarity]})

json.dump(out_data, out_file, indent = 1)

in_file.close()
out_file.close()