import unittest
import configparser
import json
import random
from faker import Faker
from DemoGChrm.config import setting
from DemoGChrm.lib.getJsonPath import getJson
from DemoGChrm.lib.log import Log
from DemoGChrm.lib.sendRequests import send_requests
from DemoGChrm.lib.login import login_hrm
from DemoGChrm.lib.getTime import getTime
from DemoGChrm.lib.get_userCert import getCert

log = Log().getLog()
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='utf-8')
USER = cf.get("user", "USER_1")
'''
添加在职人员
'''


class MyTestCase(unittest.TestCase):

    def __init__(self, testName, login_PATH, login_user=None, pwd=None):
        super(MyTestCase, self).__init__(testName)
        self.faker = Faker(locale='zh_CN')
        self.hrmapi = cf.get(login_PATH, "hrmapi")
        if login_user:
            response_login = login_hrm(path=login_PATH, user=login_user, pwd=pwd)
        else:
            response_login = login_hrm(path=login_PATH, user=USER, pwd=pwd)
        self.gcgateway = cf.get(login_PATH, "gcgateway")
        self.session_id = {'session_id': getJson(response_login, 'session_id')[0]}
        self.require_id = getJson(response_login, 'require_form_id')[0]

    def test_run(self):

        log.info("初始化下拉选择数据")
        _dictionary_group = {
            'family_people_is_emergency': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RIGHT_TYPE"}, "v": self.session_id},  # 是否紧急联系人
            'family_people_education_status': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "EDUCATION_STATUS"}, "v": self.session_id},
            # 文化程度
            'family_people_politics_status': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "POLITICS_STATUS"}, "v": self.session_id},
            # 政治面貌
            'family_people_relation': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "FAMILY_RELATION"}, "v": self.session_id},  # 与本人关系

            'base_title_way_obtain': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "HDFS"}, "v": self.session_id},  # 获得方式
            'base_title_level': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "ZCJB"}, "v": self.session_id},  # 职称级别
            'base_new_job_title_part': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "base_new_job_title_part"}, "v": self.session_id},
            # 兼任职称
            'is_attendance': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RIGHT_TYPE"}, "v": self.session_id},  # 是否考勤
            'is_clinical_staff': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RIGHT_TYPE"}, "v": self.session_id},  # 是否临床人员
            'is_dept_head': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RIGHT_TYPE"}, "v": self.session_id},  # 是否科室负责人
            'is_middle': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RIGHT_TYPE"}, "v": self.session_id},  # 是否中层
            'is_leader': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RIGHT_TYPE"}, "v": self.session_id},  # 是否院领导

            'hospital_people_type': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "HOSPITAL_USER_TYPE"}, "v": self.session_id},  # 类别
            'in_hospital_type': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "IN_HOSPITAL_TYPE"}, "v": self.session_id},  # 入院方式
            'worker_status': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RESUME_TYPE_IN_WORKER_STATUS"}, "v": self.session_id},  # 在职状态
            'employee_use_type': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "EMPLOYEE_USE_TYPE"}, "v": self.session_id},  # 用工形式
            'worker_type': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "WORKER_TYPE"}, "v": self.session_id},  # 职工类别
            'worker_employee_type': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "REQUIRE_NATURE"}, "v": self.session_id},  # 员工类型
            'biography_two': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "BIOGRAPHY_TYPE"}, "v": self.session_id},  # 编制分类
            'biography_one': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "BIOGRAPHY_TYPE"}, "v": self.session_id},  # 编制分类
            'people_nature': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "REQUIRE_NATURE"}, "v": self.session_id},  # 人员性质
            'people_type': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "PEOPLE_TYPE"}, "v": self.session_id},  # 人员类别

            'user_personal_tag': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "PERSONAL_TAG"}, "v": self.session_id},  # 个人标签
            'user_is_overseas_experience': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RIGHT_TYPE"}, "v": self.session_id},  # 海外经历
            'user_is_cultivate': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RIGHT_TYPE"}, "v": self.session_id},  # 是否完成规培
            'user_computer_level': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "COMPUTER_LEVEL"}, "v": self.session_id},  # 计算机等级
            'user_language_level': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "LANGUAGE_LEVEL"}, "v": self.session_id},  # 外语等级
            'user_title': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "TITLE_TYPE"}, "v": self.session_id},  # 职称
            'user_practice_status': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RIGHT_TYPE"}, "v": self.session_id},  # 执业资格
            'user_is_foreign': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "RIGHT_TYPE"}, "v": self.session_id},  # 是否港澳台及外籍人士
            'user_household_type': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "HOUSEHOLD_TYPE"}, "v": self.session_id},  # 户籍类型
            'user_country': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "COUNTRY_TYPE"}, "v": self.session_id},  # 国家
            'user_other_politics_status': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "POLITICS_STATUS"}, "v": self.session_id},  # 另一党派
            'user_politics_status': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "POLITICS_STATUS"}, "v": self.session_id},  # 政治面貌
            'user_health_status': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "HEALTH_STATUS"}, "v": self.session_id},  # 健康状况
            'user_marital_status': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "MARITAL_STATUS"}, "v": self.session_id},  # 婚姻状况
            'user_national': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "NATIONAL_TYPE"}, "v": self.session_id},  # 民族
            'user_cert_type': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "CERT_TYPE"}, "v": self.session_id},  # 证件类型
            'user_sex': {"a": {"source": "1284"}, "n": {"dictionary_group_type": "SEX"}, "v": self.session_id},  # 证件类型
        }

        add_info_url = self.hrmapi + "/hrm/worker/info/add"
        add_info_data = {
            "n": {
                "template_id": "1221",
                "template_type": "771",
                "worker_info": {
                },
                "is_sync": "0"
            },
            "a": {
                "source": "1284"
            },
            "v": self.session_id
        }

        log.info('''获取基本信息模板''')
        template_query_url = self.gcgateway + "/unify_users/module/template/field/group/query"
        template_query_data = {"n": {"template_id": "1221", "template_type": "771", }, "a": {"source": "1284"}, "v": self.session_id}
        response_template_query = send_requests(method='post', url=template_query_url, data=json.dumps(template_query_data))
        self.is_true(response_template_query, '获取基本信息模板')

        log.info('''根据模板生成添加在职人员信息''')
        module_details = getJson(response_template_query, 'module_details')[0]  # response_template_query['n'][0]['module_details']
        for _details in module_details:
            if _details["field_details"]:
                for _detail in _details["field_details"]:
                    if _details['module_id'] not in add_info_data['n']['worker_info'].keys():
                        if _details['module_id'] == "549":
                            add_info_data['n']['worker_info'][_details['module_id']] = {}
                        if _details['module_id'] == "72":
                            add_info_data['n']['worker_info'][_details['module_id']] = {"is_attendance": "1", "is_middle": "0", "is_leader": "0",
                                                                                        "user_resume_type": "477", "is_clinical_staff": "0",
                                                                                        "extra_info": {}}
                        else:
                            add_info_data['n']['worker_info'][_details['module_id']] = {"is_attendance": "1", "is_middle": "0", "is_leader": "0",
                                                                                        "is_clinical_staff": "0", "extra_info": {}}
                    worker_info = add_info_data['n']['worker_info'][_details['module_id']]
                    _cert_number = self.faker.ssn(min_age=30, max_age=60)
                    _cert = getCert(_cert_number)
                    _phone = self.faker.phone_number()
                    if _detail['is_show'] == '1' and _detail.get('template_type_771') and _detail['is_must'] == '1':
                        worker_info[_detail['field_name']] = ''
                        if _detail['field_type'] in ('REGION', 'INPUT'):  # 判断是否为数字输入框
                            if ('number' in _detail['field_name']) or ('phone' in _detail['field_name']):  # 判断是否为数字输入框
                                if 'phone' in _detail['field_name']:  # 判断是否为手机号输入框
                                    if _detail['is_extra'] == "1":  # 判断是否为额外字段
                                        worker_info['extra_info'][_detail['field_name']] = _phone
                                    worker_info[_detail['field_name']] = _phone
                                else:
                                    TIME = getTime.now_time.strftime("%Y%m%d%H%M%S")
                                    if _detail['is_extra'] == "1":  # 判断是否为额外字段
                                        worker_info['extra_info'][_detail['field_name']] = TIME
                                    worker_info[_detail['field_name']] = TIME

                            elif 'email' in _detail['field_name']:  # 判断是否为邮箱输入框
                                if _detail['is_extra'] == "1":  # 判断是否为额外字段
                                    worker_info['extra_info'][_detail['field_name']] = _phone + "@11.com"
                                worker_info[_detail['field_name']] = _phone + "@11.com"

                            elif _detail['field_desc'] == '姓名':  # 判断是否为姓名输入框
                                field_desc = _detail['field_desc'] + "_" + self.faker.name()
                                if _detail['is_extra'] == "1":  # 判断是否为额外字段
                                    worker_info['extra_info'][_detail['field_name']] = field_desc
                                worker_info[_detail['field_name']] = field_desc

                            else:
                                field_desc = _detail['field_desc'] + "_" + self.faker.text(max_nb_chars=10)
                                if _detail['is_extra'] == "1":  # 判断是否为额外字段
                                    worker_info['extra_info'][_detail['field_name']] = field_desc
                                worker_info[_detail['field_name']] = field_desc

                        elif _detail['field_type'] == 'SELECT':  # 判断是否为下拉选择框
                            if _detail['field_name'] in _dictionary_group.keys():
                                data = _dictionary_group[_detail['field_name']]
                            else:
                                data = {"a": {"source": "1284"}, "n": {"dictionary_group_type": _detail['field_name']}, "v": self.session_id}
                            if self._get_comboBox(data=data, value='dictionary_key'):
                                dictionary_key = random.choice(self._get_comboBox(data=data, value='dictionary_key'))
                                if _detail['is_extra'] == "1":  # 判断是否为额外字段
                                    worker_info['extra_info'][_detail['field_name']] = dictionary_key
                                worker_info[_detail['field_name']] = dictionary_key

                        elif _detail['field_type'] == 'SELECT_TREE':  # 判断是否为下拉选择框
                            data = {"n": {}, "a": {"source": "1284"}, "v": self.session_id}
                            SELECT_TREE = ['%s' % random.choice(self._get_comboBox(data=data, value='middle_dept_id'))]
                            if _detail['is_extra'] == "1":  # 判断是否为额外字段
                                worker_info['extra_info'][_detail['field_name']] = SELECT_TREE
                            worker_info[_detail['field_name']] = SELECT_TREE
                        elif _detail['field_type'] == 'DATE':  # 判断是否为日期输入输入狂
                            DATE = getTime().get_last_Years(_cert[1], random.randint(10, 20))
                            if _detail['is_extra'] == "1":  # 判断是否为额外字段
                                worker_info['extra_info'][_detail['field_name']] = DATE
                            worker_info[_detail['field_name']] = DATE
                        else:
                            log.error("未知类型--->{0}".format(_detail['field_type']))
                    if _detail['field_name'] in ('user_cert_number', 'user_sex', 'user_age', 'user_birth_time', 'user_birth_month'):
                        worker_info['user_cert_number'] = _cert_number
                        worker_info['user_sex'] = _cert[2]
                        worker_info['user_age'] = _cert[3]
                        worker_info['user_birth_time'] = _cert[1]
                        worker_info['user_birth_month'] = _cert[0]
        log.debug('生成的添加在职人员信息--->{0}'.format(add_info_data))
        log.info('''添加在职人员''')
        response_add_info = send_requests(method='post', url=add_info_url, data=json.dumps(add_info_data))
        self.is_true(response_add_info, '添加在职人员')

    def _get_comboBox(self, data, value):
        self.dictionary_group = self.hrmapi + "/hrm/dictionary/select/system"
        self.tree_query = self.gcgateway + "/unify_users/dept/sync/middle/tree/query"
        if getJson(data, 'dictionary_group_type'):
            response_comboBox = send_requests(method='post', url=self.dictionary_group, data=json.dumps(data))
        else:
            response_comboBox = send_requests(method='post', url=self.tree_query, data=json.dumps(data))
        return getJson(response_comboBox, value)

    def is_true(self, obj, msg):
        if getJson(obj, 'message')[0] == '成功':
            log.info(msg + "成功")
        else:
            log.error('{0}失败,失败信息--->{1}'.format(msg, obj))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('test_run', 'test', 'GC0200074603961341'))
    unittest.TextTestRunner(verbosity=2).run(suite)
