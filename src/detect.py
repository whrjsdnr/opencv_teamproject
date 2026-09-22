"""A 브랜치 0c6476b의 실제 구현을 B·C 공통 경로에 통합한 모듈.
전처리→MOG2→원본 좌표 침입→상태 전이 순서로 호출하며 파일 기록은 B가 담당한다.
"""
from __future__ import annotations

from typing import Any
import numpy as np
import cv2


def create_background_subtractor(config: dict[str, Any]) -> Any:
    """[담당: 팀원 A]
    목적: 실행별 MOG2 인스턴스 생성
    매개변수 / 입력 타입: config: 검증 설정 dict
    반환 / 출력 타입: OpenCV BackgroundSubtractorMOG2
    데이터 처리 순서:
        1. history, var_threshold, detect_shadows 적용
        2. 각 실행 시작마다 새 인스턴스 생성
    예외 및 경계 조건: 유효하지 않은 설정은 ValueError
    모듈 연결: pipeline에서 1회 생성
    """
    # B의 중첩 설정을 우선하고 A의 독립 호출 설정도 유지한다.
    config = {**config, **config.get("mog2", {})}
    history = config.get("history", 500)
    var_threshold = config.get("var_threshold", 16)
    detect_shadows = config.get("detect_shadows", True)

    if not isinstance(history, int) or history <= 0:
        raise ValueError(f"history는 양의 정수여야 합니다: {history}")
    if not isinstance(var_threshold, (int, float)) or var_threshold <= 0:
        raise ValueError(f"var_threshold는 양수여야 합니다: {var_threshold}")

    subtractor = cv2.createBackgroundSubtractorMOG2(
        history=history,
        varThreshold=var_threshold,
        detectShadows=detect_shadows,
    )
    return subtractor


def detect_motion(frame: np.ndarray, background_subtractor: Any, min_area: float) -> list[tuple[int, int, int, int]]:
    """[담당: 팀원 A]
    목적: 움직이는 객체 영역 검출
    매개변수 / 입력 타입: frame: 분석 BGR uint8; background_subtractor: MOG2; min_area: 분석 픽셀 면적
    반환 / 출력 타입: 분석 좌표 (x,y,w,h) 목록
    데이터 처리 순서:
        1. MOG2 적용
        2. 그림자 127 처리하고 이진화 및 노이즈 제거
        3. 외곽선 추출 및 면적 필터
        4. 바운딩 박스 반환
    예외 및 경계 조건: 움직임 없으면 []; 최소 min_area의 scale_x*scale_y 값과 적용
    모듈 연결: pipeline에서 매 프레임, 좌표·상태 관리 이관
    """
    if frame is None or frame.size == 0:
        raise ValueError("빈 프레임입니다.")

    # 1. MOG2 적용
    fg_mask = background_subtractor.apply(frame)

    # 2. 그림자(값 127) 제거 및 이진화, 노이즈 제거
    _, binary = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.dilate(binary, kernel, iterations=2)

    # 3. 외곽선 추출 및 면적 필터
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        boxes.append((x, y, w, h))

    # 4. 바운딩 박스 반환
    return boxes


def check_intrusion(boxes: list[tuple[int, int, int, int]], zones: list[dict[str, Any]]) -> dict[str, bool]:
    """[담당: 팀원 A]
    목적: 박스 하단 중앙점이 구역에 침입했는지 판단
    매개변수 / 입력 타입: boxes: 원본 좌표; zones: name, points를 가진 목록
    반환 / 출력 타입: {구역 이름: 침입 bool} (모든 구역 포함)
    데이터 처리 순서:
        1. 박스 하단 중앙점 계산
        2. pointPolygonTest로 경계를 포함한 내부 판정
        3. 구역별 하나 이상이면 True
    예외 및 경계 조건: 박스가 없으면 False; 중복 구역명은 ValueError
    모듈 연결: pipeline → state; 공통 침입 판단 기준
    """
    if not zones:
        raise ValueError("zones가 비어있습니다.")

    result: dict[str, bool] = {}

    for zone in zones:
        zone_name = zone.get("id") or zone.get("name")
        if not zone_name:
            raise ValueError(f"구역 이름이 없습니다: {zone}")

        if zone_name in result:
            raise ValueError(f"중복 구역 이름입니다: {zone_name}")
        points = zone.get("points")
        if not points or len(points) < 3:
            raise ValueError(f"구역 {zone_name}의 다각형 점이 3개 미만입니다.")

        polygon = np.array(points, dtype=np.int32)
        intruded = False

        for (x, y, w, h) in boxes:
            # 1. 박스 하단 중앙점 계산
            cx = x + w / 2
            cy = y + h

            # 2. pointPolygonTest로 점 포함 내부 판정
            inside = cv2.pointPolygonTest(polygon, (float(cx), float(cy)), False)
            if inside >= 0:
                intruded = True
                break

        # 3. 구역별 하나 이상이면 True
        result[zone_name] = intruded

    return result


if __name__ == "__main__":
    print("detect.py 모듈이 정상적으로 로드됩니다.")
