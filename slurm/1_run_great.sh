#!/bin/bash
#SBATCH --account=girirajan
#SBATCH --partition=girirajan
#SBATCH --job-name=great
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:5:0
#SBATCH --mem-per-cpu=1G
#SBATCH --chdir /data5/deepro/starrseq/main_library/8_enhancer_gene_map/src
#SBATCH -o /data5/deepro/starrseq/main_library/8_enhancer_gene_map/slurm/logs/out_great_%a.log
#SBATCH -e /data5/deepro/starrseq/main_library/8_enhancer_gene_map/slurm/logs/err_great_%a.log
#SBATCH --array 1-29%1

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/data5/deepro/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/data5/deepro/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/data5/deepro/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/data5/deepro/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

conda activate starrseq

echo `date` starting job on $HOSTNAME
LINE=$(sed -n "$SLURM_ARRAY_TASK_ID"p /data5/deepro/starrseq/main_library/8_enhancer_gene_map/slurm/files/1_smap.txt)

echo $LINE
python /data5/deepro/starrseq/main_library/8_enhancer_gene_map/src/1_run_great.py $LINE

echo `date` ending job
