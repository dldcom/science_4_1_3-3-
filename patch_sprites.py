import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS 추가
sprite_css = """
        /* 스프라이트 애니메이션 CSS */
        .tourist-sprite, .puppy-sprite, .golden-puppy-sprite {
            position: absolute;
            width: 32px; height: 32px;
            background-size: 128px 128px;
            z-index: 19000;
            transition: left 0.5s linear, top 0.5s linear;
            pointer-events: none;
            background-repeat: no-repeat;
        }
        .tourist-sprite { background-image: url('tourist_sprite.png'); }
        .puppy-sprite { background-image: url('puppy_sprite.png'); filter: drop-shadow(0 2px 2px rgba(0,0,0,0.5)); }
        .golden-puppy-sprite { 
            background-image: url('puppy_sprite.png');
            filter: drop-shadow(0 0 10px rgba(255,215,0,0.8)) sepia(1) saturate(5) hue-rotate(-20deg);
            width: 48px; height: 48px;
            background-size: 192px 192px;
        }
        .puppy-knight { filter: drop-shadow(0 0 5px rgba(200,200,255,0.8)); }
        
        @keyframes walk-normal { from { background-position-x: 0px; } to { background-position-x: -128px; } }
        @keyframes walk-golden { from { background-position-x: 0px; } to { background-position-x: -192px; } }

        .walk-down { background-position-y: 0px; }
        .walk-up { background-position-y: -32px; }
        .walk-right { background-position-y: -64px; }
        .walk-left { background-position-y: -96px; }

        .tourist-sprite.walk-down, .tourist-sprite.walk-up, .tourist-sprite.walk-right, .tourist-sprite.walk-left,
        .puppy-sprite.walk-down, .puppy-sprite.walk-up, .puppy-sprite.walk-right, .puppy-sprite.walk-left {
            animation: walk-normal 0.6s steps(4) infinite;
        }

        .golden-puppy-sprite.walk-down { background-position-y: 0px; }
        .golden-puppy-sprite.walk-up { background-position-y: -48px; }
        .golden-puppy-sprite.walk-right { background-position-y: -96px; }
        .golden-puppy-sprite.walk-left { background-position-y: -144px; }
        .golden-puppy-sprite.walk-down, .golden-puppy-sprite.walk-up, .golden-puppy-sprite.walk-right, .golden-puppy-sprite.walk-left {
            animation: walk-golden 0.6s steps(4) infinite;
        }
        .idle { animation: none !important; background-position-x: 0px !important; }
"""
html = html.replace("/* 건축물 기본 속성 */", sprite_css + "\n        /* 건축물 기본 속성 */")

# 2. JS updateSpriteDirection 함수 추가
sprite_js = """
        function updateSpriteDirection(el, dx, dy, isMoving) {
            el.classList.remove('walk-down', 'walk-up', 'walk-left', 'walk-right', 'idle');
            if (!isMoving) {
                el.classList.add('idle');
                return;
            }
            if (Math.abs(dx) > Math.abs(dy)) {
                if (dx > 0) el.classList.add('walk-right');
                else el.classList.add('walk-left');
            } else {
                if (dy > 0) el.classList.add('walk-down');
                else el.classList.add('walk-up');
            }
        }
"""
html = html.replace("function showEmotion(x, y, emoji) {", sprite_js + "\n        function showEmotion(x, y, emoji) {")

# 3. spawnTourist 수정
html = html.replace("t.className = 'tourist'; t.innerText = '👦';", "t.className = 'tourist-sprite walk-down';")

# 4. Tourist Loop 수정
html = html.replace("""                        t.x += (Math.random()-0.5)*300;
                        t.y += (Math.random()-0.5)*300;""",
"""                        let rndX = (Math.random()-0.5)*300; let rndY = (Math.random()-0.5)*300;
                        t.x += rndX;
                        t.y += rndY;
                        updateSpriteDirection(t.el, rndX, rndY, true);""")

html = html.replace("""                            const speed = 100; 
                            const ratio = Math.min(1, speed / dist);
                            t.x += dx * ratio;
                            t.y += dy * ratio;""",
"""                            const speed = 100; 
                            const ratio = Math.min(1, speed / dist);
                            let moveX = dx * ratio; let moveY = dy * ratio;
                            t.x += moveX;
                            t.y += moveY;
                            updateSpriteDirection(t.el, moveX, moveY, true);""")

html = html.replace("""                        if (dist < 80) {
                            t.state = 'enjoying';
                            t.timer = 5; 
                            t.el.style.transition = 'none'; 
                        }""",
"""                        if (dist < 80) {
                            t.state = 'enjoying';
                            t.timer = 5; 
                            t.el.style.transition = 'none';
                            updateSpriteDirection(t.el, 0, 0, false);
                        }""")

html = html.replace("""                    t.x += (t.x < 1500 ? -300 : 300);
                    t.y += (t.y < 1500 ? -300 : 300);""",
"""                    let lx = (t.x < 1500 ? -300 : 300);
                    let ly = (t.y < 1500 ? -300 : 300);
                    t.x += lx;
                    t.y += ly;
                    updateSpriteDirection(t.el, lx, ly, true);""")

