# vacc: A python helper package running scripts on the VACC
 A package to faciliate running python scrips on the UVM's VACC..

 The package has two main modules, `rsync` and `submitter`. The former is meant to accelerate the process of transfering files to and from the vacc. The latter is for use on the vacc to submit vacc jobs from a python script.

# Installation

To install, run `pip install vacc`.

 ## Rsync

Suppose your project directory has a subdirectory called `data` which you want to sync with the vacc using rsync. This can be done with the following code:

 ```{python}
from vacc import vacc_push

source_path = 'data' # the relative location of the folder
destination_path = 'my_project/data' #the relative location of the same folder on the vacc

vacc_push(source_path, destination_path, netid = <uvm_id>)
 ```

Naturally, the reverse process of pulling files from the vacc to your local computer is done with 
 ```{python}
from vacc import vacc_pull

source_path = 'data' # the relative location of the folder on the vacc
destination_path = 'my_project/data' #the relative location of the same folder on your local computer

vacc_pull(source_path, destination_path, netid = <uvm_id>)
 ```

If your password is not automatically configured, you will be prompted to enter your password.

For both of these functions, arbitrary rsync arguments can be passed along, such as

```
exclude_arg = "--exclude={'data_05-**-20','data_05-**-21'}"
vacc_push(source_path,destination_path,netid=<netid>,rsync_commands = [exclude_arg])
```

Finally, we can specify a dry run of the procedure before syncing the folder for real. This can be accomplished with

```{python}
vacc_push(source_path,destination_path,net_id=<netid>,dry_run=True)
```

## Submitter

To submit jobs on the vacc, we can use the following code:

```{python}
from vacc import vacc_submit

run_dict = {
    'module1.submodule3.func1':dict(arg1=3,arg2=False),
    'module2.myfunction':dict()
}

vacc_submit(run_dict)
```

The above snippet is equivalent to running the following script:
```{python}
from module1.submodule3 import func1
func1(arg1=3,arg2=False)

from module2 import myfunction
myfunction()
```

The `vacc_submit` function can also take arbitrary sbatch arguments for configuring resource requirements. As an example,

```{python}
vacc_submit(
    run_dict,
    partition='short',
    mem='2gb',
    time='6:00:00
)
```
All sbatch configuration commands can be found [here](https://www.uvm.edu/vacc/kb/knowledge-base/write-submit-job-bluemoon/).

