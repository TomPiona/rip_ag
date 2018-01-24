import nbformat
import json
import re
import os
import tests.configs

def __read_nb__(filename):
    """returns the notebook as a dictionary"""
    with open(filename) as f:
        notebook = json.load(f)
        f.close()
    return notebook

def __get_tests__():
    """returns the contents of the tests in a list"""
    """reads test file to run on each file
    file should return a single number that is the score"""
    filenames = [file for file in os.listdir('./tests') if file.startswith('test')]
    tests = []
    for fn in filenames:
        with open('./tests/{}'.format(fn), 'r') as f:
            tests.append(f.read())
            f.close()
    return tests

before_all = "\n__total__ = 0\n__points__ = 0\n"
before_each_test = "\n__score__ = 0\n"
after_each_test = "\n__total__ += __out_of__ \n__points__ += __score__\n"
after_all = "\nprint('Score: {} out of {}'.format(__points__, __total__))\n"

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

def __run_tests__(code):
    print('a')

    # put user code
    # then test
    # then return score

def __pls_sanitize__():
    # pls (eval, os limits)
    # limit run time
    # keep track of files w/ errors
    """s"""

def get_notebook_names():
    """returns a list of the path to student notebooks"""
    filenames = []
    for top, dirs, files in os.walk('./'):
        for nm in files:   
            if nm.endswith('ipynb'):
                filenames.append(os.path.join(top, nm))
    return filenames

def run_one(filename):
    user_id = filename.split('/')[1]
    return user_id

def run(filename):

    # create csv outline
    # user_id, code_score, FR1, FR2, ..., FRn

    for filename in directory:

        line = [filename]

        # open single user file
        notebook = __read_nb__(filename)

        # grab all code
        # append some tests and print output?
        FR_answers = []
        code = []
        for cell in notebook['cells']:
            if cell['cell_type'] == 'markdown':
                # if starts with answer
                    FR_answers.append(written_stuff)
            if cell['cell_type'] == 'code':
                code.extend(cell['source'])


        sanitized = __pls_sanitize__(code)
        score = __run_tests__(sanitized)
        line.append(score)
        line.extend(FR_answers)

        # grab the responses to written answers
        # throw into the same csv



    # for cell in notebook['cells']:
    #     if cell['cell_type'] == 'markdown':
    #         line_num = 0
    #         for line in cell['source']:

    # # generates properly formatted markdown cell
    # toc_cell = nbformat.v4.new_markdown_cell(toc_text)
    # # adds table of contents to top of page
    # notebook['cells'].insert(0, toc_cell)

    # write csv

if __name__ == '__main__':
    print('loading tests...\n')
    test_text = __get_tests__()
    ts = __create_tests_(test_text)

    for each in get_notebook_names():
        print(run_one(each))


