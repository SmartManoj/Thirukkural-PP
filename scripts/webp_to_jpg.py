from PIL import Image

file_name = r"static\imgs\45"

# Open the WEBP image
webp_image = Image.open(f"{file_name}.webp")

# Convert and save as JPG
webp_image.convert("RGB").save(f"{file_name}.jpeg", "JPEG")

# delete the WEBP image
import os
os.remove(f"{file_name}.webp")