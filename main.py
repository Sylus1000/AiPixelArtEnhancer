import os
from PIL import Image
import numpy as np
import cv2

def calculate_avg_pixel_size(image_path, lower_threshold=50, upper_threshold=50, output_edges=False):
    # Open the image file
    img = Image.open(image_path)

    # Convert image to grayscale for edge detection
    img_gray = img.convert('L')

    # Convert the image to a numpy array
    pixel_image = np.array(img_gray)

    # Apply Canny edge detection
    edges = cv2.Canny(pixel_image, lower_threshold, upper_threshold)
    
    # Save the Canny edge-detected image
    if(output_edges):
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
    output_width = adjusted_width
    output_height = adjusted_height

    # Create a new image for the output
    output_image = Image.new('RGB', (output_width, output_height))

    # Iterate through the original image and draw large pixels in the output image
    for y in range(0, adjusted_height, pixel_size):
        for x in range(0, adjusted_width, pixel_size):
            # Get the color of the current pixel
            color = original_pixels[x, y]

            # Draw the large pixel in the output image
            for dy in range(pixel_size):
                for dx in range(pixel_size):
                    if x + dx < adjusted_width and y + dy < adjusted_height:
                        output_image.putpixel((x + dx, y + dy), color)

    # Save the output image
    output_image.save(output_path, quality=100, subsampling=0)
    return original_image, output_image
    
    
def show_results(image1, image2):
    # Determine which image is smaller
    if image1.width < image2.width:
        smaller_image = image1
        larger_image = image2
    else:
        smaller_image = image2
        larger_image = image1
    
    # Resize the smaller image to match the width of the larger image with interpolation
    resized_smaller_image = smaller_image.resize((larger_image.width, larger_image.height), Image.NEAREST)
    
    # Create a new image with white background
    combined_image = Image.new('RGB', (larger_image.width + resized_smaller_image.width, larger_image.height), 'white')
    
    # Paste the larger image on the left side
    combined_image.paste(larger_image, (0, 0))
    
    # Paste the resized smaller image on the right side
    combined_image.paste(resized_smaller_image, (larger_image.width, 0))
    
    # Display or save the combined image as per your requirement
    combined_image.show()
    combined_image.save("./result_side_by_side.png", quality=100, subsampling=0)
    
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
        avg_pixel_size, max_pixel_size, min_pixel_size = calculate_avg_pixel_size(input_path)
        
        print(f"Calculated pixel size is avg.: {avg_pixel_size}, max: {max_pixel_size}, min: {min_pixel_size}")
        
        # Generate pixel art
        original_image, output_image = generate_pixel_art(input_path, output_path, avg_pixel_size)
        
        print(f"Processed {image_file} -> {output_path}")
        
        # Show images
        show_results(original_image, output_image)