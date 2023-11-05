normal_example = {
    "summary": "기본 회원가입 예제",
    "description": "기본 회원가입",
}

request_member_create_examples = {
    "member_id": "john_doe",
    "email_address": "john.doe@example.com",
    "employ_ymd": "2023-10-22",
    "cellphone_no": {
        "number": "010-1234-5678"
    },
    "office_phone_no": {
        "number": "02-345-6789"
    },
    "birth_ymd": "1990-01-15",
    "gender_cd": "M",
    "emp_nick": "John",
    "locale_type_cd": "en_US",
    "tmzn_type_cd": "PST",
    "address": {
        "zipcode": "12345",
        "addr": "123 Main Street",
        "addr_dtl": "Apt 456",
    },
    "name": "John Doe",
    "i18n_names": {
        "additionalProp1": "Name in French",
        "additionalProp2": "Name in Spanish",
        "additionalProp3": "Name in German"
    },
    "dept_external_key": "hr_department",
    "concurrent_dept_external_keys": ["it_department", "sales_department"],
    "emp_type_external_key": "full_time",
    "grade_cd_external_key": "senior",
    "job_cd_external_key": "developer",
    "password_setting_type": "complex",
    "initialize_password": "true"
},

request_member_update_examples = {
    "member_id": "john_doe",
    "email_address": "john.doe@example.com",
    "employ_ymd": "2023-10-22",
    "cellphone_no": {
        "number": "010-0000-0000"
    },
    "office_phone_no": {
        "number": "02-000-0000"
    },
    "birth_ymd": "1995-01-15",
    "gender_cd": "M",
    "emp_nick": "John",
    "locale_type_cd": "en_US",
    "tmzn_type_cd": "PST",
    "address": {
        "zipcode": "12345",
        "addr": "123 Main Street",
        "addr_dtl": "Apt 456",
    },
    "name": "John Doe",
    "i18n_names": {
        "additionalProp1": "Name in French",
        "additionalProp2": "Name in Spanish",
        "additionalProp3": "Name in German"
    },
    "dept_external_key": "hr_department",
    "concurrent_dept_external_keys": ["it_department", "sales_department"],
    "emp_type_external_key": "full_time",
    "grade_cd_external_key": "senior",
    "job_cd_external_key": "developer",
    "password_setting_type": "complex",
    "initialize_password": "true"
},
