import sys
from PIL import Image

def remove_white_bg(img_path, out_path, tolerance=230):
    img = Image.open(img_path).convert("RGBA")
    data = img.getdata()
    
    new_data = []
    for item in data:
        if item[0] > tolerance and item[1] > tolerance and item[2] > tolerance:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(out_path, "PNG")
    print("Background removed and saved to", out_path)

remove_white_bg(
    r"C:\Users\dldco\.gemini\antigravity\brain\c5ee8fed-231c-4f7e-b767-f164954dbbc0\farm_basic_1779976742531.png",
    r"c:\Users\dldco\Downloads\claude\science_3\science_4_1_3-3-\farm_basic_processed.png",
    tolerance=230
)

remove_white_bg(
    r"C:\Users\dldco\.gemini\antigravity\brain\c5ee8fed-231c-4f7e-b767-f164954dbbc0\farm_upgraded_1779976764714.png",
    r"c:\Users\dldco\Downloads\claude\science_3\science_4_1_3-3-\farm_upgraded_processed.png",
    tolerance=230
)
