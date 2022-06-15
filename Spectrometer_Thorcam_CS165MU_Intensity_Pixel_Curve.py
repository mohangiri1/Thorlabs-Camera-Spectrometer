# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 10:07:21 2022

@author: Mohan_Giri1
"""

#Preliminary Program for getting the relation between pixel and Intensity from the Thorlabs camera CS 165MU



    
    
#-----------------------------Importing libraries and packages-------------------------------------------------------------
#%matplotlib notebook 
 #This is for interactive plot in jupiter notebook.This doesn't work in spyder though (So comment on %matplotlib if you are at spider).

            #----------------Setting path in windows------------------    
try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path
    configure_path()
except ImportError:
    configure_path = None
import os
          #------------------------------------------------------------

from matplotlib import pyplot as plt        #package for the plot.
import time                                 #importing time
import numpy as np                          #Importing package for mathematical calculations.
                   #---------------------importing package for Thorlabs camera---------------------------------
from tl_camera import TLCameraSDK
from tl_mono_to_color_processor import MonoToColorProcessorSDK
from tl_camera_enums import SENSOR_TYPE
                   #--------------------------------------------------------------------------------------------
    
    
    
#------------------------------Setting the plot window--------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(111)
#-----------------------Get Information from the camera-----------------------------------------------------------------

with TLCameraSDK() as sdk:
    cameras = sdk.discover_available_cameras()
    if len(cameras) == 0:
        print("Error: no cameras detected!")

    with sdk.open_camera(cameras[0]) as camera:
        #  setup the camera for continuous acquisition
        camera.frames_per_trigger_zero_for_unlimited = 0
        _bit_depth = camera.bit_depth
        camera.image_poll_timeout_ms = 2000  # 2 second timeout
        camera.arm(2)


        image_width = camera.image_width_pixels
        image_height = camera.image_height_pixels
# ------------------------------begin acquisition----------------------------------------------------------------------
        
        camera.issue_software_trigger()
        frames_counted = 0
        iteration_number = 0
        final_data = []
        while iteration_number <= 2:     #This if loop is for the program to get information from camera continuously.  
            #for i in range(21):
            while frames_counted < 21:   #This loop is for adding 10 frame to get the spectral information.
                frame = camera.get_pending_frame_or_null()
                if frame is None:
                    raise TimeoutError("Timeout was reached while polling for a frame, program will now exit")

                frames_counted += 1
                image_data = frame.image_buffer >> (_bit_depth - 10)  #This is the data from the camera in each frame
                image_data += image_data                         #This adds data from camera for different frame in while loop
            data = np.sum(image_data, axis=0) #This adds all the vertical pixel to get 1 dimensional horizontal array.
            final_data = np.append(final_data, data)
#-----------------------------------------Plotting---------------------------------------------------------------------


            plt.rcParams['animation.html'] = 'jshtml'
            ax.plot(final_data)
            plt.xlabel("Pixel")
            plt.ylabel("Intensity")
            plt.title('Peak VS Pixel plot')
            #plt.show()
            fig.canvas.draw()
            time.sleep(0.0001)
            ax.clear()
            fig.canvas.flush_events()
            iteration_number += 1
#-----------------------------------------Getting data continuously-------------------------------------------------


            if frames_counted == 21 and iteration_number == 1:   #To go back to the acquisition
                frames_counted = 0                        #Resetting frames counting
                iteration_number = 0                              #Resetting the data acquisition number and resetting plot for new data.
                final_data = []                           #Resetting the old data from camera to get new one.
                continue
#--------------------------End of program-----------------------------------------------------------------------------