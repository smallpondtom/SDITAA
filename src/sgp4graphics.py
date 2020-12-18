"""
 ___________   _________     _____________   ______________    ______            ______
|^^^^^______| |   ___   >\  |_____   _____| |_____    _____|  /< __ >\          /> __ <\
|    |______  |  |   \   >\      |   |           |    |      /> |__| <\        /< |__| >\
|_______    | |  |    |  >|      |   |           |    |     /< ______ >\      /> ______ <\
 ______|    | |  |___/   >/  ____|   |____       |    |    /> |      | <\    /< |      | >\
|___________| |_________>/  |_____________|      |____|   /<__|      |__>\  />__|      |__<\

"""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs 
import cartopy.feature as cfeature
from matplotlib.colors import cnames
from matplotlib import animation
from typing import List, Tuple
from nptyping import NDArray
import threading

def SGP4GRAPHICS(positions: NDArray=None, velocities: NDArray=None):
    xsz, ysz, zsz = positions.shape

    # Set up figure and 3D axis for animation
    fig = plt.figure()
    # For stopping simulation with the esc key
    plt.clf()
    plt.gcf().canvas.mpl_connect('key_release_event',
                                 lambda event: [exit(0) if event.key == 'escape' else None])

    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')

    # Choose a different color for each trajectory
    colors = plt.cm.jet(np.linspace(0, 1, xsz))

    ax1 = fig.add_axes([0,0,1,1])
    galaxy_image = plt.imread('galaxy_image.jpg')
    ax1.imshow(galaxy_image)
    ax1.axis('off')


    ax2 = fig.add_axes([0.37, 0.37, 0.3, 0.3], projection=ccrs.Orthographic(
            central_latitude=0, central_longitude=0))
    ax2.add_feature(cfeature.LAND)
    ax2.add_feature(cfeature.COASTLINE)
    ax2.add_feature(cfeature.OCEAN)
    ax2.axis('off')

    # Set up lines and points
    lines = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])
    pts = sum([ax.plot([], [], [], 'o', c=c) for c in colors], [])

    # Prepare the axes limits
    xmax = np.max(positions[:, :, 0])
    xmin = np.min(positions[:, :, 0])
    ymax = np.max(positions[:, :, 1])
    ymin = np.min(positions[:, :, 1])
    zmax = np.max(positions[:, :, 2])
    zmin = np.min(positions[:, :, 2])
    ax.set_xlim((xmin - 500, xmax + 500))
    ax.set_ylim((ymin - 500, ymax + 500))
    ax.set_zlim((zmin - 500, zmax + 500))

    # Set point-of-view specified by (altitude degrees, azimuth degrees)
    ax.view_init(30, 0)

    # Initialization of animation function which plots the background of each frame
    def animation_init():
        for line, pt in zip(lines, pts):
            line.set_data(np.array([]), np.array([]))
            line.set_3d_properties(np.zeros(0))
            pt.set_data(np.array([]), np.array([]))
            pt.set_3d_properties(np.array([]))
        return lines + pts

    # Animation function which update each frame with the data
    def animate(i):
        i = (1 * i) % ysz
        for line, pt, xyz in zip(lines, pts, positions):
            x, y, z = xyz[:i].T
            line.set_data(x, y)
            line.set_3d_properties(z)
            pt.set_data(x[-1:], y[-1:])
            pt.set_3d_properties(z[-1:])
 
        # Rotate view 
        ax.view_init(30, 0.3 * i)

        fig.canvas.draw()
        return lines + pts

    def earth_animate(i):
        lon = i
        #ax2 = plt.gca()
        #ax2.remove()
        ax2 = plt.axes([0, 0, 0.5, 0.5], projection=ccrs.Orthographic(
            central_latitude=0, central_longitude=lon))
        ax2.add_feature(cfeature.LAND)
        ax2.add_feature(cfeature.COASTLINE)
        ax2.add_feature(cfeature.OCEAN)        
        ax2.set_global()
        ax2.coastlines()
        return 

    # Instigate animator
    anim = animation.FuncAnimation(fig,
                                   func=animate,
                                   init_func=animation_init,
                                   frames=100, interval=50, blit=True)

    
    """
    anim_earth = animation.FuncAnimation(fig,
                                         func=earth_animate,
                                         frames=np.linspace(0, 360, 40),
                                         interval=125, repeat=True)
    #anim.save('sampleDebris_interval-1MIN.mp4', fps=10, extra_args=['-vcodec', 'libx264'])
    """
    plt.show()


