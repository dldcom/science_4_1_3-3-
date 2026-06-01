import os
from PIL import Image

def process_sprite(in_path, out_path, mirror_row=True):
    try:
        # Step 1: Remove white background and resize to 256x256
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
        
        # Step 2: Center each frame
        width, height = img.size
        cell_w = width // 4
        cell_h = height // 4
        
        new_img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        
        frames = []
        for row in range(4):
            row_frames = []
            for col in range(4):
                box = (col*cell_w, row*cell_h, (col+1)*cell_w, (row+1)*cell_h)
                cell = img.crop(box)
                
                bbox_cell = cell.getbbox()
                if bbox_cell:
                    char = cell.crop(bbox_cell)
                    char_w = bbox_cell[2] - bbox_cell[0]
                    char_h = bbox_cell[3] - bbox_cell[1]
                    
                    new_cell = Image.new("RGBA", (cell_w, cell_h), (255, 255, 255, 0))
                    paste_x = (cell_w - char_w) // 2
                    paste_y = cell_h - char_h - 4
                    new_cell.paste(char, (paste_x, paste_y))
                else:
                    new_cell = Image.new("RGBA", (cell_w, cell_h), (255, 255, 255, 0))
                    
                row_frames.append(new_cell)
            frames.append(row_frames)
            
        if mirror_row:
            frames[3] = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in frames[2]]
            
        for row in range(4):
            for col in range(4):
                new_img.paste(frames[row][col], (col*cell_w, row*cell_h))
                
        new_img.save(out_path, "PNG")
        print(f"Successfully processed and replaced: {out_path}")
    except Exception as e:
        print(f"Error processing {in_path}: {e}")

in_p = r"C:\Users\USER\.gemini\antigravity\brain\b3b29cdf-283d-47d6-be02-cf5505cf3ab1\explorer_m_v2_1780285645701.png"
out_p = r"c:\Users\USER\Downloads\science_3\explorer_m_sprite.png"

process_sprite(in_p, out_p, mirror_row=True)
