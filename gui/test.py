import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Testing Interface for UTHT Power Distribution System.")
    parser.add_argument('-c', '--can-port', help='The serial port that the can interface is connected to.', type=int, default=None)
    parser.add_argument('-a', '--arduino-port', help='The serial port that the arduino due is connected to.', type=int, default=None)
    args = parser.parse_args()
    print(args.can_port)
    print(args.arduino_port)
  # choices = ['S', 's', 'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd']
  # ser = serial.Serial()
  # ser.baudrate = 9600
  # ser.port = 'COM13'
  # ser.timeout = 1
  # if (ser.is_open):
  #   ser.close()
  # ser.open()
  # # For some reason, the arduino prints out "initializing buffer" on initial connection.
  # # We don't want to read that, so we sleep for a second.
  # # hacky 
  # time.sleep(1)
  # while True:
  #   data = random.choice(choices)
  #   print(f"Sending {data} to arduino")
  #   ser.write(data.encode())
  #   # Read a character from the arduino to make sure it received the data
  #   res = ser.read(1)
  #   try:
  #     if res.decode('ASCII') == 'A':
  #       print(f"Arduino successfully received data: {data}")
  #     elif res.decode('ASCII') == 'N':
  #       print(f"Arduino received {data} but did not act on it.")
  #   except:
  #     print(f"Error decoding response {res}")
    # global bus
    # bus = can.ThreadSafeBus(interface='slcan', channel='COM22', bitrate=1000000)

    # listener = can.BufferedReader()
    # global n 
    # n = can.Notifier(bus, listeners=[listener], timeout=0.01)

    # while True:
    #   msg: Optional[can.Message] = listener.get_message(0.1)
    #   if msg:
    #     print(struct.unpack('f', msg.data)[0])



