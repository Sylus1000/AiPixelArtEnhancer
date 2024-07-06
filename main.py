import os
from PIL import Image
import numpy as np
import cv2

def calculate_avg_pixel_size(image_path, lower_threshold=50, upper_threshold=50):
    # Open the image file
    img = Image.open(image_path)

    # Convert image to grayscale for edge detection
    img_gray = img.convert('L')

    # Convert the image to a numpy array
    pixel_image = np.array(img_gray)

    # Apply Canny edge detection
    edges = cv2.Canny(pixel_image, lower_threshold, upper_threshold)
    
    # Save the Canny edge-detected image
    edges_image = Image.fromarray(edges)
    base_filename, file_extension = os.path.splitext(image_file)
    edges_image.save(os.path.join(base_filename + '_edges.png'))

    # Initialize lists to store distances
    horizontal_distances = []
    vertical_distances = []

    # Get dimensions of the image
    height, width = edges.shape

    # Calculate horizontal distances between edges
    for y in range(height):
        edge_indices = np.where(edges[y] > 0)[0]
        if len(edge_indices) > 1:
            distances = np.diff(edge_indices)
            horizontal_distances.extend(distances)

    # Calculate vertical distances between edges
    for x in range(width):
        edge_indices = np.where(edges[:, x] > 0)[0]
        if len(edge_indices) > 1:
            distances = np.diff(edge_indices)
            vertical_distances.extend(distances)

    # Combine horizontal and vertical distances
    all_distances = horizontal_distances + vertical_distances

    if all_distances:
        avg_distance = np.mean(all_distances)
        max_distance = np.max(all_distances)
        min_distance = np.min(all_distances)
    else:
        avg_distance = max_distance = min_distance = 0

    return int(avg_distance), int(max_distance), int(min_distance)


def generate_pixel_art(input_path, output_path, pixel_size):
    # Open the input image
    original_image = Image.open(input_path)
    original_pixels = original_image.load()

    # Get the dimensions of the original image
    width, height = original_image.size

    # Adjust the width and height to be divisible by pixel_size
    adjusted_width = (width + pixel_size - 1) // pixel_size * pixel_size
    adjusted_height = (height + pixel_size - 1) // pixel_size * pixel_size

    # Resize the original image to the adjusted dimensions
    if (adjusted_width, adjusted_height) != (width, height):
        original_image = original_image.resize((adjusted_width, adjusted_height))
        original_pixels = original_image.load()

    # Calculate the dimensions of the output image
    output_width = adjusted_width // pixel_size
    output_height = adjusted_height // pixel_size

    # Create a new image for the output
    output_image = Image.new('RGB', (output_width, output_height))

    # Iterate through the original image and draw large pixels in the output image
    for y in range(output_height):
        for x in range(output_width):
            # Get the color of the current pixel
            color = original_pixels[x * pixel_size, y * pixel_size]

            # Draw the large pixel in the output image
            for dy in range(pixel_size):
                for dx in range(pixel_size):
                    output_image.putpixel((x, y), color)

    # Save the output image
    output_image.save(output_path, quality=100, subsampling=0)
    
if __name__ == "__main__":
    # Get the current directory
    current_directory = os.getcwd()
    
    # List all files in the current directory
    files = os.listdir(current_directory)
    
    # Filter out only image files (assuming all are images)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    # Process each image
    for image_file in image_files:
        # Input and output paths
        input_path = os.path.join(current_directory, image_file)
        base_filename, file_extension = os.path.splitext(image_file)
        output_path = os.path.join(current_directory, base_filename + '_output.png')
        
        # Calculate pixel size
        avg, max, min = calculate_avg_pixel_size(input_path)
        
        print(f"Calculated pixel size is avg.: {avg}, max: {max}, min: {min}")
        
        # Generate pixel art
        generate_pixel_art(input_path, output_path, avg)
        
        print(f"Processed {image_file} -> {output_path}")
