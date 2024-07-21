import numpy as np
import pandas as pd

def calc_l(l):
    '''
    This function is the minimum of all elements in l
    '''
    return min(l)

def calc_l_dash(l, d):
    '''
    This function is the multiplication of all elements in l, whole to the power of 1/d
    '''
    result = 1
    for i in l:
        result = result * i
    result = (result ** (1/d))
    return result

def calc_m(m, d):
    '''
    This function is the multiplication of all elements in m, whole to the power of 1/d
    '''
    result = 1
    for i in m:
        result = result * i
    result = (result ** (1/d))
    return result

def calc_u_dash(u, d):
    '''
    This function is the multiplication of all elements in u, whole to the power of 1/d
    '''
    result = 1
    for i in u:
        result = result * i
    result = (result ** (1/d))
    return result

def calc_u(u):
    '''
    This function is the maximum of all elements in u
    '''
    return max(u)

def calc_ivt(arr, d):
    '''
    This function calculates the IVT of the input array.

    Parameters:
    -----------
    arr: np.array
        The input array.
    d: int
        The number of criteria.
    
    Returns:
    -----------
    list
        The list of calculated IVT.
    '''
    arr_l = []
    arr_m = []
    arr_u = []
    for i in range(len(arr)):
        arr_l.append(arr[i][0])
        arr_m.append(arr[i][1])
        arr_u.append(arr[i][2])
    l = calc_l(arr_l)
    l_dash = calc_l_dash(arr_l, d)
    m = calc_m(arr_m, d)
    u_dash = calc_u_dash(arr_u, d)
    u = calc_u(arr_u)

    result = [l, l_dash, m, u_dash, u]
    return result

def calc_ivfda(ivt_pdf, positive=True):
    '''
    This funcntion calculates positive or negative distance of input matrix ivt_pdf from the average solution.

    Parameters:
    -----------
    ivt_pdf: dict
        The input matrix in the form of dictionary.
    positive: bool
        If True, calculates positive distance, else negative distance.
    
    Returns:
    -----------
    np.array
        The array of calculated positive or negative distance.
    '''

    results = []
    for i in ivt_pdf:
        features = np.array(ivt_pdf[i])
        arr_l, arr_l_dash, arr_m, arr_u_dash, arr_u = [], [], [], [], []

        for j in features:
            arr_l.append(j[0])
            arr_l_dash.append(j[1])
            arr_m.append(j[2])
            arr_u_dash.append(j[3])
            arr_u.append(j[4])

        avg_l = np.mean(arr_l)
        avg_l_dash = np.mean(arr_l_dash)
        avg_m = np.mean(arr_m)
        avg_u_dash = np.mean(arr_u_dash)
        avg_u = np.mean(arr_u)

        ivfda_l = []
        ivfda_l_dash = []
        ivfda_m = []
        ivfda_u_dash = []
        ivfda_u = []

        for j in range(len(arr_l)):
            if positive:
                ivfda_l.append(calc_pda(arr=arr_l[j], avg=avg_l))
                ivfda_l_dash.append(calc_pda(arr=arr_l_dash[j], avg=avg_l_dash))
                ivfda_m.append(calc_pda(arr=arr_m[j], avg=avg_m))
                ivfda_u_dash.append(calc_pda(arr=arr_u_dash[j], avg=avg_u_dash))
                ivfda_u.append(calc_pda(arr=arr_u[j], avg=avg_u))
            else:
                ivfda_l.append(calc_nda(arr=arr_l[j], avg=avg_l))
                ivfda_l_dash.append(calc_nda(arr=arr_l_dash[j], avg=avg_l_dash))
                ivfda_m.append(calc_nda(arr=arr_m[j], avg=avg_m))
                ivfda_u_dash.append(calc_nda(arr=arr_u_dash[j], avg=avg_u_dash))
                ivfda_u.append(calc_nda(arr=arr_u[j], avg=avg_u))

        ivfda_arr = np.array([ivfda_l, ivfda_l_dash, ivfda_m, ivfda_u_dash, ivfda_u]).T
        # print("Final")
        # print(f"For {i}: {ivfda_arr[0]}\n")
        results.append(ivfda_arr)
    return np.array(results)


def calc_pda(arr, avg):
    result = max(0, (arr-avg)/avg)
    return result

def calc_nda(arr, avg):
    result = max(0, (avg-arr)/avg)
    return result