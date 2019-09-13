import bpy
import random
import math

def modifier():
    #adding simple deform modifier
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    bpy.context.object.modifiers["SimpleDeform"].limits[1] = random.uniform(.1,1)
    bpy.context.object.modifiers["SimpleDeform"].angle = math.radians(random.uniform(-140,140))
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier = "SimpleDeform" )
    #adding wave modifier
    bpy.ops.object.modifier_add(type='WAVE')
    bpy.context.object.modifiers["Wave"].start_position_x = random.uniform(1,3)
    bpy.context.object.modifiers["Wave"].start_position_y = random.uniform(1,30)
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier = "Wave" )
