from typing import List, Optional
import pyqtgraph as pg
import random

class Plot(pg.PlotWidget):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setBackground(None)

class LinePlot(Plot):
  # The maximum number of points shown on the plot at any given time
  dataline_len = 30
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
  def advance_dataline(self, xs: list, ys: list, dataline: pg.PlotItem, new_x, new_y) -> None:
    if len(xs) >= LinePlot.dataline_len:
      xs.pop(0)
      ys.pop(0)
    
    xs.append(new_x)
    ys.append(new_y)

    dataline.setData(xs, ys)

class BarPlot(Plot):
  unit = ''
  rgb_green = (121, 195, 119)
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.bars = None
    self.data = []
    self.labels: List[pg.TextItem] = []
    self.colors = []
  
  def set_bar_data(self, i: int, new_y) -> None:
    self.data[i] = new_y
    self.bars.setOpts(height=self.data)
    self.set_bar_label(i, self.unit)
  
  def set_bar_label(self, i: int, unit: str) -> None:
    label = pg.TextItem(text=str(self.data[i])+unit, anchor=(0.5,1), color=(0, 0, 0), border='w', fill=(255, 255, 255, 100))
    if (len(self.labels) > i):
      self.removeItem(self.labels[i])
      self.labels[i] = label
    else:
      self.labels.append(label)
    self.addItem(label)
    label.setPos(i + 1, self.data[i] + 1)

  def set_bar_labels(self) -> None: 
    for i in range(len(self.data)):
      self.set_bar_label(i, self.unit)

class VPlot(Plot):
  # Expected voltages should be within 5%
  U1_EXPECTED_V = 24
  U2_EXPECTED_V = 12
  U3_EXPECTED_V = 5
  U4_EXPECTED_V = 12
  RAIL_EXPECTED_V = 36
  HV_EXPECTED_V = 288
  # Expected LV voltage should be between 12 and 29
  LV_EXPECTED_V_LOW = 12
  LV_EXPECTED_V_HIGH = 29
  unit='V'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
  def enable_288V(self) -> None:
      pass
  
  def disable_288V(self) -> None:
    pass

class TPlot(Plot):
  # thresholds for temps in celsius.
  TEMP_THRESHOLD_WARNING = 50
  TEMP_THRESHOLD_MAX = 60
  unit='c'
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  


class VLinePlot(VPlot, LinePlot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLabel("bottom", "Time", units="s", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setLabel("left", "Voltage", units="V", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setTitle("Voltage sensors over time", **{'size': '18pt'})
    self.setYRange(0, 50, padding=0)
    self.showGrid(x=True, y=True, alpha=0.2)
    self.addLegend(colCount=2)
    self.u1_y = [random.randint(20, 28) for _ in range(1, LinePlot.dataline_len)]
    self.u1_line = self.plot([x for x in range(1, LinePlot.dataline_len)], self.u1_y, name="U1", pen=pg.mkPen(color=(255, 0, 0)))
    self.u2_y = [random.randint(8, 16) for _ in range(1, LinePlot.dataline_len)]
    self.u2_line = self.plot([x for x in range(1, LinePlot.dataline_len)], self.u2_y, name="U2", pen=pg.mkPen(color=(255, 50, 0)))
    self.u3_line = [random.randint(1, 9) for _ in range(1, LinePlot.dataline_len)]
    self.u3_line = self.plot([x for x in range(1, LinePlot.dataline_len)], self.u3_line, name="U3", pen=pg.mkPen(color=(255, 100, 0)))
    self.u4_line = [random.randint(8, 16) for _ in range(1, LinePlot.dataline_len)]
    self.u4_line = self.plot([x for x in range(1, LinePlot.dataline_len)], self.u4_line, name="U4", pen=pg.mkPen(color=(255, 150, 0)))
    self.rail_y = [random.randint(32, 40) for _ in range(1, LinePlot.dataline_len)]
    self.rail_line = self.plot([x for x in range(1, LinePlot.dataline_len)], self.rail_y, name="Power Rail", pen=pg.mkPen(color=(0, 150, 0)))
    self.hvbattery_y = [random.randint(284, 292) for _ in range(1, LinePlot.dataline_len)]
    self.hvbattery_line = self.plot([x for x in range(1, LinePlot.dataline_len)], self.hvbattery_y, name="HV Battery", pen=pg.mkPen(color=(0, 255, 100)))
    self.lvbattery_y = [random.randint(17, 29) for _ in range(1, LinePlot.dataline_len)]
    self.lvbattery_line = self.plot([x for x in range(1, LinePlot.dataline_len)], self.lvbattery_y, name="LV Battery", pen=pg.mkPen(color=(100, 255, 0)))
  
  def enable_288V(self) -> None:
    self.setYRange(0, 320, padding=0)

  def disable_288V(self) -> None:
    self.setYRange(0, 50, padding=0)


class VBarPlot(VPlot, BarPlot):
  u1_i = 0
  u2_i = 1
  u3_i = 2
  u4_i = 3
  rail_i = 4
  lvbattery_i = 5
  hvbattery_i = 6

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLabel("bottom", "Voltage Sensors", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setLabel("left", "Voltage", units="V", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setTitle("Voltage sensors", **{'size': '18pt'})
    self.setYRange(0, 50, padding=0)
    self.showGrid(x=True, y=True, alpha=0.2)
    self.data = [24, 12, 5, 12, 36, 25]
    self.colors = [self.rgb_green for _ in range(len(self.data))]
    self.bars: pg.BarGraphItem = pg.BarGraphItem(x=[x for x in range(1, len(self.data) + 1)], height=self.data, width=0.5, brushes=self.colors)
    self.addItem(self.bars)
    self.getAxis('bottom').setTicks([ [(1, "U1"), (2, "U2"), (3, "U3"), (4, "U4"), (5, "RAIL"), (6, "LVB")] ])
    self.set_bar_labels()
  
  def set_bar_data(self, i: int, new_y) -> None:
    super().set_bar_data(i, new_y)
    # TODO: change colors based on acceptable thresholds
  
  def enable_288V(self) -> None:
    self.setYRange(0, 320, padding=0)
    self.clear()

    self.data = [24, 12, 5, 12, 36, 25, 288]
    self.colors = [self.rgb_green for _ in range(len(self.data))]
    self.bars: pg.BarGraphItem = pg.BarGraphItem(x=[x for x in range(1, len(self.data) + 1)], height=self.data, width=0.5, brushes=self.colors)
    self.addItem(self.bars)
    self.getAxis('bottom').setTicks([ [(1, "U1"), (2, "U2"), (3, "U3"), (4, "U4"), (5, "RAIL"),  (6, "LVB"), (7, "HVB")] ])
    self.set_bar_labels()
  
  def disable_288V(self) -> None:
    self.setYRange(0, 50, padding=0)
    self.clear()

    self.data = [24, 12, 5, 12, 36, 25]
    self.colors = [self.rgb_green for _ in range(len(self.data))]
    self.bars: pg.BarGraphItem = pg.BarGraphItem(x=[x for x in range(1, len(self.data) + 1)], height=self.data, width=0.5, brushes=self.colors)
    self.addItem(self.bars)
    self.getAxis('bottom').setTicks([ [(1, "U1"), (2, "U2"), (3, "U3"), (4, "U4"), (5, "RAIL"), (6, "LVB")] ])
    self.set_bar_labels()
  

class TLinePlot(LinePlot, TPlot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLabel("bottom", "Time", units="s", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setLabel("left", "Temperature", units="°C", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setTitle("Temperature sensors over time", **{'size': '18pt'})
    self.setYRange(20, 70, padding=0)
    self.showGrid(x=True, y=True, alpha=0.2)
    self.addLegend(colCount=3)
    self.hvbattery1_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="HV Battery 1", pen=pg.mkPen(color=(255, 0, 0)))
    self.hvbattery2_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="HV Battery 2", pen=pg.mkPen(color=(255, 20, 0)))
    self.hvbattery3_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="HV Battery 3", pen=pg.mkPen(color=(255, 40, 0)))
    self.hvbattery4_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="HV Battery 4", pen=pg.mkPen(color=(255, 60, 0)))
    self.hvbattery5_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="HV Battery 5", pen=pg.mkPen(color=(255, 80, 0)))
    self.hvbattery6_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="HV Battery 6", pen=pg.mkPen(color=(255, 100, 0)))
    self.hvbattery7_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="HV Battery 7", pen=pg.mkPen(color=(255, 120, 0)))
    self.hvbattery8_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="HV Battery 8", pen=pg.mkPen(color=(255, 140, 0)))
    self.hvbattery9_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="HV Battery 9", pen=pg.mkPen(color=(255, 160, 0)))
    self.hvbattery10_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="HV Battery 10", pen=pg.mkPen(color=(255, 180, 0)))
    self.lvbattery_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="LV Battery", pen=pg.mkPen(color=(0, 255, 0)))
    self.pcb_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="PCB", pen=pg.mkPen(color=(255, 255, 0)))

