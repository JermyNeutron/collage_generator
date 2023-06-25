import os
import time
from PIL import Image
import random
import math

def calculate_average_color(image):
    # Calculate the average RGB color value of an image
    pixels = image.load()
    width, height = image.size
    r, g, b = 0, 0, 0

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]

    total_pixels = width * height
    avg_r = math.floor(r / total_pixels)
    avg_g = math.floor(g / total_pixels)
    avg_b = math.floor(b / total_pixels)

    return avg_r, avg_g, avg_b


def find_closest_image(target_color, collage_folder_path):
    # Find the image in the collage folder with the closest average color to the target color
    collage_files = os.listdir(collage_folder_path)
    collage_files = [file for file in collage_files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    closest_image = None
    closest_color_diff = float('inf')

    for filename in collage_files:
        collage_image_path = os.path.join(collage_folder_path, filename)
        collage_image = Image.open(collage_image_path)
        collage_avg_color = calculate_average_color(collage_image)
        color_diff = color_difference(target_color, collage_avg_color)

        if color_diff < closest_color_diff:
            closest_image = collage_image_path
            closest_color_diff = color_diff

    return closest_image


def color_difference(color1, color2):
    # Calculate the color difference between two RGB color values
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r_diff = r1 - r2
    g_diff = g1 - g2
    b_diff = b1 - b2
    return math.sqrt(r_diff**2 + g_diff**2 + b_diff**2)


def generate_collage(input_image_path, collage_folder_path, output_image_path, num_tiles=(5, 5)):
    start_time = time.time()

    input_image = Image.open(input_image_path.encode('utf-8'))

    input_width, input_height = input_image.size
    tile_size = (input_width // num_tiles[0], input_height // num_tiles[1])

    collage_width = num_tiles[0] * tile_size[0]
    collage_height = num_tiles[1] * tile_size[1]
    collage = Image.new('RGB', (collage_width, collage_height))

    for y in range(num_tiles[1]):
        for x in range(num_tiles[0]):
            # Crop the tile from the input image
            tile_box = (x * tile_size[0], y * tile_size[1], (x + 1) * tile_size[0], (y + 1) * tile_size[1])
            tile = input_image.crop(tile_box)

            # Calculate the average color of the tile
            tile_avg_color = calculate_average_color(tile)

            # Find the collage image with the closest average color
            closest_image = find_closest_image(tile_avg_color, collage_folder_path)

            if closest_image:
                # Open the closest collage image and resize it to the tile size
                collage_image = Image.open(closest_image).resize(tile_size)

                # Paste the collage image onto the canvas
                collage.paste(collage_image, (x * tile_size[0], y * tile_size[1]))

    # Save the collage image
    collage.save(output_image_path.encode('utf-8'), format='JPEG')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Collage generation completed in {elapsed_time:.2f} seconds.")

# Example usage
input_image_path = "c:/Users/Jeremy/Desktop/input image/mickey-minnie-mouse100.jpg"
collage_folder_path = "c:/Users/Jeremy/Desktop/collagefolder"
output_image_path = "c:/Users/Jeremy/Desktop/outputfolder/output_collage.jpg"
num_tiles = (50, 50)

generate_collage(input_image_path, collage_folder_path, output_image_path, num_tiles)