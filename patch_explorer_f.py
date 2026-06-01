from PIL import Image

def patch_sprite():
    path = r"c:\Users\USER\Downloads\science_3\explorer_f_sprite.png"
    img = Image.open(path).convert("RGBA")
    width, height = img.size
    cell_w = width // 4
    cell_h = height // 4
    
    # helper to get box for a frame index (0-15)
    def get_box(idx):
        row = idx // 4
        col = idx % 4
        return (col*cell_w, row*cell_h, (col+1)*cell_w, (row+1)*cell_h)
        
    # Copy 4 to 6
    img.paste(img.crop(get_box(4)), get_box(6))
    # Copy 5 to 7
    img.paste(img.crop(get_box(5)), get_box(7))
    # Copy 9 to 8
    img.paste(img.crop(get_box(9)), get_box(8))
    # Copy 13 to 12
    img.paste(img.crop(get_box(13)), get_box(12))
    
    img.save(path, "PNG")
    print(f"Successfully patched {path}")

if __name__ == "__main__":
    patch_sprite()
