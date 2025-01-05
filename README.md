# <div align = center>gSpan On EEG Data Points</div>

**gSpan** is an algorithm for mining frequent subgraphs.
##### For the gSpan mining used the [Reference](https://github.com/betterenvi/gSpan). 


### Mileston #1

gSpan minning on each patient's time-windows to find repeated motifs 

### Challenges

* format not fit
* multi-nested dicts
* t # -1 must at the end of each file not each matrix (all time windows of a patient) 
* not saving the subgraphs
* issues with python interpreter with gspan-minning library -> to use in the command that is run 1000s of times
first subgraph output (emailed):
t # 1
v 0 0 
v 1 2 
v 2 4 
e 0 1 2
e 0 2 3

Support: 54

where: [0, 5, 6, 9, 12, 17, 21, 22, 23, 25, 26, 27, 28, 33, 41, 43, 46, 47, 49, 50, 52, 53, 55, 57, 59, 60, 63, 64, 67, 69, 70, 73, 74, 77, 78, 81, 86, 88, 91, 92, 93, 94, 96, 100, 104, 107, 109, 112, 115, 119, 121, 123, 125, 127]

-----------------

t # 2
v 0 0 
v 1 2 
v 2 9 
e 0 1 2
e 0 2 2

Support: 57

where: [0, 129, 3, 5, 6, 7, 8, 9, 12, 16, 21, 22, 23, 24, 25, 27, 28, 30, 33, 35, 39, 41, 42, 43, 46, 47, 52, 53, 55, 57, 61, 64, 67, 73, 74, 77, 79, 81, 86, 89, 91, 92, 93, 94, 96, 97, 99, 100, 103, 104, 107, 109, 112, 115, 117, 125, 127]

-----------------

t # 3
v 0 0 
v 1 4 
v 2 2 
e 0 1 3
e 1 2 2

Support: 54

where: [0, 128, 130, 132, 5, 6, 11, 12, 19, 22, 23, 27, 28, 33, 34, 37, 43, 45, 46, 47, 52, 54, 55, 58, 60, 62, 64, 67, 69, 73, 74, 75, 76, 77, 78, 81, 87, 88, 91, 92, 93, 94, 95, 100, 104, 107, 109, 114, 115, 121, 122, 123, 125, 127]

-----------------


### Mileston #2

The next step is to use the motifs ( vertex labels and edges) and aggregate them to build a weighted directed graph for each patient.
 

### Mileston #3

start comparing the different graphs.












Data File Format 
"t # N" means the Nth graph,
"v M L" means that the Mth vertex in this graph has label L,
"e P Q L" means that there is an edge connecting the Pth vertex with the Qth vertex. The edge has label L.

NOTICE: 
1.	All labels cannot be ''0'' or ''1'',  and it should be larger than ''1'';
2.  Each data file or query file should end with '' t # -1'', otherwise it will lead to a bug.

t # 0
v 0 1
v 1 1
v 2 1
e 0 1 1
e 0 2 1
e 1 2 1
t # -1






### How to run

The command is:

```sh
python -m gspan_mining [-s min_support] [-n num_graph] [-l min_num_vertices] [-u max_num_vertices] [-d True/False] [-v True/False] [-p True/False] [-w True/False] [-h] database_file_name 
```


##### Some examples

- Read graph data from ./graphdata/graph.data, and mine undirected subgraphs given min support is 5000
```
python -m gspan_mining -s 5000 ./graphdata/graph.data
```

- Read graph data from ./graphdata/graph.data, mine undirected subgraphs given min support is 5000, and visualize these frequent subgraphs(matplotlib and networkx are required)
```
python -m gspan_mining -s 5000 -p True ./graphdata/graph.data
```

- Read graph data from ./graphdata/graph.data, and mine directed subgraphs given min support is 5000
```
python -m gspan_mining -s 5000 -d True ./graphdata/graph.data
```

- Print help info
```
python -m gspan_mining -h
```

The author also wrote [example code](https://github.com/betterenvi/gSpan/blob/master/main.ipynb) using Jupyter Notebook. Mining results and visualizations are presented. For detail, please refer to [main.ipynb](https://github.com/betterenvi/gSpan/blob/master/main.ipynb).

### Running time

- Environment
    + OS: Windows 10
    + Python version: Python 2.7.12
    + Processor: Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz 3.60 GHz
    + Ram: 8.00 GB


- Running time
On the dataset [./graphdata/graph.data](https://github.com/betterenvi/gSpan/blob/master/graphdata/graph.data), running time is listed below:


| Min support | Number of frequent subgraphs | Time |
| --- | --- | --- |
| 5000 | 26 | 51.48 s |
| 3000 | 52 | 69.07 s |
| 1000 | 455 | 3 m 49 s |
| 600 | 1235 | 7 m 29 s |
| 400 | 2710 | 12 m 53 s |



### Reference
- [Paper](http://www.cs.ucsb.edu/~xyan/papers/gSpan-short.pdf)

gSpan: Graph-Based Substructure Pattern Mining, by X. Yan and J. Han. 
Proc. 2002 of Int. Conf. on Data Mining (ICDM'02). 

- [gboost](http://www.nowozin.net/sebastian/gboost/)

One C++ implementation of gSpan.
