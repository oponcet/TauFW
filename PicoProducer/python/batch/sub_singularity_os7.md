
# Job Submission on HTCondor with CMSSW and Singularity

This document provides guidance for submitting jobs using HTCondor with CMSSW and Singularity `cmssw-el7`.

## Job Submission Steps


```bash
cd CMSSW_12_4_8/src/TauFW/PicoProducer/
bash start_el7.sh
```
bash start_el7.sh from (gitlab.cern.ch)[https://gitlab.cern.ch/cms-cat/cmssw-lxplus/-/tree/master]

You are now in singularity. you should be able to run condor_q.

```
cd /afs/cern.ch/user/o/oponcet/private/TauPOG_run3
source setup.sh 
cd TauFW/PicoProducer
```

Change the file `submit_HTCondor.sub`: 

```
# Submit as
#   condor_submit submit_HTCondor.sub 'mylogfile=log/myjob.$(ClusterId).$(ProcId).log' -queue arg from args.txt
universe              = vanilla
executable            = python/batch/submit_HTCondor.sh
arguments             = $(arg)
initialdir            = output
mylogfile             = log/job.$(ClusterId).$(ProcId).log
log                   = $(mylogfile)
output                = $(mylogfile)
error                 = $(mylogfile)
should_transfer_files = no
use_x509userproxy     = true
getenv                = true
# environment           = "JOBID=$(ClusterId) TASKID=$(ProcId) CMSSW_BASE=/afs/cern.ch/user/s/s.../CMSSW_12_4_8/"
environment           = "JOBID=$(ClusterId) TASKID=$(ProcId) CONTAINER=cmssw-el7 CMSSW_BASE=/afs/cern.ch/user/s/s.../CMSSW_12_4_8/"
+JobFlavour           = workday
+MaxRuntime           = 20000
#+AccountingGroup      = "group_u_BE.ABP.SLAP"
#queue arg from args.txt
MY.SingularityImage = "/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-cat/cmssw-lxplus/cmssw-el7-lxplus:latest/"
```

````
pico.py submit -c mutau -y UL2018_v10  -E jec=False --force
````
Should work fine! 


Thanks Izaak
