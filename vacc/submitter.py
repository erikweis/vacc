import subprocess
import json
import random
from pathlib import Path
from importlib import import_module

BASE_DIR = Path('')

def save_tempjson(d):
    
    """create temp json file and return filename """
    
    filename = f'{random.randint(1,10e10):015}.json'
    
    with open(BASE_DIR / filename,'w') as f:
        json.dump(d,f)

    return filename


def load_tempjson(filename):
    
    """load tempfile and delete it afterwards"""
    
    path = BASE_DIR / filename
    with open(path,'r') as f:
        out = json.load(f)
        
    path.unlink() #delete tempfile
    
    return out


def _execute(runstring_filename):
    
    #load rundict
    rundict = load_tempjson(runstring_filename)
    
    for function_path, args in rundict.items():
        
        modpath, function_name = function_path.rsplit('.',1)
        f = getattr(import_module(modpath),function_name)
        f(**args)


def vacc_submit(rundict):
    
    """
    Run an arbitary function on the vacc
    
    Args:
        rundict: a dictionary where keys are <function path> strings and values are function args
            example: {
                'module1.submodule3.func1':dict(arg1=3,arg2=False),
                'module2.myfunction':dict()
            }
    """

    filename = save_tempjson(rundict)    

    print('hello')
    #create generic function executor to be called within vacc job
    executor_path = Path(f'{random.randint(1,10e10):015}.py')
    with open(executor_path,'w') as f:
        f.write(
"""
from vacc import _execute
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('runstring_filename', type = str , help = 'file with run information')

    args = parser.parse_args()
    _execute(args.runstring_filename)
""")

    print('goodbye')

    subscript = \
        f"""#!/bin/sh

        #SBATCH --nodes=1
        #SBATCH --mem=2gb
        #SBATCH --time=12:00:00
        #SBATCH --job-name=1997


        python {executor_path.name} $RUNSTRINGFILENAME"""
    
    with open('subscript.sbatch','w') as f:
        f.write(subscript)

    script = '/usr/bin/sbatch'
    script += f' --export=ALL,RUNSTRINGFILENAME={filename}'
    script += ' subscript.sbatch'
    subprocess.call([script],shell=True)
    
    #delete generic function executor
    executor_path.unlink()
    
    