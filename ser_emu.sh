#!/bin/bash

# sudo apt install figlet

figlet Serial Port El_sign Emulator

echo "Sends information from upper to lower port"
echo "Start the python script and insert the upper port number."
echo "To display the serial input of the receiving port in real time,"
echo "start a new terminal window and insert lower port at the end"
echo "cat </dev/pts/#num#"
echo ""

gnome-terminal -- sh -c "bash -c \"socat -d -d pty,raw,echo=0 pty,raw,echo=0; exec bash\""
python3 electrode_sign_emulation.py