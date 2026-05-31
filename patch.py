import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS 추가
css_add = """
        /* 건물/강아지 관련 스타일 */
        #building-modal .modal-content { display: flex; flex-direction: column; gap: 10px; }
        .building-action-btn { padding: 12px; background: #4CAF50; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.1s; display: block; width: 100%; box-sizing: border-box; margin-bottom: 5px; }
        .building-action-btn:active { transform: scale(0.95); }
        .building-action-btn.move-btn { background: #2196F3; }
        .building-action-btn.demo-btn { background: #f44336; }
        .building-action-btn:disabled { background: #ccc; cursor: not-allowed; }
        
        .puppy { position: absolute; font-size: 40px; z-index: 19000; animation: bounceIn 0.5s; filter: drop-shadow(0 5px 5px rgba(0,0,0,0.4)); transition: left 0.5s linear, top 0.5s linear; pointer-events: none; }
        .puppy.knight { font-size: 45px; filter: drop-shadow(0 5px 10px rgba(255,215,0,0.5)); }
        .golden-puppy { position: absolute; font-size: 60px; filter: drop-shadow(0 0 20px rgba(255,215,0,1)); animation: glow 1s infinite alternate; transition: left 1s linear, top 1s linear; z-index: 19000; pointer-events: none; }
        @keyframes glow { from { filter: drop-shadow(0 0 10px rgba(255,215,0,0.8)); } to { filter: drop-shadow(0 0 25px rgba(255,215,0,1)); } }
"""
html = html.replace("/* 건축물 기본 속성 */", css_add + "\n        /* 건축물 기본 속성 */")

# 2. HTML 모달 및 인벤토리 추가
html_modal = """
        <div id="building-modal" class="modal-bg" style="z-index: 35000;" onclick="closeBuildingModal()">
            <div class="modal-content" style="max-width: 320px; padding: 20px;" onclick="event.stopPropagation()">
                <div style="font-size: 50px; margin-bottom: 5px;" id="bm-icon"></div>
                <h2 id="bm-title" style="margin: 0 0 5px 0; color: #FF5722; font-size: 22px;">이름</h2>
                <div id="bm-desc" style="font-size: 14px; color: #555; margin-bottom: 15px; word-break: keep-all; line-height: 1.3;">설명</div>
                <div id="bm-custom-ui"></div>
                <div style="margin-top: 15px;">
                    <button class="building-action-btn move-btn" onclick="moveCurrentBuilding()">🏗️ 위치 이동</button>
                    <button class="building-action-btn demo-btn" onclick="demolishCurrentBuilding()">💣 철거 (비용 50% 반환)</button>
                </div>
            </div>
        </div>
"""
html = html.replace('<div id="dict-modal"', html_modal + '\n        <div id="dict-modal"')

inv_golden = '<div class="inv-item" title="황금 물고구마 (분화구 호수에서 획득)"><span class="icon">✨🍠</span>황금: <span id="inv-golden_potato">0</span></div>'
html = html.replace('<div class="inv-item" title="용암 군고구마">', inv_golden + '\n                <div class="inv-item" title="용암 군고구마" onclick="dropItem(\'roasted\')" style="cursor:pointer; border: 2px solid #FF9800;">')
html = html.replace('id="inv-golden_potato">0</span></div>', 'id="inv-golden_potato">0</span></div>\n                <div style="width:100%; font-size:12px; color:#555; margin-top:-5px; text-align:center;">💡 군고구마를 클릭하면 바닥에 떨어뜨립니다.</div>')

# 3. inventory 변수 수정
html = html.replace('const inventory = { gas: 200, lava: 200, ash: 200, rock: 200, potato: 0, roasted: 0, tourists: 0 };', 'const inventory = { gas: 200, lava: 200, ash: 200, rock: 200, potato: 0, roasted: 0, golden_potato: 0, tourists: 0 };')

# 4. Quest 수정 (관광객 로직 변경)
html = html.replace('desc: \'관광객 5명 터치하여 반기기\', condition: () => inventory.tourists >= 5', 'desc: \'관광객 누적 10명 방문\', condition: () => inventory.tourists >= 10')

