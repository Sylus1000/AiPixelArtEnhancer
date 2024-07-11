import os
from PIL import Image
import numpy as np
import cv2

def calculate_avg_pixel_size(image_path, lower_threshold=50, upper_threshold=50, output_edges=False):
    # Open and convert the image to grayscale
    img_gray = Image.open(image_path).convert('L')

    # Apply Canny edge detection
    edges = cv2.Canny(np.array(img_gray), lower_threshold, upper_threshold)

    if output_edges:
        base_filename, _ = os.path.splitext(image_path)
        Image.fromarray(edges).save(f"{base_filename}_edges.png")

    # Calculate distances between edges
    distances = [
        np.diff(np.where(edges[y] > 0)[0]).tolist() for y in range(edges.shape[0])
    ] + [
        np.diff(np.where(edges[:, x] > 0)[0]).tolist() for x in range(edges.shape[1])
    ]
    
    all_distances = [dist for sublist in distances for dist in sublist]

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

    # Resize the image to be divisible by pixel_size
    adjusted_size = (
        (original_image.size[0] + pixel_size - 1) // pixel_size * pixel_size,
        (original_image.size[1] + pixel_size - 1) // pixel_size * pixel_size
    )
    original_image = original_image.resize(adjusted_size)

    # Create pixelated image
    output_image = original_image.resize(
        (adjusted_size[0] // pixel_size, adjusted_size[1] // pixel_size), Image.NEAREST
    ).resize(adjusted_size, Image.NEAREST)

    # Save the output image
    output_image.save(output_path, quality=100, subsampling=0)
    return original_image, output_image


def show_results(image1, image2):
    # Resize smaller image to match the larger image's width
    if image1.width < image2.width:
        smaller_image, larger_image = image1, image2
    else:
        smaller_image, larger_image = image2, image1

    resized_smaller_image = smaller_image.resize(
        (larger_image.width, larger_image.height), Image.NEAREST
    )

    # Combine images side by side
    combined_image = Image.new(
        'RGB', (larger_image.width * 2, larger_image.height), 'white'
    )
    combined_image.paste(larger_image, (0, 0))
    combined_image.paste(resized_smaller_image, (larger_image.width, 0))

    combined_image.show()
    combined_image.save("./result_side_by_side.png", quality=100, subsampling=0)


if __name__ == "__main__":
    current_directory = os.getcwd()
    image_files = [
        f for f in os.listdir(current_directory)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
    ]

    for image_file in image_files:
        input_path = os.path.join(current_directory, image_file)
        base_filename, _ = os.path.splitext(image_file)
        output_path = os.path.join(current_directory, f"{base_filename}_output.png")

        avg_pixel_size, max_pixel_size, min_pixel_size = calculate_avg_pixel_size(input_path)
        print(f"Calculated pixel size is avg.: {avg_pixel_size}, max: {max_pixel_size}, min: {min_pixel_size}")

        original_image, output_image = generate_pixel_art(input_path, output_path, avg_pixel_size)
        print(f"Processed {image_file} -> {output_path}")

        #show_results(original_image, output_image)
