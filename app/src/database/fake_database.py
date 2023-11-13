from app.models import Coordinate


class FakeDatabase:
    def __init__(self):
        self.accounts = {
            "jude0124": {
                "check_in_time": "09:00:00",  # 예정 근무 시작 시간
                "check_out_time": "18:00:00",  # 예정 근무 종료 시간
                "updated_check_in_hour": "8",  # 수정할 출근 시각 정보 (시간)
                "updated_check_in_minute": "50",  # 수정할 출근 시각 정보 (분)
                "company_coordinates": Coordinate(latitude=37.4002437530466, longitude=127.11243694616036)  # 회사 좌표
            }
        }

        self.check_ins = {}  # 출근 기록 저장

    def get_account(self, account_id):
        return self.accounts.get(account_id)

    def save_check_in(self, account_id, check_in_time):
        self.check_ins[account_id] = check_in_time

    def save_check_out(self, account_id, check_out_time):
        self.check_ins[account_id] = check_out_time

    def get_check_in_time(self, account_id):
        return self.check_ins.get(account_id)


fake_db = FakeDatabase()
