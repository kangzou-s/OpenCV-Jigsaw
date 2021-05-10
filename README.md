# Scattered puzzle generator/collector
This is a barebones basis for a student project on image processing with Python and OpenCV.


## Required packages:
* opencv2
* numpy
* matplotlib

## How to use the provided scripts
Folder [puzzle generator](puzzle_generator) contains:
1. Script [cut_into_pieces.py](puzzle_generator/cut_into_pieces.py) that takes a specified image from folder [pics](puzzle_generator/pics), a cutting pattern from folder [patterns](puzzle_generator/patterns) and generates multiple image files each containing one single piece of the puzzle, in the same folder.

2. Script [generate_scatter.py](puzzle_generator/generate_scatter.py) that takes the output images from the previous script, applies random rotations to them and put them all on a specified background, on one signle image.

This final [image](puzzle_generator/puzzle_unsolved.jpg) is the starting point for your solution. Your task is to reverse the process: extract the pieces, orient them upright and analyse their morphology.

## What to do
Files [1_segment_pieces.py](/1_segment_pieces.py), [2_extract_features.py](/2_extract_features.py)
[3_orient_pieces](/3_orient_pieces) are for you to complete. Please see the concrete tasks in the corresponding files. Your ouputs should be written to the provided folders [results](/results) and [segmented](/segmented)
