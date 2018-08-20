"""
Main handler for the AWS server component.

Usage: python3 main.py
"""

import os
import time

import comm.socks as ch

def main():
    """Main function for server loop."""

    # FACEDETECT SERVER #

    print(" -------------------------")
    print("| AWS FACEDETECT - SERVER |")
    print(" -------------------------")

    print("\n Initializing ENV variables...", end='')
    save_loc, eop_loc = ch.init_eopsock_environ_folder()
    print("Done!")

    print("\n Initializing server socket...", end='')
    server_socket = ch.init_server_socket()
    print("Done!")

    server_socket.listen(5)
    print("\nWaiting for incoming connection...")
    client, addr = server_socket.accept()
    print("Incoming connection from " + str(addr))

    frame_nbr = int(ch.receive_bytes_to_string(client))
    print("Expecting " + str(frame_nbr) + " frames from remote host.")

    print("Sending ack...", end='')
    ch.send_frame_ack(client, 0)
    print("Sent.")

    frame_step = int(ch.receive_bytes_to_string(client))
    print("Looping every " + str(frame_step) + " steps.")

    print("Sending ack...", end='')
    ch.send_frame_ack(client, 0)
    print("Sent.")

    print("\n **** RECEIVING FRAMES ****")

    for curr_frame in [frame_step*x for x in range(int(frame_nbr/frame_step))]:

        frame_size = int(ch.receive_bytes_to_string(client))
        ch.receive_frame(client, curr_frame, frame_size, save_loc)
        print("Frame " + str(curr_frame) + " received.")

        print("Segments detection...")
        os.system(eop_loc + 'easyOpenPose.bin inbox/frame'
                  + str(curr_frame) + '.jpg 0 500 500')
        os.system('mv test_openpose.jpg inbox/frame'
                  + str(curr_frame) + '.jpg')

        print("Sending ack...", end='')
        ch.send_frame_ack(client, curr_frame)
        print("Sent.")

    print("\nFrames processing completed!")

    print("\n **** SENDING FRAMES ****")

    for curr_frame in [frame_step*x for x in range(int(frame_nbr/frame_step))]:
        time.sleep(0.2)
        frame_loc = "inbox/frame" + str(curr_frame) + ".jpg"
        ch.send_frame_size(client, frame_loc)
        print("Sending frame %s..." % str(curr_frame), end='')
        ch.send_frame(client, frame_loc, sleep=0.1)
        print("Done.")
        print("Waiting for frame " + str(curr_frame) + " reception...", end='')
        ch.waiting_for_ack(client, curr_frame)
        print("ACK")

    print("\nFrames sent!")

    print("Closing sockets...", end='')
    client.close()
    server_socket.close()
    print("Done!")

    print("\n --------------------------")
    print("| AWS FACEDETECT - GOODBYE |")
    print(" --------------------------")

if __name__ == '__main__':
    main()
