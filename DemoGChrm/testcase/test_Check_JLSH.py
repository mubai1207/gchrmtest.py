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
简历审核
'''


class MyTestCase(unittest.TestCase):

    def __init__(self, testName, login_PATH, user_phone, pwd=None):
        super(MyTestCase, self).__init__(testName)
        self.faker = Faker(locale='zh_CN')
        self.user_phone = user_phone
        self.hrmapi = cf.get(login_PATH, "hrmapi")
        self.gcgateway = cf.get(login_PATH, "gcgateway")
        response_login = login_hrm(path=login_PATH, user=USER, pwd=pwd)
        self.session_id = {'session_id': getJson(response_login, 'session_id')[0]}

    def test_run(self):
        log.info("获取待审核数据")
        require_query_url = self.hrmapi + "/hrm/require/recruitment_worker_require_query"
        require_query_data = {
            "a": {
                "source": "1284"
            },
            "n": {
                "search_user_name": "",
                "search_user_phone": self.user_phone,
                "audit_result": "692",
                "search_user_cert_number": "",
                "recruitment_plan_ids": "",
                "recruit_plan_status": "",
                "search_recruitment_require_position_name": "",
                "search_user_age_start": "",
                "search_user_age_end": "",
                "search_diploma_major": "",
                "search_diploma_end": "",
                "search_diploma_highest_degree": "",
                "search_tag": "",
                "worker_resume_apply_time_range": "",
                "search_audit_time_range": ""
            },
            "v": self.session_id,
            "f": {
                "indexpage": 1,
                "repaging": "1",
                "pagesize": 20
            }
        }
        response_require_query = send_requests(method='post', url=require_query_url, data=json.dumps(require_query_data))
        self.is_true(response_require_query, '获取待审核数据')
        resume_id = getJson(response_require_query, "resume_id")
        log.info("转为待复审")
        require_audit_url = self.hrmapi + "/hrm/require/recruitment_worker_require_audit"
        require_audit_data = {
            "a": {
                "source": "1284"
            },
            "n": {
                "audit_result": "43",
                "module_id": "1",
                "resume_id_list": resume_id,
                "review_detail": {
                    "review_user_remark": "复审备注_" + self.faker.sentence(nb_words=15)
                }
            },
            "v": self.session_id
        }
        response_require_audit = send_requests(method='post', url=require_audit_url, data=json.dumps(require_audit_data))
        self.is_true(response_require_audit, '转为待复审')

        require_query_data['n']['audit_result'] = '43'
        response_require_query = send_requests(method='post', url=require_query_url, data=json.dumps(require_query_data))
        self.is_true(response_require_query, '第一次审核通过')
        resume_id = getJson(response_require_query, "resume_id")

        log.info("审核通过")
        pass_data = {
            "a": {
                "source": "1284"
            },
            "n": {
                "audit_result": "291",
                "module_id": "1",
                "pass_notice_list": [{
                    "is_send_message": 7
                }],
                "resume_id_list": resume_id
            },
            "v": self.session_id
        }
        response_pass = send_requests(method='post', url=require_audit_url, data=json.dumps(pass_data))
        self.is_true(response_pass, '审核通过')

        require_query_data['n']['audit_result'] = '291'
        response_require_query = send_requests(method='post', url=require_query_url, data=json.dumps(require_query_data))
        self.is_true(response_require_query, '审核通过')

    def is_true(self, obj, msg):
        if self.assertTrue(getJson(obj, 'message')[0], '成功'):
            log.info(msg + "成功")
        else:
            log.error('{0}失败,失败信息--->{1}'.format(msg, obj))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('test_run', 'test', '13234166661'))
    unittest.TextTestRunner(verbosity=2).run(suite)
