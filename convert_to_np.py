"""
Convert .nii.gz files to numpy.
Starts from dataPath and expects Task01_BrainTumour folder, containing imagesTr and labelsTr.
Creates folders with numpy files.
"""
import os
import nibabel as nib
import numpy as np
import skimage.transform
import tqdm

# Parser
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--dataPath', type=str, default='./data')
parser.add_argument('-r', type=bool, help='If True, it will downsample images.', default=True)
parser.add_argument('-size', type=int, help="If -r is True, it will downsample to -size.", default=32)
parser.add_argument('-low', type=int, help="Lower slice bound.", default=46)
parser.add_argument('-high', type=int, help="Upper slice bound.", default=110)
parser.add_argument('-clip', type=bool, help="If True, it will clip labels to 0,1.", default=True)
parser.add_argument('-chanFirst', type=bool, help="If True, puts channel axis first.", default=True)
parser.add_argument('-cxlow', type=int, help="Crop lower bound on x-axis", default=50)
parser.add_argument('-cxhigh', type=int, help="Crop higher bound on x-axis", default=195)
parser.add_argument('-cylow', type=int, help="Crop lower bound on y-axis", default=20)
parser.add_argument('-cyhigh', type=int, help="Crop higher bound on y-axis", default=200)
args = parser.parse_args()

dataPath = args.dataPath
RESIZE = args.r
SIZE = args.size
SLICE_LOW = args.low
SLICE_HIGH = args.high
CLIP = args.clip
CHANFIRST = args.chanFirst
CROP_X_LOW = args.cxlow
CROP_X_HIGH = args.cxhigh
CROP_Y_LOW = args.cylow
CROP_Y_HIGH = args.cyhigh

print(f'dataPath is {dataPath}')

# before we start, a helper function to resize images
def img_resize(img,
    lower=SLICE_LOW,
    upper=SLICE_HIGH,
    xlower=CROP_X_LOW,
    xupper=CROP_X_HIGH,
    ylower=CROP_Y_LOW,
    yupper=CROP_Y_HIGH,
    size=SIZE,
    inp=True,
    clip=False):
    """
    img is a 3d or 4d numpy array: DxDxSxC
        - D is dimension of width and height
        - S is the number of slices
        - C is the number of channels
    0 <= lower < upper <= S
    0 <= size <= D
    
    if clip = True, it groups all non-background together.
    """
    if inp:
        img = img[xlower:xupper,ylower:yupper,lower:upper,:]
        slices = img.shape[2]
        channels = img.shape[3]
        img = skimage.transform.resize(img,(size,size,slices,channels))
        return img
    else:
        img = img[xlower:xupper,ylower:yupper,lower:upper]
        slices = img.shape[2]
        img = skimage.transform.resize(img,
                                      (size,size,slices),
                                      preserve_range=True,
                                      anti_aliasing=False,
                                      order=0)
        img = img.astype('uint8')
        if clip:
            img = np.clip(img,0,1)
        return img


# Here we go ---------------------
# obtain paths to data and perform sanity check
t1_path = os.path.join(dataPath, 'all_gbm_pre_reg')
t1_contrast_path = os.path.join(dataPath, 'all_gbm_post_reg')
tumor_path = os.path.join(dataPath, 'all_tumors_reg')
brain_mask_path = os.path.join(dataPath, 'brain_masks')

imgPaths = os.listdir(t1_path)
t1_locations = []
for path in imgPaths:
    if path.endswith('.nii.gz'):
        t1_locations.append(path)

imgPaths = os.listdir(t1_contrast_path)
t1_contrast_locations = []
for path in imgPaths:
    if path.endswith('.nii.gz'):
        t1_contrast_locations.append(path)

imgPaths = os.listdir(tumor_path)
tumor_locations = []
for path in imgPaths:
    if path.endswith('.nii.gz'):
        tumor_locations.append(path)
        
imgPaths = os.listdir(brain_mask_path)
brain_mask_locations = []
for path in imgPaths:
    if path.endswith('.nii.gz'):
        brain_mask_locations.append(path)

# input data
if RESIZE:
    newPath = os.path.join(dataPath, 'numpyData'+str(SIZE))
else:
    newPath = os.path.join(dataPath, 'numpyDataOG')
if not os.path.exists(newPath):
    os.mkdir(newPath)

num_t1_path = os.path.join(newPath, 'num_t1')
if os.path.exists(num_t1_path):
    print('Folder already exists, so I did not create any numpy from t1.')
else:
    os.mkdir(num_t1_path)

    print('I am starting to convert t1 images.')
    path = t1_path
    t1_progress = tqdm.tqdm(enumerate(t1_locations))
    for i, imageLocation in t1_progress:
        t1_progress.set_description(f"Processing image {imageLocation}")
        # get the .nii image
        imageData = nib.load(os.path.join(path,imageLocation))
        # convert to numpy
        numpyImage = imageData.get_data()
        if RESIZE:
            numpyImage = img_resize(numpyImage)
        if CHANFIRST:
            numpyImage = np.transpose(numpyImage,(3,0,1,2))
        np.save(os.path.join(numtrainpath, imageLocation), numpyImage)
        
        
num_t1_contrast_path = os.path.join(newPath, 'num_t1_contrast')
if os.path.exists(num_t1_path):
    print('Folder already exists, so I did not create any numpy from t1 contrast.')
else:
    os.mkdir(num_t1_path)

    print('I am starting to convert t1 contrast images.')
    path = t1_contrast_path
    t1_contrast_progress = tqdm.tqdm(enumerate(t1_contrast_locations))
    for i, imageLocation in t1_contrast_progress:
        t1_contrast_progress.set_description(f"Processing image {imageLocation}")
        # get the .nii image
        imageData = nib.load(os.path.join(path,imageLocation))
        # convert to numpy
        numpyImage = imageData.get_data()
        if RESIZE:
            numpyImage = img_resize(numpyImage)
        if CHANFIRST:
            numpyImage = np.transpose(numpyImage,(3,0,1,2))
        np.save(os.path.join(t1_contrast_path, imageLocation), numpyImage)
        
num_tumor_path = os.path.join(newPath, 'num_tumor')
if os.path.exists(num_t1_path):
    print('Folder already exists, so I did not create any numpy from t1 contrast.')
else:
    os.mkdir(num_t1_path)

    print('I am starting to convert t1 contrast images.')
    path = t1_contrast_path
    t1_contrast_progress = tqdm.tqdm(enumerate(t1_contrast_locations))
    for i, imageLocation in t1_contrast_progress:
        t1_contrast_progress.set_description(f"Processing image {imageLocation}")
        # get the .nii image
        imageData = nib.load(os.path.join(path,imageLocation))
        # convert to numpy
        numpyImage = imageData.get_data()
        if RESIZE:
            numpyImage = img_resize(numpyImage)
        if CHANFIRST:
            numpyImage = np.transpose(numpyImage,(3,0,1,2))
        np.save(os.path.join(t1_contrast_path, imageLocation), numpyImage)

print('All done, I think.')