import nbformat
import json
import re
import os
import tests.configs as cfg

# extra
from halo import Halo

import matplotlib
matplotlib.use('TkAgg')

# TODO: 
# need to catch failing notebooks
# needs more testing against notebooks w/ known scores
# add max time limit & limit functionality

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

before_all = "\nimport pandas\nimport numpy as np\n__total__ = 0\n__points__ = 0\n"
before_each_test = "\n__score__ = 0\n"
after_each_test = "\n__total__ += __out_of__ \n__points__ += __score__\n"
after_all = ""#"\nprint('Score: {} out of {}'.format(__points__, __total__))\n"

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

def __run_tests__(code, tests):
    # loading animation
    # "running for ___"
    exec(code + '\n' + tests)
    return locals()['__points__'], locals()['__total__']

def get_notebook_names():
    """returns a list of the path to student notebooks"""
    filenames = []
    for top, dirs, files in os.walk('./'):
        for nm in files:   
            if nm.endswith('ipynb') and not '-checkpoint' in nm:
                filenames.append(os.path.join(top, nm))
    return filenames


def line_is_okay(line):
    if not line.startswith('_ =') and \
        not 'print' in line and not '.scatter' in line and not '.plot' in line and \
        not line.startswith('ok.') and not '___' in line and\
        not line.startswith('from client.api.notebook') and\
        not line.startswith('plt.') and not line.startswith('\tplt.') and\
        not line.startswith('!') and not line.startswith('%') and\
        not line.startswith('ok =') and not line.startswith('import matplot') and\
        not 'interact' in line and not 'IntSlider' in line:
        return True
    return False

def code_cell_parse(source):
    insertion_adjustment = 0
    for i in range(len(source)):
        if source[i+insertion_adjustment].startswith('def ') or source[i+insertion_adjustment].startswith('for '):
            source.insert(i+insertion_adjustment+1, '    3\n')
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
                print('using metadata')
            else:
                if cell['source'][0].startswith(cfg.in_cell):
                    FR_answers.append('\n'.join(cell['source'])[len(cfg.in_cell):])
        if cell['cell_type'] == 'code':
            code.extend(code_cell_parse(cell['source']))
    return code, FR_answers

def run_one(filepath, tests):
    user_id = filepath.split('/')[1]
    print(user_id)
    notebook = __read_nb__(filepath)

    # item zero is code, item 1 is a list of FR answers
    c = grab_code_and_md(notebook)
    #together = 

    # getting numerical score on code questions

    # print(''.join(c[0]))
    #cleaned_code = __pls_sanitize__(c[0])

    with open('test.py', 'w') as f:
        f.write(''.join(c[0]))
        f.close()

    score = __run_tests__(''.join(c[0]), tests)

    # if len(c[1]) != cfg.num_FR:
    #     print("number of FR answers does not align for {}".format(user_id))

    return user_id, score, c[1]

@Halo(text='running tests', spinner='dots')
def run_all():

    # create csv outline
    # user_id, code_score, FR1, FR2, ..., FRn

    test_text = __get_tests__()
    ts = __create_tests_(test_text)

    for filename in get_notebook_names():
        l = run_one(filename, ts)
        print(l)


    # write csv

if __name__ == '__main__':
    run_all()

# test_text = __get_tests__()
# ts = __create_tests_(test_text)

# c = run_one('./chench@berkeley.edu/R60P1q/intro.ipynb', ts)