import subprocess
import random


def vacc_push(
        source_path,destination_path,
        netid = None,
        #exclude = None, include = None, deletion = False,
        rsync_commands = None,
        dry_run = False
    ):
    
    """Push files from a local directory onto vacc directory.
    
    Args:
        source_dir (str): the path (relative to your current working directory)
            to the folder you want to rsync
        destination_dir(str): the path (relative to your base user directory on the vacc)
            of the folder you want to rsync
        netid: your UVM netid
        rsync_commands: a list of any extra commands you want to include
            example: ["--exclude={'data','tests'}","--backup_dir=path/to/backups"]
    """

    assert netid, 'Must supply netid.'
    i = random.randint(1,2) #select user1 or user2
    vacc_pointer = f"{netid}@vacc-user{i}.uvm.edu"

    script = f"""
        rsync -a{'n' if dry_run else ''}P {source_path}/ {vacc_pointer}:{destination_path}"""
    
    # if deletion:
    #     script += ' --delete'
    
    # if exclude is not None:
    #     assert isinstance(exclude,list)
    #     script += " --exclude=" + str(exclude).replace('[','{').replace(']','}')
    
    # if include is not None:
    #     assert isinstance(include,list)
    #     script += " --include=" + str(exclude).replace('[','{').replace(']','}')
    
    if rsync_commands is not None:
        for x in rsync_commands:
            script += f" {x}"
            
    print(script)
    
    subprocess.call([script],shell=True)
    
    
def vacc_pull(
        source_path,destination_path,
        netid = None,
        rsync_commands = None,
        dry_run = False
    ):

    """Pull files from a vacc directory onto local computer.
    
    Args:
        source_dir (str): the path (relative to your base user directory on the vacc)
            to the folder you want to rsync
        destination_dir(str): the path (relative to your current working directory)
            of the folder you want to rsync
        netid: your UVM netid
        rsync_commands: a list of any extra commands you want to include
            example: ["--exclude={'data','tests'}","--backup_dir=path/to/backups"]
    """  
    
    assert netid, 'Must supply netid.'
    i = random.randint(1,2) #select user1 or user2
    vacc_pointer = f"{netid}@vacc-user{i}.uvm.edu"

    script = f"""
        rsync -a{'n' if dry_run else ''}P {vacc_pointer}:{source_path}/ {destination_path}"""

    subprocess.call([script],shell=True)
