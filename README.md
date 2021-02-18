# K-means
## Purpose
The objective of the program is to automatically cluster similar elements.

## Rules
- The user can choose one of the files - "noraml.txt" or "unbalance.txt"
- The user can choose the count of the clusters.
- The program should use random restart, keeping the best solution in the new generations.
- The best solution is chosen based on internal cluster distance.

## About the program
The program is using the algorithm **K-means** to automatically cluster similar elements with two attributes, provided as points in the Euclidean space in the files "normal.txt" and "unbalance.txt".

- "normal.txt" - 4 Gaussian clusters
- "unbalance.txt" - 8 Gaussian clusters

### To run the program
- Run `python3 main.py`
- Input file name ("normal" or "unbalance")
- Input number of clusters

### Output
- The internal cluster distance of each generation is displayed.
- Image that shows the different clusters in different colors.

### Output - "normal.txt"
![Output-example-normal](https://github.com/luntropy/k-means/blob/main/images/output-example-normal.png)

### Output - "unbalance.txt"
![Output-example-unbalance](https://github.com/luntropy/k-means/blob/main/images/output-example-unbalance.png)

## Bonus optimizations that can be applied
- Compare results with **K-means++**
- Compare results with **Soft k-means**
- Use intercluster distance.
- Use combination of both internal cluster distance and intercluster distance.
