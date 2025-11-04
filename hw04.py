"""A solution to hw04: a module to fit attenuation coefficient data.

This file uses hw04_aux, hw04_display and mu_over_alluminum.txt 
This code is poorly written and im suprised submitty gave me full credit
my graph is wack, enjoy reading <3
"""

# =============================================================================
# IMPORT LIBRARIES AS NEEDED
# DO _NOT_ IMPORT matplotlib HERE (SEE THE INSTRUCTIONS)
# =============================================================================
import numpy as np
import hw04_aux
import fitdata

# =============================================================================
# SET DEBUG/PLOT, FILENAME, and DATA SET SELECTION
# ALSO PROVIDE DEGREES OF POLYNOMIALS TO USE FOR FITS
# =============================================================================
DEBUG     = False
DEBUG2    = False
MAKE_PLOT = False

filename  = "mu_over_rho_aluminum.txt"
#filename = r"bumpyVENV\mu_over_rho_aluminum.txt"

mu_en = False
element = True
degree_fit   = 7
degree_shell = 1
n_lines = hw04_aux.file_line_count(filename)
dataStart,dataEnd,returnlist = hw04_aux.get_line_indices(filename,n_lines,element)

data = hw04_aux.get_data(filename,n_lines,dataStart,dataEnd)
material_name,_ = hw04_aux.read_material(filename)

returnlist = returnlist[0]
i_shells = returnlist
k_idx = -1

for i in range(len(returnlist)):
    if returnlist[i] > 0:
        k_idx +=1


subK_start = 0
subK_end = returnlist[k_idx]
superK_start = subK_end
superK_end = dataEnd



# =============================================================================
# READ AND PROCESS DATA
# =============================================================================



if (DEBUG):
    #print()
    #print("Number of lines in", filename, ":", n_lines)



# =============================================================================
# MAKE FITS
# =============================================================================

# Find last shell in data set, the K shell
# (if any shell discontinuities are present)
#
# Note that if there are no shells then i_shells[0]
# will be -1 and k_idx will equal -1.
#
    
    # fit sub-K-shell data
    
    log_e = np.log( data[subK_start:subK_end, 0] )
    log_m = np.log( data[subK_start:subK_end, 1] )
    #print(log_e,log_m)
    subK_coef = fitdata.calc_fit(log_e, log_m, degree=degree_shell)
    
    # plot data for sub-K fit
    eval_size = 5
    subK_xfit = np.linspace(log_e[0], log_e[-1], eval_size)
    subK_yfit = fitdata.eval_fit(subK_coef, subK_xfit) 

    #fit super-K shell data
    log_eS = np.log( data[superK_start:superK_end, 0] )
    log_mS = np.log( data[superK_start:superK_end, 1] )
    #print(log_e,log_m)
    superK_coef = fitdata.calc_fit(log_eS, log_mS, degree=degree_fit)

    #Super K??
    eval_size = 5
    superK_xfit = np.linspace(log_eS[0], log_eS[-1], eval_size)
    superK_yfit = fitdata.eval_fit(superK_coef, superK_xfit)






    if (DEBUG):
        print()
        print("sub-K-shell polynomial coefficients:")
        print(subK_coef)

    if (DEBUG2):
        print()
        print("subK xfit =")
        print(subK_xfit)
        print("subK yfit =")
        print(subK_yfit)




# =============================================================================
# MAKE PLOT
# =============================================================================

if (MAKE_PLOT):
    import hw04_display
    hw04_display.make_plot(material_name, data, mu_en, i_shells, k_idx,
                   degree_shell, degree_fit, subK_coef, superK_coef,
                   subK_xfit, subK_yfit, superK_xfit, superK_yfit)
