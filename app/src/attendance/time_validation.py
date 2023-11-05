from abc import ABC, abstractmethod
from datetime import datetime


class TimeValidationStrategy(ABC):
    @abstractmethod
    def is_valid(self, current_time: datetime, target_time: datetime) -> bool:
        pass


class CheckInTimeValidationStrategyDefault(TimeValidationStrategy):
    def is_valid(self, current_time: datetime, check_in_time: datetime) -> bool:
        time_difference = (current_time - check_in_time).total_seconds() / 60
        return 0 <= time_difference <= 30


class CheckOutTimeValidationStrategyDefault(TimeValidationStrategy):
    def is_valid(self, current_time: datetime, check_out_time: datetime) -> bool:
        time_difference = (check_out_time - current_time ).total_seconds() / 60
        return 0 <= time_difference
