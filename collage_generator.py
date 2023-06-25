import os
from PIL import Image
import random

def generate_collage(input_image_path, collage_folder_path, output_image_path, num_tiles=(25, 25)):
    input_image = Image.open(input_image_path.encode('utf-8'))

    input_width, input_height = input_image.size
    tile_size = (input_width // num_tiles[0], input_height // num_tiles[1])

    collage_width = num_tiles[0] * tile_size[0]
    collage_height = num_tiles[1] * tile_size[1]
    collage = Image.new('RGB', (collage_width, collage_height))

    collage_files = os.listdir(collage_folder_path)
    collage_files = [file for file in collage_files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for y in range(num_tiles[1]):
        for x in range(num_tiles[0]):
            # Crop the tile from the input image
            tile_box = (x * tile_size[0], y * tile_size[1], (x + 1) * tile_size[0], (y + 1) * tile_size[1])
            tile = input_image.crop(tile_box)

            # Select a random image from the collage folder
            if len(collage_files) == 0:
                raise ValueError("No valid collage images found in the folder.")

            random_collage_image = random.choice(collage_files)
            collage_image_path = os.path.join(collage_folder_path, random_collage_image)

            try:
                # Open the collage image and resize it to the tile size
                collage_image = Image.open(collage_image_path).resize(tile_size)

                # Paste the collage image onto the canvas
                collage.paste(collage_image, (x * tile_size[0], y * tile_size[1]))
            except (IOError, OSError):
                # Skip unsupported or corrupted image files
                continue

    collage.save(output_image_path.encode('utf-8'), format='JPEG')

# Example usage
input_image_path = "c:/Users/Jeremy/Desktop/input image/mickey-minnie-mouse100.jpg"
collage_folder_path = "c:/Users/Jeremy/Desktop/collagefolder"
output_image_path = "c:/Users/Jeremy/Desktop/outputfolder/output_collage.jpg"

generate_collage(input_image_path, collage_folder_path, output_image_path)