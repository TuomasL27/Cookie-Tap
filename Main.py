import pygame as pg
import os

WIDTH = 1920
HEIGHT = 1080
FPS = 240
COOKIE_BASE_SIZE = (400, 400)
COOKIE_ON_CLICK_SIZE = (300, 300)
COOKIE_POSITION = (120, 200)

WHITE = (255, 255, 255)
FONT_SIZE = 80
FONT_COLOR = (0, 0, 0)

pg.init()
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Cookie Clicker")

font = pg.font.SysFont(None, FONT_SIZE)
coin_img = pg.image.load(os.path.join("assets", "coin.png"))
coin_img = pg.transform.scale(coin_img, (100, 100))


def load_asset(filename, size=(100, 100), folder="assets"):
    asset = pg.image.load(os.path.join(folder, filename))
    return pg.transform.scale(asset, size)


def draw(cookie_img, cookie_count):
    win.fill(WHITE)
    x = COOKIE_POSITION[0] + (COOKIE_BASE_SIZE[0] - cookie_img.get_width()) // 2
    y = COOKIE_POSITION[1] + (COOKIE_BASE_SIZE[1] - cookie_img.get_height()) // 2

    text_surface = font.render(f"{cookie_count} moneys", True, FONT_COLOR)
    text_rect = text_surface.get_rect(
        x=COOKIE_POSITION[0] + COOKIE_BASE_SIZE[0] // 2 - 40 - text_surface.get_width() // 2, y=100
    )

    win.blit(text_surface, text_rect)

    last_letter_x = text_rect.x + text_rect.width
    last_letter_y = text_rect.y
    coin_coords = (last_letter_x + 3, last_letter_y - 20)
    win.blit(coin_img, coin_coords)
    win.blit(cookie_img, (x, y))
    pg.display.update()


def scale_cookie(cookie_img, target_size, duration, cookie_count):
    original_size = cookie_img.get_size()
    current_size = original_size

    delta_width_down = (original_size[0] - target_size[0]) / (duration // 2)
    delta_height_down = (original_size[1] - target_size[1]) / (duration // 2)

    delta_width_up = (original_size[0] - target_size[0]) / (duration * 4)
    delta_height_up = (original_size[1] - target_size[1]) / (duration * 4)

    for _ in range(duration // 2):
        current_size = (current_size[0] - delta_width_down, current_size[1] - delta_height_down)
        scaled_cookie = pg.transform.scale(cookie_img, (int(current_size[0]), int(current_size[1])))
        draw(scaled_cookie, cookie_count)
        pg.time.wait(int(1000 / FPS))

    pg.time.wait(167)

    for _ in range(duration * 4):
        current_size = (current_size[0] + delta_width_up, current_size[1] + delta_height_up)
        scaled_cookie = pg.transform.scale(cookie_img, (int(current_size[0]), int(current_size[1])))
        draw(scaled_cookie, cookie_count)
        pg.time.wait(int(1000 / FPS))

    final_cookie = pg.transform.scale(cookie_img, original_size)
    draw(final_cookie, cookie_count)


def main():
    clock = pg.time.Clock()
    run = True
    FRAMES = 0
    CLICK_ANIMATION_COOLDOWN_FRAME_COUNT = 0
    CLICK_ANIMATION_COOLDOWN = 2
    clicked = False
    COOKIE_1 = load_asset("Cookie_1.png", size=COOKIE_BASE_SIZE)
    cookie_count = 0

    while run:
        clock.tick(FPS)
        FRAMES += 1

        if clicked and FRAMES - CLICK_ANIMATION_COOLDOWN_FRAME_COUNT >= CLICK_ANIMATION_COOLDOWN:
            clicked = False
            COOKIE_1 = load_asset("Cookie_1.png", size=COOKIE_BASE_SIZE)

        for event in pg.event.get():
            pos = pg.mouse.get_pos()

            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if (
                    COOKIE_POSITION[0] <= pos[0] <= COOKIE_POSITION[0] + COOKIE_BASE_SIZE[0]
                    and COOKIE_POSITION[1] <= pos[1] <= COOKIE_POSITION[1] + COOKIE_BASE_SIZE[1]
                ):
                    cookie_count += 1

                    if not clicked:
                        clicked = True
                        scale_cookie(COOKIE_1, COOKIE_ON_CLICK_SIZE, CLICK_ANIMATION_COOLDOWN, cookie_count)
                        CLICK_ANIMATION_COOLDOWN_FRAME_COUNT = FRAMES

        draw(COOKIE_1, cookie_count)


if __name__ == "__main__":
    main()
