#!/usr/bin/python3

import argparse
import json
import os
import pprint
from subprocess import run

#FILE_TYPES is a tuple to compy with endswith method
FILE_TYPES = ('.avi','.m4v', '.mkv', '.mp4')
#DEFAULT_SEARCH_FOR_CODEC is a parameter that needs the case-sensitive codec you're looking for, 
# as returned by mediainfo
DEFAULT_SEARCH_FOR_CODEC = 'HEVC'

def parse_args():
    parser = argparse.ArgumentParser(description="Find files encoded with a specific video codec", 
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-p", "--path_to_videos", help="Path to root of video files directory")
    parser.add_argument("-c", "--alt_codec_name", 
                        help="If not HEVC, provide a string for another video codec to search for. Case Sensitive.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    config = vars(args)

    print(config)
    return config

def get_file_list(path):
    video_paths = []
    print("Searching path: " + path + " for types " + ' '.join(FILE_TYPES))
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(FILE_TYPES):
                str = os.path.join(root, file)
                video_paths.append(str)

    return video_paths    

def find_matching_files(file_list, search_for_codec, verbose_logging):
    matched = []
    for filename in file_list:
        if verbose_logging:
            print("Analyzing " + filename)
        cmd = "mediainfo --Output=JSON \"{}\" ".format(filename)
        retval = run(cmd, capture_output=True, shell=True, text=True)
        try:
            media_info_json = json.loads(retval.stdout)
        except json.decoder.JSONDecodeError as ex:
            print("Failed to parse mediainfo to json for file " + filename)
            print(ex)

        if not type(media_info_json) is dict:
            print ("media info doesn't appear to be a JSON dictionary for file " + filename)
        else:
            if not ('media' in media_info_json.keys()):
                print("media information doesn't have a media blob, so cannot analyze, for " + filename)
            
            else:
                media = media_info_json['media']
                #some Plex Optimized video files seem to be missing the metadata block that starts with @ref
                if '@ref' in media.keys():# media['@ref']:
                    if 'track' in media.keys():
                        all_tracks = media['track']
                        for track in all_tracks:
                            if 'Format' in track.keys():
                                #print("File " + filename + " has format: " + track['Format'])
                                if track['Format'] == search_for_codec:
                                    matched.append(filename)

    return matched


config = parse_args()
file_list = get_file_list(config['path_to_videos'])

search_for_codec = DEFAULT_SEARCH_FOR_CODEC
if config['alt_codec_name']:
    search_for_codec = config['alt_codec_name']


matches = find_matching_files(file_list, search_for_codec, config['verbose'])
print("Video files that use the codec " + search_for_codec + " include:")
print('\n'.join(matches))
