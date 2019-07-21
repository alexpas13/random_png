import random

from PIL import Image, ImageDraw


class RandomPng:
    COLOR = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            255
        )
    BG_COLOR = (0, 0, 0, 0)

    def __init__(self, size, min_px_count=8, max_px_count=12):
        self.size = size
        self.x_block_size = size[0] // 2
        self.y_block_size = size[1] // 2
        self.img = Image.new("RGBA", size, self.BG_COLOR)
        self.pixel_size = self._generate_pixel_size(min_px_count, max_px_count)
        self.block_img = self._generate_block_image()
        self._draw_image()

    def _generate_pixel_size(self, min_count, max_count):
        min_side_size = self.size[0] if self.size[0] < self.size[1] else self.size[1]
        return random.randint(min_side_size // max_count or 1, min_side_size // min_count or 1)

    def _generate_block_image(self):
        return Block(
            (self.x_block_size, self.y_block_size),
            self.BG_COLOR,
            Pixel(self.pixel_size, self.COLOR)
        ).create_img()

    def _draw_image(self,):
        block_images = [
            (self.block_img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM), (0, 0)),
            (self.block_img.transpose(Image.FLIP_TOP_BOTTOM), (self.x_block_size, 0)),
            (self.block_img.transpose(Image.FLIP_LEFT_RIGHT), (0, self.y_block_size)),
            (self.block_img, (self.x_block_size, self.y_block_size))
        ]
        for block_img in block_images:
            self.img.paste(*block_img)

    def save(self, path):
        self.img.save(path)


class Block:
    def __init__(self, size, bg_color, pixel):
        self.img = Image.new("RGBA", size, bg_color)
        self.img_drawer = ImageDraw.Draw(self.img)
        self.pixel = pixel
        self.x_count = size[0] // pixel.size
        self.y_count = size[1] // pixel.size

    def create_img(self):
        drawn_pixels = 0
        while not drawn_pixels:
            for x in range(0, self.x_count):
                for y in range(0, self.y_count):
                    draw_pixel = random.randint(0, 1)
                    drawn_pixels += draw_pixel
                    if draw_pixel:
                        self.pixel.draw(x, y, self.img_drawer)
        return self.img


class Pixel:
    def __init__(self, size, color):
        self.size = size
        self.color = color

    def draw(self, x, y, img_drawer):
        img_drawer.rectangle(
            [
                (self.size * x, self.size * y),
                (self.size * (x + 1), self.size * (y + 1))
            ],
            self.color
        )
