import os

path = './dataset/all_tumors_reg/'
file_names = os.listdir(path)

str = "." 
suffix = "_mask"
if file_names[0].split('.')[0].endswith(suffix): 
    print("the data names have already been modified, no further action will be taken")
else: 
    for temp in file_names:
        img = os.path.join(path, temp)
        
        name = temp.split('.')
        fname = name[0]
        ext = '.' + str.join(name[1:])
        
        
    #     base_name = os.path.basename(fname)
    #     print(fname)
    #     print(ext)
        new_n = fname + '_mask' + ext
    
        print(os.path.join(path, new_n))
        os.rename(os.path.join(path, temp), os.path.join(path, new_n))
    
    print("\n suffix '_mask' is added successfully")
    