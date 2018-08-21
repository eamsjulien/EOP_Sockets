"""
Main handler for the client component.

Usage: python3 main_client.py --address ADDRESS [--frames FRAMES]
                             [--sleep SLEEP] [--rate RATE]
"""


import argparse

import comm.socks as cs
from client.camera import Camera
from client.converter import Converter

def main(): #pylint: disable=too-many-locals, too-many-statements
    """Main function for client loop."""

    # PYTHON PARSER VIA ARGPARSE #

    parser = argparse.ArgumentParser(description="AWS FaceDetect Client Main.")
    parser.add_argument("-a", "--address", required=True,
                        help="Address to connect to.", type=str)
    parser.add_argument("-f", "--frames", help="Frames to send.",
                        nargs='?', default=10, type=int)
    parser.add_argument("-i", "--increment", help="Increment loop.",
                        nargs='?', default=3, type=int)
    parser.add_argument("-s", "--sleep", help="Sleep in seconds.",
                        nargs='?', default=0.1, type=float)
    parser.add_argument("-r", "--rate", help="Video FPS.",
                        nargs='?', default=20, type=int)
    args = vars(parser.parse_args())

    frame_nbr = args['frames']
    server_addr = args['address']
    sleep = args['sleep']
    increment = args['increment']
    rate = args['rate']

    # FACEDETECT CLIENT #

    print(" -------------------------")
    print("| AWS FACEDETECT - CLIENT |")
    print(" -------------------------")

    print("\n Initializing ENV variables...", end='')
    capture_loc, save_loc = cs.init_eopsock_environ_folder()
    print("Done!")

    print("\n Initializing server socket...", end='')
    client_socket = cs.init_client_socket(server_addr)
    print("Done!")

    print("\n **** CAPTURING FRAMES ****")
    cam = Camera(frames=frame_nbr, path=capture_loc)
    cam.capture()
    print(" " + str(frame_nbr) + " frames captured!")

    print("\n **** SENDING FRAMES NBR ****")
    cs.send_total_frame_nbr(client_socket, frame_nbr)
    print(" Frames number sent to server!")

    print("Waiting frame number ack...", end='')
    cs.waiting_for_ack(client_socket, exptype='FRAME_NBR')
    print("ACK")

    print("\n **** SENDING INCREMENT NBR ****")
    cs.send_increment_nbr(client_socket, increment)
    print(" Frames increment sent to server!")

    print("Waiting increment number ack...", end='')
    cs.waiting_for_ack(client_socket, exptype='INCREMENT')
    print("ACK")

    print("\n **** SENDING FRAMES ****")
    for frame in [increment*x for x in range(int(frame_nbr/increment))]:
        frame_loc = capture_loc + "frame" + str(frame) + ".jpg"
        cs.send_frame_size(client_socket, frame_loc)
        print("Sending frame %s..." % str(frame), end='')
        cs.send_frame(client_socket, frame_loc, sleep=sleep)
        print("Done.")
        print("Waiting for frame " + str(frame) + " reception...", end='')
        cs.waiting_for_ack(client_socket, frame=frame)
        print("ACK")

    print("\nFrames sent!")

    print("\n **** RECEIVING FRAMES ****")

    for frame in [increment*x for x in range(int(frame_nbr/increment))]:

        frame_size = int(cs.receive_bytes_to_string(client_socket))
        cs.receive_frame(client_socket, frame, frame_size, save_loc)
        print("Frame " + str(frame) + " received.")

        print("Sending ack...", end='')
        cs.send_frame_ack(client_socket, frame=frame)
        print("Sent.")

    print("\nFrames received!")

    print("\n **** GENERATING VIDEO ****")

    converter = Converter(frame_nbr, increment, fps=rate)

    imglist = converter.initiate_framelist(save_loc)
    print("\n Generating video from " + str(frame_nbr/increment) +
          " frames at " + str(rate) + " fps.")

    inputlist = converter.initiate_inputlist(capture_loc)

    outputlist = converter.substract_images(imglist, inputlist)

    converter.write_video(outputlist)

    print("\nVideo encoded!")

    print("\n ---------------------")
    print("| EOP Sockets - GOODBYE |")
    print(" -----------------------")


if __name__ == '__main__':
    main()
