# _*_ coding:utf-8 _*_
import re
import datetime
import random

from faker import Faker

str = '【医院人资平台】验证码：054191。5分钟内有效。'

print(re.findall(r"\d+", str)[0])

faker = Faker(locale='zh_CN')

id = faker.ssn(min_age=18, max_age=60)
print((id))

print(faker.word(ext_word_list=None))

print("招聘计划名称_" + faker.text(max_nb_chars=10))

ls = ['1', '2', '3', '4']
print(random.randint(1, 10))

da = {
    "n": {
        "template_id": "1221",
        "template_type": "771",
        "worker_info": {
            "72": {
                "user_complete_cultivate_time": -1,
                "user_is_overseas_experience": "1",
                "user_computer_level": "81",
                "user_is_cultivate": "0",
                "user_language_level": "84",
                "is_write_position_desc": "1",
                "7f851954861348b8b692e8a2b1828501": "否",
                "user_file_number": "HHH0909",
                "user_name": "姓名11",
                "user_cert_type": "15",
                "user_cert_number": "330011199506041122",
                "user_sex": "280",
                "user_birth_time": "1995-06-04",
                "user_birth_month": "06-04",
                "user_age": 26,
                "user_national": "357",
                "user_marital_status": "38",
                "user_health_status": "716",
                "user_politics_status": "41",
                "user_in_party_time": "2020-09-09",
                "user_other_politics_status": "580",
                "user_country": "510",
                "user_native_place": "籍贯",
                "user_birth_place": "出生地",
                "place_of_domicile": "户籍所在地",
                "user_household_type": "本地农村",
                "user_is_foreign": "1",
                "user_work_time": "2021-07-06",
                "user_practice_status": "1",
                "user_title": "487",
                "user_retire_time": "2023-09-15",
                "nurse_shoe_size": "33",
                "user_blood": "o",
                "management_unit": "档案管理单位",
                "user_interest_info": "兴趣爱好",
                "wubi_code": "五笔码",
                "pinyin_code": "拼音码",
                "user_self_assessment": "自我介绍",
                "user_work_time_two": "2021-01",
                "e4760fb20168473f854ea6af64d3aa10": "教师资格",
                "5a397f4f8738419ca072b8f68d0a0009": "2021-08-31T16:00:00.000Z",
                "3eb923fa7bea469596090fabccc57cfb": "职业资格证书编号",
                "f297dcc358b542f284b06c9fd1151764": "职业资格证书颁发单位",
                "user_weight": "44",
                "user_height": "170",
                "remark": "备注备注",
                "user_cert_expire_time": "2021-09-07",
                "user_before_name": "曾用名",
                "extra_info": {
                    "7f851954861348b8b692e8a2b1828501": "否",
                    "e4760fb20168473f854ea6af64d3aa10": "教师资格",
                    "5a397f4f8738419ca072b8f68d0a0009": "2021-08-31T16:00:00.000Z",
                    "3eb923fa7bea469596090fabccc57cfb": "职业资格证书编号",
                    "f297dcc358b542f284b06c9fd1151764": "职业资格证书颁发单位"
                },
                "user_avatar": "",
                "user_resume_type": "477"
            },
            "213": {
                "main_dept": ["10b4c0fc1c074f18b7aeaa59a39c2aa8"],  # 所在部门
                "supervisor": [],
                "work_number": "GH33333",  # 工号
                "hospital_position": "岗位",
                "party_government_position": "党政职务",
                "people_type": "430",
                "people_nature": "9",
                "biography_time": "2021-09-08",
                "biography_one": "在编",
                "biography_two": "厅聘",
                "people_limit": "1",
                "worker_employee_type": "正式员工",
                "worker_type": "药师类",
                "employee_use_type": "劳动合同关系",
                "worker_status": "499",
                "hospital_contract_signing_unit": "合同签署单位",
                "in_hospital_type": "554",
                "in_hospital_time": "2021-09-06",
                "work_address": "办公地点",
                "in_hospital_remark": "备注1",
                "hospital_district": "院区",
                "hospital_people_type": "护士",
                "hospital_plan_department": "原计划科室",
                "extra_info": {}
            },
            "314": {
                "diploma_full_time_master_phd": "全日制硕博期",
                "extra_info": {}
            },
            "498": {
                "communication_phone": "18866600011",
                "communication_other_phone_one": "18866600011",
                "communication_other_phone_two": "18866600011",
                "communication_worker_phone": "0571123456",
                "communication_email": "123@11.com",
                "communication_postal_code": "330011",
                "communication_domicile_place": "户籍所在地",
                "communication_domicile_address": "户籍地址",
                "communication_now_address": "现居地址",
                "communication_address": "通讯地址",
                "extra_info": {}
            },
            "549": [{
                "family_people_name": "姓名+",
                "family_people_relation": "588",
                "family_people_sex": "32",
                "family_people_politics_status": "538",
                "family_people_is_emergency": "1",
                "family_people_phone": "15000001111",
                "family_people_id_card": "336611196603021254",
                "family_people_birth_time": "1966-03-02",
                "family_people_address": "联系地址+",
                "family_people_work_address": "工作单位+",
                "family_people_job": "职位/职务+",
                "family_people_position": "岗位+",
                "family_people_department": "部门+",
                "family_people_education_status": "502",
                "family_remark": "备注+",
                "family_people_relation_remark": "其他",
                "family_people_sex_remark": "男",
                "family_people_politics_status_remark": "民盟盟员",
                "family_people_education_status_remark": "高专",
                "family_people_is_emergency_remark": "是",
                "extra_info": {}
            }],
            "1397": {
                "base_title_name": "职称名称",
                "base_title_level": "424",
                "base_title_way_obtain": "考试",
                "base_title_way_date": "2021-09-01",
                "base_title_rating_agency": "评定机构",
                "base_title_certificate_number": "ZS11111",
                "base_title_professional_title": "职称专业",
                "base_title_jury_name": "评委会名称",
                "base_title_remark": "备注2",
                "extra_info": {}
            },
            "1528": {
                "base_new_job_title_part_time": "2021-02",
                "extra_info": {}
            },
            "1529": {
                "extra_info": {}
            }
        },
        "is_sync": "0"
    },
    "a": {
        "source": "1284"
    },
    "v": {
        "session_id": "2c8a70acc1094a53a648a8933d3beec7"
    }
}

