import os

from multiprocessing.dummy import Pool as ThreadPool
from itertools import repeat

def segmentation(loc, curr_frame):
        os.system(loc + 'easyOpenPose.bin inbox/frame'
                  + str(curr_frame) + '.jpg 0 500 500 '
                  + 'inbox/frame' + str(curr_frame) + '.jpg '
                  + loc + 'pose_deploy_linevec.prototxt '
                  + loc + 'pose_iter_440000.caffemodel')


def parallel_seg(loc, framelist, workers=3, fname='segmentation'):

    pool = ThreadPool(workers)

    pool.starmap(fname, zip(repeat(loc), framelist))

    pool.close()
    pool.join()
