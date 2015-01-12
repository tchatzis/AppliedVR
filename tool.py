 #Imports
import viz
import vizact
import viztask
import vizshape
import vizinfo
import functions
#reload( functions )

viz.setMultiSample( 4 )
viz.fov( 60 )
viz.collision( viz.ON )
viz.mouse( viz.OFF )
viz.go()

#Info Panel
modePanel = vizinfo.InfoPanel( 'Camera View', title = 'Actions', align = viz.ALIGN_LEFT_TOP, icon = False )
far = modePanel.addLabelItem( 'Far' ,viz.addRadioButton( 'ViewMode' ) )
close = modePanel.addLabelItem( 'Close' ,viz.addRadioButton( 'ViewMode' ) )
top = modePanel.addLabelItem( 'Top', viz.addRadioButton( 'ViewMode' ) )
around = modePanel.addLabelItem( 'Around', viz.addRadioButton( 'ViewMode' ) )
far.set( True )

#Variables
EYEHEIGHT = 1.82
CAPTURE_VIDEO = False
FAR_POSITION = [ 0, EYEHEIGHT, -20 ]
CLOSE_POSITION = [ 0, EYEHEIGHT, -3 ]
TOP_POSITION = [ 0, 5, -2 ]
SPEED = 10
START_ANGLE = 0

#Camera
camera = viz.MainView
camera.setPosition( FAR_POSITION )
camera.getHeadLight().disable()
camera.gravity ( 0 )
camera.collision( viz.OFF )

#Environment
origin = viz.addGroup( parent = viz.WORLD )
origin.setPosition( 0, 0, 0 )
day = viz.add( 'sky_day.osgb' )
ground = vizshape.addPlane( size = ( 30, 30 ), axis = vizshape.AXIS_Y, cullFace = True, color = ( 0.353, 0.412, 0.224 ), lighting = False )
ground.setPosition( 0, 0, 0 )

#Actions
spinX = vizact.spin( 1, 0, 0, -90, viz.FOREVER )
spinZ = vizact.spinTo( euler = ( 0, 0, -90 ), time = 3 )
moveToY = vizact.moveTo( [ 0, -4, 0 ], time = 8 )

#Lights
dLight = functions.directionalLight( color = [ 1, 1, 1 ], angle = [ 0, 75, 0 ], intensity = 0.5 )
pLight = functions.pointLight( color = [ 0.9, 0.9, 1 ], angle = 180, intensity = 0.25, position = [ 0, 10, -1 ] )

#Rig
rig = viz.add( 'models/rig.fbx' )

#Tool
tool = viz.add( 'models/tool.fbx' )
tool.setPosition( [ 0, 2, 0 ] )
tool.setEuler( [ 0, 0, 90 ] )
tool.addAction( spinX, 0 )

#Setup button click events
vizact.onbuttondown( close, functions.move_camera, camera, CLOSE_POSITION, tool, 0, SPEED )
vizact.onbuttondown( far, functions.move_camera, camera, FAR_POSITION, tool, 0, SPEED )
vizact.onbuttondown( top, functions.move_camera, camera, TOP_POSITION, tool, 0, SPEED )
vizact.onbuttondown( around, functions.revolve_camera, camera, tool, START_ANGLE, 1 )

#Timeline
def timeline():
   functions.move_camera( camera, CLOSE_POSITION, tool, EYEHEIGHT, SPEED )
   tool.addAction( moveToY, 1 )

#Space Bar to Start
vizact.onkeydown( ' ', viztask.schedule, timeline )