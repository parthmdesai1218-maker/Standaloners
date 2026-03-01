"""
SCALE IMAGES TO 1920x1080 (SMART CENTER CROP + HIGH QUALITY RESIZE)
===================================================================

Program Purpose
---------------
This program processes all supported image files in a user-provided
folder and converts them into:

• Exact resolution: 1920 x 1080
• Aspect ratio: 16:9
• No stretching
• No distortion
• Center-based cropping (only to correct aspect ratio)
• High-quality scaling
• WebP output format
• New folder with suffix "_scaled"

Important Design Rules
----------------------
1. Cropping is ONLY allowed to correct aspect ratio.
2. Cropping is done from the CENTER equally.
3. No image is resized using cropping.
4. After aspect ratio correction, image is scaled using LANCZOS
   (highest quality resampling filter).
5. Final output format is WebP.

Requirements
------------
Install Pillow:
    pip install pillow
"""

import os
from PIL import Image


# Target resolution constants
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
TARGET_RATIO = TARGET_WIDTH / TARGET_HEIGHT


def process_image(image_path, output_folder):
    """
    Processes a single image:
    1. Adjusts aspect ratio to 16:9 using centered crop.
    2. Resizes image to 1920x1080 using high-quality scaling.
    3. Saves image as WebP with '_scaled' suffix.
    """

    try:
        with Image.open(image_path) as img:

            # Extract original dimensions
            original_width, original_height = img.size
            original_ratio = original_width / original_height

            # STEP 1: Adjust aspect ratio (center crop only)
            # -----------------------------------------------
            # If ratio differs from 16:9, crop equally from both sides
            if abs(original_ratio - TARGET_RATIO) > 0.0001:

                if original_ratio > TARGET_RATIO:
                    # Image is wider than 16:9
                    # Reduce width while keeping height unchanged
                    new_width = int(original_height * TARGET_RATIO)

                    left = (original_width - new_width) // 2
                    right = left + new_width
                    top = 0
                    bottom = original_height

                else:
                    # Image is taller than 16:9
                    # Reduce height while keeping width unchanged
                    new_height = int(original_width / TARGET_RATIO)

                    top = (original_height - new_height) // 2
                    bottom = top + new_height
                    left = 0
                    right = original_width

                # Perform crop
                img = img.crop((left, top, right, bottom))

            # STEP 2: High-quality resize to exact resolution
            # -----------------------------------------------
            img = img.resize(
                (TARGET_WIDTH, TARGET_HEIGHT),
                Image.LANCZOS  # Highest quality resampling
            )

            # STEP 3: Save output in WebP format
            # -----------------------------------
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(
                output_folder,
                f"{base_name}_scaled.webp"
            )

            img.save(
                output_path,
                "WEBP",
                quality=95,
                method=6
            )

            print(f"Processed: {base_name}")

    except Exception as e:
        print(f"Failed: {image_path} | Error: {e}")


def main():
    print("Scale Images to 1920x1080 (Smart Center Crop)")
    print("---------------------------------------------")

    input_folder = input("Enter full folder path:\n> ").strip()

    if not os.path.isdir(input_folder):
        print("Invalid folder path.")
        return

    # Create output folder
    folder_name = os.path.basename(os.path.normpath(input_folder))
    parent_dir = os.path.dirname(os.path.normpath(input_folder))
    output_folder = os.path.join(parent_dir, f"{folder_name}_scaled")

    os.makedirs(output_folder, exist_ok=True)

    # Supported image formats
    supported_formats = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")

    files = [
        os.path.join(input_folder, f)
        for f in os.listdir(input_folder)
        if f.lower().endswith(supported_formats)
    ]

    if not files:
        print("No supported image files found.")
        return

    print(f"\nFound {len(files)} images. Processing...\n")

    for image_path in files:
        process_image(image_path, output_folder)

    print("\nAll images processed successfully!")
    print(f"Output folder: {output_folder}")


if __name__ == "__main__":
    main()