from PIL import Image

def process_sprite(in_path, out_path):
    try:
        img = Image.open(in_path).convert("RGBA")
        data = img.getdata()
        
        new_data = []
        for item in data:
            if item[0] > 235 and item[1] > 235 and item[2] > 235:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
                
        img.putdata(new_data)
        
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
            
        img = img.resize((256, 256), Image.NEAREST)
        img.save(out_path, "PNG")
        print(f"Processed: {out_path}")
    except Exception as e:
        print(f"Error processing {in_path}: {e}")

tasks = [
    (r"C:\Users\USER\.gemini\antigravity\brain\b3b29cdf-283d-47d6-be02-cf5505cf3ab1\tourist_woman_1780280878506.png", r"c:\Users\USER\Downloads\science_3\tourist_woman_sprite.png"),
    (r"C:\Users\USER\.gemini\antigravity\brain\b3b29cdf-283d-47d6-be02-cf5505cf3ab1\explorer_m_1780280891863.png", r"c:\Users\USER\Downloads\science_3\explorer_m_sprite.png"),
    (r"C:\Users\USER\.gemini\antigravity\brain\b3b29cdf-283d-47d6-be02-cf5505cf3ab1\explorer_f_1780280904801.png", r"c:\Users\USER\Downloads\science_3\explorer_f_sprite.png"),
    (r"C:\Users\USER\.gemini\antigravity\brain\b3b29cdf-283d-47d6-be02-cf5505cf3ab1\photographer_1780280921772.png", r"c:\Users\USER\Downloads\science_3\photographer_sprite.png")
]

for in_p, out_p in tasks:
    process_sprite(in_p, out_p)
