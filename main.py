"""
Main handler for the EOP_Sockets server component.

Usage: python3 main.py [--sleep SLEEP]
"""

import argparse

import comm.socks as ch
import server.detector as dt

def main(): # pylint: disable=too-many-statements, too-many-locals
    """Main function for server loop."""

    # PYTHON PARSER VIA ARGPARSE #

    parser = argparse.ArgumentParser(description="EOP_Sockets Client Main.")
    parser.add_argument("-s", "--sleep", help="Sleep in seconds.",
                        nargs='?', default=0.1, type=float)
    args = vars(parser.parse_args())

    sleep = args['sleep']

    # EOP_Sockets SERVER #

    print(" ----------------------")
    print("| EOP SOCKETS - SERVER |")
    print(" ----------------------")

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

    print("Sending frame number ack...", end='')
    ch.send_frame_ack(client, exptype='FRAME_NBR')
    print("Sent.")

    frame_step = int(ch.receive_bytes_to_string(client))
    print("Looping every " + str(frame_step) + " steps.")

    print("Sending increment ack...", end='')
    ch.send_frame_ack(client, exptype='INCREMENT')
    print("Sent.")

    print("\n **** RECEIVING FRAMES ****")

    frame_list = []
    for curr_frame in [frame_step*x for x in range(int(frame_nbr/frame_step))]:

        frame_size = int(ch.receive_bytes_to_string(client))
        ch.receive_frame(client, curr_frame, frame_size, save_loc)
        print("Frame " + str(curr_frame) + " received.")

        print("Sending ack...", end='')
        ch.send_frame_ack(client, frame=curr_frame)
        frame_list.append(curr_frame)
        print("Sent.")

    print("Segments detection...")
    for index_frame in range(0, len(frame_list), 3):
        current_framelist = frame_list[index_frame:index_frame+3]
        dt.parallel_seg(eop_loc, current_framelist, fname=dt.segmentation)

    print("\nFrames processing completed!")

    print("\n **** SENDING FRAMES ****")
    for curr_frame in [frame_step*x for x in range(int(frame_nbr/frame_step))]:
        frame_loc = "inbox/frame" + str(curr_frame) + ".jpg"
        ch.send_frame_size(client, frame_loc)
        print("Sending frame %s..." % str(curr_frame), end='')
        ch.send_frame(client, frame_loc, sleep=sleep)
        print("Done.")
        print("Waiting for frame " + str(curr_frame) + " reception...", end='')
        ch.waiting_for_ack(client, frame=curr_frame)
        print("ACK")

    print("\nFrames sent!")

    print("Closing sockets...", end='')
    client.close()
    server_socket.close()
    print("Done!")

    print("\n ---------------------")
    print("| EOP SOCKETS - GOODBYE |")
    print(" -----------------------")

if __name__ == '__main__':
    main()
