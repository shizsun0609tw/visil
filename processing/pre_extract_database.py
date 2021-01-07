import json
import argparse
import tensorflow as tf
import sys
import pickle

sys.path.append('/home/zhenhua/Project/Fake_News/visil')

from tqdm import tqdm
from model.visil import ViSiL
from datasets import VideoGenerator    
    
# python3 processing/pre_extract_database.py --query_file queries.txt --database_file database.txt --model_dir ckpt/resnet/

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query_file', type=str, required=True,
                        help='Path to file that contains the query videos')
    parser.add_argument('-d', '--database_file', type=str, required=True,
                        help='Path to file that contains the database videos')
    parser.add_argument('-o', '--output_file', type=str, default='results.json',
                        help='Name of the output file. Default: \"results.json\"')
    parser.add_argument('-n', '--network', type=str, default='resnet',
                        help='Backbone network used for feature extraction. '
                             'Options: \"resnet\" or \"i3d\". Default: \"resnet\"')
    parser.add_argument('-m', '--model_dir', type=str, default='ckpt/resnet',
                        help='Path to the directory of the pretrained model. Default: \"ckpt/resnet\"')
    parser.add_argument('-s', '--similarity_function', type=str, default='chamfer',
                        help='Function that will be used to calculate similarity '
                             'between query-target frames and videos.'
                             'Options: \"chamfer\" or \"symmetric_chamfer\". Default: \"chamfer\"')
    parser.add_argument('-b', '--batch_sz', type=int, default=128,
                        help='Number of frames contained in each batch during feature extraction. Default: 128')
    parser.add_argument('-g', '--gpu_id', type=int, default=0,
                        help='Id of the GPU used. Default: 0')
    parser.add_argument('-l', '--load_queries', action='store_true',
                        help='Flag that indicates that the queries will be loaded to the GPU memory.')
    parser.add_argument('-t', '--threads', type=int, default=8,
                        help='Number of threads used for video loading. Default: 8')
    args = parser.parse_args()


    # Initialize ViSiL model
    model = ViSiL(args.model_dir, net=args.network,
                  load_queries=args.load_queries, gpu_id=args.gpu_id,
                  similarity_function=args.similarity_function,
                  queries_number=None)


    # Create a video generator for the database video
    enqueuer = tf.keras.utils.OrderedEnqueuer(VideoGenerator(args.database_file, all_frames='i3d' in args.network),
                                              use_multiprocessing=True, shuffle=False)
    enqueuer.start(workers=args.threads, max_queue_size=args.threads*2)
    generator = enqueuer.get()

    # Extract database features

    features = dict()
    pbar = tqdm(range(len(enqueuer.sequence)))
    for _ in pbar:
        frames, video_id = next(generator)
        if frames.shape[0] > 1:
            features[video_id] = model.extract_features(frames, args.batch_sz).tolist()

        pbar.set_postfix(video_id=video_id)
    enqueuer.stop()

    with open('processing/database_features.pk', 'wb') as f:
        pickle.dump(features, f, protocol=pickle.HIGHEST_PROTOCOL)

    #with open('processing/database_features.json', 'w') as f:
    #    json.dump(features, f, indent=1)
