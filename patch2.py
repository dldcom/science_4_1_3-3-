import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS 추가 (top-right-btn)
css_to_add = """
        .top-right-btn { width: 35px; height: 35px; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; transition: 0.1s; display: flex; justify-content: center; align-items: center; color: white; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .top-right-btn:active { transform: scale(0.9); box-shadow: 0 0 2px rgba(0,0,0,0.2); }
        .top-right-btn.move-btn { background: #2196F3; }
        .top-right-btn.demo-btn { background: #f44336; }
"""
html = html.replace('.building-action-btn:disabled { background: #ccc; cursor: not-allowed; }', 
                   '.building-action-btn:disabled { background: #ccc; cursor: not-allowed; }' + css_to_add)

# 2. 모달 HTML 수정
old_modal = """<div class="modal-content" style="max-width: 320px; padding: 20px;" onclick="event.stopPropagation()">
                <div style="font-size: 50px; margin-bottom: 5px;" id="bm-icon"></div>
                <h2 id="bm-title" style="margin: 0 0 5px 0; color: #FF5722; font-size: 22px;">이름</h2>
                <div id="bm-desc" style="font-size: 14px; color: #555; margin-bottom: 15px; word-break: keep-all; line-height: 1.3;">설명</div>
                <div id="bm-custom-ui"></div>
                <div style="margin-top: 15px;">
                    <button class="building-action-btn move-btn" onclick="moveCurrentBuilding()">🏗️ 위치 이동</button>
                    <button class="building-action-btn demo-btn" onclick="demolishCurrentBuilding()">💣 철거 (비용 50% 반환)</button>
                </div>"""

new_modal = """<div class="modal-content" style="max-width: 320px; padding: 20px; position: relative;" onclick="event.stopPropagation()">
                <div style="position: absolute; top: 15px; right: 15px; display: flex; gap: 8px;">
                    <button class="top-right-btn move-btn" onclick="moveCurrentBuilding()" title="위치 이동">🏗️</button>
                    <button class="top-right-btn demo-btn" onclick="demolishCurrentBuilding()" title="철거 (비용 50% 반환)">💣</button>
                </div>
                <div style="font-size: 50px; margin-bottom: 5px;" id="bm-icon"></div>
                <h2 id="bm-title" style="margin: 0 0 5px 0; color: #FF5722; font-size: 22px; padding-right: 80px; word-break: keep-all;">이름</h2>
                <div id="bm-desc" style="font-size: 14px; color: #555; margin-bottom: 15px; word-break: keep-all; line-height: 1.3;">설명</div>
                <div id="bm-custom-ui"></div>"""
html = html.replace(old_modal, new_modal)

# 3. openBuildingModal 내용 수정
old_js = """            const customUI = document.getElementById('bm-custom-ui');
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
            }"""

new_js = """            const customUI = document.getElementById('bm-custom-ui');
            let extraDesc = "";
            if (key === 'wall') extraDesc = `📌 <b>관광 안내판 (패시브)</b><br>관광객이 찾아올 확률을 조금 높여줍니다.`;
            else if (key === 'bomb') extraDesc = `📌 <b>자원 분쇄기 (수동)</b><br>버튼을 눌러 암석 1개를 화산재 3개로 분쇄합니다.<br><br><button class="building-action-btn" onclick="triggerBuildingAction('bomb')">🔨 암석 분쇄</button>`;
            else if (key === 'pillar') extraDesc = `📌 <b>지질학 연구 (패시브)</b><br>30초마다 무작위 자원을 1개씩 자동 생산합니다.`;
            else if (key === 'hot') extraDesc = `📌 <b>관광객 팁 (패시브)</b><br>이 온천을 구경하고 가는 관광객이 '암석'을 바닥에 남깁니다.`;
            else if (key === 'harubang') extraDesc = `📌 <b>기념품 판매 (수동)</b><br>관광객에게 화산재 5개를 팔고 귀한 고구마 1개로 교환합니다.<br><br><button class="building-action-btn" onclick="triggerBuildingAction('harubang')">🎁 기념품 판매</button>`;
            else if (key === 'pond') extraDesc = `📌 <b>수분 공급 (수동)</b><br>10초 동안 주변에 화산 가스를 집중적으로 스폰시킵니다.<br><br><button class="building-action-btn" onclick="triggerBuildingAction('pond')">💧 가스 스폰 시작</button>`;
            else if (key === 'oven') extraDesc = `📌 <b>군고구마 굽기 (수동)</b><br>고구마 1개를 뜨거운 열기로 10초간 구워 군고구마를 만듭니다.<br><br><button class="building-action-btn" onclick="triggerBuildingAction('oven')" ${bData.baking ? 'disabled' : ''}>🔥 고구마 굽기</button>`;
            else if (key === 'sand') extraDesc = `📌 <b>조개 줍기 (패시브)</b><br>20초마다 해변 주변에 조개 대신 무작위 자원이 스폰됩니다.`;
            else if (key === 'castle') extraDesc = `📌 <b>강아지 기사단 (패시브)</b><br>군고구마 냄새를 맡고 온 일반 강아지(🐶)가 성곽에 닿으면 투구를 쓴 기사(⚔️)로 변신해 바닥의 자원을 대신 주워옵니다!`;
            else if (key === 'crater') extraDesc = `📌 <b>신비한 작용 (수동)</b><br>용암을 소비해 자원을 폭발시키거나 고구마를 황금으로 진화시킵니다.<br><br><button class="building-action-btn" onclick="triggerBuildingAction('crater_fuse')" style="background:#9C27B0; margin-bottom:8px;">🌊 풍요의 호수 폭발 (용암 10)</button><button class="building-action-btn" onclick="triggerBuildingAction('crater_gold')" style="background:#E6C229; color:black;">✨ 황금 고구마 진화 (고구마 1)</button>`;
            else if (key === 'farm') {
                extraDesc = `📌 <b>고구마 농사 (패시브)</b><br>시간이 지날 때마다 자동으로 고구마를 수확합니다.`;
                if(!bData.upgraded) extraDesc += `<br><br><button class="building-action-btn" onclick="triggerBuildingAction('farm_upgrade')" style="background:#E6C229; color:black;">⭐ 초비옥 농장 업그레이드 (화산재 20)</button>`;
                else extraDesc += `<br><br><div style="font-size:13px; color:#4CAF50; font-weight:bold;">✨ 업그레이드 완료: 생산속도 2배!</div>`;
            }
            else if (key === 'power') extraDesc = `📌 <b>자원 흡수 (패시브)</b><br>가끔씩 맵에 떨어진 자원을 발전소 쪽으로 강하게 끌어당깁니다.`;
            
            customUI.innerHTML = extraDesc ? `<div style="background:#f9f9f9; padding:12px; border-radius:8px; border:1px solid #ddd; text-align:left; font-size:13.5px; line-height:1.4; color:#333;">${extraDesc}</div>` : '';
"""
html = html.replace(old_js, new_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html successfully!")
