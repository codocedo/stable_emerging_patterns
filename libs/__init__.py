import numpy as np
from scipy.misc import comb


def stab_metric(theta,Ap,Am):
    """
    Computes the stability of an emerging pattern.
    
    Parameters
    ----------
    theta: scalar
        growth rate threshold
    Ap: integer
        cardinality of the positive part of the pattern
    Am: integer
        cardinality of the negative part of the pattern
    
    Returns
    -------
    \sigma_\theta(A): scalar
        the stability of the pattern A, for a threshold \theta
    
    See Also
    --------
    np.vectorize, ndarray's of consistent shape as args
    
    Examples
    --------
    One pattern and threshold
    
    >>> s1 = stability(10/13.0,10,3)
    0.5
    >>> s2 = stability(8/13.0,10,3)
    0.88427734375
    
    
    One pattern, several thresholds with np.vectorize
    
    >>> vStability = np.vectorize(stability)
    >>> thetas = np.linspace(0.7,0.9,5)
    >>> s3 = vStability(thetas,10,3)
    [ 0.73449707  0.62207031  0.45593262  0.26623535  0.12890625]
    
    
    Several patterns, one threshold
    
    >>> Ap = np.linspace(5,10,6)
    >>> Am = 3
    >>> s4 = vStability(0.6,Ap,Am)
    [ 0.6171875   0.71679688  0.79394531  0.85253906  0.89624023  0.92822266]
    """
    s = 0
    for kp in range(1,int(Ap)+1):
        if theta>0.0:
            kmmax =  min(Am,np.floor(kp*((1.0-theta)/theta+np.finfo(type(theta)).eps)))
        else:
            kmmax = Am
        km = np.linspace(0,kmmax,kmmax+1)
        s += np.sum(comb(Ap,kp)*comb(Am,km))
    return s/2.0**(Ap+Am)