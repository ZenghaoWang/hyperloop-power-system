# Communication

## Battery Module MCU
The `battery_module_mcu` folder contains the source code for the Arduino Micro MCUs found within the battery modules
of the pod. This code was based on the code provided by UTHT found in `old_battery_module_code_from_UTHT`.

## Communication Prototype
The `communication_prototype` folder contains Arduino code used to prototype the CAN communication bus. It contains two types of nodes: Sensors and Listeners. The sensors send data onto the CAN bus and the listeners listen to the bus and print the bus' output to the serial output. This code requires both the sensors and listeners to be Arduino Dues with "SN65HVD230 CAN Board"s used to translate the CAN_RX and CAN_TX pins into CAN_H and CAN_L (https://www.waveshare.com/sn65hvd230-can-board.htm).

## CAN ID to Sensor Data Table

THIS IS NOT FINALIZED, JUST NOTES.

Largest ID: 0x4FF

Highest Priority: 0

Lowest Priority: 15

Plan:
- 0x000 - 0x0FF: HV IDs
- 0x100 - 0x1FF: LV IDs

TODO: Put this information in a header file somehow.

| ID  | Sensor | Data Type | Priority |
| --- | ------ | --------- | -------- |
| 0x000 | HV Battery Module 0 Temp. | fp32 | 0 |
| 0x001 | HV Battery Module 1 Temp. | fp32 | 0 |
| 0x002 | HV Battery Module 2 Temp. | fp32 | 0 |
| 0x003 | HV Battery Module 3 Temp. | fp32 | 0 |
| 0x004 | HV Battery Module 4 Temp. | fp32 | 0 |
| 0x005 | HV Battery Module 5 Temp. | fp32 | 0 |
| 0x006 | HV Battery Module 6 Temp. | fp32 | 0 |
| 0x007 | HV Battery Module 7 Temp. | fp32 | 0 |
| 0x008 | HV Battery Module 8 Temp. | fp32 | 0 |
| 0x009 | HV Battery Module 9 Temp. | fp32 | 0 |
| 0x00A | HV Battery Module 0 State of Charge | fp32 | 15 |
| 0x00B | HV Battery Module 1 State of Charge | fp32 | 15 |
| 0x00C | HV Battery Module 2 State of Charge | fp32 | 15 |
| 0x00D | HV Battery Module 3 State of Charge | fp32 | 15 |
| 0x00E | HV Battery Module 4 State of Charge | fp32 | 15 |
| 0x00F | HV Battery Module 5 State of Charge | fp32 | 15 |
| 0x010 | HV Battery Module 6 State of Charge | fp32 | 15 |
| 0x011 | HV Battery Module 7 State of Charge | fp32 | 15 |
| 0x012 | HV Battery Module 8 State of Charge | fp32 | 15 |
| 0x013 | HV Battery Module 9 State of Charge | fp32 | 15 |
| 0x014 | HV System Voltage | fp32 | 3 |
| 0x015 | HV System Current | fp32 | 3 |
| 0x1?? | Unused | void | null |
| 0x100 | LV Battery Module Temp. | fp32 | 0 |
| 0x101 | LV Battery Module State of Charge | fp32 | 15 |
| 0x102 | LV Battery Current | fp32 | 4 |
| 0x103 | LV System Voltage | fp32 | 4 |
| 0x104 | LV PCB Temp. | fp32 | 7 |