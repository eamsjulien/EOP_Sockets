"""
Module supporting the Camera class, responsible for taking snapshots.

class Camera: contains the builder and the main capture function.

"""

import os
import cv2

class Camera:
    """Class responsible for taking frames captures from webcam.

    This class initiates a Camera object and then invoke the main method
    called capture. Directly capture frames from the existing webcam.
    Relies on cv2 from frames capture and save.

    Attributes:
        frames = An integer indicating the number of snapshots to take.
        path = A string indicating the path where frames are saved.
    """

    def __init__(self, frames=200, path='./'):
        """Init Camera with frames nbr and path."""
        self.frames = frames
        self.path = path

    def getframes(self):
        """Getter for Camera instance frames number.

        Args:
            None

        Returns:
            An int representing the frame number of the instance.
        """
        return self.frames

    def getpath(self):
        """Getter for Camera instance path.

        Args:
            None

        Returns:
            A string representing the path where frames are saved.
        """
        return self.path

    def setframes(self, frames):
        """Setter for Camera instance frames number.

        Args:
            frames: An int representing the new frame number.

        Returns:
            None
        """
        self.frames = frames

    def setpath(self, path):
        """Setter for Camera instance path.

        Args:
            path: An string representing the new path.

        Returns:
            None
        """
        self.path = path

    def capture(self):
        """Capture frames from webcam.

        Starts the existing camera bound to the computer and starts
        taking snapshots, or frames. Relies on the cv2 library call
        for snapshots. Takes snapshots until self.frames number then
        saves them under self.path.

        Args:
            None

        Returns:
            None
        """
        cap = cv2.VideoCapture(0)
        count = 0
        while count < self.frames:
            _, frm = cap.read()
            cv2.imwrite(os.path.join(self.path, "frame%d.jpg" % count), frm)
            count = count + 1
        cap.release()
