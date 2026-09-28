"""밝기 및 움직임 통계용 작업 골격. 검출·상태 판단과 독립적이다.

아래 계약은 향후 구현 지침이다. 현재 입력 검증이나 계산은 하지 않으며,
세 함수 모두 호출 즉시 NotImplementedError를 발생시킨다.
"""

from __future__ import annotations

from typing import Literal

import numpy as np


def calculate_brightness(frame: np.ndarray) -> float:
    """평균 밝기를 구하여 어두운 환경 확인과 야간 실험 분석에 쓰기 위한 함수.

    입력: frame은 비어 있지 않은 (H, W, 3) uint8 BGR 배열이다.
    반환: 모든 픽셀의 grayscale 평균 밝기인 0.0~255.0 범위 Python float.
    향후 구현: cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)로 변환한 후
    cv2.mean의 첫 채널 평균을 사용한다. BGR 채널 평균을 직접 쓰지 않는다.
    연동: pipeline._analysis 진입 시 표시가 그려지지 않은 frame을 받는
    분석 보조 단계가 후보다. 입력 해상도 전체 기준인지 실험 기록에 명시한다.
    주의: 빈 배열, 다른 채널 수/dtype은 향후 ValueError로 거부한다.
    원본을 수정하거나 ROI 밝기와 전체 프레임 밝기를 혼동하지 않는다.
    기존 detection threshold, MOG2 설정, State Machine, benchmark 출력,
    config는 변경하지 않는다. 밝기 결과로 감지 설정을 자동 변경하지 않는다.
    """
    # TODO: BGR uint8 입력 형식과 비어 있지 않은 크기를 검증한다.
    # TODO: cv2.cvtColor로 grayscale 영상을 별도로 생성한다.
    # TODO: cv2.mean으로 평균을 구하고 float로 반환한다.
    raise NotImplementedError("추가 담당자가 구현해야 하는 기능입니다.")


def classify_brightness(
    brightness: float,
    dark_threshold: float = 60,
    bright_threshold: float = 180,
) -> Literal["DARK", "NORMAL", "BRIGHT"]:
    """평균 밝기를 세 등급으로 분류하여 환경별 결과 비교를 돕기 위한 함수.

    입력: brightness는 calculate_brightness의 0~255 유한한 수치이다.
    두 threshold 역시 유한한 수치이며 0 <= dark_threshold <
    bright_threshold <= 255를 만족해야 한다. 기본값 외 임계값도 인자로 받는다.
    반환: brightness < dark_threshold이면 DARK, brightness >
    bright_threshold이면 BRIGHT, 두 경계값을 포함한 나머지는 NORMAL 문자열.
    향후 구현: 수치 비교만 필요하므로 직접 사용할 OpenCV 함수는 없다.
    앞 단계의 cv2.cvtColor/cv2.mean 결과를 받아 처리한다.
    연동: pipeline의 밝기 측정 직후 호출하는 보조 분석 단계가 후보이며,
    향후 호출자가 config 값을 전달할 수 있다. 여기서 config를 읽지 않는다.
    주의: 범위 밖 수치·NaN·무한대·역전/동일 임계값은 향후 ValueError로
    거부하고 경계값을 일관되게 처리한다. bool은 밝기 수치로 받지 않는다.
    기존 config 기본값, 검출 민감도, state.update_state 및 사건 발생 조건은
    변경하지 않는다. 분류는 실험용 정보이며 자동 야간 모드 전환이 아니다.
    """
    # TODO: 밝기 범위와 임계값의 순서·유한성을 검증한다.
    # TODO: 위에 명시한 경계 포함 규칙대로 세 문자열 중 하나를 반환한다.
    # TODO: OpenCV 호출이나 상태 변경 없이 전달된 수치만으로 분류한다.
    raise NotImplementedError("추가 담당자가 구현해야 하는 기능입니다.")


def calculate_motion_ratio(foreground_mask: np.ndarray) -> float:
    """전체 분석 영역에서 움직임 픽셀 비율을 구해 활동량을 비교하기 위한 함수.

    입력: foreground_mask는 기존 MOG2에서 얻은 비어 있지 않은 (H, W)
    단일 채널 uint8 마스크다. 0은 배경, 127은 그림자, 255는 전경이다.
    0/255 이진 마스크도 허용한다. 그 외 값은 향후 ValueError로 거부한다.
    반환: 전경(255) 픽셀 수 / 전체 H*W 픽셀 수인 0.0~1.0 Python float.
    향후 구현: 그림자를 제외한 별도 이진 마스크에 cv2.countNonZero를
    적용한다. 원본 MOG2 마스크의 모든 비영 픽셀을 움직임으로 세지 않는다.
    연동: detect.detect_motion의 fg_mask 또는 binary를 향후 전달받는다.
    현재 detect_motion은 박스만 반환하므로 pipeline._analysis에서 마스크를
    바로 얻을 수 없다. 전달 인터페이스 확장은 별도 통합 단계에서 결정한다.
    주의: 빈 마스크의 0 나눗셈과 다채널 입력을 검증한다. ROI/축소 마스크라면
    분모도 해당 분석 영역이며 원본 전체 영상의 비율로 해석하지 않는다.
    기존 마스크를 수정하거나 MOG2 객체를 새로 만들거나 apply를 재호출하지 않는다.
    기존 detect.py 반환 계약, morphology, threshold, State Machine과 config는
    이번 단계에서 변경하지 않는다. 비율로 침입 여부를 재판정하지 않는다.
    """
    # TODO: 단일 채널 uint8 크기 및 허용 픽셀값을 검증한다.
    # TODO: 원본을 보존하면서 255 전경만 선택한 이진 마스크를 준비한다.
    # TODO: cv2.countNonZero 결과를 전체 픽셀 수로 나누어 float로 반환한다.
    raise NotImplementedError("추가 담당자가 구현해야 하는 기능입니다.")


# ==========================================================
# 기존 시스템 연동 위치
# ==========================================================
# 이 모듈은 현재 기존 pipeline에 연결되어 있지 않다.
# 향후 구현 완료 후 다음 실제 코드 위치에서의 호출을 검토한다.
# pipeline._analysis
#   ├─ 입력 frame → calculate_brightness → classify_brightness
#   ├─ preprocess.preprocess_frame
#   ├─ detect.detect_motion 내부 fg_mask / binary → calculate_motion_ratio
#   │    현재 마스크는 외부에 반환되지 않으므로 향후 전달 경로 설계가 필요하다.
#   └─ detect.check_intrusion → RealBackend.update → state.update_state
# 통계는 보조 정보이며 기존 구역·상태 판단에 자동으로 반영하지 않는다.
# 현재 기존 pipeline.py, detect.py 및 다른 기존 파일을 수정하지 않는다.
