from pdf2image import convert_from_path
import os
import timeit
import getopt
import sys
import glob
from multiprocessing import Pool
import gc
from tqdm import tqdm

def PDF_to_img(name ,parent_dir, Output_dir):
    
    images = convert_from_path(os.path.join(parent_dir, name))
    
    Output_dir = os.path.join(Output_dir, name.split(".pdf")[0])
    os.makedirs(Output_dir)
    
    for i, img in tqdm(enumerate(images)):
        img.save(os.path.join(Output_dir ,str(i)+'.jpg'), 'JPEG')
    
    print('## '+name + 'saved. ##')
    del images
    
    gc.collect()

if __name__ == "__main__":
    # name = '1_Learn Python The Hard Way, 3rd Edition.pdf'
    # parent_dir = 'D:\\Github\\PDF_to_IMG\\Books\\'
    # Output_dir = 'D:\\Github\\PDF_to_IMG\\ImagesBooks\\'
    argLst = sys.argv[1:]
    
    options = "hi:o:p:"
    
    long_options = ["Help", "Input", "Output", "Parallel"]
    
    arguments, values = getopt.getopt(argLst, options, long_options)
    
    parallel = False
    parent_dir = ''
    Output_dir = ''
        
    for currentArg, currentVal in arguments:
        if currentArg in ('-h', '--Help'):
            print("Dislay Help")
        
        if currentArg in ('-i', '--Input'):
            parent_dir = currentVal
        
        if currentArg in ('-o', '--Output'):
            Output_dir = currentVal
        
        if currentArg in ('-p', '--Parallel'):
            parallel = currentVal
        
    if parent_dir == '':
        print("input arg cannot be null")
        print("Run Command: with arg -i \"<Filepath>\"")
        sys.exit()
    
    if Output_dir == '':
        Output_dir = parent_dir
            
    start = timeit.default_timer()
    
    # PDF_to_img(name, parent_dir, Output_dir)
    if not parallel:
        for file in os.listdir(parent_dir):
            if file.endswith('.pdf'):
                PDF_to_img(file, parent_dir, Output_dir)
    else:
        # print(parent_dir)
        file = glob.glob(os.path.join(parent_dir, "*.pdf"))
        # print(file)
        file = [[os.path.basename(f), parent_dir, Output_dir] for f in file]
        # print(file)
        Pool().starmap(PDF_to_img, file)
    
    stop = timeit.default_timer()
    
    print('Time: ', stop - start)  
    
    # python PDF_to_IMG.py -i "books" -o "ImagesBooks" -p true