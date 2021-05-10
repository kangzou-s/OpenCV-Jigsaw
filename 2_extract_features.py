# This script takes an individual piece from folder './segmented' and detects its:
# 1) Four corners;
# 2) Four edges;
# 3) Classifies each edge (0 - flat, 1 - pin, -1 - hole);
# 4) Saves the results to the disk as an object of class Piece (use pickle or json).