# 5. 관광객 터치 로직 제거 & spawnTourist 수정
html = html.replace("t.addEventListener('mousedown', () => checkCollection(t));", "")
html = html.replace("t.addEventListener('mouseover', () => { if(isSweeping) checkCollection(t); });", "inventory.tourists++; updateUI();")

# 6. checkCollection에서 관광객 제거
old_check_col = """} else if(el.classList.contains('tourist')) {
                inventory.tourists++;
                updateUI();
                showAlert("👦 관광객 터치 환영!");
            }"""
html = html.replace(old_check_col, "}")

# 7. 건물 클릭 이벤트 및 드래그 로직 분리
old_click = """                el.addEventListener('mousedown', (ev) => {
                    if(key === 'oven') handleOvenClick(el);
                    else if(key === 'farm') handleFarmClick(el);
                    else checkCollection(el);
                    dragStart(ev, el);
                });
                el.addEventListener('touchstart', (ev) => {
                    if(key === 'oven') handleOvenClick(el);
                    else if(key === 'farm') handleFarmClick(el);
                    else checkCollection(el);
                    dragStart(ev, el);
                }, {passive: false});"""

new_click = """                el.addEventListener('click', (ev) => {
                    if(isPanning) return;
                    openBuildingModal(el, key);
                });"""
html = html.replace(old_click, new_click)

