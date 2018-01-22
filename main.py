import nbformat
import json
import re  

def __read_nb__(filename):
    """returns the notebook as a dictionary"""
    with open(filename) as f:
        notebook = json.load(f)
        f.close()
    return notebook

def __read_tests__(testnames):
    """reads test file to run on each file
    file should return a single number that is the score"""

def __run_tests__(code):
    # put user code
    # then test
    # then return score
    return score

def __pls_sanitize__():
    # pls (eval, os limits)
    # limit run time
    # keep track of files w/ errors

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