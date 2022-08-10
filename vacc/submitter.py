import subprocess
import json
import random
from pathlib import Path

BASE_DIR = Path('')

def save_tempjson(d):
    
    """create temp json file and return filename """
    
    filename = f'{random.randint(1,10e10):015}.json'
    
    with open(BASE_DIR / filename,'w') as f:
        json.dump(d,f)

    return filename


def vacc_submit(function_path, args = None):

    filename = save_tempjson(args)    

    subscript = \
        f"""#!/bin/sh

        #SBATCH --nodes=1
        #SBATCH --mem=2gb
        #SBATCH --time=12:00:00
        #SBATCH --job-name=1997

        python executor.py $RUNSTRINGFILENAME"""
    
    with open('subscript.sbatch','w') as f:
        f.write(subscript)

    script = '/usr/bin/sbatch'
    script += f' --export=ALL,RUNSTRINGFILENAME={filename}'
    script += ' subscript.sbatch'
    subprocess.call([script],shell=True)