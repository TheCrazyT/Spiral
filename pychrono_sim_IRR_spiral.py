import math
import pychrono.core as chrono
import pychrono.irrlicht as chronoirr


# The path to the Chrono data directory containing various assets (meshes, textures, data files)
# is automatically set, relative to the default location of this demo.
# If running from a different directory, you must change the path to the data directory with: 
chrono.SetChronoDataPath(r'C:\Users\crazy\AppData\Local\Programs\ProjectChrono\data/')

# ---------------------------------------------------------------------
#
#  Create the simulation system and add items
#

my_system = chrono.ChSystemNSC()


# Set the default outward/inward shape margins for collision detection,
# this is epecially important for very large or very small objects.
chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

# Maybe you want to change some settings for the solver. For example you
# might want to use SetSolverMaxIterations to set the number of iterations
# per timestep, etc.

#my_system.SetSolverType(chrono.ChSolver.Type_BARZILAIBORWEIN) # precise, more slow
my_system.SetSolverMaxIterations(70)



# Create a contact material (surface property)to share between all objects.
# The rolling and spinning parameters are optional - if enabled they double
# the computational time.
brick_material = chrono.ChMaterialSurfaceNSC()
brick_material.SetFriction(0.5)
brick_material.SetDampingF(0.2)
brick_material.SetCompliance (0.0000001)
brick_material.SetComplianceT(0.0000001)
# brick_material.SetRollingFriction(rollfrict_param)
# brick_material.SetSpinningFriction(0)
# brick_material.SetComplianceRolling(0.0000001)
# brick_material.SetComplianceSpinning(0.0000001)



# Create the set of bricks in a vertical stack, along Y axis

nbricks_on_x = 1
nbricks_on_y = 240

size_brick_x = 0.25
size_brick_y = 0.12
size_brick_z = 0.12
density_brick = 1000
density_sphere = 5000
mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z;
mass_sphere = density_sphere * size_brick_x * size_brick_y * size_brick_z;

last_body_brick = None


ground = chrono.ChBody()
#ground.SetIdentifier(-1)
ground.SetBodyFixed(True)
#ground.SetCollide(False)

ground_box = chrono.ChBoxShape()
ground_box.Pos.Set(0,-3,0)
ground_box.GetBoxGeometry().Size = chrono.ChVectorD(5,0.5,5)

ground.AddAsset(ground_box)
texture = chrono.ChTexture()
texture.SetTextureFilename(chrono.GetChronoDataFile("textures/checker1.png"))
ground.AddAsset(texture)
ground.SetRot(chrono.Q_ROTATE_Y_TO_Z)

my_system.Add(ground)

