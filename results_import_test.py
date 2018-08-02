from simulation_data_io import SimulationDataIO
from model import Model
from simulation import Simulation
model = Model()
simulation_data_io = SimulationDataIO()
model.Model_Path = "c:\\temp\\BaseR011018V4ic"
simulation = Simulation(model.Model_Path)
simulation.storm_id = 11
simulation.scenario_id = 22
simulation.storm = "D25yr6h"
simulation.scenario = ""
simulation_data_io.copy_node_results(simulation, model)
simulation_data_io.copy_link_results(simulation, model)
simulation_data_io.copy_node_flooding_results(simulation, model)
simulation_data_io.copy_area_results(simulation, model)