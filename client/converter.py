import cv2

class Converter:

    def __init__(self, frames, step, videoname='video.avi', fps=20.0):
        self.frames = frames
        self.step = step
        self.videoname = videoname
        self.fps = fps

    def initiate_framelist(self, location):
        img = []
        for i in [self.step * x for x in range(int(self.frames/self.step))]:
            img.append(cv2.imread(location + '/frame' + str(i) + '.jpg'))
        return img

    def initiate_inputlist(self, location):
        img = []
        for i in [self.step * x for x in range(int(self.frames/self.step))]:
            img.append(cv2.imread(location + '/frame' + str(i) + '.jpg'))
        return img

    def substract_images(self, proc_frames, input_frames):
        subtract = []
        for item in proc_frames:
            img = cv2.subtract(proc_frames[item], input_frames[item])
            subtract.append(img)
        return subtract

    def write_video(self, imglist):
        height, width, _layers = imglist[1].shape
        video = cv2.VideoWriter(self.videoname,
                                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                self.fps, (width, height))

        for frame in range(len(imglist)):
            video.write(imglist[frame])

        video.release()
