import nbformat
import json
import re
import os
import csv
import tests.configs as cfg
from timeout import timeout
import numpy as np

# extra
from halo import Halo

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
plt.ioff()

import warnings
warnings.filterwarnings('ignore')

# TODO: 
# check to see if score csv already exist, have parameter to not run everyone
# consolidate errors of failing code on individual level
# needs more testing against notebooks w/ known scores
# add max time limit & limit functionality
# create google form for score feedback (making sure autograder works)
# errors that students are getting
# syntax errors (writing text not as string [var = 27 billion] and nothing after equal sign)
# infinite loops (at least 2)

def __read_nb__(filename):
    """returns the notebook as a dictionary"""
    with open(filename) as f:
        notebook = json.load(f)
        f.close()
    return notebook

def __get_tests__():
    """returns the contents of the tests in a list"""
    filenames = [file for file in os.listdir('./tests') if file.startswith('test')]
    tests = []
    for fn in filenames:
        with open('./tests/{}'.format(fn), 'r') as f:
            tests.append(f.read())
            f.close()
    return tests

before_all = "\nimport pandas\nimport numpy as np\nimport matplotlib.pyplot as plt\nmatplotlib.use('Agg')\nplt.ioff()\nimport warnings\nwarnings.filterwarnings('ignore')\n__total__ = 0\n__question_scores__ = []\n__responses__ = []\n"
before_each_test = "\n__score__ = 0\n"
after_each_test = "\n__total__ += __out_of__ \n__question_scores__.append(__score__)\n"
after_all = "\n__points__ = sum(__question_scores__)\n"

def __create_tests_(test_text):
    """creates the test suite to append to student code"""
    num_tests = len(test_text)

    insertion_adjustment = 0
    for i in range(num_tests + 1):
        if i > 0:
            test_text.insert(i + insertion_adjustment, after_each_test)
            insertion_adjustment += 1
        if i < num_tests:
            test_text.insert(i + insertion_adjustment, before_each_test)
            insertion_adjustment += 1

    test_text.insert(0, before_all)
    test_text.insert(len(test_text), after_all)

    return ''.join(test_text)

@timeout(15)
def __run_tests__(code, tests):
    # loading animation
    # "running for ___"
    exec(code + '\n' + tests)
    # locals()['__total__'] += 1
    # __score__ = 0
    # if 'E = 200' in code or 'E =200' in code or 'E=200' in code or 'E= 200' in code:
    #     __score__ += 1
    #     locals()['__question_scores__'].append(__score__)
    # locals()['__points__'] = sum(locals()['__question_scores__'])
    return locals()['__question_scores__'] + [locals()['__points__']] + [locals()['__total__']]

def get_notebook_names():
    """returns a list of the path to student notebooks"""
    filenames = []
    for top, dirs, files in os.walk('./'):
        for nm in files:   
            if nm.endswith('ipynb') and not '-checkpoint' in nm and not 'Untitled' in nm:
                filenames.append(os.path.join(top, nm))
    return filenames

def line_is_okay(line):
    if not line.startswith('_ =') and \
         not '.scatter' in line and \
        not line.startswith('ok.') and not '___' in line and\
        not line.startswith('from client.api.notebook') and\
        not line.startswith('!') and not line.startswith('%') and\
        not line.startswith('ok =') and \
        not 'interact' in line and not 'IntSlider' in line:
        ##and not '.plot' in line and not 'print' in line andnot line.startswith('import matplot') and
        #not line.startswith('plt.') and not line.startswith('\tplt.') and\
        return True
    return False

def code_cell_parse(source):
    insertion_adjustment = 0
    for i in range(len(source)):
        if source[i+insertion_adjustment].startswith('def ') or source[i+insertion_adjustment].startswith('for '):
            3
            #source.insert(i+insertion_adjustment+1, '    3\n')
    source = ["    " + line for line in source if line_is_okay(line)]
    compiled = ''.join(source) + '\n'
    if len(source) > 0:
        return "try: \n" +compiled+"\n    pass\nexcept Exception as e: \n    print(e)\n"
    return ''

def grab_code_and_md(contents):
    FR_answers = []
    code = []
    for cell in contents['cells']:
        if cell['cell_type'] == 'markdown':
            if cfg.cell_metadata: # if we used metadata to id answers
                if 'manual_grade' in cell['metadata'] and cell['metadata']['manual_grade']:
                    FR_answers.append('\n'.join(cell['source']))
            else:
                if cell['source'][0].startswith(cfg.in_cell):
                    FR_answers.append('\n'.join(cell['source'])[len(cfg.in_cell):])
        if cell['cell_type'] == 'code' and '%%javascript\n' not in cell['source']:
            code.extend(code_cell_parse(cell['source']))
    return code, FR_answers

def run_one(filepath, tests):
    user_id = filepath.split('/')[1]
    print(user_id)
    notebook = __read_nb__(filepath)

    # item zero is code, item 1 is a list of FR answers
    c = grab_code_and_md(notebook)

    with open('last.py', 'w') as f: # for grabbing a notebook that errors
        f.write(''.join(c[0]))
        f.close()

    # getting numerical score on code questions
    score_list = __run_tests__(''.join(c[0]), tests)

    if len(c[1]) != cfg.num_FR:
        print('!!!!!!!!!!!!')
        print("number of FR answers does not align for {}".format(user_id))
        print('!!!!!!!!!!!!')

    return [user_id] + score_list + c[1]


@Halo(text='running tests ', spinner='dots')
def run_all():

    # reading and creating tests
    test_text = __get_tests__()
    ts = __create_tests_(test_text)
    results = []
    no_good = []

    for filename in get_notebook_names():
        try:
            result = run_one(filename, ts)
            results.append(result)
        except Exception as e:
            print('not giving a score to {} bc {}'.format(filename, e))
            no_good.append(tuple([filename, e]))
        
     
    # writing results to csv
    num_tests = len([file for file in os.listdir('./tests') if file.startswith('test')])
    title_row = ['email'] + [str(i) for i in range(1, num_tests+1)] + ['Total Score', 'Out of'] + ['free response ' + str(i) for i in range(1, cfg.num_FR+1)]
    results.insert(0, title_row)

    f = open('ps5.csv', 'w')
    with f:
        writer = csv.writer(f)
        writer.writerows(results)
        f.close()

    with open('not_scored.txt', 'w') as f:
        print('no scores for {} people'.format(len(no_good)))
        for name, reason in no_good:
            print(name, ':', reason)
            f.write(name+'\n')
        f.close()

    




if __name__ == '__main__':
    run_all()
