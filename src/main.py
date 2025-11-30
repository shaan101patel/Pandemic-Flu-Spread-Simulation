"""
Main Entry Point

This script provides the main entry point for running simulations.
"""
import numpy as np
import pandas as pd
import os

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



def run_monte_carlo_analysis(num_runs=50, output_dir="results"):
    """
    Run Monte Carlo analysis with multiple replications.
    """
    print(f"Starting Monte Carlo Analysis with {num_runs} runs...")
    
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Simulation Parameters
    StateSpace = 40
    NumOfHospitals = 4
    NumAgents = 300
    SickPeople = 5
    MaxSteps = 365

    # Storage for all run data
    all_run_data = []

    for run_id in range(num_runs):
        # Initialize Simulation
        map_grid = grid.Grid(StateSpace, StateSpace)
        hospitals = create_hospitals(NumOfHospitals, StateSpace, NumAgents)
        agents = create_agents(NumAgents, StateSpace, NumSick=SickPeople)
        
        # Initial grid population
        for idx, hosp in enumerate(hospitals):
            x, y = hosp.location
            map_grid.addHospital(x, y, idx)
        for ag in agents:
            x, y = ag.location
            map_grid.addAgent(x, y, ag.id)

        # Run Simulation Loop
        for _ in range(MaxSteps):
            should_continue = step(agents, hospitals, map_grid, StateSpace)
            if not should_continue:
                break
        
        # Collect Stats
        stats = collect_stats(agents, hospitals)
        
        # Flatten stats for DataFrame
        row = {
            "Run ID": run_id + 1,
            "Total Population": stats["total_population"],
            "Total Infected": stats["total_infected"],
            "Total Deaths": stats["total_deaths"],
            "Infection Rate (%)": (stats["total_infected"] / stats["total_population"] * 100) if stats["total_population"] else 0,
            "Mortality Rate (%)": (stats["total_deaths"] / stats["total_infected"] * 100) if stats["total_infected"] else 0,
            "Fully Vaccinated": stats["vaccination_status"][2],
            "Partially Vaccinated": stats["vaccination_status"][1],
            "Unvaccinated": stats["vaccination_status"][0],
            "Vaccine Stockout (%)": (stats["hospital_stats"]["stockouts"] / stats["hospital_stats"]["requests"] * 100) if stats["hospital_stats"]["requests"] else 0,
            "Total Immune": stats["immunity_breakdown"]["total"],
            "Immune (Vaccine)": stats["immunity_breakdown"]["vaccine"],
            "Immune (Natural)": stats["immunity_breakdown"]["natural"],
            "Immune (Treatment)": stats["immunity_breakdown"]["treatment"],
            "Deaths (Unvaccinated)": stats["deaths_by_vax"][0],
            "Deaths (Partial)": stats["deaths_by_vax"][1],
            "Deaths (Full)": stats["deaths_by_vax"][2],
        }

        # Add Age Stats
        for bucket, data in stats["age_stats"].items():
            row[f"Age {bucket} Total"] = data["total"]
            row[f"Age {bucket} Infected"] = data["infected"]
            row[f"Age {bucket} Deaths"] = data["deaths"]
            row[f"Age {bucket} Mortality (%)"] = (data["deaths"] / data["infected"] * 100) if data["infected"] else 0
            
        all_run_data.append(row)
        
        if (run_id + 1) % 10 == 0:
            print(f"Run {run_id + 1}/{num_runs} completed.")

    # Create DataFrame
    df = pd.DataFrame(all_run_data)
    
    # Save to Excel/CSV
    if output_dir:
        excel_path = os.path.join(output_dir, "monte_carlo_results.xlsx")
        csv_path = os.path.join(output_dir, "monte_carlo_results.csv")
    else:
        excel_path = "monte_carlo_results.xlsx"
        csv_path = "monte_carlo_results.csv"

    try:
        df.to_excel(excel_path, index=False)
        print(f"\nResults saved to {excel_path}")
    except Exception as e:
        print(f"\nCould not save to Excel (missing openpyxl?): {e}")
        df.to_csv(csv_path, index=False)
        print(f"Results saved to {csv_path} instead.")

    # Report Summary Statistics to Console
    print("\n" + "="*60)
    print(f"MONTE CARLO ANALYSIS SUMMARY ({num_runs} Runs)")
    print("="*60)
    
    summary_cols = ["Total Infected", "Total Deaths", "Infection Rate (%)", "Mortality Rate (%)", "Fully Vaccinated", "Vaccine Stockout (%)"]
    print(f"{'Metric':<25} | {'Mean':<10} | {'Std Dev':<10} | {'Min':<10} | {'Max':<10}")
    print("-" * 75)
    
    for col in summary_cols:
        if col in df.columns:
            values = df[col]
            print(f"{col:<25} | {values.mean():<10.2f} | {values.std():<10.2f} | {values.min():<10.2f} | {values.max():<10.2f}")
    
    print("="*60 + "\n")






if __name__ == "__main__":
    # Uncomment to run Monte Carlo Analysis
    run_monte_carlo_analysis(num_runs=10)
    # main()
