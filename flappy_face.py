import random
import sys
from dataclasses import dataclass

import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
GROUND_HEIGHT = 100
PIPE_WIDTH = 80
PIPE_GAP = 180
PIPE_INTERVAL = 1500  # milliseconds
GRAVITY = 0.35
FLAP_STRENGTH = -7.5
MAX_FALL_SPEED = 9


@dataclass
class Pipe:
    x: float
    gap_y: float
    passed: bool = False

    @property
    def top_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y - PIPE_GAP / 2)

    @property
    def bottom_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.x,
            self.gap_y + PIPE_GAP / 2,
            PIPE_WIDTH,
            SCREEN_HEIGHT - GROUND_HEIGHT - (self.gap_y + PIPE_GAP / 2),
        )


class Bird:
    def __init__(self, x: float, y: float, face_surface: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.velocity = 0.0
        self.rotation = 0.0
        self.face_surface = face_surface
        self.rect = self.face_surface.get_rect(center=(self.x, self.y))

    def flap(self) -> None:
        self.velocity = FLAP_STRENGTH

    def update(self, dt: float) -> None:
        self.velocity = min(self.velocity + GRAVITY * dt, MAX_FALL_SPEED)
        self.y += self.velocity * dt
        self.rotation = max(min(self.velocity * 3, 25), -20)
        self.rect.center = (self.x, self.y)

    def draw(self, screen: pygame.Surface) -> None:
        rotated = pygame.transform.rotozoom(self.face_surface, -self.rotation, 1)
        rect = rotated.get_rect(center=self.rect.center)
        screen.blit(rotated, rect)


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Flappy Face")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("arial", 48, bold=True)
        self.font_small = pygame.font.SysFont("arial", 24)
        self.face_surface = self._create_face_surface()
        self.reset()

    def reset(self) -> None:
        self.bird = Bird(120, SCREEN_HEIGHT / 2, self.face_surface)
        self.pipes: list[Pipe] = []
        self.last_pipe_time = pygame.time.get_ticks()
        self.score = 0
        self.game_over = False

    def _create_face_surface(self) -> pygame.Surface:
        surface = pygame.Surface((96, 96), pygame.SRCALPHA)
        draw = surface.blit

        face = pygame.Surface((96, 96), pygame.SRCALPHA)
        pygame.draw.ellipse(face, (245, 213, 190), (12, 8, 72, 72))
        pygame.draw.ellipse(face, (245, 213, 190), (4, 32, 20, 28))
        pygame.draw.ellipse(face, (245, 213, 190), (72, 32, 20, 28))
        pygame.draw.polygon(face, (180, 96, 72), [(12, 36), (48, 4), (84, 36)])
        pygame.draw.rect(face, (245, 213, 190), (12, 36, 72, 28))

        eyes = pygame.Surface((96, 96), pygame.SRCALPHA)
        pygame.draw.ellipse(eyes, (255, 255, 255), (30, 36, 18, 20))
        pygame.draw.ellipse(eyes, (255, 255, 255), (50, 36, 18, 20))
        pygame.draw.ellipse(eyes, (120, 84, 60), (35, 44, 10, 12))
        pygame.draw.ellipse(eyes, (120, 84, 60), (55, 44, 10, 12))
        pygame.draw.circle(eyes, (20, 20, 20), (40, 50), 3)
        pygame.draw.circle(eyes, (20, 20, 20), (60, 50), 3)

        nose = pygame.Surface((96, 96), pygame.SRCALPHA)
        pygame.draw.polygon(nose, (232, 188, 156), [(48, 44), (42, 64), (54, 64)])

        mouth = pygame.Surface((96, 96), pygame.SRCALPHA)
        pygame.draw.rect(mouth, (214, 120, 148), (32, 64, 32, 6))
        pygame.draw.rect(mouth, (255, 255, 255), (32, 70, 32, 8))
        pygame.draw.rect(mouth, (245, 213, 190), (32, 78, 32, 3))

        jacket = pygame.Surface((96, 96), pygame.SRCALPHA)
        pygame.draw.polygon(jacket, (84, 104, 68), [(12, 72), (24, 92), (48, 78)])
        pygame.draw.polygon(jacket, (84, 104, 68), [(84, 72), (72, 92), (48, 78)])
        pygame.draw.polygon(jacket, (32, 32, 32), [(40, 78), (48, 92), (56, 78)])

        draw(face, (0, 0))
        draw(eyes, (0, 0))
        draw(nose, (0, 0))
        draw(mouth, (0, 0))
        draw(jacket, (0, 0))

        return pygame.transform.smoothscale(surface, (64, 64))

    def spawn_pipe(self) -> None:
        gap_center = random.randint(150, SCREEN_HEIGHT - GROUND_HEIGHT - 150)
        self.pipes.append(Pipe(SCREEN_WIDTH + PIPE_WIDTH, gap_center))

    def update_pipes(self, dt: float) -> None:
        for pipe in list(self.pipes):
            pipe.x -= 180 * dt / 16
            if pipe.x + PIPE_WIDTH < 0:
                self.pipes.remove(pipe)

            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1

    def check_collisions(self) -> None:
        bird_rect = self.bird.rect
        if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.game_over = True
            return

        for pipe in self.pipes:
            if bird_rect.colliderect(pipe.top_rect) or bird_rect.colliderect(pipe.bottom_rect):
                self.game_over = True
                return

    def draw_pipes(self) -> None:
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, (70, 200, 70), pipe.top_rect)
            pygame.draw.rect(self.screen, (70, 200, 70), pipe.bottom_rect)
            # pipe highlights
            pygame.draw.rect(self.screen, (90, 220, 90), (pipe.x, pipe.top_rect.height - 12, PIPE_WIDTH, 12))
            pygame.draw.rect(self.screen, (90, 220, 90), (pipe.x, pipe.bottom_rect.y, PIPE_WIDTH, 12))

    def draw_ground(self) -> None:
        pygame.draw.rect(
            self.screen,
            (222, 209, 168),
            (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT),
        )
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.polygon(
                self.screen,
                (200, 190, 150),
                [(x, SCREEN_HEIGHT - GROUND_HEIGHT), (x + 20, SCREEN_HEIGHT - GROUND_HEIGHT + 16), (x + 40, SCREEN_HEIGHT - GROUND_HEIGHT)],
            )

    def draw_score(self) -> None:
        score_surface = self.font_large.render(str(self.score), True, (30, 30, 30))
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, 60))
        self.screen.blit(score_surface, score_rect)

    def draw_game_over(self) -> None:
        text = self.font_large.render("Game Over", True, (220, 60, 60))
        retry = self.font_small.render("Press Space to try again", True, (30, 30, 30))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
        retry_rect = retry.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 24))
        self.screen.blit(text, text_rect)
        self.screen.blit(retry, retry_rect)

    def run(self) -> None:
        while True:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                    if self.game_over:
                        self.reset()
                    else:
                        self.bird.flap()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.game_over:
                        self.reset()
                    else:
                        self.bird.flap()

            if not self.game_over:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_pipe_time > PIPE_INTERVAL:
                    self.spawn_pipe()
                    self.last_pipe_time = current_time

                self.bird.update(dt)
                self.update_pipes(dt)
                self.check_collisions()

            self.screen.fill((135, 206, 235))
            self.draw_pipes()
            self.draw_ground()
            self.bird.draw(self.screen)
            self.draw_score()

            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()
