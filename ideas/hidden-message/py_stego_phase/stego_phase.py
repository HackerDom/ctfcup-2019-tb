# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
The method of phase encoding in audio steganography.

stego_phase.py
"""

__author__ = 'Ilya Shoshin (Galarius)'
__copyright__ = 'Copyright 2015, Ilya Shoshin (Galarius)'

# Examples:
# python stego_phase.py -i "wav/beat.wav" -m "msg/msg.txt" -o "wav/stego.wav"
# python stego_phase.py -i "wav/stego.wav" -m "msg/msg_recovered.txt" -k 1024

#---------------------------------------------------
# to capture console args
import sys, getopt
# math functions
from math import *
import cmath
# use numpy
import numpy as np
# wav io wrapper module
import wav_io
# helper methods for stego operations
from stego_helpers import *
#---------------------------------------------------

def hide(source, destination, message):
    """
    :param source:  source stego container filename
    :param destination:    dest stego container filename
    :param message:       message to hide
    :return:        segment_width - segment width
    """
    # read wav file
    print 'reading wave container...'
    (nchannels, sampwidth, framerate, nframes, comptype, compname),\
    (left, right) = wav_io.wav_load(source)
    # select channel to hide message in
    container = left
    container_len = len(container)
    # --------------------------------------
    # prepare container
    # --------------------------------------
    print 'preparing container...'
    message_len = 8 * len(message)          # msg len in bits
    v = int(ceil(log(message_len, 2)+1))    # get v from equation: 2^v >= 2 * message_len
    segment_width = 2**(v+1)                # + 1 to reduce container distortion after msg integration
    segment_count = int(ceil(container_len / segment_width))    # number of segments to split container in
    # add silence if needed
    if segment_count > container_len / segment_width:
        container = [(container[i] if i < container_len else 0) for i in range(0, segment_count*segment_width)]
    container_len = len(container)          # new container length
    # split signal in 'segment_count' segments with 'segment_width' width
    segments = chunks(container, segment_width)
    # --------------------------------------
    # apply FFT
    # --------------------------------------
    print 'performing fft transform...'
    delta = [np.fft.rfft(segments[n]) for n in range(0, segment_count)]  # -> segment_width / 2 + 1
    # extract amplitudes
    vabs = np.vectorize(abs)    # apply vectorization
    amps = [vabs(delta[n]) for n in range(0, segment_count)]
    # extract phases
    varg = np.vectorize(arg)    # apply vectorization
    phases = [varg(delta[n]) for n in range(0, segment_count)]
    # --------------------------------------
    # save phase subtraction
    delta_phases = segment_count*[None]
    delta_phases[0] = 0 * phases[0]
    def sub (a, b): return a - b
    vsub = np.vectorize(sub)
    for n in range(1, segment_count):
        delta_phases[n] = vsub(phases[n], phases[n-1])
    # --------------------------------------
    # integrate msg, modify phase
    print 'msg integration...'
    msg_vec = str_2_vec(message)
    msg_bits = [d_2_b(msg_vec[t]) for t in range(0, len(message))]
    msg_bits = [item for sub_list in msg_bits for item in sub_list]  # msg is a list of bits now

    segment_width_half = segment_width / 2
    phase_data = (segment_width_half + 1) * [None]  # preallocate list where msg will be stored
    for k in range(0, segment_width_half + 1):
        if k <= len(msg_bits):
            if k == 0 or k == segment_width_half:   # do not modify phases at the ends
                phase_data[k] = phases[0][k]
            if 0 < k < segment_width_half:          # perform integration begining with the hi-freq. components
                if msg_bits[k-1] == 1:
                    phase_data[segment_width_half+1-k] = -pi / 2.0
                elif msg_bits[k-1] == 0:
                    phase_data[segment_width_half+1-k] = pi / 2.0
        if k > len(msg_bits):                       # original phase
            phase_data[segment_width_half+1-k] = phases[0][segment_width_half+1-k]
    phases_modified = [phase_data]
    for n in range(1, segment_count):
        phases_modified.append((phases_modified[n-1] + delta_phases[n]))
    # --------------------------------------
    # convert data back to the frequency domain: amplitude * exp(1j * phase)
    def to_frequency_domain (amp, ph): return amp * cmath.exp(1j * ph)
    vto_fft_result = np.vectorize(to_frequency_domain)
    delta_modified = [vto_fft_result(amps[n], phases_modified[n]) for n in range(0, segment_count)]
    # restore segments
    segments_modified = [np.fft.irfft(delta_modified[n]) for n in range(0, segment_count)]
    # join segments
    container_modified = [item for sub_list in segments_modified for item in sub_list]
    # sync the size of unmodified channel with the size of modified one
    right_synced = len(container_modified) * [None]
    for i in range(0, len(container_modified)):
        if i < len(right):
            right_synced[i] = right[i]
        else:
            right_synced[i] = 0
    # --------------------------------------
    # save stego container with integrated message in freq. scope as wav file
    print 'saving stego container...'
    wav_io.wav_save(destination, (container_modified, right_synced),
                    nchannels, sampwidth, framerate, nframes, comptype, compname)
    # to recover the message the one must know the segment width, used in the process
    print "\nDone.\n"
    return segment_width


def recover(source, segment_width):
    """
    :param source: filename for the file with integrated message
    :param segment_width: segment width
    :return: message
    """
    # read wav file with integrated message
    print 'reading wave container...'
    (nchannels, sampwidth, framerate, nframes, comptype, compname),\
    (left, right) = wav_io.wav_load(source)
    container = left    # take left channel for msg recovering
    container_len = len(container)
    # --------------------------------------
    # prepare container
    print 'preparing container...'
    segment_count = int(container_len / segment_width)
    # split signal in 'segment_count' segments with 'width' width
    segments = chunks(container, segment_width)
    # --------------------------------------
    # apply FFT
    print 'performing fft transform...'
    delta = [np.fft.rfft(segments[0])]
    # extract phases
    varg = np.vectorize(arg)    # apply vectorization
    phases = [varg(delta[0])]
    phases_0_len = len(phases[0])
    # --------------------------------------
    # recover message
    print 'recovering message...'
    b = []
    for t in range(0, segment_width / 2):
        d = phases[0][phases_0_len-1-t]
        if d < -pi / 3.0:
            b.append(1)
        elif d > pi / 3.0:
            b.append(0)
        else:
            break
    msg_bits_len = int(floor(len(b) / 8.0))
    msg_bits_splitted = chunks(b, 8)
    msg_vec = []
    for i in range(0, msg_bits_len):
        msg_vec.append(b_2_d(msg_bits_splitted[i]))
    message = vec_2_str(msg_vec)
    print "\nDone.\n"
    return message


def print_usage():
    print """
          hide msg:    stego_phase.py -i <input_container_file_name> -m <message_file_name> -o <output_container_file_name>
          recover msg: stego_phase.py -i <input_container_file_name> -m <message_file_name> -k <segment_width>
          """


def main(argv):
    input_container_file_name = ''
    message_file_name = ''
    output_container_file_name = ''
    segment_width = -1
    # --------------------------------------
    try:
       opts, args = getopt.getopt(argv, "hi:m:o:k:", ["ifile=", "mfile=", "ofile=", "karg="])
    except getopt.GetoptError:
       print_usage()
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_container_file_name = arg
        elif opt in ("-m", "--mfile"):
            message_file_name = arg
        elif opt in ("-o", "--ofile"):
            output_container_file_name = arg
        elif opt in ("-k", "--karg"):
            segment_width = int(arg)

    if input_container_file_name == '':
        print_usage()
        sys.exit()

    if not output_container_file_name == '':
        # --------------------------------------
        # hide
        # --------------------------------------
        message = ''
        try:
            with open(message_file_name, "r") as reader:
                message = reader.read()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        if not message == '':
            segment_width = hide(input_container_file_name, output_container_file_name, message)
            print "Remember segment width to recover message: {0}".format(segment_width)
        # --------------------------------------
    elif segment_width > 0:
        # --------------------------------------
        # recover
        # --------------------------------------
        message = recover(input_container_file_name, segment_width)
        try:
            with open(message_file_name, "w") as writer:
                writer.write(message)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        # --------------------------------------
    else:
        print_usage()

if __name__ == "__main__":
    main(sys.argv[1:])