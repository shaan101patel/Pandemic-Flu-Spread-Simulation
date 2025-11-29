"""
Main Entry Point

This script provides the main entry point for running simulations.
"""
import numpy as np


import models.agent as agent
import models.hospital as hospital
import models.grid as grid
from simulation.engine import create_hospitals
from simulation.engine import create_agents
from simulation.engine import step
from simulation.engine import collect_stats

# Optional pygame visualization
try:
    from visulation.pygame_visualizer import run as run_visualizer
    VIS_AVAILABLE = True
except Exception:
    VIS_AVAILABLE = False


def main():
    """
    Main function to run the pandemic simulation.
    """

    # Init 
    StateSpace = 40
    NumOfHospitals = 4
    NumAgents = 300
    SickPeople = 5

    # Create grid and hospitals
    map = grid.Grid(StateSpace, StateSpace)

    hospitals = create_hospitals(NumOfHospitals, StateSpace, NumAgents)
    agents = create_agents(NumAgents, StateSpace, NumSick=SickPeople)
    
    # Add hospitals and agents to grid
    for idx, hosp in enumerate(hospitals):
        x, y = hosp.location
        map.addHospital(x, y, idx)

    for ag in agents:
        x, y = ag.location
        map.addAgent(x, y, ag.id)


    print("Initial Grid State:")
    print(map)

    # --- Minimal step function for demo/visualization ---
    def step_fn():
        return step(agents, hospitals, map, StateSpace)

    # Toggle to enable vis 
    ENABLE_VISUALIZATION = True

    if ENABLE_VISUALIZATION and VIS_AVAILABLE:
        # Run a simple visualization loop for a fixed number of steps.
        # Close the window to stop early.
        run_visualizer(
            grid=map,
            agents=agents,
            hospitals=hospitals,
            steps=365,
            cell_size=20,
            fps=8,
            step_fn=step_fn,
        )
    else:
        # Fallback: run a handful of steps headlessly and print the grid
        for i in range(10):
            should_continue = step_fn()
            if should_continue is False:
                print(f"Simulation ended early at step {i}: All agents are healthy, immune, or infected.")
                break
        print("Final Grid State (headless run):")
        print(map)
        
    # Collect and Print Stats
    stats = collect_stats(agents, hospitals)
    
    print("\n" + "="*50)
    print("SIMULATION REPORT")
    print("="*50)
    
    print("\n1. INFECTION & MORTALITY")
    print(f"Total Population: {stats['total_population']}")
    print(f"Total Infected: {stats['total_infected']}")
    print(f"Total Deaths: {stats['total_deaths']}")
    
    inf_rate = (stats['total_infected'] / stats['total_population']) * 100 if stats['total_population'] > 0 else 0
    mort_rate = (stats['total_deaths'] / stats['total_infected']) * 100 if stats['total_infected'] > 0 else 0
    print(f"Infection Rate: {inf_rate:.2f}%")
    print(f"Mortality Rate: {mort_rate:.2f}%")
    print(f"Transmission Rate: N/A (Requires contact tracing)")

    print("\n2. VACCINATION STATUS")
    print(f"Fully Vaccinated (2 doses): {stats['vaccination_status'][2]}")
    print(f"Partially Vaccinated (1 dose): {stats['vaccination_status'][1]}")
    print(f"Unvaccinated (0 doses): {stats['vaccination_status'][0]}")
    
    stockout_pct = (stats['hospital_stats']['stockouts'] / stats['hospital_stats']['requests']) * 100 if stats['hospital_stats']['requests'] > 0 else 0
    print(f"Vaccine Supply Issues (Stockouts): {stockout_pct:.2f}% ({stats['hospital_stats']['stockouts']}/{stats['hospital_stats']['requests']})")

    print("\n3. IMMUNITY BREAKDOWN")
    print(f"Total Immune: {stats['immunity_breakdown']['total']}")
    print(f"  - Vaccine-induced: {stats['immunity_breakdown']['vaccine']}")
    print(f"  - Natural Recovery: {stats['immunity_breakdown']['natural']}")
    print(f"  - Hospital Treatment: {stats['immunity_breakdown']['treatment']}")

    print("\n4. DEMOGRAPHICS & RISK ANALYSIS")
    print("Deaths by Vaccination Status:")
    print(f"  - Unvaccinated: {stats['deaths_by_vax'][0]}")
    print(f"  - Partially Vaccinated: {stats['deaths_by_vax'][1]}")
    print(f"  - Fully Vaccinated (Breakthrough): {stats['deaths_by_vax'][2]}")
    
    print("\nAge-Stratified Stats:")
    print(f"{'Age Group':<10} | {'Infected':<10} | {'Deaths':<10} | {'Mortality %':<12}")
    print("-" * 50)
    for bucket, data in stats['age_stats'].items():
        m_rate = (data['deaths'] / data['infected']) * 100 if data['infected'] > 0 else 0
        print(f"{bucket:<10} | {data['infected']:<10} | {data['deaths']:<10} | {m_rate:.2f}%")
    print("="*50 + "\n")

    pass

 
