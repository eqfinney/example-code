# Emily Quinn Finney
# March 3, 2013
""" This script should find the line-of-sight velocity of each object based on 
    its redshift and use those velocities to find the radial velocity 
    dispersion.  Uncorrected, corrected, and physical radial velocity
    dispersions should be calculated for the cluster.
"""

import math
import numpy

def main(maindir):
    """ Given a text file of all object redshifts and redshift errors and a 
        coordinates file of all RA, Dec corresponding to those objects, uses
        the helper functions defined below to calculate the corrected and 
        uncorrected line-of-sight velocity dispersions of the cluster in 
        question.
        Inputs: maindir, a file path, which will be directed to
                a redshift file of the form
                slit#  redshift  error
                and a coordinate file of the form
                slit#  RA (hh mm ss) Dec (hh mm ss)
        Outputs: None, but print statements will reveal the uncorrected velocity
                 dispersion, the corrected velocity dispersion, and the physical
                 velocity dispersion
        """
    # Sets up the necessary arrays
    redshift_array = numpy.loadtxt(maindir+'/redshifts.txt')

    # Determine the cluster median
    median = numpy.median(redshift_array[:,1])

     # Throw out the redshifts that aren't close
    i=0
    redshifts=[]
    errors=[]
    for line in redshift_array:
        if numpy.absolute(line[1]-median) < 0.01: # z=0.01~2500km/s
            redshifts.append(line[1])
            errors.append(line[2])
            i=i+1
    print "There are", numpy.size(redshifts), "cluster members."

    # Find the mean redshift, the likely center of the overdensity
    mean = numpy.mean(redshifts)
    print "The mean of the redshifts is:", mean
    esquared = [x**2 for x in errors]
    z_err = math.sqrt(numpy.sum(esquared))/numpy.size(errors)
    print "The error of the redshifts is:", z_err

    # Initialize an array of the same length as the others
    velocities=numpy.zeros(len(redshifts))
    
    # Find the velocities and corrected velocities
    i=0
    for z in redshifts:
        velocities[i]=find_velocity(z,mean)
        velocities_corr[i] = corr_velocity(z, mean, lats[i], longs[i])
        i=i+1
    velavg=[numpy.absolute(x) for x in velocities]
    mvel=numpy.mean(velavg)
    print "The mean velocity is:", mvel
    
     # Find the dispersions
    disp = dispersion(mean, velocities, errors)
    disp_corr = dispersion(mean, velocities_corr, errors)
    disp_phys = math.sqrt(3)*disp
    print "The uncorrected line-of-sight velocity dispersion for this cluster is:", disp
    print "The corrected line-of-sight velocity dispersion for this cluster is:", disp_corr
    print "The physical line-of-sight velocity dispersion for this cluster is:", disp_phys
    return

def convert(path):
    """ Given a text file containing a slit number, an RA (in hh mm ss) and a
        dec (in deg arcmin arcsec), converts from equatorial coordinates to 
        galactic coordinates.
        Input: path, gives the location of a text file (string)
        Output: coords, an array giving galactic coordinates (l,b)
        """
    # reads in the file of equatorial coordinates
    eq = numpy.loadtxt(path)
    coords= numpy.zeros((numpy.shape(eq)[0],3))

    for slit in range(numpy.shape(eq)[0]):
        # Converting RA and dec from original form to degrees
        RA = eq[slit][1]/15. + eq[slit][2]/300. + eq[slit][3]/18000.
        dec= -1*(-1*eq[slit][4] + eq[slit][5]/60. + eq[slit][6]/3600.)
        # Converting RA and dec to galactic coordinates
        b=math.asin( math.sin(dec)*math.cos(62.6) - math.cos(dec)*math.sin(RA-282.25)*math.cos(62.6) )
        l= math.acos( math.cos(dec)*math.cos(RA-282.25)/math.cos(b) ) - 33
        # Adding to the table
        coords[slit][0]=slit
        coords[slit][1]=l
        coords[slit][2]=b
    
    return coords
    
def find_velocity(z,z_cosm):
    """ Given a galaxy redshift and an estimate of cosmological redshift, 
        calculates the uncorrected line-of-sight velocity of the galaxy.
        Input: z, a redshift (float)
               z_cosm, a redshift (float)
        Output: velocity, the object's line-of-sight velocity (float)
        """

    c=(2.99*10**8)/1000 # c in km/s
    velocity=c*(z-z_cosm)/(1+z_cosm)
    return velocity

def corr_velocity(z,z_cosm,l,b):
    """ Given a galaxy redshift, an estimate of cosmological redshift, and 
        the galactic coordinates of the object, calculates the corrected
        line-of-sight velocity of the galaxy.
        Input: z, a redshift (float)
               z_cosm, a redshift (float)
               l, the galactic longitude of the object (float)
               b, the galactic latitude of the object (float)
        Output: velocity, the object's corrected line-of-sight velocity (float)
        """
    
    c=(2.99*10**8/1000) # c in km/s
    v0=300*math.sin(l)*math.cos(b) 
    z0=v0/c
    velocity=c*((z-z0-z_cosm-z0*z_cosm)/( (1+z0)*(1+z_cosm) ))
    return velocity

def dispersion(z_cosm, velocities, errors):
    """ Finds the dispersion of an array of velocities (with associated errors)
        using the ideas presented in Mischa's summary of Danese et al. 1980,
        Harrison 1974.  
        Input: z_cosm, a redshift (float)
               velocities, an array of velocities (array of floats)
               errors, an array of the errors associated with the velocities
                   (array of floats)
        Output: dispersion, a velocity dispersion (float)
        """
    
    c=(2.99*10**8)/1000 # c in km/s

    # Use a list comprehension to square the velocities
    squared=[v**2 for v in velocities]
    # Find the length of the original list
    v_len=numpy.size(velocities)
    # Add the new list together
    v_sum=numpy.sum(squared)
    # Divide the added new list by the length of the original list minus one
    main_term=v_sum/(v_len - 1)
    print "Main term is:", main_term

    # Add the errors together and multiply by c
    e_sum=numpy.sum(errors)
    delta=c*e_sum
    # Find the length of the original errors list
    e_len=numpy.size(errors)
    # Divide the added new list by the length of the original list and square
    delta_avg=delta/e_len
    delta_square=delta_avg**2
    # Divide the new value by (1+z_cosm)**2
    error_term=delta_square/( (1+z_cosm)**2 )
    print "Error term is:",error_term
    
    # Subtract the value obtained for the error term from the value obtained for
    # the original standard deviation
    if main_term > error_term:
        dispersion = math.sqrt(main_term - error_term)
        print "dispersion is:", dispersion
    
    else:
        print "ERROR!!!"
        dispersion = 'UNKNOWN'

    return dispersion
