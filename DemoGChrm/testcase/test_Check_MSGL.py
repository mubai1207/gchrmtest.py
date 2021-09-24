import unittest
import configparser
import json
from faker import Faker
from DemoGChrm.config import setting
from DemoGChrm.lib.getJsonPath import getJson
from DemoGChrm.lib.log import Log
from DemoGChrm.lib.sendRequests import send_requests
from DemoGChrm.lib.login import login_hrm
from DemoGChrm.lib.getSession import getSession

log = Log().getLog()
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='utf-8')
USER = cf.get("user", "USER_1")
'''
面试管理
'''


class MyTestCase(unittest.TestCase):

    def __init__(self, testName, login_PATH, user_phone, pwd=None):
        super(MyTestCase, self).__init__(testName)
        self.faker = Faker(locale='zh_CN')
        self.user_phone = user_phone
        self.hrmapi = cf.get(login_PATH, "hrmapi")
        self.gcgateway = cf.get(login_PATH, "gcgateway")
        login_hrm(path=login_PATH, user=USER, pwd=pwd)
        self.session_id = getSession()

    def test_run(self):
        log.info("获取面试轮数")
        interview_plan_url = self.hrmapi + "/hrm/interview/config_query/plan_id"
        interview_plan_data = {
            "n": {
                "recruitment_plan_id": ""
            },
            "a": {
                "source": "1284"
            },
            "v": self.session_id
        }
        response_interview_plan = send_requests(method='post', url=interview_plan_url, data=json.dumps(interview_plan_data))
        self.is_true(response_interview_plan, '获取面试轮数')
        examine_details = getJson(response_interview_plan, 'n')[0]
        # for _details in examine_details:
        #     _details['interview_details'][0]['max_score'] = 'null'
        #     _details['interview_details'][0]['min_score'] = 'null'

        log.info("查询用户信息")
        interview_query_url = self.hrmapi + "/hrm/interview/recruitment_interview_query"
        interview_query_data = {
            "a": {
                "source": "1284"
            },
            "n": {
                "examine_details": examine_details,
                "recruitment_plan_id": "",
                "recruitment_plan_name": "",
                "round_number": 1,
                "search_interview_meet_score_end": "",
                "search_interview_meet_score_start": "",
                "search_interview_total_score_end": "",
                "search_interview_total_score_start": "",
                "search_recruitment_require_position_name": "",
                "search_user_cert_number": "",
                "search_user_name": "",
                "search_user_phone": self.user_phone,
                "user_personal_tag": ""
            },
            "v": self.session_id,
            "f": {
                "indexpage": 1,
                "repaging": "1",
                "pagesize": 10
            }
        }
        response_interview_query = send_requests(method='post', url=interview_query_url, data=json.dumps(interview_query_data))
        self.is_true(response_interview_query, '查询用户信息')
        interview_id = getJson(response_interview_query, 'interview_id')

        log.info("进入下一轮面试")
        interview_audit_url = self.hrmapi + "/hrm/interview/recruitment_interview_audit"
        interview_audit_data = {
            "a": {
                "source": "1284"
            },
            "n": {
                "interview_status": "45",
                "module_id": "2",
                "interview_id_list": interview_id,
                "retest_detail": [],
                "tag_list": []
            },
            "v": self.session_id,
            "f": {
                "indexpage": "1",
                "repaging": "1",
                "pagesize": "10"
            }
        }
        response_interview_audit = send_requests(method='post', url=interview_audit_url, data=json.dumps(interview_audit_data))
        self.is_true(response_interview_audit, '进入下一轮面试')

        log.info("进入拟录用")
        interview_audit_data['n'].pop('retest_detail')
        interview_audit_data['n']['interview_status'] = '293'
        interview_audit_data['n']['proposed_employment_detail'] = []
        response_interview_audit = send_requests(method='post', url=interview_audit_url, data=json.dumps(interview_audit_data))
        self.is_true(response_interview_audit, '进入拟录用')

        log.info("确定录用")
        select_system_url = self.hrmapi + "/hrm/dictionary/select/system"
        select_system_data = {
            "a": {
                "source": "1284"
            },
            "n": {
                "dictionary_group_type": "PERSONAL_TAG"
            },
            "v": self.session_id
        }
        response_select_system = send_requests(method='post', url=select_system_url, data=json.dumps(select_system_data))
        dictionary_value = getJson(response_select_system, "dictionary_value")
        interview_audit_data['n']['interview_status'] = '486'
        interview_audit_data['n']['tag_list'] = dictionary_value
        interview_audit_data['n']['employment_detail'] = []
        response_interview_audit = send_requests(method='post', url=interview_audit_url, data=json.dumps(interview_audit_data))
        self.is_true(response_interview_audit, '确定录用')

    def is_true(self, obj, msg):
        if self.assertTrue(getJson(obj, 'message')[0], '成功'):
            log.info(msg + "成功")
        else:
            log.error('{0}失败,失败信息--->{1}'.format(msg, obj))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('test_run', 'test', '13234166661'))
    unittest.TextTestRunner(verbosity=2).run(suite)
