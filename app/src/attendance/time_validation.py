from abc import ABC, abstractmethod
from datetime import datetime


class TimeValidationStrategy(ABC):
    @abstractmethod
    def is_valid(self, current_time: datetime, work_start_time: datetime) -> bool:
        pass


class TimeValidationStrategyDefault(TimeValidationStrategy):
    def is_valid(self, current_time: datetime, work_start_time: datetime) -> bool:
        time_difference = (current_time - work_start_time).total_seconds() / 60
        return 0 <= time_difference <= 30
