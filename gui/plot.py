import pyqtgraph as pg
import random

class Plot(pg.PlotWidget):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setBackground(None)

class VPlot(Plot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
  def enable_288V(self) -> None:
      pass
  
  def disable_288V(self) -> None:
    pass


class VLinePlot(VPlot):
  u1_line: pg.PlotItem
  u2_line: pg.PlotItem
  u3_line: pg.PlotItem
  u4_line: pg.PlotItem
  rail_line: pg.PlotItem
  hvbattery_line: pg.PlotItem
  lvbattery_line: pg.PlotItem

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLabel("bottom", "Time", units="s", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setLabel("left", "Voltage", units="V", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setTitle("Voltage sensors over time", **{'size': '18pt'})
    self.setYRange(0, 50, padding=0)
    self.showGrid(x=True, y=True, alpha=0.2)
    self.addLegend(colCount=2)
    self.u1_line = self.plot([x for x in range(1, 10)], [random.randint(20, 28) for _ in range(1, 10)], name="U1", pen=pg.mkPen(color=(255, 0, 0)))
    self.u2_line = self.plot([x for x in range(1, 10)], [random.randint(8, 16) for _ in range(1, 10)], name="U2", pen=pg.mkPen(color=(255, 50, 0)))
    self.u3_line = self.plot([x for x in range(1, 10)], [random.randint(1, 9) for _ in range(1, 10)], name="U3", pen=pg.mkPen(color=(255, 100, 0)))
    self.u4_line = self.plot([x for x in range(1, 10)], [random.randint(8, 16) for _ in range(1, 10)], name="U4", pen=pg.mkPen(color=(255, 150, 0)))
    self.rail_line = self.plot([x for x in range(1, 10)], [random.randint(32, 40) for _ in range(1, 10)], name="Power Rail", pen=pg.mkPen(color=(0, 150, 0)))
    self.hvbattery_line = self.plot([x for x in range(1, 10)], [random.randint(284, 292) for _ in range(1, 10)], name="HV Battery", pen=pg.mkPen(color=(0, 255, 100)))
    self.lvbattery_line = self.plot([x for x in range(1, 10)], [random.randint(17, 29) for _ in range(1, 10)], name="LV Battery", pen=pg.mkPen(color=(100, 255, 0)))
  
  def enable_288V(self) -> None:
    self.setYRange(0, 320, padding=0)

  def disable_288V(self) -> None:
    self.setYRange(0, 50, padding=0)


class VBarPlot(VPlot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLabel("bottom", "Voltage Sensors", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setLabel("left", "Voltage", units="V", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setTitle("Voltage sensors", **{'size': '18pt'})
    self.setYRange(0, 50, padding=0)
    self.showGrid(x=True, y=True, alpha=0.2)
    self.voltages = [24, 12, 5, 12, 36, 25]
    self.bars: pg.BarGraphItem = pg.BarGraphItem(x=[x for x in range(1, len(self.voltages) + 1)], height=self.voltages, width=0.5, brush=(121, 195, 119))
    self.addItem(self.bars)
    self.getAxis('bottom').setTicks([ [(1, "U1"), (2, "U2"), (3, "U3"), (4, "U4"), (5, "RAIL"), (6, "LVB")] ])
    for i in range(1, len(self.voltages) + 1):
      label = pg.TextItem(text=str(self.voltages[i - 1])+"V", anchor=(0.5,1), color=(0, 0, 0), border='w', fill=(255, 255, 255, 100))
      self.addItem(label)
      label.setPos(i, self.voltages[i - 1] + 1)
  
  def enable_288V(self) -> None:
    self.setYRange(0, 320, padding=0)
    self.clear()

    self.voltages = [24, 12, 5, 12, 36, 25, 288]
    self.bars: pg.BarGraphItem = pg.BarGraphItem(x=[x for x in range(1, len(self.voltages) + 1)], height=self.voltages, width=0.5, brush=(121, 195, 119))
    self.addItem(self.bars)
    self.getAxis('bottom').setTicks([ [(1, "U1"), (2, "U2"), (3, "U3"), (4, "U4"), (5, "RAIL"),  (6, "LVB"), (7, "HVB")] ])
    for i in range(1, len(self.voltages) + 1):
      label = pg.TextItem(text=str(self.voltages[i - 1])+"V", anchor=(0.5,1), color=(0, 0, 0), border='w', fill=(255, 255, 255, 100))
      self.addItem(label)
      label.setPos(i, self.voltages[i - 1] + 1)
  
  def disable_288V(self) -> None:
    self.setYRange(0, 50, padding=0)
    self.clear()

    self.voltages = [24, 12, 5, 12, 36, 25]
    self.bars: pg.BarGraphItem = pg.BarGraphItem(x=[x for x in range(1, len(self.voltages) + 1)], height=self.voltages, width=0.5, brush=(121, 195, 119))
    self.addItem(self.bars)
    self.getAxis('bottom').setTicks([ [(1, "U1"), (2, "U2"), (3, "U3"), (4, "U4"), (5, "RAIL"), (6, "LVB")] ])
    for i in range(1, len(self.voltages) + 1):
      label = pg.TextItem(text=str(self.voltages[i - 1])+"V", anchor=(0.5,1), color=(0, 0, 0), border='w', fill=(255, 255, 255, 100))
      self.addItem(label)
      label.setPos(i, self.voltages[i - 1] + 1)
  

class TLinePlot(Plot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLabel("bottom", "Time", units="s", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setLabel("left", "Temperature", units="°C", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setTitle("Temperature sensors over time", **{'size': '18pt'})
    self.setYRange(20, 70, padding=0)
    self.showGrid(x=True, y=True, alpha=0.2)
    self.addLegend(colCount=3)
    self.hvbattery1_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 1", pen=pg.mkPen(color=(255, 0, 0)))
    self.hvbattery2_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 2", pen=pg.mkPen(color=(255, 20, 0)))
    self.hvbattery3_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 3", pen=pg.mkPen(color=(255, 40, 0)))
    self.hvbattery4_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 4", pen=pg.mkPen(color=(255, 60, 0)))
    self.hvbattery5_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 5", pen=pg.mkPen(color=(255, 80, 0)))
    self.hvbattery6_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 6", pen=pg.mkPen(color=(255, 100, 0)))
    self.hvbattery7_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 7", pen=pg.mkPen(color=(255, 120, 0)))
    self.hvbattery8_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 8", pen=pg.mkPen(color=(255, 140, 0)))
    self.hvbattery9_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 9", pen=pg.mkPen(color=(255, 160, 0)))
    self.hvbattery10_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 10", pen=pg.mkPen(color=(255, 180, 0)))
    self.lvbattery_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="LV Battery", pen=pg.mkPen(color=(0, 255, 0)))
    self.pcb_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="PCB", pen=pg.mkPen(color=(255, 255, 0)))

class TBarPlot(Plot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLabel("bottom", "Temperature Sensors", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setLabel("left", "Temperature", units="°C", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setTitle("Temperature Sensors", **{'size': '18pt'})
    self.setYRange(20, 70, padding=0)
    self.showGrid(x=True, y=True, alpha=0.2)
    self.temps = [random.randint(30, 50) for _ in range(1, 13)]
    self.bars :pg.BarGraphItem = pg.BarGraphItem(x=[x for x in range(1, len(self.temps) + 1)], height=self.temps, width=0.5, brush=(121, 195, 119))
    self.addItem(self.bars)
    self.getAxis('bottom').setTicks([ [(1, "HV1"), (2, "HV2"), (3, "HV3"), (4, "HV4"), (5, "HV5"), (6, "HV6"), (7, "HV7"), (8, "HV8"), (9, "HV9"), (10, "HV10"), (11, "LVB"), (12, "PCB")] ])
    for i in range(1, 13):
      label = pg.TextItem(text=str(self.temps[i - 1])+"C", anchor=(0.5,1), color=(0, 0, 0), border='w', fill=(255, 255, 255, 100))
      self.addItem(label)
      label.setPos(i, self.temps[i - 1] + 1)

class CLinePlot(Plot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setLabel("bottom", "Time", units="s", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setLabel("left", "Current", units="A", **{'font-size': '16pt', 'color': 'grey', 'font-weight': 'bold'})
    self.setTitle("Temperature sensors over time", **{'size': '18pt'})
    # self.setYRange(0, 5, padding=0)
    self.showGrid(x=True, y=True, alpha=0.2)
    self.addLegend(colCount=1)

    self.lvcurrent_line = self.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="LV Current", pen=pg.mkPen(color=(0, 255, 0)))
    self.hvcurrent_line = self.plot([x for x in range(1, 10)], [random.randint(60, 80) for _ in range(1, 10)], name="HV Current", pen=pg.mkPen(color=(255, 0, 0)))