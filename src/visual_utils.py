"""화면 정보 표시용 작업 골격. 현재 pipeline에서 사용하지 않는다.

모든 반환값·검증·처리 설명은 향후 구현 계약이며, 현재는 호출 즉시
NotImplementedError를 발생시킨다. OpenCV 호출과 입력 검증도 구현하지 않는다.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np


def draw_zone_label(
    frame: np.ndarray,
    polygon: Sequence[Sequence[int]] | np.ndarray,
    zone_name: str,
) -> np.ndarray:
    """위험구역 주변에 이름을 표시하여 여러 구역을 구분하기 위한 함수.

    입력: frame은 비어 있지 않은 (H, W, 3) uint8 BGR 배열이다.
    polygon은 같은 프레임 좌표계의 (N, 2) 정수 꼭짓점 목록/배열(N >= 3),
    zone_name은 비어 있지 않은 구역 이름이다. 기존 zone의 points/name을 받는다.
    반환: 이름이 그려진 별도 BGR 배열. 입력과 크기·dtype이 같아야 한다.

    향후 구현: cv2.putText로 다각형 위쪽 또는 안쪽의 읽기 쉬운 위치에
    구역명을 표시한다. cv2.getTextSize로 글자 영역을 확인할 수 있다.
    연동: pipeline._draw의 구역 표시 단계에서 표시용 프레임을 전달한다.
    주의: 화면 가장자리·작은 프레임·긴 이름의 배치를 정하고, OpenCV 기본
    글꼴의 한글 미지원은 명시적인 표시 정책으로 처리한다. 프레임 확대 금지.
    잘못된 프레임/다각형/빈 이름은 향후 ValueError로 거부한다.
    입력 배열과 polygon을 수정하지 않으며 기존 구역 좌표, 침입 판정,
    config, 녹화 원본과 기존 _draw의 표시 동작은 이번 단계에서 건드리지 않는다.
    """
    # TODO: 입력 형식과 좌표계를 검증하고 표시용 복사본을 준비한다.
    # TODO: 다각형 주변에서 글자가 화면 밖으로 잘리지 않는 기준점을 정한다.
    # TODO: cv2.putText로 이름을 그린 뒤 같은 크기의 복사본을 반환한다.
    raise NotImplementedError("추가 담당자가 구현해야 하는 기능입니다.")


def draw_timestamp(frame: np.ndarray, current_time: float) -> np.ndarray:
    """영상 경과 시간을 표시하여 사건 발생 시점을 쉽게 확인하기 위한 함수.

    입력: frame은 비어 있지 않은 (H, W, 3) uint8 BGR 배열,
    current_time은 0 이상의 유한한 영상 경과 초이다. 벽시계 시각이 아니다.
    반환: 시간 문자열이 표시된 별도 배열로 입력의 크기·dtype을 유지한다.

    향후 구현: 소수 초를 버린 뒤 1시간 미만은 MM:SS, 이상은 HH:MM:SS로
    표시한다. 시는 24시간을 넘어도 누적하며 각 필드는 최소 두 자리로 한다.
    cv2.putText를 사용하고 필요하면 cv2.getTextSize로 표시 영역을 계산한다.
    연동: pipeline.run_pipeline의 packet["media_time_s"]를 표시 단계에서
    전달한다. 현재 _draw 인자에는 시각이 없으므로 향후 전달 경로가 필요하다.
    주의: 음수/NaN/무한대 시각과 잘못된 프레임은 향후 ValueError로 거부한다.
    배너·FPS 표시와 겹치지 않도록 배치하고 작은 영상에서도 크기를 바꾸지 않는다.
    기존 timestamp_mode, packet 시각, benchmark 계측, recorder 시각은 변경하지
    않는다. 원본 frame을 직접 수정하거나 이 함수에서 시간을 새로 측정하지 않는다.
    """
    # TODO: 프레임과 초 단위 시각의 유효성을 검증하고 복사본을 준비한다.
    # TODO: 경과 초를 위 형식의 문자열로 변환하고 다른 표시와 겹치지 않게 배치한다.
    # TODO: cv2.putText로 표시한 복사본을 반환한다.
    raise NotImplementedError("추가 담당자가 구현해야 하는 기능입니다.")


def draw_event_banner(frame: np.ndarray, message: str = "WARNING") -> np.ndarray:
    """침입 경보를 눈에 띄게 전달하는 화면 상단 배너를 그리기 위한 함수.

    입력: frame은 비어 있지 않은 (H, W, 3) uint8 BGR 배열이며,
    message는 비어 있지 않은 경고 문자열이다. 기본값은 WARNING이다.
    반환: 원본 크기·dtype을 유지하는 배너 표시 복사본이다.

    향후 구현: cv2.rectangle로 상단 배경을 채우고 cv2.putText로 대비되는
    색의 문구를 표시한다. 배너 높이는 프레임 내부에 들어가도록 제한한다.
    연동: pipeline._draw의 states 값 중 status == "ALERT"가 있을 때
    호출자가 호출한다. 이 함수 자체는 상태 판단이나 이벤트 생성을 하지 않는다.
    주의: 기존 _draw에도 경고 표시가 있으므로 향후 통합 시 중복 표시와
    timestamp/FPS 겹침을 조정한다. 긴 문구·한글 글꼴 제약을 명시적으로 처리한다.
    잘못된 프레임/빈 문구는 향후 ValueError로 거부한다. 입력 배열은 보존한다.
    state.update_state의 전이, ALERT 조건, 녹화 시작 조건, 기존 config와
    pipeline 코드는 이번 작업에서 변경하지 않는다.
    """
    # TODO: 입력을 검증하고 원본과 독립된 표시용 복사본을 만든다.
    # TODO: cv2.rectangle로 화면 내부 상단 배너 배경을 그린다.
    # TODO: cv2.putText로 문구를 배치하고 크기가 같은 복사본을 반환한다.
    raise NotImplementedError("추가 담당자가 구현해야 하는 기능입니다.")


# ==========================================================
# 기존 시스템 연동 위치
# ==========================================================
# 이 모듈은 현재 기존 pipeline에 연결되어 있지 않다.
# 향후 구현 완료 후 pipeline.run_pipeline의 표시 단계 / pipeline._draw가 후보다.
#   ├─ zone["points"], zone["name"] → draw_zone_label
#   ├─ packet["media_time_s"] → draw_timestamp (향후 시각 전달 경로 필요)
#   └─ states의 status == "ALERT" → draw_event_banner
# _draw는 현재 복사본에 구역명과 경고도 표시하므로 향후 중복 표시를 조정한다.
# 표시용 좌표는 packet["frame"] 기준이며 original_frame과 크기가 다를 수 있다.
# 현재 기존 pipeline.py 및 다른 기존 파일을 수정하지 않는다.
