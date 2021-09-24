import unittest
import configparser
import json
from faker import Faker
from DemoGChrm.config import setting
from DemoGChrm.lib.getJsonPath import getJson
from DemoGChrm.lib.log import Log
from DemoGChrm.lib.sendRequests import send_requests
from DemoGChrm.lib.login import login_work_base, login_hrm

log = Log().getLog()
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='utf-8')
USER = cf.get("user", "USER_1")
'''
招聘岗位报名
'''


class MyTestCase(unittest.TestCase):

    def __init__(self, testName, login_PATH, login_phone):
        super(MyTestCase, self).__init__(testName)
        self.faker = Faker(locale='zh_CN')
        self.hrmapi = cf.get(login_PATH, "hrmapi")
        self.gcgateway = cf.get(login_PATH, "gcgateway")
        self.corp_id = cf.get(login_PATH, "corp_id")
        self.login_phone = login_phone
        self.login_PATH = login_PATH
        self.login_work_data = login_work_base(path=login_PATH, phone=self.login_phone)
        self.session_id = {"session_id": getJson(self.login_work_data, 'session_id')[0]}  #

    def test_run(self):

        log.info("""获取招聘岗位""")
        require_home_url = self.hrmapi + "/hrm/recruit/require/info/query/home"
        require_home_data = {"a": {"source": "757"},
                             "n": {"position_name": "", "area_id": "", "plan_type": "", "year": "", "corp_id": self.corp_id},
                             "v": {},
                             "f": {"indexpage": 1, "repaging": "1", "pagesize": 20}}
        response_home_query = send_requests(method='post', url=require_home_url, data=json.dumps(require_home_data))
        self.is_true(response_home_query, '获取招聘岗位结果')

        template_id = getJson(response_home_query, 'job_form_id')[0]
        require_id = getJson(response_home_query, 'require_id')[0]
        plan_id = getJson(response_home_query, 'plan_id')[0]
        response_is_have = self.is_have(template_id)

        if getJson(response_is_have, 'is_have_base')[0] == 1:
            log.info("""招聘岗位报名""")
            worker_user_id = getJson(response_is_have, 'worker_user_id')[0]
            require_check_url = self.hrmapi + "/hrm/require/recruitment_worker_require_check_delivery"
            require_check_data = {
                "a": {
                    "source": "757"
                },
                "n": {
                    "require_id": require_id,
                    "recruitment_plan_id": plan_id
                },
                "v": self.session_id
            }
            response_require_check = send_requests(method='post', url=require_check_url, data=json.dumps(require_check_data))

            if getJson(response_require_check, "message")[0] == "成功":
                require_delivery_url = self.hrmapi + "/hrm/require/recruitment_worker_require_delivery"
                require_delivery_data = {
                    "a": {
                        "source": "757"
                    },
                    "n": {
                        "require_id": require_id,
                        "worker_user_id": worker_user_id,
                        "recruitment_plan_id": plan_id
                    },
                    "v": self.session_id,
                    "f": {
                        "indexpage": "1",
                        "repaging": "1",
                        "pagesize": "10"
                    }
                }
                require_delivery = send_requests(method='post', url=require_delivery_url, data=json.dumps(require_delivery_data))
                self.is_true(require_delivery, '招聘岗位报名')
            else:
                if getJson(response_require_check, "message")[0] == '您已经投递过':
                    response_login = login_hrm(path=self.login_PATH, user=USER)
                    session_hrm = {'session_id': getJson(response_login, 'session_id')[0]}
                    log.info('删除投递岗位')
                    audit_result = [692, 43, 291, 407]  # 692待审核,43待复审,291审核通过,407审核不通过
                    require_query_url = self.hrmapi + '/hrm/require/recruitment_worker_require_query'  # 审核通过
                    for _result in audit_result:
                        require_query_data = {
                            "a": {
                                "source": "1284"
                            },
                            "n": {
                                "search_user_name": "",
                                "search_user_phone": self.login_phone,
                                "audit_result": _result,
                                "search_user_cert_number": "",
                                "recruitment_plan_ids": [],
                                "recruit_plan_status": [],
                                "search_recruitment_require_position_name": "",
                                "search_user_age_start": "",
                                "search_user_age_end": "",
                                "search_diploma_major": "",
                                "search_diploma_end": [],
                                "search_diploma_highest_degree": [],
                                "search_tag": [],
                                "worker_resume_apply_time_range": "",
                                "search_audit_time_range": ""
                            },
                            "v": session_hrm,
                            "f": {
                                "indexpage": 1,
                                "repaging": "1",
                                "pagesize": 20
                            }
                        }
                        response_require_query = send_requests(method='post', url=require_query_url, data=json.dumps(require_query_data))

                        if getJson(response_require_query, "resume_id"):
                            batch_delete_url = self.hrmapi + "/hrm/require/resume/batch_delete"
                            batch_delete_data = {
                                "a": {
                                    "source": "1284"
                                },
                                "n": {
                                    "resume_id_list": getJson(response_require_query, "resume_id")
                                },
                                "v": session_hrm
                            }
                            response_batch_delete = send_requests(method='post', url=batch_delete_url, data=json.dumps(batch_delete_data))
                            self.is_true(response_batch_delete, '删除投递岗位')
                            self.test_run()
                            break
                else:
                    log.info(getJson(response_require_check, "message")[0])
        else:
            log.info("""应聘记录信息未填写""")

    def is_have(self, template_id):
        log.info("""判断是否存在基本信息""")
        is_have_url = self.hrmapi + "/hrm/work_user/is_have_base"
        is_have_data = {"n": {"template_id": template_id}, "v": self.session_id}
        response_is_have = send_requests(method='post', url=is_have_url, data=json.dumps(is_have_data))
        return response_is_have

    def is_true(self, obj, msg):
        if getJson(obj, 'message')[0] == '成功':
            log.info(msg + "成功")
        else:
            log.error('{0}失败,失败信息--->{1}'.format(msg, obj))


if __name__ == '__main__':
    # MyTestCase('test_run','test', '15103477778').test_run()
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('test_run', 'test', '17205434095'))
    unittest.TextTestRunner(verbosity=2).run(suite)
    # now = time.strftime("%Y-%m-%d %H_%M_%S")  # 获取当前系统时间
    # result_path = setting.TEST_REPORT
    # filename = result_path + '/' + now + 'result.html'  # 定义报告名称
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='接口自动化测试报告', description='环境：windows 10 浏览器：chrome', tester='RaoPQ')
    # runner.run(suite)  # 执行所有的测试用例
    # fp.close()
