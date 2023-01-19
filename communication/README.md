# Communication

## Battery Module MCU
The `battery_module_mcu` folder contains the source code for the Arduino Micro MCUs found within the battery modules
of the pod. This code was based on the code provided by UTHT found in `old_battery_module_code_from_UTHT`.

## Communication Prototype
The `communication_prototype` folder contains Arduino code used to prototype the CAN communication bus. It contains two types of nodes: Sensors and Listeners. The sensors send data onto the CAN bus and the listeners listen to the bus and print the bus' output to the serial output. This code requires both the sensors and listeners to be Arduino Dues with "SN65HVD230 CAN Board"s used to translate the CAN_RX and CAN_TX pins into CAN_H and CAN_L (https://www.waveshare.com/sn65hvd230-can-board.htm).
