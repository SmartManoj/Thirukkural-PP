from PIL import Image
import os
import random
import math

def create_collage(images_dir='static/imgs', output_path='collage.jpg', grid_size=(4, 4), image_size=(200, 200), specific_range=None):
    """
    Create a collage from images in the specified directory.
    
    Args:
        images_dir: Directory containing images
        output_path: Output path for the collage
        grid_size: Tuple of (rows, cols) for the grid layout
        image_size: Size to resize each image to
        specific_range: Tuple of (start, end) for specific image numbers
    """
    if specific_range:
        # Get specific numbered images
        start, end = specific_range
        selected_images = []
        for i in range(start, end + 1):
            # Try different extensions
            for ext in ['.jpeg', '.jpg', '.png']:
                img_path = os.path.join(images_dir, f'{i}{ext}')
                if os.path.exists(img_path):
                    selected_images.append(img_path)
                    break
    else:
        # Get all image files
        image_files = []
        for file in os.listdir(images_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(images_dir, file))
        
        if not image_files:
            print("No images found in the directory")
            return
        
        # Randomly select images for the collage
        num_images = grid_size[0] * grid_size[1]
        selected_images = random.sample(image_files, min(num_images, len(image_files)))
    
    if not selected_images:
        print("No images found in the specified range")
        return
    
    # Create the collage canvas
    canvas_width = grid_size[1] * image_size[0]
    canvas_height = grid_size[0] * image_size[1]
    collage = Image.new('RGB', (canvas_width, canvas_height), 'white')
    
    # Place images on the canvas
    for i, img_path in enumerate(selected_images):
        try:
            # Open and resize image
            img = Image.open(img_path)
            img = img.resize(image_size, Image.Resampling.LANCZOS)
            
            # Calculate position
            row = i // grid_size[1]
            col = i % grid_size[1]
            x = col * image_size[0]
            y = row * image_size[1]
            
            # Paste image onto canvas
            collage.paste(img, (x, y))
            
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            continue
    
    # Fill remaining empty spaces with white rectangles if needed
    total_spots = grid_size[0] * grid_size[1]
    for i in range(len(selected_images), total_spots):
        row = i // grid_size[1]
        col = i % grid_size[1]
        x = col * image_size[0]
        y = row * image_size[1]
        
        # Draw white rectangle for empty spot
        from PIL import ImageDraw
        draw = ImageDraw.Draw(collage)
        draw.rectangle([x, y, x + image_size[0], y + image_size[1]], fill='white', outline='lightgray')
    
    # Save the collage
    collage.save(output_path, 'JPEG', quality=95)
    print(f"Collage saved as {output_path}")

if __name__ == "__main__":
    # Create grid collage with images 116-127 (12 images total)
    print("Creating grid collage with images 116-127...")
    create_collage(output_path='grid_collage_116_127.jpg', grid_size=(3, 4), specific_range=(116, 127))
    
