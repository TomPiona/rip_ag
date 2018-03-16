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
Free response answers will be found based on the information in this file. If `cell_metadata` is `True`, then the parser will grab markdown cells that have a specified metadata tag. Otherwise, the parser will look for cells that start with the phrase given in `in_cell`.

Note: It is only necessary to specify `num_FR` if not using cell metadata (for numbering purposes).

```
num_FR = 5
cell_metadata = True
in_cell = "<font color='blue'> ANSWER:"
```

It is recommended that you use the cell metadata method, and add the following metadata to the submission cells for markdown:

```
  "manual_problem_id": "some_name",
  "deletable": false
```
By making the cell non-deletable, you'll end up with the correct number of free-response answers for each student, and the manual tag makes the collection process relatively robust to student changes.

### Running the grader.
1. Activate environment.

    `source env/bin/activate`
    
2. `python main.py`
    
    This will run the main code and markdown parsing.
    
There is also a Makefile with the following commands (I recommend using `make run` instead of `python main.py`):

* `run`: runs the code and markdown parsing, but then zips all of the notebooks that had errors together, so they can easily be uploaded to datahub and run manually.
* `md`: just parses out the free-response questions and throws them into a csv.

### Results
The results are written as a csv with a name given in `main.py`.

If there is an error along the way, the contents of the last running notebook can be found in `last.py`. 

### Notes:

* The code autograder will steamroll most student errors, and still evaluate the tests, but currently will not allow syntax errors. It will stop running on those, and those are the notebooks that are put into the zip file when using `make run`.
* The tests are just appended to the end of the notebook, so try not to reuse variable names.

Both of these "features" could be removed, but I have yet to have the time.
