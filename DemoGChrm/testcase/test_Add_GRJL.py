import unittest
import configparser
import json
import random
from faker import Faker
from DemoGChrm.config import setting
from DemoGChrm.lib.getJsonPath import getJson
from DemoGChrm.lib.log import Log
from DemoGChrm.lib.sendRequests import send_requests
from DemoGChrm.lib.login import login_work_base
from DemoGChrm.lib.get_userCert import getCert
from DemoGChrm.lib.getTime import *

log = Log().getLog()
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='utf-8')
'''
个人简历填写
'''


class MyTestCase(unittest.TestCase):

    def __init__(self, testName, login_PATH, login_phone):
        super(MyTestCase, self).__init__(testName)
        self.faker = Faker(locale='zh_CN')
        self.hrmapi = cf.get(login_PATH, "hrmapi")
        self.gcgateway = cf.get(login_PATH, "gcgateway")
        self.corp_id = cf.get(login_PATH, "corp_id")
        self.login_phone = login_phone
        self.login_work_data = login_work_base(path=login_PATH, phone=self.login_phone)
        self.session_id = {"session_id": getJson(self.login_work_data, 'session_id')[0]}

    def test_run(self):
        template_id = getJson(self.login_work_data, 'personal_template_id')[0]
        _comboBox_data = {
            'CERT_TYPE': {"a": {"source": "757"}, "n": {"group_id": "CERT_TYPE"}, "v": self.session_id},  # 证件类型
            'SEX': {"a": {"source": "757"}, "n": {"group_id": "SEX"}, "v": self.session_id},  # 性别
            'NATIONAL_TYPE': {"a": {"source": "757"}, "n": {"group_id": "NATIONAL_TYPE"}, "v": self.session_id},  # 民族
            'MARITAL_STATUS': {"a": {"source": "757"}, "n": {"group_id": "MARITAL_STATUS"}, "v": self.session_id},  # 婚姻状况
            'HEALTH_STATUS': {"a": {"source": "757"}, "n": {"group_id": "HEALTH_STATUS"}, "v": self.session_id},  # 健康状况
            'POLITICS_STATUS': {"a": {"source": "757"}, "n": {"group_id": "POLITICS_STATUS"}, "v": self.session_id},  # 政治面貌
            'COUNTRY_TYPE': {"a": {"source": "757"}, "n": {"group_id": "COUNTRY_TYPE"}, "v": self.session_id},  # 国家或地区
            'RIGHT_TYPE': {"a": {"source": "757"}, "n": {"group_id": "RIGHT_TYPE"}, "v": self.session_id},  # 是否选择
            'TITLE_TYPE': {"a": {"source": "757"}, "n": {"group_id": "TITLE_TYPE"}, "v": self.session_id},  # 取得职称
            'LANGUAGE_LEVEL': {"a": {"source": "757"}, "n": {"group_id": "LANGUAGE_LEVEL"}, "v": self.session_id},  # 外语等级
            'COMPUTER_LEVEL': {"a": {"source": "757"}, "n": {"group_id": "COMPUTER_LEVEL"}, "v": self.session_id},  # 计算机等级
            'EDUCATION_STATUS': {"a": {"source": "757"}, "n": {"group_id": "EDUCATION_STATUS"}, "v": self.session_id},  # 初始学历
            'DEGREE_TYPE': {"a": {"source": "757"}, "n": {"group_id": "DEGREE_TYPE"}, "v": self.session_id},  # 最高学位
            'SCHOOL_TYPE': {"a": {"source": "1284"}, "n": {"group_id": "SCHOOL_TYPE"}, "v": self.session_id},  # 院校形式
            'STUDY_TYPE': {"a": {"source": "757"}, "n": {"group_id": "STUDY_TYPE"}, "v": self.session_id},  # 学习形式
            'SCHOOL_SYSTEM_TYPE': {"a": {"source": "757"}, "n": {"group_id": "SCHOOL_SYSTEM_TYPE"}, "v": self.session_id},  # 学制
            'CERTIFICATE_TYPE': {"a": {"source": "757"}, "n": {"group_id": "CERTIFICATE_TYPE"}, "v": self.session_id},  # 证书类型
            'LANGUAGE_TYPE': {"a": {"source": "757"}, "n": {"group_id": "LANGUAGE_TYPE"}, "v": self.session_id}  # 语种
        }

        log.info("""获取签名""")
        get_sign_url = self.hrmapi + "/hrm/user/oss/get_sign"
        get_sign_data = {"a": {"source": "757"}, "n": {"dir": "sourcedata/file/" + self.corp_id}, "v": self.session_id}
        response_get_sign = send_requests(method='post', url=get_sign_url, data=json.dumps(get_sign_data))
        self.assertEqual(getJson(response_get_sign, 'message')[0], '查询成功', '返回签名结果失败')

        log.info("""上传一寸照""")
        oss_url = "https://gchrmdata.oss-accelerate.aliyuncs.com/"
        t = getTime().get_Time()
        # oss_data = {'OSSAccessKeyId': (None, response_get_sign['n']['access_id']),
        #             'policy': (None, response_get_sign['n']['encoded_policy']),
        #             'signature': (None, response_get_sign['n']['post_signature']),
        #             'key': (None, 'sourcedata/file/{0}/{1}/unittest.png'.format(self.corp_id, t)),
        #             'success_action_status': (None, 200),
        #             'file': (None, 'binary')
        #             }
        # fils = {'file': ('unittest.png', open(r'C:\Users\goocan\Desktop\share\unittest.png', 'rb'), 'image/png')}
        # oss_data = MultipartEncoder({'OSSAccessKeyId': response_get_sign['n']['access_id'],
        #                              'policy': response_get_sign['n']['encoded_policy'],
        #                              'signature': response_get_sign['n']['post_signature'],
        #                              'key': 'sourcedata/file/{0}/{1}/unittest.png'.format(self.corp_id, t),
        #                              'success_action_status': '200',
        #                              'file': 'binary'
        #                              })
        #
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        #     "Content-Type": oss_data.content_type
        # }
        #
        # response_oss = requests.post(url=oss_url, data=oss_data, verify=False, headers=headers)
        # file_upload_url = self.gcgateway + '/unify_public/file/upload'
        # file_upload_data = {
        #     "n": {
        #         "file_array": [{
        #             "status": "success",
        #             "name": "unittest.png",
        #             "size": 180969,
        #             "percentage": 100,
        #             "uid": t,
        #             "raw": {
        #                 "uid": t
        #             },
        #             "response": "",
        #             "file_url": "sourcedata/file/{0}/{1}/unittest.png".format(self.corp_id, t),
        #             "file_name": "unittest.png",
        #             "file_uuid": t
        #         }],
        #         "is_generate_preview_url": 1
        #     },
        #     "a": {
        #         "source": "757"
        #     },
        #     "v": self.session_id
        # }
        # response_file_upload = send_requests(method='post', url=file_upload_url, data=json.dumps(file_upload_data))
        user_avatar = '6a02a4b3d5dc40509643bf27295cf56f'  # getJson(response_file_upload, 'file_group_id')

        log.info("""基本信息填写""")
        _cert_number = self.faker.ssn(min_age=30, max_age=60)
        _cert = getCert(_cert_number)
        add_base_info_data = {
            "a": {
                "source": "757"
            },
            "n": {
                "extra_info": {},
                "user_avatar": user_avatar,  # 头像
                "remark": "备注_" + self.faker.sentence(nb_words=15),  # 备注
                "user_age": _cert[3],  # 年龄
                "user_birth_month": _cert[0],  # 出生月日
                "user_birth_time": _cert[1],  # 出生年月日
                "user_cert_expire_time": "",  #
                "user_cert_number": _cert_number,  # 完成规培日期
                "user_cert_type": self._get_comboBox(data=_comboBox_data['CERT_TYPE'], value='value')[0],  # 证据类型
                "user_complete_cultivate_time": getTime().get_last_Years(_cert[1], 20),  # 完成规培日期
                "user_computer_level": self._get_comboBox(data=_comboBox_data['COMPUTER_LEVEL'], value='value')[0],  # 计算机等级
                "user_country": self._get_comboBox(data=_comboBox_data['COUNTRY_TYPE'], value='value')[0],  # 国家或地区
                "user_health_status": self._get_comboBox(data=_comboBox_data['HEALTH_STATUS'], value='value')[0],  # 健康状况
                "user_height": random.randint(150, 200),  # 身高
                "user_in_party_time": "",
                "user_interest_info": "兴趣爱好_" + self.faker.sentence(nb_words=5),  # 兴趣爱好
                "user_is_cultivate": self._get_comboBox(data=_comboBox_data['RIGHT_TYPE'], value='value')[0],  # 是否完成规培
                "user_is_foreign": "",
                "user_is_overseas_experience": self._get_comboBox(data=_comboBox_data['RIGHT_TYPE'], value='value')[1],  # 是否有海外经历
                "user_language_level": self._get_comboBox(data=_comboBox_data['LANGUAGE_LEVEL'], value='value')[0],  # 外语等级
                "user_marital_status": self._get_comboBox(data=_comboBox_data['MARITAL_STATUS'], value='value')[0],  # 婚姻状况
                "user_name": "姓名_" + self.faker.name(),
                "user_national": self._get_comboBox(data=_comboBox_data['NATIONAL_TYPE'], value='value')[0],  # 民族
                "user_native_place": "籍贯_" + self.faker.city(),  # 籍贯
                "user_other_politics_status": "",
                "user_politics_status": self._get_comboBox(data=_comboBox_data['POLITICS_STATUS'], value='value')[0],  # 政治面貌
                "user_practice_status": self._get_comboBox(data=_comboBox_data['RIGHT_TYPE'], value='value')[1],  # 是否有执业资格
                "user_retire_time": "",
                "user_self_assessment": "自我评价_" + self.faker.sentence(nb_words=50),  # 自我评价
                "user_sex": _cert[2],
                "user_title": self._get_comboBox(data=_comboBox_data['TITLE_TYPE'], value='value')[1],  # 取得职称
                "user_weight": random.randint(50, 100),  # 体重
                "user_work_time": getTime().get_last_Years(_cert[1], 20),  # 参加工作时间
                "work_base_diploma_detail": {  # 学历概况
                    "extra_info": {},
                    "diploma_end": self._get_comboBox(data=_comboBox_data['EDUCATION_STATUS'], value='value')[1],  # 最高学历
                    "diploma_go_school_time": getTime().get_last_Years(_cert[1], 15),  # 入学时间
                    "diploma_graduate_school": "毕业院校_" + self.faker.sentence(nb_words=10),  # 毕业院校
                    "diploma_highest_supervisor_name": "最高学历导师姓名_" + self.faker.name(),  # 最高学历导师姓名
                    "diploma_graduation_time": getTime().get_last_Years(_cert[1], 19),  # 毕业时间
                    "diploma_highest_degree": self._get_comboBox(data=_comboBox_data['DEGREE_TYPE'], value='value')[1],  # 最高学位
                    "diploma_is_fresh": self._get_comboBox(data=_comboBox_data['RIGHT_TYPE'], value='value')[0],  # 是否应届
                    "diploma_is_full": self._get_comboBox(data=_comboBox_data['RIGHT_TYPE'], value='value')[1],  # 是否全日制
                    "diploma_major": "专业_" + self.faker.sentence(nb_words=10),  # 专业
                    "diploma_start": self._get_comboBox(data=_comboBox_data['EDUCATION_STATUS'], value='value')[1]  # 初始学历
                },
                "work_now_work_detail": {  # 现工作信息
                    "extra_info": {},
                    "work_company": "现工作单位_" + self.faker.company(),  # 现工作单位
                    "work_job": "职务_" + self.faker.job(),  # 职务
                    "work_time": getTime().get_last_Years(_cert[1], 25) + "-03",
                    "work_title": "职称_" + self.faker.sentence(nb_words=5)  # 职称
                },
                "work_communication_detail": {
                    "extra_info": {},
                    "communication_domicile_address": "户籍住址_" + self.faker.address(),  # 户籍住址
                    "communication_domicile_place": "户籍所在地_" + self.faker.street_address(),  # 户籍所在地
                    "communication_email": str(self.login_phone) + "@qq.com",  # 邮箱
                    "communication_now_address": "现居地址_" + self.faker.street_name() + self.faker.building_number(),  # 现居地址
                    "communication_other_phone_one": self.login_phone,
                    "communication_other_phone_two": self.login_phone,
                    "communication_phone": self.login_phone,  # 手机号
                    "communication_postal_code": self.faker.postcode()  # 邮政编码
                },
                "user_resume_type": "31",  # 简历类型,个人简历
                "check_module_id": ["72", "314", "425", "498"],  # 个人信息\基本信息\现工作信息\通讯信息
                "template_id": template_id,
            },
            "v": self.session_id,
            "f": {
                "indexpage": "1",
                "repaging": "1",
                "pagesize": "10"
            }
        }
        response_is_have = self.is_have(template_id)
        if getJson(response_is_have, 'is_have_base')[0] == 1:
            add_base_info_url = self.hrmapi + '/hrm/work_user/update_base_info'
            worker_user_id = getJson(response_is_have, 'worker_user_id')[0]
            add_base_info_data['n']['worker_user_id'] = worker_user_id

        else:
            add_base_info_url = self.hrmapi + '/hrm/work_user/add_base_info'
        response_add_base_info = send_requests(method='post', url=add_base_info_url, data=json.dumps(add_base_info_data))
        self.is_true(response_add_base_info, "基本信息填写")
        worker_user_id = getJson(self.is_have(template_id), 'worker_user_id')[0]
        if worker_user_id:
            log.info("""教育经历填写""")
            add_education_url = self.hrmapi + '/hrm/work_user/add_education_info'
            add_education_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "extra_info": {},
                    "education_graduate_school": "毕业院校_" + self.faker.sentence(nb_words=5),  # 毕业院校
                    "education_go_school_time": getTime().get_last_Years(_cert[1], 10),  # 入学时间
                    "education_graduation_time": getTime().get_last_Years(_cert[1], 15),  # 毕业日期
                    "education_graduate_school_type": self._get_comboBox(data=_comboBox_data['SCHOOL_TYPE'], value='value')[0],  # 院校形式
                    "education_major": "专业_" + self.faker.job(),  # 专业
                    "education_study_type": self._get_comboBox(data=_comboBox_data['STUDY_TYPE'], value='value')[0],  # 学习形式
                    "education_school_system_type": self._get_comboBox(data=_comboBox_data['SCHOOL_SYSTEM_TYPE'], value='value')[0],  # 学制
                    "education_diploma": self._get_comboBox(data=_comboBox_data['EDUCATION_STATUS'], value='value')[0],  # 学历
                    "education_degree": self._get_comboBox(data=_comboBox_data['DEGREE_TYPE'], value='value')[0],  # 学位
                    "education_desc": "教育经历描述_" + self.faker.sentence(nb_words=15),  # 教育经历描述
                    "user_resume_type": "31",
                    "template_id": template_id,
                    "worker_user_id": worker_user_id,
                    "check_module_id": "591"  # 教育经历
                },
                "v": self.session_id,
                "f": {
                    "indexpage": "1",
                    "repaging": "1",
                    "pagesize": "10"
                }
            }
            response_add_education = send_requests(method='post', url=add_education_url, data=json.dumps(add_education_data))
            self.is_true(response_add_education, "教育经历填写")

            log.info("""培训/实习经历填写""")
            add_training_intern_url = self.hrmapi + '/hrm/work_user/add_training_intern_info'
            add_training_intern_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "extra_info": {},
                    "training_intern_organ": "实习经历_" + self.faker.job(),
                    "training_intern_start_time": getTime().get_last_Years(_cert[1], 15) + "-04",  #
                    "training_intern_end_time": getTime().get_last_Years(_cert[1], 20) + "-01",
                    "training_intern_position": "岗位_" + self.faker.job(),
                    "training_intern_job": "职务_" + self.faker.job(),
                    "training_intern_desc": "教育经历描述_" + self.faker.sentence(nb_words=15),
                    "user_resume_type": "31",
                    "template_id": template_id,
                    "worker_user_id": worker_user_id,
                    "check_module_id": "623"
                },
                "v": self.session_id,
                "f": {
                    "indexpage": "1",
                    "repaging": "1",
                    "pagesize": "10"
                }
            }
            response_add_training_intern = send_requests(method='post', url=add_training_intern_url, data=json.dumps(add_training_intern_data))
            self.is_true(response_add_training_intern, "培训/实习经历填写")

            log.info("""工作经历填写""")
            add_experience_work_url = self.hrmapi + '/hrm/work_user/add_experience_work_info'
            add_experience_work_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "extra_info": {},
                    "work_experience_company": "工作单位_" + self.faker.company(),
                    "work_experience_start_time": getTime().get_last_Years(_cert[1], 20),
                    "work_experience_end_time": getTime().get_last_Years(_cert[1], 22),
                    "work_experience_department": "部门_" + self.faker.company_prefix(),
                    "work_experience_position": "岗位_" + self.faker.job(),
                    "work_experience_title": "职称_" + self.faker.job(),
                    "work_experience_desc": "工作描述_" + self.faker.sentence(nb_words=15),
                    "user_resume_type": "31",
                    "template_id": template_id,
                    "worker_user_id": worker_user_id,
                    "check_module_id": "653"
                },
                "v": self.session_id,
                "f": {
                    "indexpage": "1",
                    "repaging": "1",
                    "pagesize": "10"
                }
            }
            response_add_experience_work = send_requests(method='post', url=add_experience_work_url, data=json.dumps(add_experience_work_data))
            self.is_true(response_add_experience_work, "工作经历填写")

            log.info("""证书填写""")
            add_certificate_url = self.hrmapi + "/hrm/work_user/add_certificate_info"
            add_certificate_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "extra_info": {},
                    "certificate_name": "证书名称_" + self.faker.sentence(nb_words=5),
                    "certificate_type": self._get_comboBox(data=_comboBox_data['CERTIFICATE_TYPE'], value='value')[0],  # 证书类型
                    "certificate_number": "证书编号_" + str(t),
                    "certificate_get_time": getTime().get_last_Years(_cert[1], 20) + "-03",
                    "certificate_organ": "发证机构_" + self.faker.company_prefix(),
                    "certificate_effective_start_time": getTime().get_last_Years(_cert[1], 18) + "-04",
                    "certificate_effective_end_time": getTime().get_last_Years(_cert[1], 20) + "-05",
                    "certificate_remark": "备注_" + self.faker.sentence(nb_words=15),
                    "user_resume_type": "31",
                    "template_id": template_id,
                    "worker_user_id": worker_user_id,
                    "check_module_id": "679",
                    "certificate_attach": user_avatar
                },
                "v": self.session_id,
                "f": {
                    "indexpage": "1",
                    "repaging": "1",
                    "pagesize": "10"
                }
            }
            response_add_certificate = send_requests(method='post', url=add_certificate_url, data=json.dumps(add_certificate_data))
            self.is_true(response_add_certificate, "证书填写")

            log.info("""项目课题情况填写""")
            add_project_url = self.hrmapi + "/hrm/work_user/add_project_info"
            add_project_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "extra_info": {},
                    "project_name": "项目课题名称_" + self.faker.sentence(nb_words=5),
                    "project_level": "等级_" + self.faker.word(ext_word_list=None),
                    "project_department": "下达部门_" + self.faker.word(ext_word_list=None),
                    "project_approval_time": getTime().get_last_Years(_cert[1], 26) + "-06",
                    "project_end_time": getTime().get_last_Years(_cert[1], 28) + "-08",
                    "project_self_rank": "3",  # 排名
                    "project_total_people": "30",  # 项目总人数
                    "project_fund": "30000",
                    "project_remark": "备注_" + self.faker.sentence(nb_words=15),
                    "user_resume_type": "31",
                    "template_id": template_id,
                    "worker_user_id": worker_user_id,
                    "check_module_id": "97"
                },
                "v": self.session_id,
                "f": {
                    "indexpage": "1",
                    "repaging": "1",
                    "pagesize": "10"
                }
            }
            response_add_project = send_requests(method='post', url=add_project_url, data=json.dumps(add_project_data))
            self.is_true(response_add_project, "项目课题情况填写")

            log.info("""获奖情况填写""")
            add_award_url = self.hrmapi + "/hrm/work_user/add_award_info"
            add_award_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "extra_info": {},
                    "award_name": "奖励名称_" + self.faker.sentence(nb_words=5),
                    "award_company": "授奖单位_" + self.faker.company(),
                    "award_time": getTime().get_last_Years(_cert[1], 28) + "-07",
                    "award_level": "奖励级别_" + self.faker.sentence(nb_words=5),
                    "award_self_rank": "3",
                    "award_total_people": "40",
                    "award_remark": "备注_" + self.faker.sentence(nb_words=15),
                    "user_resume_type": "31",
                    "template_id": template_id,
                    "worker_user_id": worker_user_id,
                    "check_module_id": "118"
                },
                "v": self.session_id,
                "f": {
                    "indexpage": "1",
                    "repaging": "1",
                    "pagesize": "10"
                }
            }
            response_add_award = send_requests(method='post', url=add_award_url, data=json.dumps(add_award_data))
            self.is_true(response_add_award, "获奖情况填写")

            log.info("""论文著作情况填写""")
            add_thesis_url = self.hrmapi + "/hrm/work_user/add_thesis_info"
            add_thesis_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "extra_info": {},
                    "thesis_name": "论文/著作名称_" + self.faker.sentence(nb_words=5),
                    "thesis_publisher": "发表刊物/出版社_" + self.faker.sentence(nb_words=5),
                    "thesis_publish_time": getTime().get_last_Years(_cert[1], 28) + "-08",
                    "thesis_include_type": "收录杂志类别_" + self.faker.sentence(nb_words=10),
                    "thesis_self_rank": "4",
                    "thesis_total_people": "44",
                    "thesis_remark": "备注_" + self.faker.sentence(nb_words=15),
                    "user_resume_type": "31",
                    "template_id": template_id,
                    "worker_user_id": worker_user_id,
                    "check_module_id": "139"
                },
                "v": self.session_id,
                "f": {
                    "indexpage": "1",
                    "repaging": "1",
                    "pagesize": "10"
                }
            }
            response_add_thesis = send_requests(method='post', url=add_thesis_url, data=json.dumps(add_thesis_data))
            self.is_true(response_add_thesis, "论文著作情况填写")

            log.info("""专利情况填写""")
            add_patent_url = self.hrmapi + "/hrm/work_user/add_patent_info"
            add_patent_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "extra_info": {},
                    "patent_name": "专利名称_" + self.faker.sentence(nb_words=15),
                    "patent_apply_number": t,
                    "patent_apply_time": getTime().get_last_Years(_cert[1], 20) + "-09",
                    "patent_public_number": "专利号_" + str(t),
                    "patent_public_time": getTime().get_last_Years(_cert[1], 20) + "-10",
                    "patent_apply_people": "申请人_" + self.faker.sentence(nb_words=5),
                    "patent_proxy_organ": "专利代理机构_" + self.faker.sentence(nb_words=10),
                    "patent_self_rank": "5",
                    "patent_total_people": "55",
                    "patent_remark": "备注_" + self.faker.sentence(nb_words=15),
                    "user_resume_type": "31",
                    "template_id": template_id,
                    "worker_user_id": worker_user_id,
                    "check_module_id": "159"
                },
                "v": self.session_id,
                "f": {
                    "indexpage": "1",
                    "repaging": "1",
                    "pagesize": "10"
                }
            }
            response_add_patent = send_requests(method='post', url=add_patent_url, data=json.dumps(add_patent_data))
            self.is_true(response_add_patent, "专利情况填写")

            log.info("""语言能力填写""")
            add_language_url = self.hrmapi + "/hrm/work_user/add_language_info"
            add_language_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "extra_info": {},
                    "language_type": self._get_comboBox(data=_comboBox_data['LANGUAGE_TYPE'], value='value')[0],
                    "language_read_write_ability": "读写能力_" + self.faker.word(ext_word_list=None),
                    "language_listen_speak_ability": "听说能力_" + self.faker.word(ext_word_list=None),
                    "language_remark": "3",
                    "user_resume_type": "31",
                    "template_id": template_id,
                    "worker_user_id": worker_user_id,
                    "check_module_id": "177"
                },
                "v": self.session_id,
                "f": {
                    "indexpage": "1",
                    "repaging": "1",
                    "pagesize": "10"
                }
            }
            response_add_language = send_requests(method='post', url=add_language_url, data=json.dumps(add_language_data))
            self.is_true(response_add_language, "语言能力填写")

            log.info("""电子证件上传""")
            electronic_materials_url = self.hrmapi + "/hrm/work_user/electronic_materials_info_detail"
            electronic_materials_data = {"a": {"source": "757"}, "n": {"template_id": template_id, "worker_user_id": worker_user_id},
                                         "v": self.session_id}
            response_electronic_materials = send_requests(method='post', url=electronic_materials_url, data=json.dumps(electronic_materials_data))
            add_electronic_materials_url = self.hrmapi + "/hrm/work_user/add_electronic_materials_info"
            add_electronic_materials_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "extra_info": {},
                    "electronic_materials_id_card": user_avatar,
                    "electronic_materials_schooling_record_certificate": user_avatar,
                    "electronic_materials_diploma": user_avatar,
                    "electronic_materials_employment_form": user_avatar,
                    "electronic_materials_transcript": user_avatar,
                    "electronic_materials_qualification_certificate": user_avatar,
                    "electronic_materials_title_certificate": user_avatar,
                    "electronic_materials_work_experience_proof": user_avatar,
                    "worker_user_id": worker_user_id,
                    "template_id": template_id,
                    "check_module_id": "195",
                },
                "v": self.session_id
            }
            if getJson(response_electronic_materials, 'electronic_materials_id'):
                add_electronic_materials_url = self.hrmapi + "/hrm/work_user/update_electronic_materials_info"
                electronic_materials_id = getJson(response_electronic_materials, 'electronic_materials_id')[0]
                add_electronic_materials_data['n']['electronic_materials_id'] = electronic_materials_id
            response_update = send_requests(method='post', url=add_electronic_materials_url, data=json.dumps(add_electronic_materials_data))
            self.is_true(response_update, "电子证件上传")
        else:
            log.error('worker_user_id没有返回数据')

    def _get_comboBox(self, data, value):
        self.dictionary_group = self.hrmapi + "/hrm/dictionary/system/comboBox"
        self.group_id = self.hrmapi + "/hrm/dictionary/query_group_new"
        self.tree_query = self.hrmapi + "/hrm/organ/message/tree/query"

        if getJson(data, 'dictionary_group'):
            response_comboBox = send_requests(method='post', url=self.dictionary_group, data=json.dumps(data))
        elif getJson(data, 'group_id'):
            response_comboBox = send_requests(method='post', url=self.group_id, data=json.dumps(data))
        else:
            response_comboBox = send_requests(method='post', url=self.tree_query, data=json.dumps(data))
        return getJson(response_comboBox, value)

    def is_have(self, template_id):
        log.info("""判断是否存在基本信息""")
        is_have_url = self.hrmapi + "/hrm/work_user/is_have_base"
        is_have_data = {"n": {"template_id": template_id}, "v": self.session_id}
        response_is_have = send_requests(method='post', url=is_have_url, data=json.dumps(is_have_data))
        return response_is_have

    def is_true(self, obj, msg):
        if self.assertTrue(getJson(obj, 'message')[0], '成功'):
            log.info(msg + "成功")
        else:
            log.error('{0}失败,失败信息--->{1}'.format(msg, obj))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('test_run', 'test', '13234166667'))
    unittest.TextTestRunner(verbosity=2).run(suite)
