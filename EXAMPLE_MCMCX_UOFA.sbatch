#!/bin/bash

#SBATCH --job-name=ede
#SBATCH --output=./projects/edemay2022/ede-%A_%a.out
#SBATCH -e ./projects/edemay2022/ede-%A_%a.out.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --ntasks-per-socket=2
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=10
#SBATCH --time=110:00:00
#SBATCH --partition=standard
#SBATCH --account=cosmolike

# Clear the environment from any previously loaded modules
module purge > /dev/null 2>&1
module load anaconda
conda init bash
source ~/.bashrc 

echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`
echo Slurm job NAME is $SLURM_JOB_NAME
echo Slurm job ID is $SLURM_JOBID
echo Number of MPI cores is $SLURM_NTASKS
echo Number of OpenMP cores is $SLURM_CPUS_PER_TASK
echo SLURM DIR is $SLURM_SUBMIT_DIR

cd $SLURM_SUBMIT_DIR
conda activate cocoa
source start_cocoa

export OMP_PROC_BIND=close
if [ -n "$SLURM_CPUS_PER_TASK" ]; then
  export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
else
  export OMP_NUM_THREADS=1
fi

mpirun -n ${SLURM_NTASKS} --mca btl tcp,self --bind-to core:overload-allowed --map-by numa:pe=${OMP_NUM_THREADS} cobaya-run ./projects/edemay2022/EXAMPLE_MCMC_${SLURM_ARRAY_TASK_ID}.yaml -r
