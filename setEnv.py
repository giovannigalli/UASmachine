##########################################################################################

import bpy
import math

##########################################################################################

def setEnvironmentTexture(par):

    # Add Environment-texture to image collection
    bpy.ops.image.open(filepath = par.mainPath + '/tex/' + par.id_back, directory = par.mainPath + '/tex/')
    
    # Add nodes
    bpy.data.worlds['World'].use_nodes = True
    texEnv = bpy.data.worlds['World'].node_tree.nodes.new(type='ShaderNodeTexEnvironment')
    nodeMap = bpy.data.worlds['World'].node_tree.nodes.new(type='ShaderNodeMapping')
    texCoord = bpy.data.worlds['World'].node_tree.nodes.new(type='ShaderNodeTexCoord')
    background = bpy.data.worlds['World'].node_tree.nodes['Background']

    # Link Nodes
    links = bpy.data.worlds['World'].node_tree.links
    links.new(texCoord.outputs[0], nodeMap.inputs[0])
    links.new(nodeMap.outputs[0], texEnv.inputs[0])
    links.new(texEnv.outputs[0], background.inputs[0])

    bpy.data.worlds['World'].node_tree.nodes['Environment Texture'].image = bpy.data.images[par.id_back]
    bpy.data.worlds['World'].node_tree.nodes["Background"].inputs[1].default_value = 2
    bpy.data.worlds['World'].light_settings.use_ambient_occlusion = True
    
    #setting noon (moving sun nadir) check if needed
    bpy.data.worlds['World'].node_tree.nodes['Mapping'].rotation.x = math.radians(par.rot_back_x)
    bpy.data.worlds['World'].node_tree.nodes['Mapping'].rotation.y = math.radians(par.rot_back_y)
    bpy.data.worlds['World'].node_tree.nodes['Mapping'].rotation.z = math.radians(par.rot_back_z)
    
    #setting visibility of background
    bpy.data.worlds['World'].cycles_visibility.camera = par.visible

##########################################################################################