# 8. 자바스크립트 모달 제어 로직, 건물 기능들, 강아지 로직 등 한방에 삽입
script_insert = """
        let currentBuildingEl = null;
        let currentBuildingKey = null;

        function closeBuildingModal() {
            document.getElementById('building-modal').style.display = 'none';
            currentBuildingEl = null;
            currentBuildingKey = null;
        }

        function openBuildingModal(el, key) {
            currentBuildingEl = el;
            currentBuildingKey = key;
            const item = items[key];
            const bData = placedBuildings.find(b => b.el === el);
            
            document.getElementById('bm-icon').innerHTML = item.img ? `<img src="${item.img}" style="width:50px;height:50px;">` : item.emoji;
            document.getElementById('bm-title').innerText = item.name + (bData.upgraded ? " (업그레이드됨)" : "");
            document.getElementById('bm-desc').innerText = item.desc;
            
            const customUI = document.getElementById('bm-custom-ui');
            customUI.innerHTML = '';
            
            // 건물별 커스텀 버튼
            if (key === 'bomb') {
                customUI.innerHTML = `<button class="building-action-btn" onclick="triggerBuildingAction('bomb')">🔨 자원 분쇄 (암석 1 ➔ 화산재 3)</button>`;
            } else if (key === 'harubang') {
                customUI.innerHTML = `<button class="building-action-btn" onclick="triggerBuildingAction('harubang')">🎁 기념품 판매 (화산재 5 ➔ 고구마 1)</button>`;
            } else if (key === 'pond') {
                customUI.innerHTML = `<button class="building-action-btn" onclick="triggerBuildingAction('pond')">💧 수분 공급 (10초간 가스 생성)</button>`;
            } else if (key === 'oven') {
                customUI.innerHTML = `<button class="building-action-btn" onclick="triggerBuildingAction('oven')" ${bData.baking ? 'disabled' : ''}>🔥 고구마 굽기 (고구마 1 소모)</button>`;
            } else if (key === 'castle') {
                customUI.innerHTML = `<div style="font-size:13px; color:#555; margin-bottom:5px;">🏰 강아지가 도착하면 기사(⚔️)가 됩니다!</div>`;
            } else if (key === 'crater') {
                customUI.innerHTML = `<button class="building-action-btn" onclick="triggerBuildingAction('crater_fuse')" style="background:#9C27B0;">✨ 풍요의 호수 (용암 10 소모)</button>
                                      <button class="building-action-btn" onclick="triggerBuildingAction('crater_gold')" style="background:#E6C229; color:black;">🍠 전설의 황금 고구마 진화 (고구마 1)</button>`;
            } else if (key === 'farm') {
                if(!bData.upgraded) {
                    customUI.innerHTML = `<button class="building-action-btn" onclick="triggerBuildingAction('farm_upgrade')" style="background:#E6C229; color:black;">⭐ 초비옥 농장 업그레이드 (화산재 20)</button>`;
                } else {
                    customUI.innerHTML = `<div style="font-size:13px; color:#4CAF50; font-weight:bold;">✨ 업그레이드 완료: 고구마 생성 2배!</div>`;
                }
            }

            document.getElementById('building-modal').style.display = 'flex';
        }

        function triggerBuildingAction(action) {
            const el = currentBuildingEl;
            const bData = placedBuildings.find(b => b.el === el);
            if(!bData) return;
            
            if (action === 'bomb') {
                if (inventory.rock >= 1) {
                    inventory.rock -= 1; inventory.ash += 3; updateUI();
                    showAlert("🔨 암석을 부숴 화산재 3개를 얻었습니다!");
                } else showAlert("암석이 부족합니다!");
            } else if (action === 'harubang') {
                if (inventory.ash >= 5) {
                    inventory.ash -= 5; inventory.potato += 1; updateUI();
                    showAlert("🎁 관광객에게 기념품을 팔고 고구마를 얻었습니다!");
                } else showAlert("화산재가 부족합니다!");
            } else if (action === 'pond') {
                showAlert("💧 10초간 화산 가스가 스폰됩니다.");
                let count = 0;
                let intv = setInterval(() => {
                    if(!document.body.contains(el)) return clearInterval(intv);
                    createParticle('gas', parseInt(el.style.left)+30, parseInt(el.style.top)+30);
                    count++;
                    if(count >= 10) clearInterval(intv);
                }, 1000);
            } else if (action === 'oven') {
                if (inventory.potato >= 1 && !bData.baking) {
                    inventory.potato--; updateUI();
                    bData.baking = true;
                    if(el.querySelector('.oven-fire')) el.querySelector('.oven-fire').style.display = 'block';
                    el.style.filter = 'drop-shadow(0 0 15px #FF5722) brightness(1.2)';
                    showAlert("🔥 고구마를 굽는 중... (10초)");
                    closeBuildingModal();
                    setTimeout(() => {
                        if(!document.body.contains(el)) return;
                        bData.baking = false;
                        if(el.querySelector('.oven-fire')) el.querySelector('.oven-fire').style.display = 'none';
                        el.style.filter = '';
                        inventory.roasted++; updateUI();
                        showAlert("🍕 용암 군고구마 완성!");
                    }, 10000);
                } else showAlert("구울 고구마가 없습니다!");
            } else if (action === 'farm_upgrade') {
                if (inventory.ash >= 20) {
                    inventory.ash -= 20; bData.upgraded = true; updateUI();
                    el.style.background = `url('farm_upgraded_processed.webp') no-repeat center/contain`;
                    showAlert("✨ 초비옥 농장으로 업그레이드 되었습니다!");
                    closeBuildingModal();
                } else showAlert("화산재 20개가 필요합니다!");
            } else if (action === 'crater_fuse') {
                if(inventory.lava >= 10) {
                    inventory.lava -= 10; updateUI(); closeBuildingModal();
                    showAlert("🌊 풍요의 호수가 폭발합니다!");
                    for(let i=0; i<6; i++) {
                        setTimeout(()=>createParticle(resTypes[Math.floor(Math.random()*resTypes.length)], parseInt(el.style.left)+45, parseInt(el.style.top)+45), i*200);
                    }
                } else showAlert("용암이 10개 필요합니다!");
            } else if (action === 'crater_gold') {
                if(inventory.potato >= 1 && !bData.baking) {
                    inventory.potato--; updateUI(); bData.baking = true; closeBuildingModal();
                    showAlert("✨ 30초 뒤 황금 물고구마가 완성됩니다!");
                    el.style.filter = 'drop-shadow(0 0 20px #FFD700)';
                    setTimeout(() => {
                        if(!document.body.contains(el)) return;
                        bData.baking = false; el.style.filter = '';
                        inventory.golden_potato++; updateUI();
                        showAlert("✨ 황금 물고구마를 얻었습니다!");
                    }, 30000);
                } else showAlert("고구마가 1개 필요합니다!");
            }
        }

        function moveCurrentBuilding() {
            if(!currentBuildingEl) return;
            const el = currentBuildingEl;
            closeBuildingModal();
            // 임시로 이벤트 에뮬레이션
            let ev = new MouseEvent('mousedown', { clientX: window.innerWidth/2, clientY: window.innerHeight/2 });
            dragStart(ev, el);
        }

        function demolishCurrentBuilding() {
            if(!currentBuildingEl || !currentBuildingKey) return;
            if(confirm("정말 철거하시겠습니까? 건설 비용의 50%를 돌려받습니다.")) {
                const item = items[currentBuildingKey];
                for(let res in item.cost) {
                    inventory[res] += Math.floor(item.cost[res] / 2);
                }
                placedBuildings = placedBuildings.filter(b => b.el !== currentBuildingEl);
                currentBuildingEl.remove();
                updateUI();
                showAlert("💣 건물이 철거되었습니다.");
                closeBuildingModal();
            }
        }

        // 아이템 바닥에 버리기 (강아지 시스템)
        let droppedItems = [];
        let puppiesList = [];
        
        function dropItem(type) {
            if(type === 'roasted' && inventory.roasted >= 1) {
                inventory.roasted--; updateUI();
                spawnDroppedItem('🍕', 'roasted');
            } else if(type === 'golden_potato' && inventory.golden_potato >= 1) {
                inventory.golden_potato--; updateUI();
                spawnDroppedItem('✨🍠', 'golden');
            }
        }
        
        document.getElementById('inv-golden_potato').parentElement.onclick = () => dropItem('golden_potato');
        document.getElementById('inv-golden_potato').parentElement.style.cursor = 'pointer';

        function spawnDroppedItem(emoji, type) {
            const cx = (window.innerWidth / 2 - boardX) / zoomLevel;
            const cy = (window.innerHeight / 2 - boardY) / zoomLevel;
            const p = document.createElement('div');
            p.className = 'crop';
            p.innerText = emoji;
            p.style.left = (cx - 20) + 'px';
            p.style.top = (cy - 20) + 'px';
            board.appendChild(p);
            
            const dropData = { el: p, type: type, x: cx, y: cy };
            droppedItems.push(dropData);
            showAlert(type === 'golden' ? "✨ 전설의 향기가 퍼집니다..." : "🐶 맛있는 냄새가 퍼집니다!");
            
            // 강아지 스폰
            setTimeout(() => spawnPuppy(dropData, type === 'golden'), 1000);
        }
        
        function spawnPuppy(targetDrop, isGolden) {
            const edges = [ {x: Math.random()*3000, y: -50}, {x: Math.random()*3000, y: 3050}, {x: -50, y: Math.random()*3000}, {x: 3050, y: Math.random()*3000} ];
            const edge = edges[Math.floor(Math.random() * edges.length)];
            
            const p = document.createElement('div');
            p.className = isGolden ? 'golden-puppy' : 'puppy';
            p.innerText = isGolden ? '🐕✨' : '🐶';
            p.style.left = edge.x + 'px'; p.style.top = edge.y + 'px';
            board.appendChild(p);
            
            puppiesList.push({ el: p, x: edge.x, y: edge.y, target: targetDrop, state: 'seeking', isKnight: false, isGolden: isGolden });
        }
"""
html = html.replace('function erupt(amountMultiplier = 1) {', script_insert + '\n        function erupt(amountMultiplier = 1) {')

