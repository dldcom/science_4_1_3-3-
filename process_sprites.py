from PIL import Image
import os

def process_sprite(in_path, out_path):
    try:
        img = Image.open(in_path).convert("RGBA")
        data = img.getdata()
        
        # Replace white background with transparent
        new_data = []
        for item in data:
            if item[0] > 235 and item[1] > 235 and item[2] > 235:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
                
        img.putdata(new_data)
        
        # Crop whitespace
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
            
        # Resize to perfect multiple for 4x4 grid (256x256 -> 64x64 per frame)
        img = img.resize((256, 256), Image.NEAREST)
        img.save(out_path, "PNG")
        print(f"Processed: {out_path}")
    except Exception as e:
        print(f"Error processing {in_path}: {e}")

tourist_in = r"C:\Users\dldco\.gemini\antigravity\brain\6b079053-14bf-4d63-9095-e52d21b0088c\tourist_spritesheet_1780158500319.png"
puppy_in = r"C:\Users\dldco\.gemini\antigravity\brain\6b079053-14bf-4d63-9095-e52d21b0088c\puppy_spritesheet_1780158515693.png"

tourist_out = r"c:\Users\dldco\Downloads\claude\science_3\science_4_1_3-3-\tourist_sprite.png"
puppy_out = r"c:\Users\dldco\Downloads\claude\science_3\science_4_1_3-3-\puppy_sprite.png"

process_sprite(tourist_in, tourist_out)
process_sprite(puppy_in, puppy_out)