# 5. spawnPuppy 수정
html = html.replace("""            p.className = isGolden ? 'golden-puppy' : 'puppy';
            p.innerText = isGolden ? '🐕✨' : '🐶';""",
"""            p.className = (isGolden ? 'golden-puppy-sprite' : 'puppy-sprite') + ' walk-down';""")

# 6. Puppy Loop 수정
html = html.replace("""                            pup.x += dx * (speed/dist); pup.y += dy * (speed/dist);
                        }
                    } else {
                        pup.state = 'roaming';
                    }""",
"""                            let mx = dx * (speed/dist); let my = dy * (speed/dist);
                            pup.x += mx; pup.y += my;
                            updateSpriteDirection(pup.el, mx, my, true);
                        }
                    } else {
                        pup.state = 'roaming';
                    }""")

html = html.replace("""                        if(dist < 40) {
                            pup.state = 'eating'; pup.timer = 4;
                            pup.target.el.remove();
                            droppedItems = droppedItems.filter(d => d !== pup.target);
                        } else {""",
"""                        if(dist < 40) {
                            pup.state = 'eating'; pup.timer = 4;
                            pup.target.el.remove();
                            droppedItems = droppedItems.filter(d => d !== pup.target);
                            updateSpriteDirection(pup.el, 0, 0, false);
                        } else {""")

html = html.replace("""                            pup.state = 'roaming';
                        }
                    }
                } else if (pup.state === 'roaming') {""",
"""                            pup.state = 'roaming';
                        }
                    }
                } else if (pup.state === 'roaming') {""")

html = html.replace("""                        } else {
                            pup.x += (Math.random()-0.5)*200; pup.y += (Math.random()-0.5)*200;
                        }
                    } else {
                        // 일반 강아지는 성곽(castle)을 찾으면 기사로 진급
                        const castles = placedBuildings.filter(b => b.key === 'castle');
                        if(castles.length > 0 && Math.random() < 0.2) {
                            const c = castles[Math.floor(Math.random()*castles.length)];
                            pup.targetEl = c.el;
                            pup.state = 'going_castle';
                        } else {
                            pup.x += (Math.random()-0.5)*200; pup.y += (Math.random()-0.5)*200;
                        }
                    }""",
"""                        } else {
                            let rx = (Math.random()-0.5)*200; let ry = (Math.random()-0.5)*200;
                            pup.x += rx; pup.y += ry;
                            updateSpriteDirection(pup.el, rx, ry, true);
                        }
                    } else {
                        // 일반 강아지는 성곽(castle)을 찾으면 기사로 진급
                        const castles = placedBuildings.filter(b => b.key === 'castle');
                        if(castles.length > 0 && Math.random() < 0.2) {
                            const c = castles[Math.floor(Math.random()*castles.length)];
                            pup.targetEl = c.el;
                            pup.state = 'going_castle';
                        } else {
                            let rx = (Math.random()-0.5)*200; let ry = (Math.random()-0.5)*200;
                            pup.x += rx; pup.y += ry;
                            updateSpriteDirection(pup.el, rx, ry, true);
                        }
                    }""")

html = html.replace("""                            pup.isKnight = true; pup.el.innerText = '🐶⚔️'; pup.el.classList.add('knight');
                            showEmotion(pup.x, pup.y, '⚔️'); pup.state = 'roaming';
                        } else {
                            pup.x += dx * (speed/dist); pup.y += dy * (speed/dist);
                        }""",
"""                            pup.isKnight = true; pup.el.classList.add('puppy-knight');
                            let sword = document.createElement('div'); sword.innerText = '⚔️'; sword.style.position = 'absolute'; sword.style.top = '-15px'; sword.style.left = '5px'; sword.style.fontSize = '20px'; pup.el.appendChild(sword);
                            showEmotion(pup.x, pup.y, '⚔️'); pup.state = 'roaming';
                            updateSpriteDirection(pup.el, 0, 0, false);
                        } else {
                            let mx = dx * (speed/dist); let my = dy * (speed/dist);
                            pup.x += mx; pup.y += my;
                            updateSpriteDirection(pup.el, mx, my, true);
                        }""")

html = html.replace("""                            pup.targetEl.remove();
                            showEmotion(pup.x, pup.y, '🦴');
                            pup.state = 'roaming';
                        } else {
                            pup.x += dx * (speed/dist); pup.y += dy * (speed/dist);
                        }""",
"""                            pup.targetEl.remove();
                            showEmotion(pup.x, pup.y, '🦴');
                            pup.state = 'roaming';
                            updateSpriteDirection(pup.el, 0, 0, false);
                        } else {
                            let mx = dx * (speed/dist); let my = dy * (speed/dist);
                            pup.x += mx; pup.y += my;
                            updateSpriteDirection(pup.el, mx, my, true);
                        }""")

html = html.replace("""                } else if (pup.state === 'leaving') {
                    pup.x -= 300; pup.y -= 300;
                    if(pup.x < -200 || pup.y < -200) { pup.el.remove(); puppiesList[i] = null; }
                }""",
"""                } else if (pup.state === 'leaving') {
                    pup.x -= 300; pup.y -= 300;
                    updateSpriteDirection(pup.el, -300, -300, true);
                    if(pup.x < -200 || pup.y < -200) { pup.el.remove(); puppiesList[i] = null; }
                }""")


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html for spritesheets successfully!")
