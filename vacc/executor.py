import argparse
import json
from importlib import import_module
from pathlib import Path

BASE_DIR = Path()

def load_tempjson(filename):
    
    """load tempfile and delete it afterwards"""
    
    path = BASE_DIR / filename
    with open(path,'r') as f:
        out = json.load(f)
        
    path.unlink() #delete tempfile
    
    return out

def execute(runstring_filename):
    
    
    #load rundict
    rundict = load_tempjson(runstring_filename)
    
    for function_path, args in rundict.items():
        
        modpath, function_name = function_path.rsplit('.',1)
        f = getattr(import_module(modpath),function_name)
        f(**args)



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('runstring_filename', type = str , help = 'file with run information')

    args = parser.parse_args()
    execute(args.runstring_filename)
