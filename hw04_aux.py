"""Module Docstring: This module is a poorly writen way to access data from two kinds of text files those with element data and those with composition data.

    This module is written to be used in conjuntion with hw04
    Some functions have hardcoded values that will return the wrong values if the
    .txt files are not formatted properly, because hardcoding the values in was simpler
"""

import numpy as np 
def file_line_count(filename):
    '''Input: string with complete filename (e.g., "mu_over_rho_aluminum.txt").
    Output: scalar integer number of lines of information in the file (including data,
    headers, extraneous information, and blank lines).
    '''
    n_lines = 0
    with open(filename,"r",encoding='utf8') as file:
        for line in file:
            n_lines +=1
    return n_lines

def read_material(filename):
    '''Input: string with complete filename (e.g., "mu_over_rho_aluminum.txt").
    Output: string with material name (e.g., “Aluminum”);
    scalar integer atomic number (e.g., 13) or -1 for a compound.
    '''
    with open(filename,"r",encoding="utf8") as file:
        materialName = file.readline().strip()
        atomicNumber = file.readline().strip("Z = \n")
        if atomicNumber == "ASCII format":
            atomicNumber = -1
        else:
            atomicNumber = int(atomicNumber)
    return materialName,atomicNumber

def get_line_indices(filename,n_lines, element = True):
    '''Input: string with complete filename (e.g., "mu_over_rho_aluminum.txt");
    scalar integer number of lines in the file (e.g., 49);
    optional Boolean which defaults to True, indicating the file contains
    element data. If set to False, the file contains composition data.

    Output: file line number that data starts on (inclusive);
    file line number that data ends on (inclusive);
    a 16-element 1D ndarray of integer data line numbers (not file line
    numbers, only counting lines of data) that have shell indicators, or
    -1 for shells not indicated in the file, in sequence from low energy
    to high energy.
    '''
    returnList = -1 * np.ones((1,16), dtype= int)
    dataStart = 0
    dataEnd = 0
    lineNum = 0
    noData = True
    with open(filename,"r",encoding="utf8") as file:
        shellIndex = 0 
        while lineNum < n_lines:
            line = file.readline().strip()
            lineNum+=1
            if element:
                shellSpacing = 0 
            else:
                shellSpacing = 4
            if noData:
                if line[:11] != "1.00000E-03":
                    dataStart +=1
                else:
                    noData = False
            else:
                if not line[shellSpacing].isdigit():
                        
                    returnList[0,shellIndex] = dataEnd - dataStart
                    shellIndex+=1
            dataEnd +=1
        dataEnd-=1
    return dataStart, dataEnd, returnList
 
#print(get_line_indices(r"bumpyVENV\mu_over_rho_aluminum.txt",49))


def get_data(filename,n_lines,i_start,i_end,mu_en=False,element=True):
    '''Input: string with complete filename (e.g., "mu_over_rho_aluminum.txt");
    scalar integer number of lines in the file (e.g., 49);
    scalar integer file line number for first line of data (e.g., 3);
    scalar integer file line number for last line of data (e.g., 8);
    optional Boolean which defaults to False, indicating the data requested is
    (μen/rho) if True, and (μ/rho) if False.
    optional Boolean which defaults to True, indicating the file contains
    element data. If set to False, the file contains composition data.
    
    Output: a 2D NumPy ndarray with two columns (energy, and either (μ/rho) or (μen/rho)
    depending on what parameter mu_en is set to) and as many rows as there
    are rows of data in the file.
    '''

    data = np.zeros((i_end-i_start+1,2))
    lineNum = i_start
    dataIndex = 0
    shellSpacing = 0
    #print(i_start,i_end)
    with open(filename,"r",encoding="utf8") as file:

        for i in range(0,i_start):
            file.readline()

        while lineNum < i_end+1:
            if element:
                shellSpacing = 0
            else:
                shellSpacing = 3

            line = file.readline().strip()


            if not line[shellSpacing].isdigit():
                line = line[(shellSpacing+3):]

            data[dataIndex,0] += float(line[0:11])

            if not mu_en:
                data[dataIndex,1] += float(line[13:22])
            else:
                data[dataIndex,1] += float(line[24:])

            dataIndex+=1

            if not line:
                break

            lineNum+=1
            #print(data.shape)
    return data
#print(get_line_indices(r"bumpyVENV\mu_over_rho_aluminum.txt",49))
#print(get_data(r"bumpyVENV\mu_over_rho_aluminum.txt",0,11,48))

def back_sub(lu_fac: np.ndarray,y: np.ndarray):
    """Computes backwards substitution for lu_fac and y
    inputs should be a square 2d np.ndarray and a 1d ndarray
    output is a 1d ndarray 
    this code is reused from a previous ICA
    """
    #assert lu_fac.shape[0] == lu_fac.shape[1], "lu_fac must be square"
    x = y.copy()
    for i in range(x.shape[0]-1,-1,-1):
        for j in range(i+1,x.shape[0]):
            x[i] -= lu_fac[i][j] * x[j]
        #assert abs(lu_fac[i][i]) >= 1.0e-15, "Division by zero"
        x[i] /= lu_fac[i][i]
    return x
