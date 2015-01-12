import viz
import vizact
import vizshape
import projector
import math

viz.setMultiSample(4)
viz.fov(60)
viz.go()

#import vizinfo
#vizinfo.InfoPanel()

#Move the viewpoint
viz.MainView.move([0,1,-3])

#Add a wall
wall = vizshape.addQuad(size=[10,10],pos=[0,5,5],color=viz.GRAY)

#Add a ground
ground = viz.addChild('ground.osgb')

#Add a spinning pyramid
pyramid = vizshape.addPyramid(base=[0.75,0.75],height=0.75,pos=[-1.25,2,3.5])
pyramid.addAction(vizact.spin(0,1,0,15))

#Add a spinning cube
cube = vizshape.addCube(size=0.75,pos=[1.25,2.4,3.5])
cube.addAction(vizact.spin(1,1,0,15))

#add a torus moving back and forth
torus = vizshape.addTorus(radius=0.5,axis=vizshape.AXIS_Z,pos=[3,1,3.5])
torus.addAction(vizact.sequence([vizact.moveTo(pos=[-3,1,3.5],time=5),vizact.moveTo(pos=[3,1,3.5],time=5)], viz.FOREVER))

#Add a video texture which will be the texture for the projector
video = viz.addVideo('mona.mpg')
video.loop()
video.play()

#Create a projector using the video texture
proj = projector.add(video)

#Translate the projector to the center of the room
proj.setPosition([0,1.3,0])

#Set the projectors fov
proj.fov(30,1)

#Make the wall be affected by the projector
proj.affect(wall)
#Make the ground be affected by the projector
proj.affect(ground)
#Make the pyramid be affected by the projector
proj.affect(pyramid)
#Make the cylinder be affected by the projector
proj.affect(cube)
#Make the torus be affected by the projector
proj.affect(torus)

#Create a yaw variable for the projector
proj.yaw = 0

def mytimer():

    #Have the projector look around in a circle
    proj.yaw += 1

    x = math.sin(viz.radians(proj.yaw))
    y = math.cos(viz.radians(proj.yaw))

    proj.lookAt([x,1.3+y,5])

vizact.ontimer(0, mytimer)