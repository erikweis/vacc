import subprocess
import random


def vacc_push(
        source_path,destination_path,
        netid = None, vacc_pointer = None, 
        #exclude = None, include = None, deletion = False,
        rsync_commands = None,
        dry_run = False
    ):
    
    if not vacc_pointer:
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
        netid = None, vacc_pointer = None, 
        #exclude = None, include = None, deletion = False, 
        rsync_commands = None,
        dry_run = False
    ):

    
    if not vacc_pointer:
        assert netid, 'Must supply netid.'
        i = random.randint(1,2) #select user1 or user2
        vacc_pointer = f"{netid}@vacc-user{i}.uvm.edu"

    script = f"""
        rsync -a{'n' if dry_run else ''}P {vacc_pointer}:{source_path}/ {destination_path}"""

    subprocess.call([script],shell=True)
