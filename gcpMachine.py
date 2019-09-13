##########################################################################################

import bpy
import easyFun as ef

##########################################################################################

def gcpDraw(par):
    file_gcp = par.mainPath + '/blends/cycles/' + par.id_blend_gcp + '/Object/' #path to gcp
    for nn, pl in enumerate(par.id_gcp):
        bpy.ops.wm.append(filename = pl, directory = file_gcp)
    Xcoord_gcp = par.layout_gcp[:,0] * (1.5 * par.blockX + par.spacing_block_X)
    Ycoord_gcp = par.layout_gcp[:,1] * (1.5 * par.blockY + par.spacing_block_Y)
    #writing coordinate file
    GCP = open(par.mainPath + '/meta/' + par.trial + '/' + par.trial + '.GCP.txt', 'w')
    GCP.write("#Label\tEasting/X/Longitude\tNorthing/Y/Latitude\tZ/Altitude" + '\n')
    ef.select("none")
    for i_gcp in range(par.layout_gcp.shape[0]):
        centery = int(Ycoord_gcp[i_gcp])
        centerx = int(Xcoord_gcp[i_gcp])
        curMain = par.id_gcp[i_gcp]
        bpy.data.objects[curMain].select = True
        bpy.context.scene.objects.active = bpy.data.objects[curMain]
        ef.translate(centerx, centery, par.soil) #moves the object to position
        GCP.write('target ' + curMain + '\t' + str(centerx +  1000) + '\t' +  str(centery +  1000) + '\t' + str(par.soil) + '\n')
        ef.select("none")
    GCP.close()

#gcpDraw(par)