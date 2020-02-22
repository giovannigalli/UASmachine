##########################################################################################

import bpy
import numpy as np
import random
import math
import os
import easyFun as ef
import modifier as md

##########################################################################################

def ceres(par):
    file_crop = par.mainPath + '/blends/cycles/' + par.id_blend_crop + '/Object/' #path to the main object
    frame = np.loadtxt(par.mainPath + '/R/bpy.' + par.trial[:-3] + '.txt') #imports phenotypes
    #writing coordinate file
    IND = open(par.mainPath + '/meta/' + par.trial + '/' + par.trial + '.IND.txt', 'w')
    IND.write("#Label\tRow\tCol\tEasting/X/Longitude\tNorthing/Y/Latitude\tZ/Altitude" + '\n')
    #further variables
    n_total_plants = str(par.n_block*par.n_row*par.n_plant)
    n_plant_byblock = par.n_plant*par.n_row
    #importing main object
    for nn, pl in enumerate(par.id_crop):
        bpy.ops.wm.append(filename = pl, directory = file_crop)
    #loop through blocks
    for b in range(par.n_block):
        centery = par.Ycoord[b]
        centerx = par.Xcoord[b]
        curBlock = frame[np.where(frame[:,0] == b)]
        #loop through grid y axis
        for row in range(0, par.n_row, 1):
            jpos = row * (1 / (par.n_row - 1))
            y = + par.blockY / 2 - jpos * par.blockY
            curRow = curBlock[np.where(curBlock[:,2] == row)]
            #loop through grid x axis
            for k in range(0, par.n_plant):
                kpos = k * (1 / (par.n_plant))
                x = - par.blockX / 2 + kpos * par.blockX + (par.spacing_plant/2) #last part added to adjust to center
                #duplicating objects
                curMain = random.choice(par.id_crop)
                bpy.data.objects[curMain].select = True
                bpy.context.scene.objects.active = bpy.data.objects[curMain]
                bpy.ops.object.duplicate()
                #translating objects
                ef.translate(centerx + x, centery + y, par.soil) #moves the object to position
                name = "b" + str(b) + "_row" + str(row) + "_t" + str(int(curRow[k,3])) + "_p" + str(k)
                #rotating objects
                ef.rotate(random.randint(0,364), False, False, True)           ###change to radians
                #Resizing objects
                bpy.ops.transform.resize(value=(curRow[k,6]*0.85, curRow[k,6]*0.85, curRow[k,6]), constraint_axis=(True, True, True))
                #applying modifiers (wave and deform)
                md.modifier()
                #verbose
                print('Individual ' + str(int(curRow[k,11])) + ' of ' + n_total_plants + ' imported.\n')
                #writing text file
                IND.write(name + '\t' + str(row) + '\t' + str(b) + '\t' + str(float(centerx + x +  1000)) + '\t' +  str(float(centery + y + 1000)) + '\t' + str(par.soil) + '\n') #write IND coordinates
                ef.select('none')
        
        #joining objects from the same block
        list_tojoin = bpy.data.objects[-(n_plant_byblock):]
        for i in range(n_plant_byblock):
            list_tojoin[i].select = True
        bpy.context.scene.objects.active = list_tojoin[0]
        bpy.ops.object.join()
        ef.select('none')
    IND.close()
    
    #adding border if required
    if par.contour == True:
        
        print('Importing borders.')
        
        #UAV goes from left bottom to right top
        Xmax = max(par.Xcoord.tolist())[0]
        Xmin = min(par.Xcoord.tolist())[0]
        Ymax = max(par.Ycoord.tolist())[0]
        Ymin = min(par.Ycoord.tolist())[0]
        bord_xleft = Xmin - (par.blockX/2) + par.spacing_plant/2
        bord_xright = Xmax + (par.blockX/2) - par.spacing_plant/2
        bord_y = (Ymax + (par.blockY/2) + par.spacing_row, Ymin - (par.blockY/2) - par.spacing_row)
        n_plants_singlebord = int((abs(bord_xleft) + (bord_xright))/par.spacing_plant) + 1
        
        for s in range(2):
            y = bord_y[s]
            bord_xleft = Xmin - (par.blockX/2)
            for m in range(n_plants_singlebord):
                #duplicating objects
                curMain = random.choice(par.id_crop)
                bpy.data.objects[curMain].select = True
                bpy.context.scene.objects.active = bpy.data.objects[curMain]
                bpy.ops.object.duplicate()
                #moves the object to position
                ef.translate((bord_xleft + (par.spacing_plant/2)), y, par.soil)
                #rotating objects
                ef.rotate(random.randint(0,364), False, False, True)           ###change to radians
                #Resizing objects
                error = random.normalvariate(0, par.sigma_e)
                bpy.ops.transform.resize(value = ((par.x_hat + error)*0.85, (par.x_hat + error)*0.85, (par.x_hat + error)), constraint_axis=(True, True, True))
                bord_xleft = bord_xleft + par.spacing_plant
                ef.select('none')
        
        #joining objects from the same block
        list_tojoin = bpy.data.objects[-(n_plants_singlebord*2):]
        for i in range(n_plants_singlebord*2):
            list_tojoin[i].select = True
        bpy.context.scene.objects.active = list_tojoin[0]
        bpy.ops.object.join()
        ef.select('none')
    
    #deleting main object
    for nn, pl in enumerate(par.id_crop):
        bpy.data.objects[pl].select = True
        bpy.ops.object.delete()        
    
##########################################################################################