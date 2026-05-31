import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# JS 로직 수정: 이모지 칼 제거하고 백그라운드 이미지 변경으로 대체
old_knight_js = """                            pup.isKnight = true; pup.el.classList.add('puppy-knight');
                            let sword = document.createElement('div'); sword.innerText = '⚔️'; sword.style.position = 'absolute'; sword.style.top = '-15px'; sword.style.left = '5px'; sword.style.fontSize = '20px'; pup.el.appendChild(sword);
                            showEmotion(pup.x, pup.y, '⚔️'); pup.state = 'roaming';
                            updateSpriteDirection(pup.el, 0, 0, false);"""

new_knight_js = """                            pup.isKnight = true; pup.el.classList.add('puppy-knight');
                            pup.el.style.backgroundImage = "url('knight_puppy_sprite.png')";
                            showEmotion(pup.x, pup.y, '⚔️'); pup.state = 'roaming';
                            updateSpriteDirection(pup.el, 0, 0, false);"""

html = html.replace(old_knight_js, new_knight_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html for knight puppy successfully!")
