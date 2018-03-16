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

def __read_nb__(filename):
    """returns the notebook as a dictionary"""
    with open(filename) as f:
        notebook = json.load(f)
        f.close()
    return notebook

def get_notebook_names():
    """returns a list of the path to student notebooks"""
    filenames = []
    for top, dirs, files in os.walk('./'):
        for nm in files:   
            if nm.endswith('ipynb') and not '-checkpoint' in nm and not 'Untitled' in nm:
                filenames.append(os.path.join(top, nm))
    return filenames


def grab_md(contents):
    FR_answers = []
    for cell in contents['cells']:
        if cell['cell_type'] == 'markdown':
            if cfg.cell_metadata: # if we used metadata to id answers
                if 'manual_grade' in cell['metadata'] and cell['metadata']['manual_grade']:
                    FR_answers.append('\n'.join(cell['source']))
            else:
                if cell['source'][0].startswith(cfg.in_cell):
                    FR_answers.append('\n'.join(cell['source'])[len(cfg.in_cell):])
    return FR_answers

def run_one(filepath):
    user_id = filepath.split('/')[1]
    print('\n', user_id)
    notebook = __read_nb__(filepath)

    # a list of free response answers
    c = grab_md(notebook)

    if len(c) != cfg.num_FR:
        print('!!!!!!!!!!!!')
        print("number of FR answers does not align for {}".format(user_id))
        print('!!!!!!!!!!!!')

    return [user_id] + c

@Halo(text='grabbing md ', spinner='dots')
def run_all():

    # for storing results
    results = []
    no_good = []

    for filename in get_notebook_names():
        try:
            result = run_one(filename)
            if len(result) == cfg.num_FR + 1:
                results.append(result)
            else:
                no_good.append(tuple([filename, 'not correct number of FR']))
        except Exception as e:
            print('not giving a score to {} bc {}'.format(filename, e))
            no_good.append(tuple([filename, e]))
        
     
    # writing results to csv
    title_row = ['email'] + ['free response ' + str(i) for i in range(1, cfg.num_FR+1)]
    results.insert(0, title_row)

    f = open('ps6_md.csv', 'w')
    with f:
        writer = csv.writer(f)
        writer.writerows(results)
        f.close()

    with open('ppl_wo_FR.txt', 'w') as f:
        print('no FR answers for {} person(s)'.format(len(no_good)))
        for name, reason in no_good:
            print(name, ':', reason)
            f.write(name+'\n')
        f.close()

if __name__ == '__main__':
    run_all()
