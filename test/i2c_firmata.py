import pyfirmata2

# main program

# Adjust that the port match your system, see samples below:
# On Linux: /dev/ttyACM0,
# On Windows: COM1, COM2, ...
PORT =  pyfirmata2.Arduino.AUTODETECT

# Creates a new board
board = pyfirmata2.Arduino(PORT, debug=True)


import pdb; pdb.set_trace()

print(f"Our firmata version: {board.get_firmata_version()}")

print("To stop the program press return.")
# Just blocking here to do nothing.
input()


# close the serial connection
board.exit()