AA={
	"n": {
		"template_id": "1221",
		"template_type": "771",
		"worker_info": {
			"72": {
				"extra_info": {
					"e4760fb20168473f854ea6af64d3aa10": "准入证",
					"5a397f4f8738419ca072b8f68d0a0009": "1993-10",
					"3eb923fa7bea469596090fabccc57cfb": "职业资格证书编号_进入朋友历史出来.",
					"f297dcc358b542f284b06c9fd1151764": "职业资格证书颁发单位_虽然各种资料谢谢."
				},
				"user_file_number": "20210914171658",
				"user_name": "姓名_查看而且科技无法.",
				"user_cert_type": "21",
				"user_cert_number": "330825196802015138",
				"remark": "备注_情况有限留言实现.",
				"e4760fb20168473f854ea6af64d3aa10": "准入证",
				"5a397f4f8738419ca072b8f68d0a0009": "1993-10",
				"3eb923fa7bea469596090fabccc57cfb": "职业资格证书编号_进入朋友历史出来.",
				"f297dcc358b542f284b06c9fd1151764": "职业资格证书颁发单位_虽然各种资料谢谢.",
				"user_complete_cultivate_time": -1,
				"is_attendance": "1",
				"is_middle": "0",
				"is_leader": "0",
				"is_clinical_staff": "0",
				"user_sex": "32",
				"user_birth_time": "1968-02-01",
				"user_birth_month": "02-01",
				"user_age": 53,
				"user_avatar": "",
				"user_resume_type": "477"
			},
			"213": {
				"extra_info": {},
				"work_number": "20210914171658",
				"main_dept": ["f81af5ab34984fa2af94ca71b846e99d"],
				"is_leader": "0",
				"is_middle": "1",
				"is_dept_head": "0",
				"is_clinical_staff": "0",
				"is_attendance": "1",
				"supervisor": [],

			},
			"498": {
				"extra_info": {},
				"communication_phone": "18042749186",
				"is_attendance": "1",
				"is_middle": "0",
				"is_leader": "0",
				"is_clinical_staff": "0",

			},
			"549": {
				"extra_info": {},
				"family_people_name": "姓名_他们",
				"family_people_relation": "494",
				"family_people_phone": "18042749186",
				"family_people_is_emergency": "0"
			}
		},
		"is_sync": "0"
	},
	"a": {
		"source": "1284"
	},
	"v": {
		"session_id": "923d97560a134a718cc086a4cfdfbd26"
	}
}
if ('number' in 'work_number') or ('phone' in 'communication_phone'):
    print('********')