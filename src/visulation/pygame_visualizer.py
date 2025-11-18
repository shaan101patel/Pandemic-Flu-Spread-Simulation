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
    # Draw agents as circles; if multiple agents share a cell, we'll slightly jitter positions
    # within the cell for visibility.
    offsets = [(-0.2, -0.2), (0.2, -0.2), (-0.2, 0.2), (0.2, 0.2), (0.0, 0.0)]
    per_cell_counts = {}
    r = max(3, cell_size // 4)

    for ag in agents:
        x, y = ag.location
        count = per_cell_counts.get((x, y), 0)
        per_cell_counts[(x, y)] = count + 1
        dx, dy = offsets[count % len(offsets)]
        cx = int((x + 0.5 + dx) * cell_size)
        cy = int((y + 0.5 + dy) * cell_size)
        pygame.draw.circle(surface, RED, (cx, cy), r)


def run(
    grid,
    agents,
    hospitals,
    steps: int = 300,
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

            pygame.display.flip()
            clock.tick(fps)
            frame += 1
    finally:
        pygame.quit()
