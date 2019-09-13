##########################################################################################

import bpy
import numpy as np
import math
import os

##########################################################################################

def UAVfly(par):

    #adding camera
    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0, 0, par.pos_cam_z), rotation=(0, 0, math.radians(-90)))

    bpy.context.scene.camera = bpy.data.objects['Camera'] #selects the scene camera
    cam = bpy.data.objects['Camera']

    #camera presets
    bpy.context.scene.render.resolution_percentage = 100
    
    if par.camera == 'Phantom4':
        bpy.context.scene.render.resolution_x = 5472
        bpy.context.scene.render.resolution_y = 3648    
        bpy.context.object.data.lens = 24 #lens focal length
        bpy.context.object.data.sensor_fit = 'HORIZONTAL'
        bpy.context.object.data.sensor_height = 8.8
        bpy.context.object.data.sensor_width = 13.2
    
    #bpy.context.scene.render.use_local_coords = True #check
    bpy.context.scene.render.image_settings.file_format = 'TIFF' #image format
    bpy.context.scene.render.image_settings.tiff_codec = 'NONE' #no compression

    #angles of view
    AOVh = 2*np.arctan(bpy.context.object.data.sensor_width/(2*bpy.context.object.data.lens))
    AOVv = 2*np.arctan(bpy.context.object.data.sensor_height/(2*bpy.context.object.data.lens))

    dist_photo_side = 2*par.pos_cam_z*np.tan(AOVh/2)*(1-par.overlap)
    dist_photo_front = 2*par.pos_cam_z*np.tan(AOVv/2)*(1-par.overlap)

    #UAV goes from left bottom to right top
    Xmax = max(par.Xcoord.tolist())[0]
    Xmin = min(par.Xcoord.tolist())[0]
    Ymax = max(par.Ycoord.tolist())[0]
    Ymin = min(par.Ycoord.tolist())[0]

    size_exp_x = abs(Xmin) + abs(Xmax)
    size_exp_y = abs(Ymin) + abs(Ymax)

    #getting the positions of cam in y
    n_trips_y = math.ceil(size_exp_y/dist_photo_side) + 3 
    size_cam_y = (n_trips_y - 2)*dist_photo_side #subtract 1 to match the real size

    pos_cam_y = list(range(n_trips_y))
    for p in range(n_trips_y):
        pos_cam_y[p] = p * dist_photo_side
    
    pos_cam_y_cent = pos_cam_y - size_cam_y/2 #centered position on 0

    #getting the positions of cam in x
    n_photos_x = math.ceil(size_exp_x/dist_photo_front) + 3
    size_cam_x = (n_photos_x - 2)*dist_photo_front #subtract 1 to match the real size
    
    n_cameras = n_trips_y * n_photos_x
    
    pos_cam_x = list(range(n_photos_x))
    for p in range(n_photos_x):
        pos_cam_x[p] = p * dist_photo_front
    
    pos_cam_x_cent = pos_cam_x - size_cam_x/2 #centered position on 0

    #estimating pixel size for photoscan
    def pixelSize(camd):
        f_in_mm = camd.lens
        scene = bpy.context.scene
        resolution_x_in_px = scene.render.resolution_x
        resolution_y_in_px = scene.render.resolution_y
        scale = scene.render.resolution_percentage / 100
        sensor_width_in_mm = camd.sensor_width
        sensor_height_in_mm = camd.sensor_height
        pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
        if (camd.sensor_fit == 'VERTICAL'):
            # the sensor height is fixed (sensor fit is horizontal), 
            # the sensor width is effectively changed with the pixel aspect ratio
            s_u = 1/(resolution_x_in_px * scale / sensor_width_in_mm / pixel_aspect_ratio)
            s_v = 1/(resolution_y_in_px * scale / sensor_height_in_mm)
        else: # 'HORIZONTAL' and 'AUTO'
            # the sensor width is fixed (sensor fit is horizontal), 
            # the sensor height is effectively changed with the pixel aspect ratio
            pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
            s_u = 1/(resolution_x_in_px * scale / sensor_width_in_mm)
            s_v = 1/(resolution_y_in_px * scale * pixel_aspect_ratio / sensor_height_in_mm)
        return (s_u,s_v)

    PS = open(par.mainPath + '/meta/' + par.trial + '/' + par.trial + '.PS.txt', 'w')
    PS.write('\n\nPhotoscan information:\n\tFocal length:' + str(bpy.context.object.data.lens) + '\n\tEstimated pixel size: ' + str(pixelSize(bpy.context.object.data)))
    PS.close()
    print('\n\nPhotoscan information:\n\tFocal length:' + str(bpy.context.object.data.lens) + '\n\tEstimated pixel size: ' + str(pixelSize(bpy.context.object.data)))
        
    EXIF = open(par.mainPath + '/meta/' + par.trial + '/' + par.trial + '.EXIF.txt', 'w')
    EXIF.write("#Label\tEasting/X/Longitude\tNorthing/Y/Latitude\tZ/Altitude\tYaw\tPitch\tRoll" + '\n')

    #looping across positions 
    for ypos in range(n_trips_y):
        #positioning the camera
        cam.location.y = pos_cam_y_cent[ypos]
        
        for xpos in range(n_photos_x):
            #positioning the camera
            cam.location.x = pos_cam_x_cent[xpos]
            id_img = 'shot_x%d.y%d.tif' % (xpos,ypos)

            #taking pictures
            print('\n\nRendering camera ' + str((ypos + 1) * (xpos + 1)) + ' of ' + str(n_cameras) + '.\n\n')
            bpy.data.scenes["Scene"].render.filepath = par.mainPath + '/render/' + par.trial + '/' + id_img
            bpy.ops.render.render( write_still=True )
            EXIF.write(id_img + '\t' + str(cam.location.x + 1000) + '\t' + str(cam.location.y + 1000) + '\t' + str(par.pos_cam_z) + '\t' + str(round(math.degrees(cam.rotation_euler.z ),2)) + '\t' + str(round(math.degrees(cam.rotation_euler.y),2)) + '\t' + str(round(math.degrees(cam.rotation_euler.x),2)) + '\n')
            #summing 1000 meters to stay away from negative values (for UTM reference)
            #yaw, pitch and roll are not correct for some reason
    EXIF.close()
   
##########################################################################################