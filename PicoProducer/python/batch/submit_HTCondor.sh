#! /bin/bash
## Script to run on a HTCondor batch system

# START
START=`date +%s`
echo "Job start at `date`"
echo "Running job on machine `uname -a`, host $HOSTNAME"
function peval { echo ">>> $@"; eval "$@"; }

# SETTING
TASKCMD="python TauES/createinputsTES.py -y UL2018 -c TauES_ID/config/FitSetupTES_mutau_noSF_pt_DM_WP.yml"
WORKDIR="$PWD"
printf '=%.0s' `seq 60`; echo
echo "\$PWD=$PWD"
echo "\$JOBID=$JOBID"
echo "\$TASKID=$TASKID"
echo "\$HOSTNAME=$HOSTNAME"
echo "\$TASKCMD=$TASKCMD"
echo "\$WORKDIR=$WORKDIR"
#printf '=%.0s' `seq 60`; echo
#env
#printf '=%.0s' `seq 60`; echo

# ENVIRONMENT
if [ ! -z "$CMSSW_BASE" -a -d "$CMSSW_BASE/src" ]; then
  peval "cd $CMSSW_BASE/src"
  peval 'eval `scramv1 runtime -sh`'
  peval "cd $WORKDIR"
  peval "cp -r $CMSSW_BASE/src $WORKDIR"
  peval "cd $CMSSW_BASE/src/TauFW/Fitter"
fi

# MAIN FUNCTIONALITY

#TASKCMD="python TauFW/Fitter/TauES/createinputsTES.py -y UL2018 -c TauFW/Fitter/TauES_ID/config/testeur.yml"
echo "\$PWD=$PWD"
peval "$TASKCMD"

# FINISH
echo
END=`date +%s`; RUNTIME=$((END-START))
echo "Job complete at `date`"
printf "Took %d minutes %d seconds" "$(( $RUNTIME / 60 ))" "$(( $RUNTIME % 60 ))"