#for ix in range(0,nbricks_on_x):
ix = 0
D = 2.0
# create it
body_brick = chrono.ChBody()
# Collision shape
body_brick.GetCollisionModel().ClearModel()
# set initial position
#body_brick.SetPos(chrono.ChVectorD(ix*size_brick_x, W, V ))
#body_brick.SetRot(quat)
# set mass properties
body_brick.SetMass(mass_brick)
for iy in range(0,nbricks_on_y):
    D -= 0.005
    size_brick_x += 0.03
    r = iy * 2.0
    V = math.sin(r*math.pi/180.0) * D
    W = math.cos(r*math.pi/180.0) * D
    
    quat = chrono.ChQuaternionD()
    quat.Q_from_AngAxis(r * chrono.CH_C_DEG_TO_RAD, chrono.ChVectorD(1,0,0))
    mat = chrono.ChMatrix33D()
    mat.Set_A_quaternion(quat)


    SIZEBRICK = (size_brick_x/2, size_brick_y/2, size_brick_z/2)
    POSBRICK = (ix*size_brick_x-size_brick_x/2, W, V)
    body_brick.GetCollisionModel().AddBox(brick_material, *SIZEBRICK , chrono.ChVectorD(*POSBRICK), mat)
    
    SIZELEFTBORDER = (0.12, 0.12*3, 0.12)
    SIZERIGHTBORDER = (0.12, 0.12*3, 0.12)
    POSLEFTBORDER = (0, W, V)
    POSRIGHTBORDER = (ix*size_brick_x-size_brick_x, W, V)
    
    #Left border
    body_brick.GetCollisionModel().AddBox(brick_material, *SIZELEFTBORDER, chrono.ChVectorD(*POSLEFTBORDER), mat)
    
    #Right border
    body_brick.GetCollisionModel().AddBox(brick_material, *SIZERIGHTBORDER, chrono.ChVectorD(*POSRIGHTBORDER), mat)

    #Left border
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.Pos.Set(*POSLEFTBORDER)
    body_brick_shape.Rot = mat
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(*SIZELEFTBORDER)
    if iy%2==0 :
        body_brick_shape.SetColor(chrono.ChColor(0.0, 0.0, 1.0))
    else:
        body_brick_shape.SetColor(chrono.ChColor(0.0, 1.0, 0.0))
    body_brick.GetAssets().push_back(body_brick_shape)

    #Right border
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.Pos.Set(*POSRIGHTBORDER)
    body_brick_shape.Rot = mat
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(*SIZERIGHTBORDER)
    if iy%2==0 :
        body_brick_shape.SetColor(chrono.ChColor(0.0, 0.0, 1.0))
    else:
        body_brick_shape.SetColor(chrono.ChColor(0.0, 1.0, 0.0))
    body_brick.AddAsset(body_brick_shape)

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.Pos.Set(*POSBRICK)
    body_brick_shape.Rot = mat
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(*SIZEBRICK)
    if iy%2==0 :
        body_brick_shape.SetColor(chrono.ChColor(0.0, 0.0, 1.0))
    else:
        body_brick_shape.SetColor(chrono.ChColor(0.0, 1.0, 0.0))
    body_brick.AddAsset(body_brick_shape)
    #if not last_body_brick is None:
    #    mlink = chrono.ChLinkLockLock()
    #    # the coordinate system of the constraint reference in abs. space:
    #    mframe = chrono.ChFrameD(chrono.ChVectorD(0.1,0.5,0))
    #    # initialize the constraint telling which part must be connected, and where:
    #    mlink.Initialize(last_body_brick,body_brick, chrono.CSYSNORM)#, mframe)
    #    my_system.Add(mlink)
    #last_body_brick = body_brick
body_brick.GetCollisionModel().BuildModel()
body_brick.SetRot(chrono.Q_ROTATE_Z_TO_X)


#body_brick.SetShowCollisionMesh(True)
#body_brick.SetRot(chrono.Q_ROTATE_Y_TO_Z)
body_brick.SetCollide(True)
texture = chrono.ChTexture()
texture.SetTextureFilename(chrono.GetChronoDataFile("textures/checker2.png"))
body_brick.AddAsset(texture)

#body_brick.SetBodyFixed(True)


#body_brick = chrono.ChBodyEasyCylinder(1, 1, 1)
#body_brick.SetPos(chrono.ChVectorD(0, 0, 1))
#body_brick.SetRot(chrono.Q_ROTATE_Y_TO_Z)
#body_brick.SetBodyFixed(True)

my_system.Add(body_brick)

rev = chrono.ChLinkLockRevolute()
rev.Initialize(body_brick, ground, chrono.ChCoordsysD(chrono.ChVectorD(0, 0, 1)))

my_system.AddLink(rev)





