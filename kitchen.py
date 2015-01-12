 #Imports
import viz
import vizact
import vizshape
import viztask
#User Defined
import functions
#reload( functions )

viz.setMultiSample( 4 )
viz.fov( 60 )
viz.go()
viz.collision( viz.ON )
viz.mouse( viz.OFF )
#vizshape.addAxes()

#Variables
EYEHEIGHT = 1.5
VIDEO_CAPTURE = False
SPEED = 1

#Sky
day = viz.add( 'sky_day.osgb' )

#Lights
dLight = functions.directionalLight( color = [ 1, 1, 1 ], angle = [ 0, 120, 0 ], intensity = 0.5 )

pLight = functions.pointLight( color = [ 1, 1, 1 ], angle = 180, intensity = 0.7, position = [ 0, 2.5, 0 ] )
pLight.position( 0, 1, 0 )

#sLight = functions.spotLight( color = [ 1, 0, 0 ], angle = 15, intensity = 1, exponent = 2, position = [ 0, 2.5, -8 ] )
#sLight.position( 0, 1, 0 )
#sLight.direction( 0, 0, 1 )

#Floor
floor = viz.addChild( 'ground.osgb' )
floor.collidePlane()

#Kitchen
viz.setOption( 'viz.model.apply_collada_scale', 1 )
kitchen = viz.add( 'kitchen.dae' )
functions.origin_object( kitchen )
kitchen.setEuler( [ 0, 0, 0 ], viz.REL_LOCAL )

#Mirror
mirror = viz.addTexQuad()
mirror.setScale( [ 1.2, 1.4, 0.1 ] )
mirror.setPosition( [ -0.95, 1.65, 2.9 ] )
functions.addReflection( mirror )

#Glass
#glass = viz.addTexQuad()
#glass.alpha( 0.2 )
#glass.color( 0, 0, 0 )
#glass.appearance( viz.TEXMODULATE )
#glass.setScale( [ 2, 2.6, 0.1 ] )
#glass.setPosition( [ 1, 1.2, 2 ] )
#functions.addReflection( glass )

#Subject
subject = viz.addAvatar( 'vcc_female.cfg', pos = ( -1, 0, 2 ), euler = ( 0, 0, 0 ) )
subject.state( 9 )

#Friend
friend = viz.addAvatar( 'vcc_male.cfg', pos = ( 0, 0, -3 ), euler = ( 0, 0, 0 ) )
friend.state( 14 )
friend.setScale( 1, 1, 1 )

#Coach
coach = viz.addAvatar( 'vcc_male2.cfg', pos = ( 1.2, 0, 2 ), euler = ( 270, 0, 0 ) )
coach.state( 4 )

#Camera
camera = viz.MainView
camera.getHeadLight().disable()
camera.gravity ( 0 )
camera.eyeheight( EYEHEIGHT )
camera.move( [ 3.5, 0.5, 0 ] )
camera.move( [ 0, 0, -3.5 ] )
camera.lookAt( subject.getPosition() )
camera.collision( viz.OFF )

#Timeline
def timeline():
	if VIDEO_CAPTURE is True:
		viz.setOption( 'viz.AVIRecorder.maxWidth', 800 )
		viz.setOption( 'viz.AVIRecorder.maxHeight', 450 )
		viz.setOption( 'viz.AVIRecorder.fps', '29.97' )
		viz.window.startRecording( 'VIDEO_CAPTURE/kitchen.avi' )

	#Move Camera 0:00:00:00 - 0:00:02:00
	functions.move_camera( camera, [ 0, EYEHEIGHT, 0 ], subject, EYEHEIGHT, SPEED )

	#Start Video on Mirror 0:00:02:00 - 0:00:10:00
	yield viztask.waitTime( 8 )
	functions.media_play( 'degasser.mpg', 12, mirror )

	#Move into Mirror 0:00:10:00 - 0:00:12:00
	yield viztask.waitTime( 2 )
	functions.change_state( subject, 1 )
	functions.move_camera( camera, [ -1, EYEHEIGHT, 2.1 ], mirror, 0, SPEED )

	#Move back to origin 0:00:12:00 - 0:00:30:00
	yield viztask.waitTime( 18 )
	functions.move_camera( camera, [ 0, EYEHEIGHT, 0 ], mirror, 0, SPEED )

	#Clap at end of Video 0:00:30:00 - 0:00:31:00
	yield viztask.waitTime( 1 )
	functions.temp_state( subject, 4 )

	#Change back to Mirror
	functions.addReflection( mirror )

	#Quit
	yield viztask.waitTime( 9 )

	if VIDEO_CAPTURE is True:
		viz.window.stopRecording()

	viz.quit()

vizact.onkeyup( ' ', viztask.schedule, timeline )
