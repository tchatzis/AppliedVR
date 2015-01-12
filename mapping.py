import viz
import vizact

viz.setMultiSample(4)
viz.fov(60)
viz.go()

import vizinfo
#vizinfo.InfoPanel()

#Add the vizard logo
logo = viz.addChild('logo.ive')

#Add the texture that will represent the environment
texture = viz.addTexture('images/img_0247.jpg')

#Apply the texture to the logo
logo.texture(texture)

#Set the appearance of the logo to viz.TEXGEN and viz.TEXDECAL
logo.appearance(viz.TEXGEN|viz.TEXDECAL)

#Spin the logo
logo.addAction(vizact.spin(0,1,0,10))

#Place the logo in front of the viewer
logo.setPosition([0,1,2])

#Turn the sky blue
viz.clearcolor(viz.SLATE)