# 9. 주기적 게임 루프 수정 (건물 패시브 & 강아지 로직)
loop_add = """
            // 추가 건물 패시브 로직
            placedBuildings.forEach(b => {
                if(b.key === 'pillar' && dayTick % 30 === 0) {
                    createParticle(resTypes[Math.floor(Math.random()*resTypes.length)], parseInt(b.el.style.left)+15, parseInt(b.el.style.top)+15);
                }
                if(b.key === 'beach' && dayTick % 20 === 0) {
                    createParticle(resTypes[Math.floor(Math.random()*resTypes.length)], parseInt(b.el.style.left)+30, parseInt(b.el.style.top)+30);
                }
            });

            // 강아지 이동 루직 (0.5초마다 갱신하기 위해 setInterval 분리하는게 좋지만, 여기서는 좌표 이동 계산)
"""
html = html.replace('if(dayTick % 10 === 0) erupt(1);', loop_add + '\n            if(dayTick % 10 === 0) erupt(1);')

# 10. 강아지 AI 루프 (touristsList loop 바로 밑에 추가)
puppy_loop = """
        setInterval(() => {
            puppiesList.forEach((pup, i) => {
                if(!pup) return;
                
                let speed = pup.isGolden ? 80 : 50;
                if(pup.isKnight) speed = 90;
                
                if (pup.state === 'seeking') {
                    if(pup.target && pup.target.el.parentNode) {
                        let dx = pup.target.x - pup.x; let dy = pup.target.y - pup.y;
                        let dist = Math.sqrt(dx*dx + dy*dy);
                        if(dist < 40) {
                            pup.state = 'eating'; pup.timer = 4;
                            pup.target.el.remove();
                            droppedItems = droppedItems.filter(d => d !== pup.target);
                        } else {
                            pup.x += dx * (speed/dist); pup.y += dy * (speed/dist);
                        }
                    } else {
                        pup.state = 'roaming';
                    }
                } else if (pup.state === 'eating') {
                    pup.timer--;
                    if(pup.timer <= 0) {
                        showEmotion(pup.x, pup.y, '💖');
                        if(pup.isGolden) {
                            showAlert("✨ 황금 강아지가 엄청난 보상을 남겼습니다!");
                            erupt(15); 
                            pup.state = 'leaving';
                        } else {
                            pup.state = 'roaming';
                        }
                    }
                } else if (pup.state === 'roaming') {
                    if(pup.isKnight) {
                        // 기사는 맵의 particle을 찾음
                        const particles = Array.from(document.querySelectorAll('.particle'));
                        if(particles.length > 0) {
                            const targetP = particles[Math.floor(Math.random() * particles.length)];
                            pup.targetEl = targetP;
                            pup.state = 'fetching';
                        } else {
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
                    }
                } else if (pup.state === 'going_castle') {
                    if(pup.targetEl && pup.targetEl.parentNode) {
                        let tx = parseInt(pup.targetEl.style.left)+45; let ty = parseInt(pup.targetEl.style.top)+45;
                        let dx = tx - pup.x; let dy = ty - pup.y; let dist = Math.sqrt(dx*dx + dy*dy);
                        if(dist < 50) {
                            pup.isKnight = true; pup.el.innerText = '🐶⚔️'; pup.el.classList.add('knight');
                            showEmotion(pup.x, pup.y, '⚔️'); pup.state = 'roaming';
                        } else {
                            pup.x += dx * (speed/dist); pup.y += dy * (speed/dist);
                        }
                    } else pup.state = 'roaming';
                } else if (pup.state === 'fetching') {
                    if(pup.targetEl && pup.targetEl.parentNode) {
                        let tx = parseInt(pup.targetEl.style.left); let ty = parseInt(pup.targetEl.style.top);
                        let dx = tx - pup.x; let dy = ty - pup.y; let dist = Math.sqrt(dx*dx + dy*dy);
                        if(dist < 50) {
                            inventory[pup.targetEl.dataset.res]++; updateUI();
                            pup.targetEl.remove();
                            showEmotion(pup.x, pup.y, '🦴');
                            pup.state = 'roaming';
                        } else {
                            pup.x += dx * (speed/dist); pup.y += dy * (speed/dist);
                        }
                    } else pup.state = 'roaming';
                } else if (pup.state === 'leaving') {
                    pup.x -= 300; pup.y -= 300;
                    if(pup.x < -200 || pup.y < -200) { pup.el.remove(); puppiesList[i] = null; }
                }
                
                pup.x = Math.max(0, Math.min(3000, pup.x));
                pup.y = Math.max(0, Math.min(3000, pup.y));
                pup.el.style.left = pup.x + 'px'; pup.el.style.top = pup.y + 'px';
            });
            puppiesList = puppiesList.filter(p => p !== null);
        }, 500);
"""
html = html.replace('touristsList = touristsList.filter(t => t !== null);\n        }, 1000);', 'touristsList = touristsList.filter(t => t !== null);\n        }, 1000);\n' + puppy_loop)

# 변경사항 저장
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html successfully!")
