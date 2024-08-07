import pandas as pd
from nipype import Node, Workflow
from nipype.interfaces import fsl
import os
import glob
# Replace 'your_file.xlsx' with the path to your Excel 
base_path = '/home/rehman.tariq/Desktop/AICE_Study/Subjects'
excel_file_path = '/home/rehman.tariq/Desktop/AICE_Study/subjects.xlsx'
# Read the Excel file into a Pandas DataFrame
df = pd.read_excel(excel_file_path)
subjects_list =[]
MNI_152_path = '/global/software/fsl/fsl-6.0.0/data/standard/MNI152_T1_1mm_brain.nii.gz'
# Display the DataFrame
for subject in range(len(df['Subject ID'])):
    subject_ID = str(df['Subject ID'][subject])
    subject_path = os.path.join(base_path, subject_ID)
    T1_file = df['T1'][subject]
    T1_post_file = df['T1-Post'][subject]
    T2_file = df['T2'][subject]
    FLAIR_file = df['FLAIR'][subject]
    FLAIR_post_file = df['FLAIR-Post'][subject]
    #Case where T1, T2, and FLAIR files exist
    if T1_file==1 and T2_file ==1 and FLAIR_file==1:
        print(subject_path)
        try: 
            T1_dir = os.path.join(subject_path, 'T1')
            T1_file_path = glob.glob(os.path.join(T1_dir,'*brain_bfc.nii.gz'))[0]
            T2_dir = os.path.join(subject_path, 'T2')
            T2_file_path = glob.glob(os.path.join(T2_dir,'*brain_bfc.nii.gz'))[0]
            FLAIR_dir = os.path.join(subject_path, 'FLAIR')
            FLAIR_file_path = glob.glob(os.path.join(FLAIR_dir,'*brain_bfc.nii.gz'))[0]
        except:
            print(f'Subject {subject_ID} does not exist')
            subjects_list.append(subject_ID)
            continue
        T1_T2_reg = Node(fsl.FLIRT(), name='T1_T2_reg')
        T1_FLAIR_reg = Node(fsl.FLIRT(), name='T1_FLAIR_reg')
        T1_MNI_reg = Node(fsl.FLIRT(), name='T1_MNI_reg')
        T2_transformation = Node(fsl.ApplyXFM(), name='T2_transformation')
        FLAIR_transformation = Node(fsl.ApplyXFM(), name='FLAIR_transformation')
        # T2 to T1 Registration
        T1_T2_reg.inputs.in_file = T2_file_path
        T1_T2_reg.inputs.reference = T1_file_path
        T1_T2_reg.inputs.dof = 6
        T1_T2_reg.inputs.out_file = os.path.join(T1_dir, 'T2_Registered_To_T1.nii.gz')
        result = T1_T2_reg.run()
        # FLAIR to T1 Registration
        T1_FLAIR_reg.inputs.in_file = FLAIR_file_path
        T1_FLAIR_reg.inputs.reference = T1_file_path
        T1_FLAIR_reg.inputs.dof = 6
        T1_FLAIR_reg.inputs.out_file = os.path.join(T2_dir, 'FLAIR_Registered_To_T1.nii.gz')
        result = T1_FLAIR_reg.run()
        #T1 to MNI Registration
        T1_MNI_reg.inputs.in_file = T1_file_path
        T1_MNI_reg.inputs.reference = MNI_152_path
        T1_MNI_reg.inputs.dof = 12
        T1_MNI_reg.inputs.out_file = os.path.join(T1_dir, 'T1_brain_bfc_MNIreg.nii.gz')
        T1_MNI_reg.inputs.out_matrix_file = os.path.join(T1_dir, 'T1_MNIregis.mat')
        result = T1_MNI_reg.run()
        #T2 to MNI Registration
        T2_transformation.inputs.in_file= T1_T2_reg.inputs.out_file
        T2_transformation.inputs.reference = MNI_152_path
        T2_transformation.inputs.in_matrix_file = T1_MNI_reg.inputs.out_matrix_file
        T2_transformation.inputs.out_file =os.path.join(T2_dir, 'T2_brain_bfc_MNIreg.nii.gz')
        result = T2_transformation.run()
        #FLAIR to MNI Registration
        FLAIR_transformation.inputs.in_file= T1_FLAIR_reg.inputs.out_file
        FLAIR_transformation.inputs.reference = MNI_152_path
        FLAIR_transformation.inputs.in_matrix_file = T1_MNI_reg.inputs.out_matrix_file
        FLAIR_transformation.inputs.out_file =os.path.join(FLAIR_dir, 'FLAIR_brain_bfc_MNIreg.nii.gz')
        result = FLAIR_transformation.run()




    #Case where T1, T2, and FLAIR post exist
    elif T1_file == 1 and T2_file == 1 and FLAIR_post_file==1:
        print(subject_path)
        try: 
            T1_dir = os.path.join(subject_path, 'T1')
            T1_file_path = glob.glob(os.path.join(T1_dir,'*brain_bfc.nii.gz'))[0]
            T2_dir = os.path.join(subject_path, 'T2')
            T2_file_path = glob.glob(os.path.join(T2_dir,'*brain_bfc.nii.gz'))[0]
            FLAIR_dir = os.path.join(subject_path, 'FLAIR-Post')
            FLAIR_file_path = glob.glob(os.path.join(FLAIR_dir,'*brain_bfc.nii.gz'))[0]
        except:
            print(f'Subject {subject_ID} does not exist')
            subjects_list.append(subject_ID)
            continue
        T1_T2_reg = Node(fsl.FLIRT(), name='T1_T2_reg')
        T1_FLAIR_reg = Node(fsl.FLIRT(), name='T1_FLAIR_reg')
        T1_MNI_reg = Node(fsl.FLIRT(), name='T1_MNI_reg')
        T2_transformation = Node(fsl.ApplyXFM(), name='T2_transformation')
        FLAIR_transformation = Node(fsl.ApplyXFM(), name='FLAIR_transformation')
        # T2 to T1 Registration
        T1_T2_reg.inputs.in_file = T2_file_path
        T1_T2_reg.inputs.reference = T1_file_path
        T1_T2_reg.inputs.dof = 6
        T1_T2_reg.inputs.out_file = os.path.join(T1_dir, 'T2_Registered_To_T1.nii.gz')
        result = T1_T2_reg.run()
        # FLAIR to T1 Registration
        T1_FLAIR_reg.inputs.in_file = FLAIR_file_path
        T1_FLAIR_reg.inputs.reference = T1_file_path
        T1_FLAIR_reg.inputs.dof = 6
        T1_FLAIR_reg.inputs.out_file = os.path.join(T2_dir, 'FLAIR_Registered_To_T1.nii.gz')
        result = T1_FLAIR_reg.run()
        #T1 to MNI Registration
        T1_MNI_reg.inputs.in_file = T1_file_path
        T1_MNI_reg.inputs.reference = MNI_152_path
        T1_MNI_reg.inputs.dof = 12
        T1_MNI_reg.inputs.out_file = os.path.join(T1_dir, 'T1_brain_bfc_MNIreg.nii.gz')
        T1_MNI_reg.inputs.out_matrix_file = os.path.join(T1_dir, 'T1_MNIregis.mat')
        result = T1_MNI_reg.run()
        #T2 to MNI Registration
        T2_transformation.inputs.in_file= T1_T2_reg.inputs.out_file
        T2_transformation.inputs.reference = MNI_152_path
        T2_transformation.inputs.in_matrix_file = T1_MNI_reg.inputs.out_matrix_file
        T2_transformation.inputs.out_file =os.path.join(T2_dir, 'T2_brain_bfc_MNIreg.nii.gz')
        result = T2_transformation.run()
        #FLAIR to MNI Registration
        FLAIR_transformation.inputs.in_file= T1_FLAIR_reg.inputs.out_file
        FLAIR_transformation.inputs.reference = MNI_152_path
        FLAIR_transformation.inputs.in_matrix_file = T1_MNI_reg.inputs.out_matrix_file
        FLAIR_transformation.inputs.out_file =os.path.join(FLAIR_dir, 'FLAIR_brain_bfc_MNIreg.nii.gz')
        result = FLAIR_transformation.run()
    #Case where T1 post, T2, and FLAIR exist
    elif T1_post_file==1 and T2_file==1 and FLAIR_file==1:
        print(subject_path)
        try: 
            T1_dir = os.path.join(subject_path, 'T1-Post')
            T1_file_path = glob.glob(os.path.join(T1_dir,'*brain_bfc.nii.gz'))[0]
            T2_dir = os.path.join(subject_path, 'T2')
            T2_file_path = glob.glob(os.path.join(T2_dir,'*brain_bfc.nii.gz'))[0]
            FLAIR_dir = os.path.join(subject_path, 'FLAIR')
            FLAIR_file_path = glob.glob(os.path.join(FLAIR_dir,'*brain_bfc.nii.gz'))[0]
        except:
            print(f'Subject {subject_ID} does not exist')
            subjects_list.append(subject_ID)
            continue
        T1_T2_reg = Node(fsl.FLIRT(), name='T1_T2_reg')
        T1_FLAIR_reg = Node(fsl.FLIRT(), name='T1_FLAIR_reg')
        T1_MNI_reg = Node(fsl.FLIRT(), name='T1_MNI_reg')
        T2_transformation = Node(fsl.ApplyXFM(), name='T2_transformation')
        FLAIR_transformation = Node(fsl.ApplyXFM(), name='FLAIR_transformation')
        # T2 to T1 Registration
        T1_T2_reg.inputs.in_file = T2_file_path
        T1_T2_reg.inputs.reference = T1_file_path
        T1_T2_reg.inputs.dof = 6
        T1_T2_reg.inputs.out_file = os.path.join(T1_dir, 'T2_Registered_To_T1.nii.gz')
        result = T1_T2_reg.run()
        # FLAIR to T1 Registration
        T1_FLAIR_reg.inputs.in_file = FLAIR_file_path
        T1_FLAIR_reg.inputs.reference = T1_file_path
        T1_FLAIR_reg.inputs.dof = 6
        T1_FLAIR_reg.inputs.out_file = os.path.join(T2_dir, 'FLAIR_Registered_To_T1.nii.gz')
        result = T1_FLAIR_reg.run()
        #T1 to MNI Registration
        T1_MNI_reg.inputs.in_file = T1_file_path
        T1_MNI_reg.inputs.reference = MNI_152_path
        T1_MNI_reg.inputs.dof = 12
        T1_MNI_reg.inputs.out_file = os.path.join(T1_dir, 'T1_brain_bfc_MNIreg.nii.gz')
        T1_MNI_reg.inputs.out_matrix_file = os.path.join(T1_dir, 'T1_MNIregis.mat')
        result = T1_MNI_reg.run()
        #T2 to MNI Registration
        T2_transformation.inputs.in_file= T1_T2_reg.inputs.out_file
        T2_transformation.inputs.reference = MNI_152_path
        T2_transformation.inputs.in_matrix_file = T1_MNI_reg.inputs.out_matrix_file
        T2_transformation.inputs.out_file =os.path.join(T2_dir, 'T2_brain_bfc_MNIreg.nii.gz')
        result = T2_transformation.run()
        #FLAIR to MNI Registration
        FLAIR_transformation.inputs.in_file= T1_FLAIR_reg.inputs.out_file
        FLAIR_transformation.inputs.reference = MNI_152_path
        FLAIR_transformation.inputs.in_matrix_file = T1_MNI_reg.inputs.out_matrix_file
        FLAIR_transformation.inputs.out_file =os.path.join(FLAIR_dir, 'FLAIR_brain_bfc_MNIreg.nii.gz')
        result = FLAIR_transformation.run()
    #Case where T1 post, t2, and flair post exist
    elif T1_post_file==1 and T2_file==1 and FLAIR_post_file==1:
        print(subject_path)
        try: 
            T1_dir = os.path.join(subject_path, 'T1-Post')
            T1_file_path = glob.glob(os.path.join(T1_dir,'*brain_bfc.nii.gz'))[0]
            T2_dir = os.path.join(subject_path, 'T2')
            T2_file_path = glob.glob(os.path.join(T2_dir,'*brain_bfc.nii.gz'))[0]
            FLAIR_dir = os.path.join(subject_path, 'FLAIR-Post')
            FLAIR_file_path = glob.glob(os.path.join(FLAIR_dir,'*brain_bfc.nii.gz'))[0]
        except:
            print(f'Subject {subject_ID} does not exist')
            subjects_list.append(subject_ID)
            continue
        T1_T2_reg = Node(fsl.FLIRT(), name='T1_T2_reg')
        T1_FLAIR_reg = Node(fsl.FLIRT(), name='T1_FLAIR_reg')
        T1_MNI_reg = Node(fsl.FLIRT(), name='T1_MNI_reg')
        T2_transformation = Node(fsl.ApplyXFM(), name='T2_transformation')
        FLAIR_transformation = Node(fsl.ApplyXFM(), name='FLAIR_transformation')
        # T2 to T1 Registration
        T1_T2_reg.inputs.in_file = T2_file_path
        T1_T2_reg.inputs.reference = T1_file_path
        T1_T2_reg.inputs.dof = 6
        T1_T2_reg.inputs.out_file = os.path.join(T1_dir, 'T2_Registered_To_T1.nii.gz')
        result = T1_T2_reg.run()
        # FLAIR to T1 Registration
        T1_FLAIR_reg.inputs.in_file = FLAIR_file_path
        T1_FLAIR_reg.inputs.reference = T1_file_path
        T1_FLAIR_reg.inputs.dof = 6
        T1_FLAIR_reg.inputs.out_file = os.path.join(T2_dir, 'FLAIR_Registered_To_T1.nii.gz')
        result = T1_FLAIR_reg.run()
        #T1 to MNI Registration
        T1_MNI_reg.inputs.in_file = T1_file_path
        T1_MNI_reg.inputs.reference = MNI_152_path
        T1_MNI_reg.inputs.dof = 12
        T1_MNI_reg.inputs.out_file = os.path.join(T1_dir, 'T1_brain_bfc_MNIreg.nii.gz')
        T1_MNI_reg.inputs.out_matrix_file = os.path.join(T1_dir, 'T1_MNIregis.mat')
        result = T1_MNI_reg.run()
        #T2 to MNI Registration
        T2_transformation.inputs.in_file= T1_T2_reg.inputs.out_file
        T2_transformation.inputs.reference = MNI_152_path
        T2_transformation.inputs.in_matrix_file = T1_MNI_reg.inputs.out_matrix_file
        T2_transformation.inputs.out_file =os.path.join(T2_dir, 'T2_brain_bfc_MNIreg.nii.gz')
        result = T2_transformation.run()
        #FLAIR to MNI Registration
        FLAIR_transformation.inputs.in_file= T1_FLAIR_reg.inputs.out_file
        FLAIR_transformation.inputs.reference = MNI_152_path
        FLAIR_transformation.inputs.in_matrix_file = T1_MNI_reg.inputs.out_matrix_file
        FLAIR_transformation.inputs.out_file =os.path.join(FLAIR_dir, 'FLAIR_brain_bfc_MNIreg.nii.gz')
        result = FLAIR_transformation.run()