"""Provided code to create plot for hw04"""

def make_plot(material_name, data, mu_en, i_shells, k_idx,
              degree_shell, degree_fit, subK_coef, superK_coef,
              subK_xfit, subK_yfit, superK_xfit, superK_yfit):
    """Display plots of HW04 data, fits, and provide fit information.

    Input Parameters
    ----------------
    material_name : string; name of element or compound
    data          : 2D ndarray of floats; two columns of data:
                    energy [MeV], and either mu/rho or mu_en/rho
                    [cm2/g], depending on input `mu_en`
    mu_en         : Boolean; False for mu/rho data, True for
                    mu_en/rho data
    i_shells      : 1D ndarray of integers; data line index of
                    all electron shells in data file
    k_idx         : scalar integer; index of the highest energy
                    shell (the last non-negative-1 element in
                    array i_shells)
    degree_shell  : scalar integer; degree of polynomial used to
                    fit subK data
    degree_fit    : scalar integer; degree of polynomial used to
                    fit superK data
    subK_coef     : 1D ndarray of subK data fit coefficients
                    [c_0, c_1,... c_(n-1)]
    superK_coef   : 1D ndarray of superK data fit coefficients
                    [c_0, c_1,... c_(n-1)]
    subK_xfit     : 1D ndarray of floats; x coordinates of
                    sequence of points to connect with lines
                    to display the subK fit
    subK_yfit     : 1D ndarray of floats; y coordinates of
                    sequence of points to connect with lines
                    to display the subK fit
    superK_xfit   : 1D ndarray of floats; x coordinates of
                    sequence of points to connect with lines
                    to display the superK fit
    superK_yfit   : 1D ndarray of floats; y coordinates of
                    sequence of points to connect with lines
                    to display the superK fit

    OUTPUT:  None
    """
    import numpy as np
    import matplotlib.pyplot as plt

    # start plot
    plt.figure(1, figsize=(6, 4))

    # plot the data
    data_label = material_name + " data"
    plt.loglog(data[:,0], data[:,1], "k.", label=data_label)

    if (k_idx >= 0):
        # plot the sub-K fit; note the linear plot of exponential data
        subK_fit_label  = "subK region; fit degree = " + str(subK_coef.size-1)
        plt.plot(np.exp(subK_xfit), np.exp(subK_yfit), "b-", label=subK_fit_label)

    # plot the super K fit; note the linear plot of exponential data
    superK_fit_label  = "superK region; fit degree = " + str(superK_coef.size-1)
    plt.plot(np.exp(superK_xfit), np.exp(superK_yfit), "g-", label=superK_fit_label)

    # set plot bounds and draw grid
    plt.xlim([0.7e-3, 3.0e1])
    plt.ylim([1.0e-2, 1.0e4])
    plt.gca().grid()

    # plot axis labels, legend, title, and text box
    plt.rcParams["font.family"] = "Consolas"
    plt.xlabel("energy, E [MeV]", fontsize=11)
    if (mu_en):
        plt.ylabel("mass energy attenuation, $\\mu_{en}/\\rho$ [$cm^2/g$]", fontsize=11)
    else:
        plt.ylabel("mass attenuation, $\\mu/\\rho$ [$cm^2/g$]", fontsize=11)
    plt.legend(fontsize=10, loc=1)

    if (k_idx >= 0):
        shell_string  = "K shell is at\n"
        shell_string += str(data[i_shells[k_idx], 0]) + " [MeV]"
        plt.text(0.001, 0.03, shell_string, fontsize=10,
                    bbox={"facecolor": "black", "alpha": 0.04, "pad": 2})

    suptitle_string  = "Mass attenuation coefficient for "
    suptitle_string += material_name
    plt.suptitle(suptitle_string, fontsize=12, y=0.92)

    np.set_printoptions(precision=1)
    title_string  = "\nsubK fit: " + str(subK_coef)
    title_string += "\nsuperK fit: " + str(superK_coef)
    plt.title(title_string, fontsize=8)

    plt.tight_layout()
    plt.savefig('simona6_plot.png', dpi=300, edgecolor="none")
    plt.show()

    return None