def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    
    Advanced Implementation Notes:
        - Use argparse for clean CLI
        - Arguments:
            --config: path to config file
            --runs: number of Monte Carlo runs
            --output: output directory
            --seed: random seed
            --interventions: which interventions to enable
            --parallel: number of parallel processes
        - Provide helpful defaults
        - Validate arguments
    """
    pass


def run_single_simulation(config_path, output_dir):
    """
    Run a single simulation with given configuration.
    
    Args:
        config_path (str): Path to configuration file
        output_dir (str): Directory to save results
    
    Advanced Implementation Notes:
        - Load configuration
        - Create simulation
        - Run simulation
        - Collect results
        - Generate plots
        - Save everything
        - Quick way to run one simulation
    """
    pass


def run_monte_carlo_analysis(config_path, num_runs, output_dir):
    """
    Run Monte Carlo analysis with multiple replications.
    
    Args:
        config_path (str): Path to configuration file
        num_runs (int): Number of replications
        output_dir (str): Directory to save results
    
    Advanced Implementation Notes:
        - Run multiple simulations with different seeds
        - Aggregate results
        - Calculate confidence intervals
        - Generate comparison plots
        - More robust than single run
        - Can parallelize across runs
    """
    pass


def run_intervention_comparison(config_path, interventions, output_dir):
    """
    Compare different intervention strategies.
    
    Args:
        config_path (str): Path to base configuration
        interventions (list): List of intervention configurations
        output_dir (str): Directory to save results
    
    Advanced Implementation Notes:
        - Run baseline (no interventions)
        - Run with each intervention strategy
        - Compare outcomes
        - Cost-effectiveness analysis
        - Generate comparison plots
        - Policy-relevant analysis
    """
    pass


def run_parameter_sweep(config_path, parameter_ranges, output_dir):
    """
    Run parameter sweep to explore sensitivity.
    
    Args:
        config_path (str): Path to base configuration
        parameter_ranges (dict): Parameters to vary
        output_dir (str): Directory to save results
    
    Advanced Implementation Notes:
        - Grid or random search over parameters
        - Run simulation for each parameter combination
        - Analyze sensitivity
        - Find optimal parameters
        - Generate sensitivity plots
        - Computationally intensive
    """
    pass


def run_optimization(config_path, optimization_type, output_dir):
    """
    Run optimization to find best intervention strategy.
    
    Args:
        config_path (str): Path to base configuration
        optimization_type (str): Type of optimization
        output_dir (str): Directory to save results
    
    Advanced Implementation Notes:
        - Optimize intervention timing, intensity, or portfolio
        - Use appropriate optimization algorithm
        - Save optimal parameters
        - Validate with additional runs
        - Report findings
    """
    pass


if __name__ == "__main__":
    """
    Script entry point.
    
    Advanced Implementation Notes:
        - Call main() function
        - Handle exceptions gracefully
        - Exit with appropriate code
    """
    main()
