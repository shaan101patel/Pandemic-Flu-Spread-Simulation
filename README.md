# Pandemic Flu Spread Simulation

## Overview

This project implements an advanced agent-based simulation model to study pandemic influenza spread across a population. The model incorporates spatial heterogeneity, realistic movement patterns, demographic diversity, and various intervention strategies to analyze epidemic dynamics and inform public health policy decisions.

The goal is to simulate the spread of pandemic flu within a large, spatially explicit population using an agent-based approach. The model allows for investigation of infection dynamics, intervention strategies, and vaccination logistics, providing a rigorous platform for quantitative analysis and policy exploration.

## Features

### Core Capabilities
- **Agent-Based Modeling**: Individual agents with demographics (age, health status, occupation)
- **Spatial Structure**: 10×10 grid with diverse location types (homes, workplaces, schools, hospitals, public spaces)
- **SEIR Disease Model**: Susceptible → Exposed → Infectious → Recovered dynamics
- **Realistic Contact Networks**: Age-structured mixing patterns and location-specific transmission
- **Hospital Capacity Constraints**: Limited beds affecting mortality outcomes

### Intervention Strategies
- **Social Distancing**: Reduce contact rates between individuals
- **Vaccination Campaigns**: Prioritized immunization programs
- **School Closures**: Reduce transmission among children
- **Workplace Closures**: Balance economic and health impacts
- **Public Space Restrictions**: Limit high-density gatherings

### Analysis Tools
- **Monte Carlo Simulation**: 100+ runs for statistical confidence
- **Parameter Optimization**: Find optimal intervention strategies
- **Sensitivity Analysis**: Identify key parameters affecting outcomes
- **Cost-Effectiveness Analysis**: Compare intervention strategies
- **Spatial Visualization**: Track geographic spread patterns

## Project Structure

```
Pandemic-Flu-Spread-Simulation/
├── src/                    # Source code
│   ├── models/            # Agent, Location, Grid, Disease models
│   ├── interventions/     # Intervention strategies
│   ├── simulation/        # Simulation engine
│   ├── analysis/          # Statistics and optimization
│   ├── visualization/     # Plotting and dashboards
│   └── utils/             # Configuration and utilities
├── config/                # Configuration files
├── tests/                 # Unit and integration tests
├── notebooks/             # Example Jupyter notebooks
├── data/                  # Input and processed data
├── results/               # Simulation outputs
└── docs/                  # Documentation
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/shaan101patel/Pandemic-Flu-Spread-Simulation.git
cd Pandemic-Flu-Spread-Simulation
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Run a Basic Simulation
```bash
python src/main.py --config config/simulation_config.yaml
```

### Run Monte Carlo Analysis
```bash
python src/main.py --config config/simulation_config.yaml --runs 100
```

### Compare Intervention Strategies
```bash
python src/main.py --compare-interventions --output results/comparison/
```

### Interactive Analysis (Jupyter)
```bash
jupyter notebook notebooks/simulation_example.py
```

## Configuration

Edit `config/simulation_config.yaml` to customize:
- Population size and demographics
- Disease transmission parameters
- Spatial grid dimensions
- Intervention strategies and timing
- Output preferences

Example configuration snippet:
```yaml
population:
  total_agents: 1000
  age_distribution:
    children: 0.20
    adults: 0.60
    elderly: 0.20

disease:
  transmission_probability:
    base: 0.05
    home: 0.15
    workplace: 0.08

interventions:
  social_distancing:
    enabled: true
    start_day: 30
    contact_reduction: 0.50
```

## Key Metrics

The simulation tracks:
- **Epidemic Metrics**: Total infections, attack rate, peak infections
- **Health Outcomes**: Deaths, hospitalizations, recovery rates
- **Healthcare Impact**: Hospital bed occupancy, ICU utilization
- **Intervention Effects**: R₀/Rₜ, infections averted, deaths prevented
- **Spatial Patterns**: Geographic clusters, spread velocity

## Visualization

The project generates various visualizations:
- **SEIR Curves**: Disease state progression over time
- **Epidemic Curves**: Daily new infections ("flatten the curve")
- **Hospital Occupancy**: Track healthcare system strain
- **Spatial Heatmaps**: Geographic spread patterns
- **Contact Networks**: Transmission chains and superspreaders
- **Intervention Comparisons**: Side-by-side scenario analysis
- **Monte Carlo Distributions**: Confidence intervals and uncertainty

## Testing

Run the test suite:
```bash
pytest tests/
```

Tests cover:
- Unit tests for individual components
- Integration tests for full simulation
- SEIR conservation validation
- Reproducibility checks
- Intervention effectiveness verification

## Research Applications

This simulation framework supports:
- **Policy Analysis**: Compare intervention strategies and timing
- **Resource Allocation**: Optimize hospital capacity and vaccination distribution
- **Equity Assessment**: Analyze disparate impacts across demographics
- **Preparedness Planning**: Identify vulnerabilities and bottlenecks
- **Scenario Exploration**: "What-if" analysis for various outbreak conditions

## Implementation Status

**Current Status**: Complete project architecture with detailed method specifications

All classes include **advanced implementation comments** describing:
- Required data structures and algorithms
- Edge cases and error handling
- Optimization opportunities
- Validation approaches
- Research considerations

**Next Steps**: Implement actual code following the detailed specifications

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## References

1. Ferguson et al. (2006). "Strategies for mitigating an influenza pandemic." *Nature*.
2. Halloran et al. (2008). "Modeling targeted layered containment of an influenza pandemic." *PNAS*.
3. Eubank et al. (2004). "Modelling disease outbreaks in realistic urban social networks." *Nature*.

## Acknowledgments

This project implements concepts from epidemiological modeling, agent-based simulation, and operations research literature. See documentation for detailed references.

---

**Version**: 1.0.0  
**Last Updated**: October 2025  
**Status**: Architecture Complete - Implementation In Progress  
**First Commit**: 10/7/25