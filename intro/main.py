import nbformat
import json
import re
import os
import tests.configs as cfg

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

def __run_tests__(code, tests):
    
    # loading animation
    # "running for ___"
    exec(code + '\n' + tests)
    return __points__, __total__


###################################
###################################
def __pls_sanitize__(list_of_code):
    # pls (eval, os limits)
    # limit run time
    # get rid of ok cells / submit cells
    # keep track of files w/ errors
    # approved imports
    """s"""
    some_clean = [line for line in list_of_code if not line.startswith('_ =') and \
        not 'print' in line and not line.startswith('ok.') and \
        not line.startswith('from client.api.notebook') and \
        not line.startswith('plt.') and not line.startswith('\tplt.') and\
        not line.startswith('!')]
    return [line + '\n\t#for functions' for line in some_clean if line.startswith('def') and not line.endswith('\n')]

###################################
###################################

def get_notebook_names():
    """returns a list of the path to student notebooks"""
    filenames = []
    for top, dirs, files in os.walk('./'):
        for nm in files:   
            if nm.endswith('ipynb'):
                filenames.append(os.path.join(top, nm))
    return filenames

def grab_code_and_md(contents):
    FR_answers = []
    code = []
    for cell in contents['cells']:
        if cell['cell_type'] == 'markdown':
            if cfg.cell_metadata: # if we used metadata to id answers
                print('using metadata')
            else:
                if cell['source'][0].startswith(cfg.in_cell):
                    FR_answers.append('\n'.join(cell['source'][len(cfg.in_cell):]))
        if cell['cell_type'] == 'code':
            code.extend(cell['source'])
    return code, FR_answers

def run_one(filename, tests):
    user_id = filename.split('/')[1]

    notebook = __read_nb__(filename)
    c = grab_code_and_md(notebook)
    cleaned_code = __pls_sanitize__(c[0])
    for ln in cleaned_code:
        print(ln)

    score = __run_tests__('\n'.join(cleaned_code), tests)

    return user_id, score, c[1]


def run_all(filename):

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
                if cfg.cell_metadata: # if we used metadata to id answers
                    print('using metadata')
                else:
                    if cell['source'][0].startswith(cfg.in_cell):
                        FR_answers.append(cell['source'])
            if cell['cell_type'] == 'code':
                code.extend(cell['source'])

        if len(FR_answers) != cfg.num_FR:
            print("we've got a problem")
            print('do something')


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

# if __name__ == '__main__':
#     print('loading tests...\n')
#     test_text = __get_tests__()
#     ts = __create_tests_(test_text)

#     for each in get_notebook_names():
#         print(each)

#     c = run_one('./chench@berkeley.edu/R60P1q/intro.ipynb')

test_text = __get_tests__()
ts = __create_tests_(test_text)

c = run_one('./chench@berkeley.edu/R60P1q/intro.ipynb', ts)

