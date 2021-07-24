

import bpy
import mathutils

class BlenderHelper_CenterObject:

    def __init__(self):
        print('BlenderHelper_CenterObject ready')

    def ResetObject(self):
        self.cursor.location = self.original_Object_locationvec
        self.act_obj.location = self.original_Object_locationvec - self.cursorDiff
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    def CenterObject(self, Object_, SnapToFloor):
        #Get active object    
        self.act_obj = Object_
            
        #Get self.cursor
        self.cursor = bpy.context.scene.cursor

        #Get original self.cursor location
        original_cursor_location = (self.cursor.location[0], self.cursor.location[1], self.cursor.location[2])  
        self.cursor.location = self.act_obj.location 
        original_Object_location = (self.cursor.location)   
        self.original_Object_locationvec = mathutils.Vector(self.cursor.location)
        
        print("original_Object_location", original_Object_location)
        #Make sure origin is set to geometry for self.cursor z move 
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')  

        #Set self.cursor location to object location
        self.cursor.location = self.act_obj.location
        if SnapToFloor:
            #Get self.cursor z move  
            half_act_obj_z_dim = self.act_obj.dimensions[2] / 2
            self.cursor_z_move = self.cursor.location[2] - half_act_obj_z_dim   
            
            #Move self.cursor to bottom of object
            self.cursor.location[2] = self.cursor_z_move
        self.cursorDiff = self.original_Object_locationvec - mathutils.Vector(self.cursor.location)
        print("self.cursor.location", self.cursor.location)
        print("self.cursor Diff", self.cursorDiff)
        #Set origin to self.cursor
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        

        #Assuming you're wanting object center to grid
        bpy.ops.object.location_clear(clear_delta=False)


def Test():
    
    BlenderHelper_CenterObject_ = BlenderHelper_CenterObject()           
    BlenderHelper_CenterObject_.CenterObject(bpy.context.active_object,True)
    bpy.ops.export_scene.fbx(filepath= "C:/temp/usd/t6/GG_New.fbx", use_selection =True)
    BlenderHelper_CenterObject_.ResetObject()
    
if __name__ == '__main__':
    Test()