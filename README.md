# video-codec-finder
Scans through your video collection and finds videos that are encoded with a specific codec.

## Use Cases and Summary

This utility finds files encoded with a specific video codec. You can specify which codec as a command line argument. It 
will print out a list of video files that are using the specified codec. This lets you re-encode or post-process those 
files as needed.

My use case: I have a NAS device that runs Plex. Plex sometimes struggles to transcode certain 
types of files due to an underpowered NAS CPU. When Plex struggles to transcode, the video stream is choppy and unwatchable.

The purpose of this script is to find all of the video files encoded with the challenging codec. I can then transcode 
them at an idle time, and watch a nice streaming video later!

# Dependencies
*Requires:*

python3 [link](https://www.python.org/downloads/)

mediainfo - a free, open source command-line utility that parses video and audio files to extract their codec information
[link](https://mediaarea.net/en/MediaInfo/Download)

# Usage

A basic find for HEVC encoded files with verbose logging turned on, to watch progress:
>  ./find_hevc.py --path_to_videos ~/Movies --verbose

A find for x264 encoded files:
> ./find_hevc.py --path_to_videos ~/Movies --alt_codec_name 264

*Note*: Since each file needs to be opened to obtain media info, if you are storing your video files on a network volume, this script may run slowly. Turn on verbose logging mode to watch progress.
# Output

A list of files with their full path. Try it out and see