class TBarPlot(BarPlot, TPlot):
  hvbattery1_i = 0
  hvbattery2_i = 1
  hvbattery3_i = 2
  hvbattery4_i = 3
  hvbattery5_i = 4
  hvbattery6_i = 5
  hvbattery7_i = 6
  hvbattery8_i = 7
  hvbattery9_i = 8
  hvbattery10_i = 9
  lvbattery_i = 10
  pcb_i = 11
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLabel("bottom", "Temperature Sensors", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setLabel("left", "Temperature", units="°C", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setTitle("Temperature Sensors", **{'size': '18pt'})
    self.setYRange(20, 70, padding=0)
    self.showGrid(x=True, y=True, alpha=0.2)
    self.data = [random.randint(30, 50) for _ in range(1, 13)]
    self.colors = [(121, 195, 119) for _ in range(len(self.data))]
    self.bars :pg.BarGraphItem = pg.BarGraphItem(x=[x for x in range(1, len(self.data) + 1)], height=self.data, width=0.5, brushes=self.colors)
    self.addItem(self.bars)
    self.getAxis('bottom').setTicks([ [(1, "HV1"), (2, "HV2"), (3, "HV3"), (4, "HV4"), (5, "HV5"), (6, "HV6"), (7, "HV7"), (8, "HV8"), (9, "HV9"), (10, "HV10"), (11, "LVB"), (12, "PCB")] ])
    self.set_bar_labels()
  
  def set_bar_data(self, i: int, new_y) -> None:
    super().set_bar_data(i, new_y)
    # TODO: change colors based on acceptable thresholds

class CLinePlot(LinePlot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLabel("bottom", "Time", units="s", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setLabel("left", "Current", units="A", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setTitle("Temperature sensors over time", **{'size': '18pt'})
    # self.setYRange(0, 5, padding=0)
    self.showGrid(x=True, y=True, alpha=0.2)
    self.addLegend(colCount=1)

    self.lvcurrent_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(20, 40) for _ in range(1, LinePlot.dataline_len)], name="LV Current", pen=pg.mkPen(color=(0, 255, 0)))
    self.hvcurrent_line = self.plot([x for x in range(1, LinePlot.dataline_len)], [random.randint(60, 80) for _ in range(1, LinePlot.dataline_len)], name="HV Current", pen=pg.mkPen(color=(255, 0, 0)))