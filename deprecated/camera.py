from picamera import PiCamera#, Color
from time import sleep

camera = PiCamera()

#camera.rotation = 180
#camera.resolution = (2592, 1944)
#camera.framerate = 15
camera.start_preview()
for effect in camera.IMAGE_EFFECTS:
	camera.image_effect = effect
	camera.annotate_text = "Effect: %s" % effect
	sleep(5)
#for i in range(100):
#	camera.annotate_text = "Contrast: %s" % i
#	camera.contrast = i
#	sleep(0.1)
#camera.annotate_background = Color('blue')
#camera.annotate_foreground = Color('yellow')
#camera.annotate_text_size = 50
#camera.annotate_text = "Hello world!"
#camera.start_recording('/home/pi/video.h264')
#for i in range(5):
#	sleep(5)
#	camera.capture('/home/pi/test%s.jpg' % i)
#sleep(5)
#camera.stop_recording()
#camera.capture('/home/pi/bright.jpg')
camera.stop_preview()
