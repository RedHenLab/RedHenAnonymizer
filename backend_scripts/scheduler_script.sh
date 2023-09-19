#!/bin/bash
#this script will setup the files in correct directories before scheduling the 
#batch script

#read files of all the directories in input directory one by one and transfer 
#them to some input directory in scratch folder

#set the parameters of anonymization according to the config.json file for batch 
#batch job script

module load Python/3.10.8-GCCcore-12.2.0-bare
export PATH="/usr/local/easybuild_allnodes/software/Python/3.10.8-GCCcore-12.2.0-bare/bin:/usr/local/easybuild_allnodes/software/OpenSSL/1.1/bin:/usr/local/easybuild_allnodes/software/XZ/5.2.7-GCCcore-12.2.0/bin:/usr/local/easybuild_allnodes/software/SQLite/3.39.4-GCCcore-12.2.0/bin:/usr/local/easybuild_allnodes/software/Tcl/8.6.12-GCCcore-12.2.0/bin:/usr/local/easybuild_allnodes/software/ncurses/6.3-GCCcore-12.2.0/bin:/usr/local/easybuild_allnodes/software/bzip2/1.0.8-GCCcore-12.2.0/bin:/usr/local/easybuild_allnodes/software/binutils/2.39-GCCcore-12.2.0/bin:/usr/local/easybuild_allnodes/software/GCCcore/12.2.0/bin:/usr/local/software/singularity/3.10.4/bin:/usr/local/easybuild_allnodes/software/CUDAcore/11.1.1/nvvm/bin:/usr/local/easybuild_allnodes/software/CUDAcore/11.1.1/bin:/home/sxg1373/miniconda3/bin:/home/sxg1373/miniconda3/condabin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/dell/srvadmin/bin:/home/sxg1373/.local/bin:/home/sxg1373/bin"
scratch_dir="/scratch/users/sxg1373/input_files"
for f in /home/sxg1373/sxg1373gallinahome/anonymizer_storage/input/*; do
if [ -d "$f" ]; then
echo $f
status=`grep -o '"status": "[^"]*' $f/config.json | grep -o '[^"]*$'`

#python /home/sxg1373/change_status.py $f/config.json
#change the status to 1 by default the status is 0
cp -r $f/ $scratch_dir/

ls $scratch_dir
project_name=`grep -o '"project_name": "[^"]*' $f/config.json | grep -o '[^"]*$'`
visual_anonymization=`grep -o '"visual_anonymization": "[^"]*' $scratch_dir/$project_name/config.json | grep -o '[^"]*$'`
pitch=`grep -o '"pitch": "[^"]*' $scratch_dir/$project_name/config.json | grep -o '[^"]*$'`
echo_=`grep -o '"echo": "[^"]*' $scratch_dir/$project_name/config.json | grep -o '[^"]*$'`
distortion=`grep -o '"distortion": "[^"]*' $scratch_dir/$project_name/config.json | grep -o '[^"]*$'`
rm $scratch_dir/$project_name/config.json
mkdir /home/sxg1373/sxg1373gallinahome/anonymizer_storage/output/$project_name
output_dir="sxg1373@hpc8:/home/sxg1373/sxg1373gallinahome/anonymizer_storage/output/$project_name"
echo $project_name $visual_anonymization $pitch $echo_ $distortion $output_dir
#call the batch script and pass the parameters to it
job_id_str=`sbatch rha.slurm $project_name $visual_anonymization $pitch $echo_ $distortion $output_dir`
echo "batch job scheduled $job_id_str"
rm -r $f
echo "removed file from anonymizer_storage"

#else
#echo "No files found"
fi

done
