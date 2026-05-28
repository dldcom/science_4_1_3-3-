# 화산 타쿤 게임 에셋 이미지 생성 가이드

이 가이드는 다른 이미지 생성 AI(Midjourney, DALL-E, Stable Diffusion 등)를 사용하여 현재 게임과 완벽하게 어울리는 에셋을 직접 생성하기 위한 프롬프트 가이드 및 후처리 방법입니다.

## 1. 프롬프트 작성 공식 (필수 키워드)

현재 게임의 모든 이미지는 통일된 뷰와 스타일을 가지고 있습니다. 프롬프트 작성 시 아래의 **기본 공식**을 반드시 포함해야 합니다.

### 기본 프롬프트 구조 (영문 권장)
```text
2.5D game asset, front view of [원하는 건물/지형 설명], [세부 디테일], Cute casual cartoon style, perfectly isolated on a pure #ffffff white background
```

### 핵심 키워드 설명
* **`2.5D game asset, front view`**: 건물을 탑다운 2.5D 시점의 **정면**에서 바라보도록 강제합니다. (쿼터뷰나 완전한 위에서 본 탑뷰가 되지 않게 방지)
* **`Cute casual cartoon style`**: 너무 실사 같지 않은 귀여운 캐주얼 게임 그래픽 스타일을 유지합니다.
* **`perfectly isolated on a pure #ffffff white background`**: 파이썬 스크립트로 배경을 쉽게 지우기 위해, 그림자나 그라데이션이 없는 **완벽한 순백색 배경**을 강제합니다.

### 예시 프롬프트

* **검은 모래 해변 타일 (2x2)**
  > 2.5D game asset, front view of a flat ground tile covered in dark black volcanic sand. Small blue water waves touching the edge. Cute casual cartoon style, perfectly isolated on a pure #ffffff white background
* **수정하고 싶으셨던 일반 밭 (3x3)**
  > 2.5D game asset, 3x3 tile size, front view of a basic farming plot with normal brown soil mixed with a few dark grey volcanic rocks. A few tiny green sprouts are growing. Cute casual cartoon style, perfectly isolated on a pure #ffffff white background
* **지열 발전소 (3x3)**
  > 2.5D game asset, front view of a modern geothermal power plant made of dark basalt stone and metal pipes, steam coming out of cooling towers. Cute casual cartoon style, perfectly isolated on a pure #ffffff white background

---

## 2. 배경 투명화 파이썬 스크립트 적용

이미지를 생성하셨다면, 배경을 투명하게(PNG) 만들어야 게임 맵과 자연스럽게 어우러집니다.

### Python 스크립트 (`remove_bg.py`)

생성된 이미지의 절대 경로를 스크립트에 입력하여 실행하면 배경이 완벽하게 제거됩니다.

```python
import sys
from PIL import Image

def remove_white_bg(img_path, out_path, tolerance=230):
    img = Image.open(img_path).convert("RGBA")
    data = img.getdata()
    
    new_data = []
    for item in data:
        # 픽셀이 흰색에 가까우면 (R,G,B가 모두 tolerance 이상이면) 투명하게 만듦
        if item[0] > tolerance and item[1] > tolerance and item[2] > tolerance:
            new_data.append((255, 255, 255, 0)) # 투명(Alpha 0)
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(out_path, "PNG")
    print("Background removed and saved to", out_path)

# 사용 예시 (경로를 수정하여 사용하세요)
input_image = r"C:\path\to\your\generated_image.png"
output_image = r"C:\Users\dldco\Downloads\claude\science_3\science_4_1_3-3-\your_item_processed.png"

remove_white_bg(input_image, output_image, tolerance=230)
```

### 실행 방법
1. 터미널(또는 명령 프롬프트)을 엽니다.
2. `Pillow` 라이브러리가 없다면 설치합니다: `py -m pip install Pillow`
3. 파이썬 스크립트를 실행합니다: `py remove_bg.py`

### 주의사항
* 안티앨리어싱(경계선 번짐)이나 회색 그림자가 강하게 생성된 경우 `tolerance=230` 수치를 조절하세요 (예: `240`으로 올리면 더 엄격하게 완전 흰색만 지움).
* 생성된 `_processed.png` 이미지를 `index.html`의 `items` 리스트에 `img` 속성으로 등록하시면 게임 내 상점과 보드에 바로 반영됩니다!
