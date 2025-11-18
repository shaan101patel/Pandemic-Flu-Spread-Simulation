"""
Example Jupyter Notebook for Running Simulations

This notebook demonstrates how to use the pandemic simulation framework.
"""

# Cell 1: Imports and Setup
"""
Import required libraries and modules.
"""
# import sys
# sys.path.append('../src')
# 
# from models import Agent, Grid, DiseaseModel
# from simulation import PandemicSimulation
# from analysis import StatisticsCollector, ParameterOptimizer
# from visualization import SimulationVisualizer
# from utils import ConfigLoader
# 
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# 
# %matplotlib inline


# Cell 2: Load Configuration
"""
Load simulation configuration from YAML file.
"""
# config_loader = ConfigLoader('../config/simulation_config.yaml')
# config = config_loader.load_config()
# print("Configuration loaded successfully")
# print(f"Population size: {config['population']['total_agents']}")
# print(f"Simulation duration: {config['simulation']['duration_days']} days")


# Cell 3: Run Baseline Simulation
"""
Run a single baseline simulation without interventions.
"""
# baseline_sim = PandemicSimulation(config)
# baseline_sim.setup()
# results_baseline = baseline_sim.run()
# print(f"Baseline simulation complete")
# print(f"Total infections: {results_baseline['total_infections']}")
# print(f"Total deaths: {results_baseline['total_deaths']}")


# Cell 4: Visualize Baseline Results
"""
Create visualizations for baseline results.
"""
# viz = SimulationVisualizer(results_baseline, config)
# 
# # SEIR curves
# viz.plot_seir_curves()
# plt.show()
# 
# # Daily new infections
# viz.plot_new_infections()
# plt.show()
# 
# # Hospital occupancy
# viz.plot_hospitalizations()
# plt.show()


# Cell 5: Run Simulation with Social Distancing
"""
Run simulation with social distancing intervention.
"""
# config_sd = config.copy()
# config_sd['interventions']['social_distancing']['enabled'] = True
# config_sd['interventions']['social_distancing']['start_day'] = 30
# 
# sd_sim = PandemicSimulation(config_sd)
# sd_sim.setup()
# results_sd = sd_sim.run()
# 
# print(f"Social distancing simulation complete")
# print(f"Total infections: {results_sd['total_infections']}")
# print(f"Reduction vs baseline: {results_baseline['total_infections'] - results_sd['total_infections']}")


# Cell 6: Compare Intervention Strategies
"""
Compare outcomes with different interventions.
"""
# # Run with vaccination
# config_vax = config.copy()
# config_vax['interventions']['vaccination']['enabled'] = True
# vax_sim = PandemicSimulation(config_vax)
# results_vax = vax_sim.run()
# 
# # Compare results
# results_dict = {
#     'Baseline': results_baseline,
#     'Social Distancing': results_sd,
#     'Vaccination': results_vax
# }
# 
# viz_compare = SimulationVisualizer(results_dict, config)
# viz_compare.plot_intervention_comparison(results_dict)
# plt.show()


# Cell 7: Monte Carlo Analysis
"""
Run multiple simulations for statistical confidence.
"""
# mc_results = []
# n_runs = 50
# 
# for i in range(n_runs):
#     config_mc = config.copy()
#     config_mc['simulation']['random_seed'] = 42 + i
#     sim = PandemicSimulation(config_mc)
#     result = sim.run()
#     mc_results.append(result)
#     print(f"Run {i+1}/{n_runs} complete")
# 
# # Visualize uncertainty
# viz_mc = SimulationVisualizer(mc_results, config)
# viz_mc.plot_monte_carlo_results(mc_results)
# plt.show()


# Cell 8: Parameter Sensitivity Analysis
"""
Analyze sensitivity to key parameters.
"""
# optimizer = ParameterOptimizer(config, objective_function=lambda x: x['total_deaths'])
# 
# parameter_ranges = {
#     'disease.transmission_probability.base': [0.03, 0.05, 0.07],
#     'interventions.social_distancing.start_day': [20, 30, 40]
# }
# 
# sensitivity_results = optimizer.sensitivity_analysis(parameter_ranges)
# 
# # Plot sensitivity
# viz.plot_sensitivity_analysis(sensitivity_results, 'transmission_probability')
# plt.show()


# Cell 9: Optimize Intervention Timing
"""
Find optimal timing for intervention activation.
"""
# optimal_timing = optimizer.optimize_intervention_timing(
#     intervention_type='social_distancing',
#     metric='total_deaths'
# )
# 
# print(f"Optimal start day: {optimal_timing['best_day']}")
# print(f"Deaths with optimal timing: {optimal_timing['best_outcome']}")


# Cell 10: Export Results
"""
Save results and visualizations for reporting.
"""
# # Export time series data
# stats = StatisticsCollector()
# stats.export_time_series('../results/baseline_timeseries.csv')
# 
# # Generate comprehensive report
# stats.generate_report('../results/simulation_report.md')
# 
# # Save all figures
# viz.plot_seir_curves(save_path='../results/seir_curves.png')
# viz.create_dashboard(save_path='../results/dashboard.png')
# 
# print("Results exported successfully")
