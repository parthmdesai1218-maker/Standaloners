"""
PNG TO WEBP CONVERTER
=====================

Program Purpose
---------------
This program converts all PNG images inside a user-provided folder
into WebP format while:

• Maintaining original image resolution
• Preserving high visual quality
• Reducing overall file size
• Creating a separate output folder
• Keeping original filenames (with .webp extension)

The program does NOT:
• Resize images
• Change aspect ratios
• Stretch or distort images

How It Works
------------
1. User provides input folder path.
2. Program scans folder for .png files.
3. Creates a new folder:
       originalFolderName_webp
4. Converts each PNG file to WebP format.
5. Prints file size comparison.
6. Displays total size reduction.

Requirements
------------
Install Pillow before running:
    pip install pillow
"""

import os
from PIL import Image


def convert_png_to_webp(input_folder, quality=90, method=6, lossless=False):
    """
    Converts all PNG images in the specified folder to WebP format.

    Parameters:
    ----------
    input_folder : str
        Path to the folder containing PNG files.

    quality : int (0-100)
        Controls compression quality.
        90 = High quality with good compression.
        100 = Near-lossless.

    method : int (0-6)
        Compression effort.
        6 = Best compression (slower but smaller size).

    lossless : bool
        True  -> Lossless compression (no quality loss, larger size).
        False -> High-quality lossy compression.
    """

    # Validate that the provided path exists
    if not os.path.isdir(input_folder):
        print("\nInvalid folder path. Please check and try again.")
        return

    # Extract folder name and create output directory
    folder_name = os.path.basename(os.path.normpath(input_folder))
    parent_dir = os.path.dirname(os.path.normpath(input_folder))
    output_folder = os.path.join(parent_dir, f"{folder_name}_webp")

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Collect all PNG files (case-insensitive)
    png_files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(".png")
    ]

    if not png_files:
        print("\nNo PNG files found in the folder.")
        return

    print(f"\nFound {len(png_files)} PNG files.")
    print("Converting to WebP...\n")

    total_original = 0
    total_new = 0

    # Process each PNG file
    for filename in png_files:

        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".webp"
        output_path = os.path.join(output_folder, output_filename)

        try:
            # Open image safely using context manager
            with Image.open(input_path) as img:

                # Save image as WebP with defined compression settings
                img.save(
                    output_path,
                    "WEBP",
                    quality=quality,
                    method=method,
                    lossless=lossless
                )

            # Calculate size comparison
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)

            total_original += original_size
            total_new += new_size

            print(f"{filename} → {output_filename}")
            print(f"Original: {original_size/1024:.2f} KB | WebP: {new_size/1024:.2f} KB")

        except Exception as e:
            print(f"Failed to convert {filename}: {e}")

    # Print total compression summary
    if total_original > 0:
        reduction = ((total_original - total_new) / total_original) * 100

        print("\nConversion Complete!")
        print(f"Output folder: {output_folder}")
        print(f"Total Size Reduction: {reduction:.2f}%")
    else:
        print("\nNo files were processed.")


if __name__ == "__main__":
    print("PNG to WebP Converter")
    print("----------------------")

    input_folder_path = input(
        "Enter the full folder path containing PNG images:\n> "
    ).strip()

    quality_input = input(
        "Enter quality (0-100, default 90): "
    ).strip()

    quality = int(quality_input) if quality_input.isdigit() else 90

    lossless_input = input(
        "Use lossless mode? (y/n, default n): "
    ).strip().lower()

    lossless = True if lossless_input == "y" else False

    convert_png_to_webp(input_folder_path, quality=quality, lossless=lossless)