"""
Main handler for the client component.

Usage: python3 main_client.py --address ADDRESS [--frames FRAMES]
                             [--sleep SLEEP]
"""


import argparse

import client.client as cl
from client.camera import Camera

def main():
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
    args = vars(parser.parse_args())

    frame_nbr = args['frames']
    server_addr = args['address']
    sleep = args['sleep']
    increment = args['increment']

    # FACEDETECT CLIENT #

    print(" -------------------------")
    print("| AWS FACEDETECT - CLIENT |")
    print(" -------------------------")

    print("\n Initializing ENV variables...", end='')
    capture_loc = cl.init_facedetect_environ_folder()
    print("Done!")

    print("\n Initializing server socket...", end='')
    client_socket = cl.init_client_socket(server_addr)
    print("Done!")

    print("\n **** CAPTURING FRAMES ****")
    cam = Camera(frames=frame_nbr, path=capture_loc)
    cam.capture()
    print(" " + str(frame_nbr) + " frames captured!")

    print("\n **** SENDING FRAMES NBR ****")
    cl.send_total_frame_nbr(client_socket, frame_nbr)
    print(" Frames number sent to server!")

    print("\n **** SENDING INCREMENT NBR ****")
    cl.send_increment_nbr(client_socket, increment)
    print(" Frames increment sent to server!")

    print("\n **** SENDING FRAMES ****")
    for frame in [increment*x for x in range(int(frame_nbr/increment))]:
        frame_loc = capture_loc + "frame" + str(frame) + ".jpg"
        cl.send_frame_size(client_socket, frame_loc)
        print("Sending frame %s..." % str(frame), end='')
        cl.send_frame(client_socket, frame_loc, sleep=sleep)
        print("Done.")
        print("Waiting for frame " + str(frame) + " reception...", end='')
        cl.waiting_for_ack(client_socket, frame)
        print("ACK")

    print("\nFrames sent!")
    print("\n --------------------------")
    print("| AWS FACEDETECT - GOODBYE |")
    print(" --------------------------")


if __name__ == '__main__':
    main()
