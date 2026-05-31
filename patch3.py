import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. HTML 수정: 이모지를 텍스트로 변경
html = html.replace('<button class="top-right-btn move-btn" onclick="moveCurrentBuilding()" title="위치 이동">🏗️</button>', 
                    '<button class="top-right-btn move-btn" onclick="moveCurrentBuilding()">이동</button>')
html = html.replace('<button class="top-right-btn demo-btn" onclick="demolishCurrentBuilding()" title="철거 (비용 50% 반환)">💣</button>', 
                    '<button class="top-right-btn demo-btn" onclick="demolishCurrentBuilding()">철거</button>')

# 2. CSS 수정: 크기를 정사각형(글씨에 맞게)과 폰트 크기 조절
old_css = ".top-right-btn { width: 35px; height: 35px; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; transition: 0.1s; display: flex; justify-content: center; align-items: center; color: white; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }"
new_css = ".top-right-btn { width: 40px; height: 40px; border: none; border-radius: 8px; font-size: 13px; font-weight: bold; cursor: pointer; transition: 0.1s; display: flex; justify-content: center; align-items: center; color: white; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }"
html = html.replace(old_css, new_css)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html text buttons successfully!")
