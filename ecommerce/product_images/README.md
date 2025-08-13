# 📦 Product Images Dataset

## Download Required!

The product images dataset (12,114 images, ~8GB) is distributed separately due to GitHub size limits.

### Download from Slack:
1. Go to **#capstone-data** channel
2. Download **`product_images.zip`**
3. Extract all files to THIS directory
4. Delete the zip file after extraction

### Verify Success:
After extraction, this directory should contain:
- 12,114 .jpg files
- Files like: `10016743.jpg`, `10019867.jpg`, etc.

### Check with Python:
```python
import os
images = [f for f in os.listdir('.') if f.endswith('.jpg')]
print(f"Found {len(images)} product images")
# Should print: Found 12114 product images
```

⚠️ **The Visual Search CNN model requires these images!**