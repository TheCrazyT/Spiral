import bpy
import mathutils
import math
from math import radians
from math import pow
from mathutils import Vector
 
# Define the coordinates of the vertices. Each vertex is defined by a tuple of 3 floats.
#coords=[(-1.0, -1.0, -1.0), (1.0, -1.0, -1.0), (1.0, 1.0 ,-1.0), \
#(-1.0, 1.0,-1.0), (0.0, 0.0, 1.0)]
coords = []
#H = 10
H = 1
G = 360
S = 8
F = 360*H
grow = 0.02
D = 100
growB = 0.02

#mat_rot = mathutils.Matrix.Rotation(radians(90),4,'X')
#v = Vector((1,1,0))
#v.rotate(mat_rot)
#print(v)
#print(v.x,v.y,v.z)


for z in range(0,F):
     mat_rot = mathutils.Matrix.Rotation(radians(z), 4, 'X')
     DN = D - growB*z
     y2 = math.cos(radians(z))*DN
     z2 = math.sin(radians(z))*DN
     v = Vector((1+grow*z,0,0))
     v.rotate(mat_rot)
     coords.append((v.x,y2+v.y,z2+v.z))
     v = Vector((1+grow*z,1,0))
     v.rotate(mat_rot)
     coords.append((v.x,y2+v.y,z2+v.z))
     v = Vector((0,1,0))
     v.rotate(mat_rot)
     coords.append((v.x,y2+v.y,z2+v.z))
     v = Vector((0,0,0))
     v.rotate(mat_rot)
     coords.append((v.x,y2+v.y,z2+v.z))
     #for i in range(0,G,S):
     #     x = math.cos(radians(i))*(1+grow*z)
     #     y = math.sin(radians(i))
     #     v = Vector((x,y,0))
     #     v.rotate(mat_rot)
     #     #print(v.x,v.y,v.z)
     #     coords.append((v.x,y2+v.y,z2+v.z))

 
# Define the faces by index numbers of its vertices. Each face is defined by a tuple of 3 or more integers.
# N-gons would require a tuple of size N.
#faces=[ (2,1,0,3), (0,1,4), (1,2,4), (2,3,4), (3,0,4)]
faces=[]
#GN=int(G/S)
GN=4
print(GN)
for i in range(0,GN-1):
     for x in range(0,F-1):
          faces.append((x*GN+i,x*GN+i+1,i+(x+1)*GN+1))
          faces.append((x*GN+i,i+(x+1)*GN+1,i+(x+1)*GN))
#          faces.append((x*GN+i,x*GN+i+1,i+(x+1)*GN+1,i+(x+1)*GN))
#for x in range(0,F-1):
#     faces.append((x*GN+GN,x*GN+1,(x+1)*GN+1,GN+(x+1)*GN))

me = bpy.data.meshes.new("PlanMesh")   # create a new mesh  
 
ob = bpy.data.objects.new("Plan", me)          # create an object with that mesh
bpy.context.collection.objects.link(ob)                # Link object to scene
 
# Fill the mesh with verts, edges, faces 
me.from_pydata(coords,[],faces)   # edges or faces should be [], or you ask for problems
me.update(calc_edges=True)    # Update mesh with new data
