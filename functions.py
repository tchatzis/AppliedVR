# imports
import viz
import vizmat
import vizact
import viztask
import math

#Variables
STATE = 0;
REFLECT_MASK = viz.addNodeMask()

def directionalLight( color = [ 1, 1, 1 ], angle = [ 0, 90, 0 ], intensity = 1 ):
	object = viz.addLight()
	object.color( color )
	object.setEuler( angle )
	object.intensity( intensity )
	return object

def pointLight( color = [ 1, 1, 1 ], angle = 180, intensity = 1, position = [ 0, 0, -10 ] ):
	object = viz.addLight()
	object.enable()
	object.color( color )
	object.spread( angle )
	object.intensity( intensity )
	object.setPosition( position )
	return object

def spotLight( color = [ 1, 1, 1 ], angle = 45, intensity = 2, exponent = 10, position = [ 0, 0, 0 ] ):
	object = viz.addLight()
	object.position( position )
	object.color( color )
	object.spread( angle )
	object.intensity( intensity )
	object.spotexponent( exponent )
	object.setPosition( [ position[ 0 ], position[ 1 ] + 1, position[ 2 ] ] )
	return object

def origin_object( object ):
	object_box = object.getBoundingBox()
	object.setPosition( [ -object_box.xmin, -object_box.ymin, -object_box.zmin ], viz.REL_LOCAL )
	object.setPosition( [ -object_box.width / 2, -object_box.ymin, -object_box.depth / 2 ], viz.REL_LOCAL )
	return object

def increment_state( avatar ):
	"""Loops through all of the avatar states

	vizact.onkeydown( ' ', functions.increment_state, coach )"""

	global STATE

	if STATE > 15:
		STATE = 0

	STATE = STATE + 1

	avatar.state( STATE )
	return avatar

def change_state( avatar, state ):
	"""Change avatar to given state

	vizact.onkeydown( '7', functions.change_state, coach, 7 )"""

	if state > 0 and state < 16:
		avatar.state( state )
		return avatar
	else:
		pass

def temp_state( avatar, state ):
	"""Change avatar to given state

	vizact.onkeydown( '7', functions.change_state, coach, 7 )"""

	if state > 0 and state < 16:
		avatar.execute( state )
		return avatar
	else:
		pass

def addReflection( object, eye = viz.BOTH_EYE, resolution=[ 1024, 1024 ] ):
	"""Object shows reflection"""

	mat = viz.Matrix()
	mat.setPosition( object.getPosition( viz.ABS_GLOBAL ) )
	mat.setEuler( -180, 0, 0 )

	pos = viz.Vector( mat.getPosition() )

	dir = viz.Vector( mat.getForward() )
	dir.normalize()

	quat = mat.getQuat()

	tex = viz.addRenderTexture()

	#Create render node for rendering reflection
	lens = viz.addRenderNode( size = resolution )
	lens.attachTexture( tex )
	lens.setInheritView( True, viz.POST_MULT )
	lens.enable( viz.FLIP_POLYGON_ORDER, op = viz.OP_OVERRIDE )
	lens.setCullMask( REFLECT_MASK )
	lens.renderToEye( eye )

	object.renderToEye( eye )
	object.renderToAllRenderNodesExcept( [ lens ] )

	if eye == viz.LEFT_EYE:
		lens.disable( viz.RENDER_RIGHT )
		object.setMask( REFLECT_MASK | viz.RIGHT_MASK, mode = viz.MASK_REMOVE )
	elif eye == viz.RIGHT_EYE:
		lens.disable( viz.RENDER_LEFT )
		object.setMask( REFLECT_MASK | viz.LEFT_MASK, mode = viz.MASK_REMOVE )
	else:
		object.setMask( REFLECT_MASK, mode = viz.MASK_REMOVE )

	#Setup reflection matrix
	rot = viz.Matrix.quat( quat )
	invRot = rot.inverse()
	lens.setMatrix( viz.Matrix.translate( -pos ) * invRot * viz.Matrix.scale( 1, 1, -1 ) * rot * viz.Matrix.translate( pos ) )

	#Setup reflection clip plane
	s = viz.sign( viz.Vector( dir ) * viz.Vector( pos ) )
	plane = vizmat.Plane( pos = pos, normal = dir )
	dist = plane.distance( [ 0, 0, 0 ] )
	lens.clipPlane( [ dir[ 0 ], dir[ 1 ], dir[ 2 ], s * dist - 0.01 ] )

	#Project reflection texture onto object
	object.texture( tex )
	object.texGen( viz.TEXGEN_PROJECT_EYE )

	return lens

def move_camera( camera, position, focus, yoffset, speed ):
	"""Moves camera to a position while keeping focus on object

	vizact.onkeydown( ' ', functions.move_camera, camera, [ 0, eyeheight, 0 ], subject, eyeheight ) #action key, function, camera, end position, object of focus, y offset"""

	pivot = [ focus.getPosition()[ 0 ], focus.getPosition()[ 1 ] + yoffset, focus.getPosition()[ 2 ] ]
	action = vizact.goto( position, value = speed, mode = viz.SPEED, rotate_mode = viz.PIVOT_ROTATE, pivot = pivot, ori_mask = viz.HEAD_ORI )
	camera.runAction( action )
	return camera

def revolve_camera( camera, focus, angle, speed ):
	pivot = [ focus.getPosition()[ 0 ], camera.getPosition()[ 1 ], focus.getPosition()[ 2 ] ]
	radius = vizmat.Distance( camera.getPosition(), pivot )

	if ( angle == 360 ):
		angle = 0

	while ( angle <= 360 ):
		position = calculate_position( camera, angle, radius )
		action = vizact.goto( position, value = speed * radius / 1000, mode = viz.TIME, rotate_mode = viz.PIVOT_ROTATE, pivot = focus.getPosition(), ori_mask = viz.HEAD_ORI )
		camera.addAction( action )
		angle = angle + 10

def calculate_position( camera, angle, radius ):
	radians = math.radians( angle )
	x = math.sin( radians ) * radius
	y = camera.getPosition()[ 1 ]
	z = -math.cos( radians ) * radius
	position = [ x, y, z ]
	return position


def media_end( e ):
	"""Check if media has ended

	viz.callback( viz.MEDIA_EVENT, media_end )"""

	if e.event == viz.MEDIA_END:
		return True

def media_play( file, fps, screen ):
	"""Play media file

	functions.media_play( 'filename', 12, object )"""

	video = viz.addVideo( 'videos/' + file )
	video.setFrame( fps )
	screen.texture( video )
	video.play()

def debug( variable ):
	screen_text( 'value: ', variable )
	#return variable

def screen_text( label, message ):
	#Display Text
	print label, message
	textArea = viz.addText( '', viz.SCREEN , pos = ( 0.1, 0.2, 0 ) )
	textArea.message( label % ( message ) )