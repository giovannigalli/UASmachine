
scenario = 1 ### change this from 0 to 5!!!!
heights = [60]

##########################################################################################

import bpy
import os
import numpy as np
import random
import math
import os

mainPath = "F:\\analysis\\UAVMachine"
os.chdir(mainPath)

#importing txt scripts
if len(bpy.data.texts.items()) == 0:
    files = sorted(os.listdir(mainPath))
    codes = [i for i in files if i.endswith('.py')]
    #codes.remove('main.py')
    for i in range(len(codes)):
        bpy.data.texts.load(mainPath + '/' + codes[i], internal = True)
        bpy.data.texts[codes[i]].use_fake_user = True
'''
#importing txt scripts        
files = sorted(os.listdir(mainPath))
codes = [i for i in files if i.endswith('.py')]
codes.remove('main.py')
for i in range(len(codes)):
    bpy.data.texts.load(mainPath + '/' + codes[i], internal = True)
    bpy.data.texts[codes[i]].use_fake_user = True
'''

import onCuda as oc
import setEnv as se
import easyFun as ef
import gcpMachine as gm
import UAVmachine as um
import sowingMachine as sm
import layout as lt

##########################################################################################

#setting units system
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1
        
##########################################################################################
        
#setting rendering motor
bpy.context.scene.render.engine="CYCLES"
#oc.cudaMachine() #out of memory for whole exp

##########################################################################################

class envs:
    #ENVIRONMENT (USER)
    mainPath = mainPath
    id_back = 'noon_grass_2k.hdr'
    rot_back_x = -4.3
    rot_back_y = 1.5
    rot_back_z = 0
    visible = False

par = envs
                        
#setting environment texture (lightning)
se.setEnvironmentTexture(par)

##########################################################################################

#setting up scenarios

os.chdir(mainPath + '\\R')
comb =['bpy.lattice.0.9.0.0005','bpy.lattice.0.3.0.05','bpy.lattice.0.6.0.05','bpy.lattice.0.6.0.0005','bpy.lattice.0.3.0.0005','bpy.lattice.0.9.0.05']
files = os.listdir()
os.chdir(mainPath)

#subparameters
rep = [i for i in files if i.startswith(comb[scenario])]
##########heights = [20,40,60]

for r in rep:
    trial = r[4:-4] #gets current trial and removes '.txt'
    for h in heights:
        height = h    
        ##########################################################################################
        #removing all objects prior to start
        ef.select("all")
        bpy.ops.object.delete(use_global=True)
        ##########################################################################################
        #user defined parameters
        class params:
            mainPath = mainPath
            #EXPERIMENTAL SETTINGS (USER)
            trial = trial
            id_crop = ('Maize.000','Maize.001','Maize.002','Maize.003','Maize.004','Maize.005','Maize.006','Maize.007')
            id_blend_crop = 'maize_packed_extreme_col_oneTex_OK.blend'
            id_gcp = ('1','2','3','4','5','6')
            id_blend_gcp = 'gcp_packed_code.blend'
            #FLIGHT SETTINGS (USER)
            pos_cam_z = height #height
            overlap = .8 #0.001 to .999
            camera = 'Phantom4' 
            #DESIGN INFO (USER) 
            spacing_row = .5
            spacing_plant = .33
            spacing_block_Y = spacing_row
            spacing_block_X = spacing_plant * 2
            soil = 0
            ##LAYOUTS (USER)
            #blocking layout
            layout = lt.layoutbase
            layout_block = layout.b2x7
            layout_gcp = layout.g2x3b3x3
            #ENVIRONMENT (USER)
            contour = True #border contour north and south
            #DESIGN INFO (MACHINE)
            info_par = np.loadtxt(mainPath + '/R/par.'+ trial + '.txt').tolist() #imports parameters
            n_treat_byblock = int(info_par[6])
            n_treat_row = int(info_par[4])
            n_plant = int(info_par[2])
            x_hat = float(info_par[7])
            sigma_e = math.sqrt(float(info_par[8]))
            n_row = n_treat_byblock * n_treat_row #added border
            n_block = layout_block.shape[0]
            blockX = (n_plant) * spacing_plant
            blockY = (n_row - 1)* (spacing_row)
            Xcoord = layout_block[:,0] * (blockX + spacing_block_X)
            Ycoord = layout_block[:,1] * (blockY + spacing_block_Y)
            trial = trial + '.' + str(height)
        par = params
        ##########################################################################################
        #creating dir for metadata
        try:
            os.mkdir(par.mainPath + '/meta/' + par.trial)
        except:
            pass
        ##########################################################################################
        #including ground control points
        sm.ceres(par)
        ##########################################################################################
        #including ground control points                 
        gm.gcpDraw(par)
        ##########################################################################################
        #importing soil
        #bpy.ops.import_scene.obj(filepath= mainPath + '/obj/soil.obj') #imports object
        #bpy.ops.mesh.primitive_plane_add(location=(0, 0, (par.soil-0.001)))
        #bpy.ops.transform.resize(value=(500, 500, 0))
        bpy.ops.wm.append(filename = 'Soil', directory = par.mainPath + '/blends/cycles/' + 'soil_procedural.blend' + '/Object/')
        
        ##########################################################################################
        
        #creating flight plan and taking cameras
        um.UAVfly(par)
        
        ##########################################################################################
