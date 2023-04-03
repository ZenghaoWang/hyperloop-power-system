# Communication

## Battery Module MCU
The `battery_module_mcu` folder contains the source code for the Arduino Micro MCUs found within the battery modules
of the pod. This code was based on the code provided by UTHT found in `old_battery_module_code_from_UTHT`.

## Communication Prototype
The `communication_prototype` folder contains Arduino code used to prototype the CAN communication bus. It contains two types of nodes: Sensors and Listeners. The sensors send data onto the CAN bus and the listeners listen to the bus and print the bus' output to the serial output. This code requires both the sensors and listeners to be Arduino Dues with "SN65HVD230 CAN Board"s used to translate the CAN_RX and CAN_TX pins into CAN_H and CAN_L (https://www.waveshare.com/sn65hvd230-can-board.htm).

## CAN ID to Sensor Data Table

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
| 0x014 | HV System Voltage | fp32 | 3 |
| 0x015 | HV System Current | fp32 | 3 |
| 0x100 | LV Battery Module Temp. | fp32 | 0 |
| 0x101 | LV Battery Voltage | fp32 | 4 |
| 0x102 | LV Battery Current | fp32 | 4 |
| 0x103 | LV System Voltage | fp32 | 4 |
| 0x104 | LV PCB Temp. | fp32 | 7 |
| 0x105 | Buck A Voltage | fp32 | 4 |
| 0x106 | Buck B Voltage | fp32 | 4 |
| 0x107 | Buck C Voltage | fp32 | 4 |
| 0x108 | Buck D Voltage | fp32 | 4 |

## LV MCU Signals
The LV MCU has signals that it will use to enable or disable different things in the LV system. These signals are communicated with the LV MCU over serial USB using a 1 Byte command. The MCU will respond to the command with a 1 Byte Response. Each Byte sent will be Acknowledged or No-Acknowledge if the message was received. Multiple Bytes may be sent before a response is received. The Arduino comes with a buffer to hold Serial messages before they are handled.

Note: Currently, which Buck Converter is which does not really matter; it just made the most sense to letter them for the sake of code clarity. The real problem is that there is two 12V Buck Converters and it's hard to specify between them. For the future we will need to formalize which Buck Converter is which. I would like to propose the following:

| Buck Code | Buck Converter |
| --------- | -------------- |
| Buck A | 24V Buck Converter |
| Buck B | First 12V Buck Converter |
| Buck C | Second 12V Buck Converter |
| Buck D | 5V Buck Converter |


| Command | Signal | Description |
| ------- | ------ | ----------- |
| 'S' | Software Switch Enable | Closes the software switch such that power is coming from the HV batteries |
| 's' | Software Switch Disable | Opens the software switch such that the power is coming from the LV battery |
| 'A' | Buck A Enable | Enables Buck A such that it generates voltage on the rail |
| 'a' | Buck A Disable | Disables Buck A such that it does not generate voltage on the rail |
| 'B' | Buck B Enable | Enables Buck B such that it generates voltage on the rail |
| 'b' | Buck B Disable | Disables Buck B such that it does not generate voltage on the rail |
| 'C' | Buck C Enable | Enables Buck C such that it generates voltage on the rail |
| 'c' | Buck C Disable | Disables Buck C such that it does not generate voltage on the rail |
| 'D' | Buck D Enable | Enables Buck D such that it generates voltage on the rail |
| 'd' | Buck D Disable | Disables Buck D such that it does not generate voltage on the rail |

| Response | Meaning |
| -------- | ------- |
| 'A' | Acknowledge: Message received and acted upon |
| 'N' | No-Acknowledge: Message received but for one reason or another the message was not acted upon |

An example interaction between the Main Computer and the MCU is provided below:

| Command | Response | Action on MCU |
| ------- | -------- | ------------- |
| 'a' | | |
| | 'A' | Buck A is disabled |
| 'q' | | |
| | 'N' | Invalid command, no action is taken |
| 'ABCD' | | |
| | 'A' | Buck A is enabled |
| | 'A' | Buck B is enabled |
| | 'A' | Buck C is enabled |
| | 'A' | Buck D is enabled |

Note: The Main Computer should take into account a timeout in the case that the MCU is disconnected or if there is errors on the channel. The Main Computer should interpret no response as one of these two cases.

Note: No action is taken on terminating characters such as '\0' and '\n'.