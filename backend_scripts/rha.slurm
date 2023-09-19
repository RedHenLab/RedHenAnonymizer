#!/bin/bash

#SBATCH -p gpu
#SBATCH --mem=8gb
#SBATCH --gres=gpu:1#!/bin/bash 
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --mem=8gb
#SBATCH --output=test.o%j 
#SBATCH --partition=gpu 
#SBATCH -C gpu2v100|gpu4v100
#SBATCH --gres=gpu:1               # Request one gpu out of 2 (Max) 

#SBATCH --account=mbt8     # substitute appropriate group here  

module load singularity
module load CUDA/11.1.1-GCC-10.2.0

export PATH="/usr/local/software/singularity/3.10.4/bin:/usr/local/easybuild_allnodes/software/CUDAcore/11.1.1/nvvm/bin:/usr/local/easybuild_allnodes/software/CUDAcore/11.1.1/bin:/usr/local/easybuild_allnodes/software/binutils/2.35-GCCcore-10.2.0/bin:/usr/local/easybuild_allnodes/software/GCCcore/10.2.0/bin:/home/sxg1373/miniconda3/bin:/home/sxg1373/miniconda3/condabin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/dell/srvadmin/bin:/home/sxg1373/.local/bin:/home/sxg1373/bin"
echo "hello"
echo $PFSDIR
scp -r /scratch/users/sxg1373/input_files/$1 /scratch/users/sxg1373/1.jpg /home/sxg1373/rha_sing.sif $PFSDIR
ls "$PFSDIR"
final_output_dir=$6
input_dir=$PFSDIR/$1
mkdir $PFSDIR/output_files
output_dir=$PFSDIR/output_files
img_dir=$PFSDIR/1.jpg

for file in "$input_dir"/*
do
   echo "$file"
   file_name=`echo "${file##*/}"`
   echo "This is the file name $file_name"
   singularity run --nv --bind "$PFSDIR" $PFSDIR/rha_sing.sif "$2" "audiovideo" $3 $4 $5 "$file" "$output_dir/output_$file_name.mp4" "$img_dir"
done
echo "saving  files"

scp -r $output_dir/* $final_output_dir
rm -rf "$PFSDIR"/*
rm -r /scratch/users/sxg1373/input_files/$1
