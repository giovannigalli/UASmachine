##########################################################################################

import bpy

##########################################################################################

#easy access functions
def duplicate():
    bpy.ops.object.duplicate()

def translate(x,y,z):
    bpy.ops.transform.translate(value=(x,y,z))

def rotate(value,x,y,z):
    bpy.ops.transform.rotate(value=value, axis=(x,y,z))
    
def resize(vx,vy,vz,cx,cy,cz):
    bpy.ops.transform.resize(value=(vx,vy,vz), constraint_axis=(cx,cy,cz))

def select(what): #deselecting all objects
    if what == "none":
        bpy.ops.object.select_all(action='DESELECT')
    if what == "all":
        bpy.ops.object.select_all(action='SELECT')

##########################################################################################
