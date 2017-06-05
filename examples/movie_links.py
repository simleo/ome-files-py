# http://matplotlib.org/examples/animation/dynamic_image2.html
# blit=True does not seem to work on Macs

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
# http://stackoverflow.com/questions/20250154/linecollection-animation-when-updating-the-frames-in-a-loop
import datapackage
import pandas as pd

import ome_files


DP_FN = "trackmate_dp/datapackage.json"
SCALE = 3.10559006211


def get_table(datapackage_fn, table_name):
    dp = datapackage.DataPackage(datapackage_fn)
    res_map = dict((_.descriptor["name"], _.local_data_path)
                   for _ in dp.resources)
    return pd.read_csv(res_map[table_name])


obj_df = get_table(DP_FN, "objects_table")
links_df = get_table(DP_FN, "links_table")
links_map = links_df.groupby("LINK_ID").agg(lambda x: set(x)).to_dict()
# at each frame, for each obj, see if there is an obj in the previous frame that belongs to the same link


fig = plt.figure()

# ims is a list of lists, each row is a list of artists to draw in the
# current frame
ims = []
reader = ome_files.OMETIFFReader()
reader.set_id("9I5TT808_F00000010.ome.tif")
#for i in xrange(reader.get_image_count()):
for i in xrange(20):
    pixels = reader.open_array(i)
    im = plt.imshow(pixels, cmap="gray", animated=True)
    obj_df_slice = obj_df[obj_df["FRAME"] == i]
    x = SCALE * obj_df_slice["POSITION_X"].values
    y = SCALE * obj_df_slice["POSITION_Y"].values
    scatter = plt.scatter(x=x, y=y, s=100, edgecolors='b', facecolors='none',
                          animated=True)
    ims.append([im, scatter])

ani = animation.ArtistAnimation(fig, ims, interval=500, repeat_delay=1000)

# ani.save('dynamic_images.mp4')

plt.show()
