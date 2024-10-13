#!/usr/bin/env python
__credits__     = "https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters"

import time


def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        #print()
        print(f'{prefix} |{fill * filledLength}| 100% {suffix}    ', end = '\n')


if __name__ == "__main__":
    # initialize the progress bar by set curr progress to zero
    for i in range(100):
        time.sleep(0.01)
        print_progress_bar(i, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
        time.sleep(0.01)
    
    print_progress_bar(100, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)