## TEST ##
from sgp4_debris_traj import SGP4PREDICT
def main():
    TLE_sample = ['0 VANGUARD 1',
                  '1     5U 58002B   20270.72609959 +.00000008 +00000-0 +35143-4 0  9996',
                  '2     5 034.2447 276.2975 1845776 088.0693 292.9082 10.84868479216254',
                  '0 VANGUARD 2',
                  '1    11U 59001A   20270.83057634 -.00000014 +00000-0 -52792-5 0  9991',
                  '2    11 032.8687 034.7609 1467087 103.7620 273.0083 11.85679410287012',
                  '0 VANGUARD R/B',
                  '1    12U 59001B   20270.89554473 +.00000372 +00000-0 +19820-3 0  9999',
                  '2    12 032.9137 356.0609 1666130 249.2921 092.1676 11.44320987291609',
                  '0 VANGUARD R/B',
                  '1    16U 58002A   20270.85942587 -.00000022 +00000-0 -46274-4 0  9994',
                  '2    16 034.2702 221.8316 2022572 305.2573 037.4791 10.48675665469485',
                  '0 VANGUARD 3',
                  '1    20U 59007A   20270.48712837 +.00000328 +00000-0 +14121-3 0  9999',
                  '2    20 033.3411 182.1436 1666591 082.6853 295.9308 11.55733657242298',
                  '0 EXPLORER 7',
                  '1    22U 59009A   20270.68850821 +.00000323 +00000-0 +46901-4 0  9998',
                  '2    22 050.2861 347.0443 0139436 285.4847 073.0739 14.95205750485528',
                  '0 TIROS 1',
                  '1    29U 60002B   20270.51303602 -.00000101 +00000-0 +16003-4 0  9997',
                  '2    29 048.3794 191.6811 0024581 304.4255 055.4334 14.74372853233453',
                  '0 TRANSIT 2A',
                  '1    45U 60007A   20270.87697544 -.00000081 +00000-0 +70910-5 0  9995',
                  '2    45 066.6929 113.6127 0262116 242.5192 114.9042 14.33687614080375',
                  '0 SOLRAD 1 (GREB)',
                  '1    46U 60007B   20270.90681461 +.00000039 +00000-0 +31064-4 0  9999',
                  '2    46 066.6896 132.4066 0203897 054.4060 307.5857 14.49317409153818',
                  '0 THOR ABLESTAR R/B',
                  '1    47U 60007C   20270.67888321 -.00000040 +00000-0 +16368-4 0  9991',
                  '2    47 066.6644 244.3196 0233780 230.3761 127.6505 14.42103295149279',
                  '0 DELTA 1 R/B',
                  '1    50U 60009B   20270.45814876 -.00000089  00000-0 -40244-4 0  9991',
                  '2    50  47.2307 167.7862 0113683 266.9466  91.8310 12.20112284683000',
                  '0 ECHO 1 DEB (METAL OBJ)',
                  '1    51U 60009C   20270.77783235 -.00000155 +00000-0 -66528-3 0  9997',
                  '2    51 047.2148 033.9443 0107347 105.2138 256.0549 12.18276304676444',
                  '0 COSMOS 86',
                  '1  1584U 65073A   20270.84441890 -.00000096 +00000-0 -90198-6 0  9998',
                  '2  1584 056.0607 043.0461 0211763 335.4680 193.5629 12.51876101515807', ]

    # Add custom date to conduct prediction
    ti = "2020-10-11 00:02:30"
    tf = "2020-12-12 14:02:30"
    sgp4sim = SGP4PREDICT(tledata=TLE_sample, linespertle=3, start_date=ti, end_date=tf, interval="T")
    r, v = sgp4sim.run_sgp4()
    SGP4GRAPHICS(r, v)

if __name__ == '__main__': main()
