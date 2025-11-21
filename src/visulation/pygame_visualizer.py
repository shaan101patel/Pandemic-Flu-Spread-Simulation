from __future__ import annotations

import sys
from typing import Callable, List, Tuple, Optional

import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (120, 120, 120)
BLUE = (50, 120, 220)
RED = (220, 60, 60)
GREEN = (60, 180, 75)
YELLOW = (255, 255, 0)


def _draw_grid(surface, width: int, height: int, cell_size: int) -> None:
    # Fill background
    surface.fill(WHITE)
    # Grid lines
    for x in range(width + 1):
        pygame.draw.line(surface, LIGHT_GRAY, (x * cell_size, 0), (x * cell_size, height * cell_size), 1)
    for y in range(height + 1):
        pygame.draw.line(surface, LIGHT_GRAY, (0, y * cell_size), (width * cell_size, y * cell_size), 1)


def _cell_rect(x: int, y: int, cell_size: int) -> pygame.Rect:
    return pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)


def _draw_hospitals(surface, hospitals, cell_size: int) -> None:
    for idx, hosp in enumerate(hospitals):
        x, y = hosp.location
        rect = _cell_rect(x, y, cell_size)
        pygame.draw.rect(surface, BLUE, rect)
        # Small "H" label
        font = pygame.font.SysFont(None, max(12, cell_size // 2))
        text = font.render("H", True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)


def _draw_agents(surface, agents, cell_size: int) -> None:
    # Group agents by location
    location_agents = {}
    for ag in agents:
        loc = ag.location
        if loc not in location_agents:
            location_agents[loc] = []
        location_agents[loc].append(ag)
    
    font = pygame.font.SysFont(None, int(cell_size * 0.8))

    for (x, y), ag_list in location_agents.items():
        count = len(ag_list)
        center_x = int((x + 0.5) * cell_size)
        center_y = int((y + 0.5) * cell_size)
        radius = int(cell_size * 0.4)
        
        # Determine color based on the most severe status in the cell
        # Priority: Infectious (Red) > Infected (Yellow) > Healthy (Green)
        has_infectious = any(ag.health == "infectious" for ag in ag_list)
        has_infected = any(ag.health == "infected" for ag in ag_list)
        
        if has_infectious:
            color = RED
        elif has_infected:
            color = YELLOW
        else:
            color = GREEN
        
        pygame.draw.circle(surface, color, (center_x, center_y), radius)
        
        if count > 1:
            # Draw number
            text = font.render(str(count), True, WHITE)
            text_rect = text.get_rect(center=(center_x, center_y))
            surface.blit(text, text_rect)


def _draw_step_counter(surface, step: int, width: int, cell_size: int) -> None:
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Step: {step}", True, BLACK)
    text_rect = text.get_rect(topright=(width * cell_size - 10, 10))
    surface.blit(text, text_rect)


def run(
    grid,
    agents,
    hospitals,
    steps: int = 30000,
    cell_size: int = 20,
    fps: int = 8,
    step_fn: Optional[Callable[[], None]] = None,
) -> None:
    """Run a simple visualization loop using pygame.

    Close the window or press ESC to exit early.
    """
    pygame.init()
    try:
        width, height = grid.width, grid.height
        screen = pygame.display.set_mode((width * cell_size, height * cell_size))
        pygame.display.set_caption("Pandemic Simulation")
        clock = pygame.time.Clock()

        running = True
        frame = 0
        while running and frame < steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            # Advance the simulation one step if provided
            if step_fn is not None:
                step_fn()

            # Draw
            _draw_grid(screen, width, height, cell_size)
            _draw_hospitals(screen, hospitals, cell_size)
            _draw_agents(screen, agents, cell_size)
            _draw_step_counter(screen, frame, width, cell_size)

            pygame.display.flip()
            clock.tick(fps)
            frame += 1
    finally:
        pygame.quit()
