
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Frame:
	hv_batt0_temp: float
	hv_batt1_temp: float
	hv_batt2_temp: float
	hv_batt3_temp: float
	hv_batt4_temp: float
	hv_batt5_temp: float
	hv_batt6_temp: float
	hv_batt7_temp: float
	hv_batt8_temp: float
	hv_batt9_temp: float
	hv_batt0_soc: float
	hv_batt1_soc: float
	hv_batt2_soc: float
	hv_batt3_soc: float
	hv_batt4_soc: float
	hv_batt5_soc: float
	hv_batt6_soc: float
	hv_batt7_soc: float
	hv_batt8_soc: float
	hv_batt9_soc: float
	hv_voltage: float 
	hv_current: float
	unused: float
	lv_batt_temp: float
	lv_batt_soc: float
	lv_batt_current: float
	lv_voltage: float
	lv_PCB_temp: float

	@classmethod
	def from_bytearray(cls, data: bytearray) -> Frame:
		frame = Frame(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20], data[21], data[22], data[23], data[24], data[25], data[26], data[27])
		return frame