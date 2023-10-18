from abc import ABC, abstractmethod

from app.models import Coordinate


class CoordinateValidationStrategy(ABC):
    @abstractmethod
    def is_within_error_range(self, current_coordinate: Coordinate, target_coordinate: Coordinate) -> bool:
        pass


class CoordinateValidationStrategyDefault(CoordinateValidationStrategy):
    def is_within_error_range(self, coord1, coord2, max_error=0.01):
        # 좌표 간의 거리 계산
        lat1, lon1 = coord1.latitude, coord1.longitude
        lat2, lon2 = coord2.latitude, coord2.longitude
        distance = ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5
        return distance <= max_error
