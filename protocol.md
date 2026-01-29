# v0.1 사람 + 화재 겸용

## 공통 규칙

### 좌표 기준

* 모든 좌표는 **영상 프레임의 픽셀 좌표** 기준
* 원점 `(0,0)`은 **좌상단**
* `x`는 **오른쪽으로 증가**, `y`는 **아래로 증가**
* 예: `(120,80)`은 “왼쪽에서 120px, 위에서 80px” 위치

### Zone inside 판정 공통

* `inside=true` 판정은 **event_type별 rule_point**를 계산한 뒤, 그 점이 **zone polygon 내부**면 true
* rule_point 정의:

  * **사람 침입 (`ZONE_INTRUSION`, `object_type=PERSON`)**
    `bottom_center = ((x1+x2)/2, y2)`
  * **화재/연기 (`FIRE_DETECTED`, `SMOKE_DETECTED`, `object_type=FIRE|SMOKE`)**
    `bbox_center = ((x1+x2)/2, (y1+y2)/2)` *(권장)*

> 참고: 팀이 “모든 타입을 bottom_center로 통일”하고 싶으면 가능하지만, 화재/연기는 bbox_center가 더 자연스럽다.

---

## 1) 이벤트 JSON 스키마 (AI -> 백엔드)

### 필드 정의(요약)

* **공통 필수**: `event_id`, `ts`, `site_id`, `camera_id`, `event_type`, `severity`, `bbox`, `confidence`, `zone`, `snapshot_path`
* **조건부**:

  * `track_id`: `object_type=PERSON`일 때 **필수**, `FIRE/SMOKE`는 **optional**
  * `object_type`: **권장(사실상 필수로 써도 됨)** — 프론트/IoT 단순화를 위해 넣자

### 이벤트 예시 1) 사람 Zone 침입

```jsonc
{
  "event_id": "2f7f3e6a-3c0e-4f3b-9a2e-5f1d7d0b9f3a",
  // 이벤트 고유 ID (중복 방지/추적용). 보통 UUID.

  "ts": "2026-01-28T14:03:21+09:00",
  // 이벤트 발생 시각(ISO-8601). +09:00은 KST.
  // 기준: (권장) "프레임 캡처 시각"

  "site_id": "S001",
  // 현장/시설 식별자

  "camera_id": "C012",
  // 카메라 식별자

  "event_type": "ZONE_INTRUSION",
  // 이벤트 종류(enum)
  // - ZONE_INTRUSION
  // - FIRE_DETECTED
  // - SMOKE_DETECTED

  "object_type": "PERSON",
  // 감지 대상(enum) - 권장
  // - PERSON | FIRE | SMOKE

  "severity": "HIGH",
  // 심각도(예: LOW/MEDIUM/Hदम/HIGH/CRITICAL 등 팀 합의)

  "track_id": 37,
  // 추적 ID
  // - PERSON(ZONE_INTRUSION)에서는 필수
  // - FIRE/SMOKE에서는 optional(없거나 null 가능)

  "bbox": { "x1": 120, "y1": 80, "x2": 260, "y2": 410 },
  // 바운딩 박스 (픽셀). (x1,y1)=좌상단, (x2,y2)=우하단

  "confidence": 0.91,
  // 신뢰도(0~1)

  "zone": { "zone_id": "Z3", "inside": true },
  // zone 결과
  // inside는 "event_type별 rule_point"가 polygon 내부면 true

  "snapshot_path": "snapshots/S001/C012/20260128_140321_37.jpg"
  // 스냅샷 경로/키 (프론트가 접근 가능한 형태로 쓰는 것을 권장)
}
```

### 이벤트 예시 2) 화재 감지(불꽃)

```jsonc
{
  "event_id": "7a9c9f2b-8d7f-4a6a-9a4c-4b2b2e1f0c21",
  "ts": "2026-01-28T14:03:21+09:00",
  "site_id": "S001",
  "camera_id": "C012",

  "event_type": "FIRE_DETECTED",
  "object_type": "FIRE",

  "severity": "CRITICAL",

  "bbox": { "x1": 430, "y1": 210, "x2": 560, "y2": 390 },
  "confidence": 0.88,

  "zone": { "zone_id": "Z3", "inside": true },

  "snapshot_path": "snapshots/S001/C012/20260128_140321_fire.jpg"

  // track_id는 FIRE/SMOKE에서는 optional
}
```

> 참고: 주석 포함 JSON은 `jsonc` 표기. 실제 전송은 주석 없는 JSON.

---

## 2) Zone 폴리곤 포맷 (프론트/백/AI 공통)

```jsonc
{
  "zone_id": "Z3",
  // zone 고유 ID

  "site_id": "S001",
  // 현장 ID

  "camera_id": "C012",
  // 카메라 ID (polygon 좌표 해석 기준)

  "name": "restricted_area_1",
  // 표시용 이름

  "zone_type": "restricted",
  // zone 분류(enum 예: restricted/danger/warning)

  "polygon": [[120,80],[500,90],[520,400],[140,420]],
  // 다각형 꼭짓점 목록 ([x,y] 픽셀)

  "enabled": true
  // 활성 여부(false면 AI는 무시)
}
```

---

## 3) 백엔드 API 2개

### GET zones

* **GET /api/sites/S001/cameras/C012/zones**

  * 의미: 특정 site/camera의 zone 목록 조회

응답 예시:

```jsonc
[
  {
    "zone_id": "Z3",
    "camera_id": "C012",
    "zone_type": "restricted",
    "polygon": [[120,80],[500,90],[520,400],[140,420]],
    "enabled": true
  }
]
```

> 참고: 응답 필드는 “Zone 공통 포맷과 동일”로 갈지, “AI 최소필드만” 줄지 팀에서 통일 권장.

### POST events

* **POST /api/events**

  * 의미: AI 이벤트 전송(저장/알림/프론트 전달/Iot 연동)

요청 바디:

* 위 이벤트 JSON 그대로

응답 예시:

```json
{ "ok": true }
```

---

## 4) 스트림 표준 (초기 고정값)

* 프로토콜: RTSP
* 코덱: H.264
* 해상도: 1280x720
* FPS: 15

RTSP URL 예시:

* `rtsp://user:pass@192.168.0.10:554/stream1`

---

## (권장) v0.1.1에서 팀이 “결정”으로 체크할 항목

* `ts` 기준: **프레임 캡처 시각**으로 고정할지?
* 화재/연기의 zone inside rule_point: **bbox_center**로 고정할지?

---