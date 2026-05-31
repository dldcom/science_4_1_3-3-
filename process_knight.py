from PIL import Image
import os

def fix_sprite(path, out_path, mirror_row=True):
    try:
        img = Image.open(path).convert("RGBA")
        width, height = img.size
        cell_w = width // 4
        cell_h = height // 4
        
        new_img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        
        frames = []
        for row in range(4):
            row_frames = []
            for col in range(4):
                # Extract cell
                box = (col*cell_w, row*cell_h, (col+1)*cell_w, (row+1)*cell_h)
                cell = img.crop(box)
                
                # Strip white background
                data = cell.getdata()
                new_data = []
                for item in data:
                    if item[0] > 235 and item[1] > 235 and item[2] > 235:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                cell.putdata(new_data)
                
                # Find bounding box
                bbox = cell.getbbox()
                if bbox:
                    # Crop to exact character
                    char = cell.crop(bbox)
                    char_w = bbox[2] - bbox[0]
                    char_h = bbox[3] - bbox[1]
                    
                    # Create new centered cell (align to bottom center is better for characters)
                    new_cell = Image.new("RGBA", (cell_w, cell_h), (255, 255, 255, 0))
                    paste_x = (cell_w - char_w) // 2
                    paste_y = cell_h - char_h - 4 # 4 pixels from bottom
                    new_cell.paste(char, (paste_x, paste_y))
                else:
                    new_cell = Image.new("RGBA", (cell_w, cell_h), (255, 255, 255, 0))
                    
                row_frames.append(new_cell)
            frames.append(row_frames)
            
        # Mirror Right (Row 2) to Left (Row 3)
        if mirror_row:
            frames[3] = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in frames[2]]
            
        # Paste back
        for row in range(4):
            for col in range(4):
                new_img.paste(frames[row][col], (col*cell_w, row*cell_h))
                
        new_img = new_img.resize((256, 256), Image.NEAREST)
        new_img.save(out_path, "PNG")
        print(f"Fixed sprite: {out_path}")
    except Exception as e:
        print(f"Error fixing {path}: {e}")

knight_in = r"C:\Users\dldco\.gemini\antigravity\brain\6b079053-14bf-4d63-9095-e52d21b0088c\knight_puppy_1780159034585.png"
knight_out = r"c:\Users\dldco\Downloads\claude\science_3\science_4_1_3-3-\knight_puppy_sprite.png"

fix_sprite(knight_in, knight_out, mirror_row=True)
