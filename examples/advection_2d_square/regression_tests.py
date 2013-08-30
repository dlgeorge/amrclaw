"""
Runs "make .plots" and then compares the .png files in _plots with the
archived results in the Clawpack gallery. 

Function test returns True if all .png files agree in the two directories.

Image differences can be viewed by opening a browser to 
    _image_diff/_ImageDiffIndex.html

For this to work you need to first clone and fetch the latest gallery
results from
     git://github.com/clawpack/clawpack.github.com

"""

import os, subprocess
from clawpack.clawutil import imagediff
reload(imagediff)

verbose = True
relocatable = False  # True ==> create directory _image_diff that can be posted 
                     # online (copies all images to subdirs of _image_diff)

def test():
    try:
        CLAW = os.environ['CLAW']
    except:
        raise Exception("Environment variable CLAW not set")

    # Compare plots to what is in the Clawpack gallery:
    gallery_dir = CLAW + "/clawpack.github.com/doc/_static/"

    # For testing with gallery built locally, instead use:
    # gallery_dir = CLAW + "/doc/doc/gallery/"  

    this_example = os.path.split(os.getcwd())[-1]
    
    gallery_plots = gallery_dir + "amrclaw/examples/" + this_example + "/_plots"
    if not os.path.isdir(gallery_plots):
        error_msg = "Missing directory %s\n Need to clone clawpack.github.com"\
                     % gallery_plots
        raise Exception(error_msg)

    # Run the code and create _plots directory:
    cmd = "make clean; make .plots"
    status=subprocess.Popen(cmd,shell=True).wait()
    if status != 0:
        raise Exception("Problem running the code, status = %s" % status)

    # Compare the resulting plots to the gallery version:
    try:
        regression_ok = imagediff.imagediff_dir('_plots',gallery_plots, \
                                relocatable=relocatable,overwrite=True, \
                                verbose=verbose)
    except:
        error_msg = "Error running imagediff with directories \n  %s\n  %s" \
                    % ('_plots',gallery_plots)
        raise Exception(error_msg)
    
    return regression_ok
    
if __name__=="__main__":
    regression_ok = test()
    print "regression_ok = ",regression_ok


