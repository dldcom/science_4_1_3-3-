from PIL import Image
import os

def fix_sprite(path, mirror_row=True):
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
                box = (col*cell_w, row*cell_h, (col+1)*cell_w, (row+1)*cell_h)
                cell = img.crop(box)
                
                bbox = cell.getbbox()
                if bbox:
                    char = cell.crop(bbox)
                    char_w = bbox[2] - bbox[0]
                    char_h = bbox[3] - bbox[1]
                    
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
                
        new_img.save(path, "PNG")
        print(f"Fixed sprite: {path}")
    except Exception as e:
        print(f"Error fixing {path}: {e}")

tasks = [
    r"c:\Users\USER\Downloads\science_3\tourist_woman_sprite.png",
    r"c:\Users\USER\Downloads\science_3\explorer_m_sprite.png",
    r"c:\Users\USER\Downloads\science_3\explorer_f_sprite.png",
    r"c:\Users\USER\Downloads\science_3\photographer_sprite.png"
]

for p in tasks:
    fix_sprite(p, mirror_row=True)
