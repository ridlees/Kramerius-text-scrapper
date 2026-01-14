import img2pdf
import os
import re

def save(image_folder="./temp", output="./output.pdf"):
    def numeric_key(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    images = [
        os.path.join(image_folder, f)
        for f in sorted(os.listdir(image_folder), key=numeric_key)
        if f.lower().endswith((".jpeg", ".jpg"))
    ]

    if not images:
        print("No images found to convert.")
        return

    with open(output, "wb") as f:
        f.write(img2pdf.convert(images))

    print(f"PDF created: {output}")
    """
    for image in images:
        os.remove(image)
    """