rad = 0.05
for i3 in range(0,6):
    for i1 in range(0,24):
        for i2 in range(0,10):
            body_sphere = chrono.ChBody()
            body_sphere_shape = chrono.ChSphereShape()
            body_sphere_shape.GetSphereGeometry().rad = rad
            #body_sphere_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x/2, size_brick_y/2, size_brick_z/2)
            body_sphere.SetPos(chrono.ChVectorD(-1+i1*(2*rad), i3*(2*rad), 1+i2*(2*rad) ))
            #body_sphere.SetMass(mass_sphere)
            #body_sphere.SetInertiaXX(chrono.ChVectorD(inertia_brick,inertia_brick,inertia_brick))       
            body_sphere.GetCollisionModel().ClearModel()
            body_sphere.GetCollisionModel().AddSphere(brick_material, rad)
            body_sphere.GetCollisionModel().BuildModel()
            body_sphere.SetCollide(True)
            #body_sphere.SetBodyFixed(True)
            body_sphere_shape.SetColor(chrono.ChColor(1.0, 0.0, 0.0))
            body_sphere.AddAsset(body_sphere_shape)
            body_sphere.AddAsset(chrono.ChColorAsset(0.6, 0, 0))
            my_system.Add(body_sphere)

import numpy as np
import matplotlib.pyplot as plt

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)        
        #update plot label/title
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1


line1 = []
size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = np.zeros(len(x_vec))
i = 0

NOGUI = True

if NOGUI:
    my_system.SetChTime(0)
    while True:
        my_system.DoStepDynamics(0.01)
        rv = body_brick.GetRotAxis()
        y_vec[-1] = rv.x
        line1 = live_plotter(x_vec,y_vec,line1)
        y_vec = np.append(y_vec[1:],0.0)
else:
    # ---------------------------------------------------------------------
    #
    #  Create an Irrlicht application to visualize the system
    #

    myapplication = chronoirr.ChIrrApp(my_system, 'PyChrono example', chronoirr.dimension2du(1024,768))
    myapplication.AddTypicalSky()
    myapplication.AddTypicalLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
    myapplication.AddTypicalCamera(chronoirr.vector3df(2,0,6.0))
    myapplication.AddLightWithShadow(chronoirr.vector3df(-2,4,2),    # point
                                     chronoirr.vector3df(0,0,0),    # aimpoint
                                     9,                 # radius (power)
                                     1,9,               # near, far
                                     30)                # angle of FOV

                # ==IMPORTANT!== Use this function for adding a ChIrrNodeAsset to all items
                # in the system. These ChIrrNodeAsset assets are 'proxies' to the Irrlicht meshes.
                # If you need a finer control on which item really needs a visualization proxy in
                # Irrlicht, just use application.AssetBind(myitem); on a per-item basis.

    myapplication.AssetBindAll();

                # ==IMPORTANT!== Use this function for 'converting' into Irrlicht meshes the assets
                # that you added to the bodies into 3D shapes, they can be visualized by Irrlicht!

    myapplication.AssetUpdateAll();

                # If you want to show shadows because you used "AddLightWithShadow()'
                # you must remember this:
    myapplication.AddShadowAll();
    myapplication.SetTimestep(0.001)
    myapplication.SetTryRealtime(True)

    # ---------------------------------------------------------------------
    #
    #  Run the simulation
    #
    while(myapplication.GetDevice().run()):
        i += 1
        #V += 1
        #if (V//20)% 2 == 0:
        #    quat = chrono.ChQuaternionD()
        #    quat.Q_from_AngAxis(45 * chrono.CH_C_DEG_TO_RAD, chrono.ChVectorD(1,0,0))
        #    mat = chrono.ChMatrix33D()
        #    mat.Set_A_quaternion(quat)
        #    ground.SetRot(quat)
        #else:
        #    quat = chrono.ChQuaternionD()
        #    quat.Q_from_AngAxis(-45 * chrono.CH_C_DEG_TO_RAD, chrono.ChVectorD(1,0,0))
        #    mat = chrono.ChMatrix33D()
        #    mat.Set_A_quaternion(quat)
        #    ground.SetRot(quat)

        myapplication.BeginScene()
        myapplication.DrawAll()
        for substep in range(0,5):
            myapplication.DoStep()
        #print(body_brick.GetRotAxis())
        rv = body_brick.GetRotAxis()
        y_vec[-1] = rv.x
        line1 = live_plotter(x_vec,y_vec,line1)
        y_vec = np.append(y_vec[1:],0.0)
        myapplication.EndScene()


