"""사건 대표 정지 이미지용 작업 골격. 기존 동영상 Recorder와 별개다.

아래 반환값·검증·저장 규칙은 향후 구현 계약이다. 현재는 파일/디렉터리 생성,
영상처리, 입력 검증 없이 모든 함수가 NotImplementedError를 발생시킨다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np


def crop_zone_snapshot(
    frame: np.ndarray,
    polygon: Sequence[Sequence[int]] | np.ndarray,
    padding: int = 20,
) -> np.ndarray:
    """위험구역 주변을 잘라 사건 위치를 자세히 확인할 이미지로 만들기 위한 함수.

    입력: frame은 비어 있지 않은 (H, W, 3) uint8 BGR 배열이다.
    polygon은 동일 좌표계의 (N, 2) 정수 꼭짓점 목록/배열(N >= 3)이고,
    padding은 bounding box 사방에 더할 0 이상 정수 픽셀 수이다.
    반환: 잘린 (crop_H, crop_W, 3) uint8 BGR 복사본이다. 원본과 메모리를
    공유하지 않으며 polygon 내부만 마스킹하는 기능은 포함하지 않는다.
    향후 구현: cv2.boundingRect로 사각형을 구하고 padding을 더한 뒤,
    좌상단/우하단을 프레임 경계로 clipping하여 해당 부분을 복사한다.
    연동: pipeline.run_pipeline의 alert 이벤트 처리 후 해당 zone의 points와
    frame을 받아 save_event_snapshot에 넘길 선택적 전처리로 사용할 수 있다.
    주의: 배열 슬라이스의 끝 좌표는 제외됨을 고려한다. 잘못된 입력/음수 padding,
    면적 없는 polygon 또는 clipping 후 빈 교차 영역은 향후 ValueError로 거부한다.
    backend.zones는 입력 해상도 기준이므로 original_frame을 쓰면 호출자가
    좌표를 먼저 맞춰야 한다. 이 함수에서 해상도 비율을 추측하지 않는다.
    기존 zones 데이터, 검출 ROI, 원본 배열, pipeline 및 recorder는 변경하지 않는다.
    """
    # TODO: 프레임·polygon·padding의 계약을 검증한다.
    # TODO: cv2.boundingRect의 범위를 padding만큼 늘리고 영상 경계로 제한한다.
    # TODO: 유효 교차 영역의 독립된 복사본을 반환하여 원본 수정을 방지한다.
    raise NotImplementedError("추가 담당자가 구현해야 하는 기능입니다.")


def save_event_snapshot(
    frame: np.ndarray,
    output_dir: str | Path,
    event_id: str | int,
    zone_name: str | None = None,
) -> Path:
    """침입 확정 순간의 대표 JPG를 저장하여 사건을 빠르게 확인하기 위한 함수.

    입력: frame은 비어 있지 않은 (H, W, 3) uint8 BGR 원본 또는 crop 결과,
    output_dir은 저장 디렉터리, event_id는 비어 있지 않은 문자열 또는
    0 이상 정수 사건 ID, zone_name은 생략 가능하고 제공 시 비어 있지 않은 이름이다.
    반환: cv2.imwrite 성공을 확인한 JPG 경로인 pathlib.Path이다.
    향후 구현: 디렉터리를 준비하고 event_{id}_{zone}.jpg로 저장한다.
    정수/숫자 문자열 ID는 최소 네 자리로 표현한다(1 또는 "1" → 0001).
    zone_name=None이면 구역 접미사를 생략한다. 예: event_0001_zone1.jpg.
    숫자가 아닌 기존 mock ID도 문자열로 수용한다.
    연동: pipeline.run_pipeline에서 정규화된 event["type"] == "alert"일 때
    event_id/zone_name과 같은 시점의 packet["original_frame"]을 전달한다.
    지속 ALERT의 매 프레임마다 저장하지 않도록 호출자가 이벤트당 한 번 호출한다.
    주의: ID/구역명의 경로 구분자·상위 경로 이동 문자를 안전한 문자로 치환하고,
    같은 이름이 존재하면 덮어쓰지 않고 FileExistsError로 알리는 계약이다.
    반복 실행에는 호출자가 실행별 output_dir을 제공한다. 잘못된 입력은
    ValueError, 디렉터리/인코딩/쓰기 실패는 OSError로 알려 실패를 숨기지 않는다.
    기존 recorder.record_frame은 동영상 클립 담당이며 이 함수는 정지 이미지 전용이다.
    Recorder 버퍼·클립·CSV 구조, 사건 ID 생성, config, 원본 픽셀은 변경하지 않는다.
    """
    # TODO: 입력과 파일명 요소를 검증하고 안전한 JPG 저장 경로를 결정한다.
    # TODO: 디렉터리를 준비하고 이름 충돌 시 기존 파일을 보호한다.
    # TODO: cv2.imwrite 반환값/예외를 확인한 뒤 성공한 Path만 반환한다.
    raise NotImplementedError("추가 담당자가 구현해야 하는 기능입니다.")


def make_event_thumbnail(
    frame: np.ndarray, width: int = 320, height: int = 180
) -> np.ndarray:
    """사건 목록·보고서 preview에 사용할 일정 크기 축소 이미지를 만들기 위한 함수.

    입력: frame은 비어 있지 않은 (H, W, 3) uint8 BGR snapshot 또는 crop,
    width/height는 양의 정수 목표 픽셀 크기이다. 기본 출력은 320x180이다.
    반환: 정확히 (height, width, 3)인 별도 uint8 BGR 배열이다.
    향후 구현: 두 축에 동일 배율을 적용해 cv2.resize로 목표 안에 맞춘다.
    남는 공간은 cv2.copyMakeBorder의 검정 상수색 letterbox로 채운다.
    연동: alert 시점에 확보한 frame/crop을 사건 목록이나 보고서용으로
    가공할 때 호출한다. 기존 보고서 생성 코드에는 아직 연결하지 않는다.
    주의: 종횡비를 유지하고 강제 늘리기/잘라내기를 하지 않는다. 정수 반올림
    오차로 목표 크기를 넘거나 한 변이 0이 되지 않도록 제한한다. 홀수 여백은
    아래/오른쪽에 한 픽셀 더 둔다. 축소는 INTER_AREA, 확대는 INTER_LINEAR를
    사용할 예정이다. 작은 입력은 목표 영역에 맞게 확대할 수 있다.
    잘못된 프레임/0 이하 크기/bool 크기는 향후 ValueError로 거부한다.
    파일 저장은 하지 않고 원본 배열, 검출 해상도, 기존 Recorder 영상 크기,
    config 및 benchmark/보고서 코드는 변경하지 않는다.
    """
    # TODO: 입력과 목표 크기를 검증하고 종횡비를 보존할 크기를 계산한다.
    # TODO: cv2.resize로 변환하고 cv2.copyMakeBorder로 남은 여백을 채운다.
    # TODO: 정확한 목표 shape와 원본으로부터 독립된 배열을 반환한다.
    raise NotImplementedError("추가 담당자가 구현해야 하는 기능입니다.")


# ==========================================================
# 기존 시스템 연동 위치
# ==========================================================
# 이 모듈은 현재 기존 pipeline에 연결되어 있지 않다.
# 향후 구현 완료 후 다음 실제 코드 위치가 호출 후보다.
# pipeline.run_pipeline
#   ├─ RealBackend.update → state.update_state → 정규화된 events
#   └─ event["type"] == "alert" 발생 (상태 유지와 구별)
#        ├─ packet["original_frame"] → save_event_snapshot
#        ├─ 같은 좌표계 frame + zone["points"] → crop_zone_snapshot (선택)
#        └─ snapshot/crop 배열 → make_event_thumbnail → 목록/보고서 preview
# event["event_id"]와 event["zone_name"]을 저장 인자로 전달할 수 있다.
# backend.zones는 packet["frame"] 좌표계이므로 원본 crop에는 좌표 변환이 필요하다.
# recorder.record_frame의 동영상 저장과 독립적으로 연결할 후보이며 교체하지 않는다.
# 현재 기존 pipeline.py, recorder.py 및 다른 기존 파일을 수정하지 않는다.
