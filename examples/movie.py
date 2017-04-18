# http://matplotlib.org/examples/animation/dynamic_image2.html
# blit=True does not seem to work on Macs

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import ome_files


fig = plt.figure()

# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame
ims = []
reader = ome_files.OMETIFFReader()
reader.set_id("9I5TT808_F00000010.ome.tif")
#for i in xrange(reader.get_image_count()):
for i in xrange(5):
    pixels = reader.open_array(i)
    im = plt.imshow(pixels, cmap="gray", animated=True)
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=500, repeat_delay=1000)

# ani.save('dynamic_images.mp4')

plt.show()
