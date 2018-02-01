# rip_ag
## Setting up
1. Clone repo.
2. Set-up `virtualenv`.

    `virtualenv -p python3 env`
    
3. `pip install -r requirements.txt`.
## Running
### Setting up for an individual assignment.
###### If notebooks are collected via okpy.
1. Move zipped notebooks into top directory.
2. `unzip cal_....zip`
3. Copy files from `example` into notebook directory. 

    `cp -r example cal_...`
    
### Create the tests.

Tests should be saved as .py files. Tests should start with the phrase `test`, but than can have anything after that (just make sure that the test names are unique for this assignment).

A basic format for one test:

```
__out_of__ = 1

try:
    if satisfies_condition_to_give_points_for:
        __score__ += 1
except: 
  pass
```

There is also a global variable `__responses__` that you can append to, if you want to see the value of a variable, in addition to just getting the point value for a question.

### Edit the configs.py file.
Free response answers will be found based on the information in this file. If `cell_metadata` is `True`, then the parser will grab markdown cells with the given metadata tags. Otherwise, the parser will look for cells that start with the phrase given in `in_cell`.

Note: It is only necessary to specify `num_FR` if not using cell metadata (for numbering purposes).

```
num_FR = 28
cell_metadata = False
metadata_tags = []
in_cell = "<font color='blue'> ANSWER:"
```

### Running the tests.
1. Activate environment.

    `source env/bin/activate`
    
2. `python main.py`

### Results
The results are written as a csv with a name given in `main.py`.

If there is an error along the way, the contents of the last running notebook can be found in `last.py`. 

You can see summary statistics about scores by running `show_stats.py`.
