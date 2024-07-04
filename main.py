import os
from PIL import Image

def color_difference(color1, color2, threshold):
    """ 
    Calculate the difference between two RGB colors.
    Returns True if the difference is greater than the threshold, False otherwise.
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    # Calculate Euclidean distance between colors
    distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
    
    return distance > threshold

def calculate_pixel_size(image_path, threshold=85):
    # Open the image
    img = Image.open(image_path)
    
    # Get image size (width, height)
    width, height = img.size
    
    # Start scanning from the top left corner (0, 0) to (width, 0)
    initial_color = img.getpixel((0, 0))  # Get the color of the top-left pixel
    pixel_size = 1  # Initialize the pixel size
    
    # Scan horizontally across the top row
    for x in range(1, width):
        current_color = img.getpixel((x, 0))
        
        # Compare current pixel color with the initial color
        if color_difference(current_color, initial_color, threshold):
            pixel_size = x  # This is the size of the pixels
            break
    
    return pixel_size

def generate_pixel_art(input_path, output_path, pixel_size):
    # Open the input image
    original_image = Image.open(input_path)
    original_pixels = original_image.load()

    # Get the dimensions of the original image
    width, height = original_image.size

    # Calculate the dimensions of the output image
    output_width = width // pixel_size
    output_height = height // pixel_size

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
        pixel_size = calculate_pixel_size(input_path)
        
        print(f"Calculated pixel size is: {pixel_size}")
        
        # Generate pixel art
        generate_pixel_art(input_path, output_path, pixel_size)
        
        print(f"Processed {image_file} -> {output_path}")