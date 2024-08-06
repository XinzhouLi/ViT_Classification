#!/bin/bash
#SBATCH --partition=cpu2019,cpu2021,cpu2022,cpu2023
#SBATCH --job-name=data_preproc
#SBATCH --output=output/preproc_%A_%a.out
#SBATCH --array=0-12
#SBATCH -c 1
#SBATCH -t 1-00:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --mail-user=olayinka.oladosu1@ucalgary.ca
#SBATCH --mail-type=ALL

echo "Running on host: `hostname`"
cd $SLURM_SUBMIT_DIR
echo "Current working directory is `pwd`"

echo "Starting run at: `date`"
source ~/.bashrc
pwd=$PWD

DIRS=( CIMS* )
d=${DIRS[${SLURM_ARRAY_TASK_ID}]}

cd ${pwd}/${d}/* || return
echo "$PWD"

mkdir lesreg
fslswapdim T2_raw.nii.gz RL PA IS lesreg/T2.nii.gz || fslswapdim T2_raw.nii.gz LR PA IS lesreg/T2.nii.gz
fslswapdim FLAIR_raw.nii.gz RL PA IS lesreg/FLAIR.nii.gz || fslswapdim FLAIR_raw.nii.gz LR PA IS lesreg/FLAIR.nii.gz

# cp T2_*.nii.gz lesreg/T2.nii.gz
# cp FLAIR_*.nii.gz lesreg/FLAIR.nii.gz

cd lesreg

#Gibbs Ringing Correction
# mrdegibbs -force T2.nii.gz T2.nii.gz
# mrdegibbs -force FLAIR.nii.gz FLAIR.nii.gz

#Bias Field Correction - destroys sform
N4BiasFieldCorrection -d 3 -i T2.nii.gz -o T2_restore.nii.gz
N4BiasFieldCorrection -d 3 -i FLAIR.nii.gz -o FLAIR_restore.nii.gz

#Brain Extraction
flirt -in T2_restore.nii.gz -ref T2_restore.nii.gz -applyisoxfm 1 -o T2_iso.nii.gz
flirt -in FLAIR_restore.nii.gz -ref FLAIR_restore.nii.gz -applyisoxfm 1 -o FLAIR_iso.nii.gz

fslmaths $FSLDIR/data/standard/MNI152_T1_1mm_brain_mask.nii.gz -fillh26 -ero -fmean T1_MNI_mask

antsBrainExtraction.sh -d 3 -a T2_iso.nii.gz -e $FSLDIR/data/standard/MNI152_T1_1mm.nii.gz -m T1_MNI_mask.nii.gz -o T2 -c 4x3x2x1
mv T2BrainExtractionBrain.nii.gz T2_brain.nii.gz
antsBrainExtraction.sh -d 3 -a FLAIR_iso.nii.gz -e $FSLDIR/data/standard/MNI152_T1_1mm.nii.gz -m T1_MNI_mask.nii.gz -o FLAIR -c 4x1x3x2
mv FLAIRBrainExtractionBrain.nii.gz FLAIR_brain.nii.gz

fslcpgeom T2_iso T2_brain
fslcpgeom FLAIR_iso FLAIR_brain

#MNI Alignment
# flirt -in $FSLDIR/data/atlases/JHU/JHU-ICBM-T2-1mm.nii.gz -ref $FSLDIR/data/atlases/JHU/JHU-ICBM-T2-1mm.nii.gz -o MNI.nii.gz -applyisoxfm 1.2
# flirt -in $FSLDIR/data/standard/FSL_HCP1065_L3_1mm.nii.gz -ref $FSLDIR/data/standard/FSL_HCP1065_L3_1mm.nii.gz -o MNI.nii.gz -applyisoxfm 1.2
# flirt -in $FSLDIR/data/standard/MNI152_T1_1mm_brain.nii.gz -ref $FSLDIR/data/standard/MNI152_T1_1mm_brain.nii.gz -o MNI.nii.gz -applyisoxfm 1.2
flirt -in $FSLDIR/data/standard/MNI152_T1_1mm_brain.nii.gz -ref $FSLDIR/data/standard/MNI152_T1_1mm_brain.nii.gz -o MNI.nii.gz -applyisoxfm 1.2
maxval=$(fslstats MNI -P 100)
fslmaths MNI -thrP 1 -uthrP 99 -sub $maxval -mul -1 -mas MNI MNI_inv.nii.gz
# fslroi MNI MNI_scale -52 256 -20 256 -5 156
fslroi MNI_inv MNI_scale -52 256 -20 256 -20 156
flirt -in T2_brain.nii.gz -ref T2_brain.nii.gz -o T2_scale.nii.gz -applyisoxfm 1.0 -noresampblur
fslcpgeom T2_scale.nii.gz MNI_scale.nii.gz -d
flirt -in T2_scale.nii.gz -ref MNI_scale.nii.gz -omat T2acpc.mat -dof 6 -searchrx -180 180 -searchry -180 180 -searchrz -180 180
fslroi T2_scale T2_out 0 256 0 256 0 156
flirt -in T2_scale.nii.gz -ref T2_out.nii.gz -o T2_reg.nii.gz -applyxfm -init T2acpc.mat

#Structural Transformations
antsRegistrationSyN.sh -d 3 -f T2_reg.nii.gz -m FLAIR_brain.nii.gz -o FLAIR_T2 -t a
fslmaths FLAIR_T2Warped.nii.gz -mas T2_reg.nii.gz FLAIR_reg.nii.gz

cd "${pwd}"

echo "Job finished at: `date`"

