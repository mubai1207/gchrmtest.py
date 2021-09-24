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

log = Log().getLog()
cf = configparser.ConfigParser()
cf.read(setting.TEST_CONFIG, encoding='utf-8')
USER = cf.get("user", "USER_1")
'''
添加用人需求
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
        # try:
        log.info("获取选择数据")
        _comboBox_data = {
            'tree_query': {"a": {"source": "1284"}, "n": {"organ_crop_type": "395", "organ_father_id": "", "organ_id": ""}, "v": self.session_id},
            # 需求部门选择
            'ZPGW': {"a": {"source": "1284"}, "n": {"dictionary_group": "ZPGW"}, "v": self.session_id},  # 需求岗位选择
            'XQYQ': {"a": {"source": "1284"}, "n": {"dictionary_group": "XQYQ"}, "v": self.session_id},  # 需求院区选择
            'GWLB': {"a": {"source": "1284"}, "n": {"group_id": "GWLB"}, "v": self.session_id},  # 岗位类别选择
            'DJYQ': {"a": {"source": "1284"}, "n": {"dictionary_group": "DJYQ"}, "v": self.session_id},  # 等级要求选择
            'XQGWFL': {"a": {"source": "1284"}, "n": {"dictionary_group": "XQGWFL"}, "v": self.session_id},  # 岗位分类选择
            'YRXZ': {"a": {"source": "1284"}, "n": {"dictionary_group": "YRXZ"}, "v": self.session_id},  # 用人性质选择
            'NLSX': {"a": {"source": "1284"}, "n": {"dictionary_group": "NLSX"}, "v": self.session_id},  # 年龄上限选择
            'XQXL': {"a": {"source": "1284"}, "n": {"dictionary_group": "XQXL"}, "v": self.session_id},  # 学历要求选择
            'DEGREE_TYPE': {"a": {"source": "1284"}, "n": {"group_id": "DEGREE_TYPE"}, "v": self.session_id},  # 学位要求选择
            'ZCYQ': {"a": {"source": "1284"}, "n": {"dictionary_group": "ZCYQ"}, "v": self.session_id},  # 职称要求选择
            'ZYZG': {"a": {"source": "1284"}, "n": {"dictionary_group": "ZYZG"}, "v": self.session_id},  # 专业技术资格选择
            'ZYTJ': {"a": {"source": "1284"}, "n": {"dictionary_group": "ZYTJ"}, "v": self.session_id},  # 专业条件选择
            'RIGHT_TYPE': {"a": {"source": "1284"}, "n": {"group_id": "RIGHT_TYPE"}, "v": self.session_id},  # 是否完成规培
            'ZPFL': {"a": {"source": "1284"}, "n": {"dictionary_group": "ZPFL"}, "v": self.session_id},  # 招聘分类
            'ZPBQ': {"a": {"source": "1284"}, "n": {"dictionary_group": "ZPBQ   "}, "v": self.session_id},  # 发布平台\#招聘标签
            'PUSH_TYPE': {"a": {"source": "1284"}, "n": {"group_id": "PUSH_TYPE"}, "v": self.session_id},  # 发布栏目
            'XQJG': {"a": {"source": "1284"}, "n": {"dictionary_group": "XQJG"}, "v": self.session_id},  # 需求机构

        }

        log.info('''初始化请求参数''')
        _recruitment_require = {
            "recruitment_require_age_limit": random.choice(self._get_comboBox(data=_comboBox_data['NLSX'], value='value')),  # 年龄上限
            "recruitment_require_area": random.choice(self._get_comboBox(data=_comboBox_data['XQYQ'], value='value')),  # 需求院区
            "recruitment_require_degrees": random.choice(self._get_comboBox(data=_comboBox_data['DEGREE_TYPE'], value='value')),  # 学位要求
            "recruitment_require_department_leader": {"name": ""},
            "recruitment_require_education": random.choice(self._get_comboBox(data=_comboBox_data['XQXL'], value='value')),  # 学历要求
            "recruitment_require_is_fresh": "824",  # 是否应届
            "recruitment_require_is_shortage": "1",  # 是否紧缺岗位
            "recruitment_require_level": random.choice(self._get_comboBox(data=_comboBox_data['DJYQ'], value='value')),  # 等级要求
            "recruitment_require_major_condition": [random.choice(self._get_comboBox(data=_comboBox_data['ZYTJ'], value='value'))],  # 专业条件
            "recruitment_require_nature": random.choice(self._get_comboBox(data=_comboBox_data['YRXZ'], value='value')),  # 用人性质
            "recruitment_require_other_condition": "其他条件_" + self.faker.text(max_nb_chars=15),  # 其他条件
            "recruitment_is_complete_cultivate": random.choice(self._get_comboBox(data=_comboBox_data['RIGHT_TYPE'], value='value')),  # 是否完成规赔

            "recruitment_require_practice": [random.choice(self._get_comboBox(data=_comboBox_data['ZYZG'], value='value'))],  # 专业技术资格
            "recruitment_require_reason": "申报原因_" + self.faker.text(max_nb_chars=30),  # 申报原因
            "recruitment_require_title_level": random.choice(self._get_comboBox(data=_comboBox_data['ZCYQ'], value='value')),  # 职称要求
            "recruitment_require_year": "2021",  # 年度
            "recruitment_require_position_classify": random.choice(self._get_comboBox(data=_comboBox_data['XQGWFL'], value='value')),  # 岗位分类
            "recruitment_require_position_type": random.choice(self._get_comboBox(data=_comboBox_data['GWLB'], value='value')),  # 岗位类别
            "recruitment_require_position_id": random.choice(self._get_comboBox(data=_comboBox_data['ZPGW'], value='value')),  # 需求岗位
        }

        log.info('''默认请求参数''')
        position_name = "岗位名称_" + self.faker.job()
        _add_data = {
            "a": {
                "source": "1284"
            },
            "n": {
                "recruitment_require_depart": random.choice(self._get_comboBox(data=_comboBox_data['tree_query'], value='id')),  # 需求部门
                "recruitment_require_position_name": position_name,  # 岗位名称
                "recruitment_require_people_count": random.randint(1, 10),  # 招聘人数
                "dept_id": "",
                "position_id": "",
                "require_extra_info": {},  # 其他需求信息
                "template_id": "ZPXQFORM1",
                "add_entrance_type": "823"
            },
            "v": self.session_id,
            "f": {
                "indexpage": "1",
                "repaging": "1",
                "pagesize": "10"
            }
        }

        log.info('''获取用人需求模板''')
        template_group_data = {"n": {"template_type": "790", "template_id": self.require_id}, "a": {"source": "1284"}, "v": self.session_id}  # 用人需求模板
        template_group = self.gcgateway + "/unify_users/module/template/field/group/query"
        response_template_group = send_requests(method='post', url=template_group, data=json.dumps(template_group_data))
        self.is_true(response_template_group, '获取用人需求模板')

        show_group = []
        for i, j in enumerate(getJson(response_template_group, 'is_show')):
            if j == '1':
                show_group.append(getJson(response_template_group, 'field_name')[i])

        log.info('''根据用人需求模板更新请求参数''')
        for i, _require in enumerate(show_group):
            if _require in _recruitment_require.keys():
                _add_data['n'][_require] = _recruitment_require[_require]
                continue
            if "require" not in _require:
                _add_data['n']['require_extra_info'][_require] = "其他需求信息_" + str(i) + self.faker.text(max_nb_chars=15, ext_word_list=None)
            # if _require in _recruitment_require.keys():
            #     _add_data['n'][_require] = _recruitment_require[_require]
            # else:
            #     _add_data['n']['require_extra_info'][_require] = "其他需求信息_" + str(i) + self.faker.text(max_nb_chars=15, ext_word_list=None)
        log.info("用人需求模板更新后参数--->{0}".format(_add_data))

        log.info('''添加用人需求''')
        add_require_url = self.hrmapi + '/hrm/recruit/require/info/add'
        add_detail_url = self.hrmapi + "/hrm/code/query/detail"  # 用人需求编号是否需要填写
        add_detail_adta = {"a": {"source": "1284"}, "n": {"code_type": "536"}, "v": self.session_id}
        response_add_detail = send_requests(method='post', url=add_detail_url, data=json.dumps(add_detail_adta))
        if getJson(response_add_detail, 'rule_type')[0] == '774':
            _add_data['n']['require_id'] = getTime.now_time.strftime("%Y%m%d%H%M%S")
        response_require_add = send_requests(method='post', url=add_require_url, data=json.dumps(_add_data))
        self.is_true(response_require_add, '添加用人需求')

        log.info('''获取用人需求列表数据''')
        require_info_data = {
            "a": {
                "source": "1284"
            },
            "n": {
                "recruitment_require_number": "",
                "year": "",
                "require_status": [],
                "dept_need": "",
                "position_name": "",
                "area_id": "",
                "position_need": ""
            },
            "v": self.session_id,
            "f": {
                "indexpage": 1,
                "repaging": "1",
                "pagesize": 10
            },
        }
        require_info_url = self.hrmapi + '/hrm/recruit/require/info/query'
        response_require_info = send_requests(method='post', url=require_info_url, data=json.dumps(require_info_data))
        require_id = getJson(response_require_info, 'require_id')
        self.is_true(response_require_info, '获取用人需求列表数据')

        '''删除用人需求'''
        delete_require_url = self.hrmapi + '/hrm/recruit/require/info/delete'
        delete_require_data = {"a": {"source": "1284"}, "n": {"require_id": require_id[0]}, "v": self.session_id}
        # response_delete_require = send_requests(method='post', url=delete_require_url, data=json.dumps(delete_require_data))
        # log.info('用人需求删除结果--->{0}'.format(getJson(response_delete_require, 'message')[0]))

        log.info('''确认用人需求''')
        update_require_url = self.hrmapi + '/hrm/recruit/require/info/update'
        update_require_data = _add_data
        update_require_data['n']['year'] = _add_data['n']['recruitment_require_year']
        update_require_data['n']['status'] = '816'
        update_require_data['n']['require_id'] = require_id[0]
        update_require_data['n']['remark'] = '确定招聘备注_' + self.faker.text(max_nb_chars=15, ext_word_list=None)
        update_require_data['n'].pop('require_extra_info')
        update_require_data['n'].pop('recruitment_require_year')
        update_require_data['n'].pop('add_entrance_type')
        response_update_require = send_requests(method='post', url=update_require_url, data=json.dumps(update_require_data))
        self.is_true(response_update_require, '确认用人需求')

        # '''直接发布用人需求'''
        # template_list_url = self.gcgateway + "/unify_users/module/template/info/query/list"
        # template_list_data = {"n": {"template_type": "297"}, "a": {"source": "1284"}, "v": self.session_id}  # 选择应聘登记表
        # response_template_list = getJson(send_requests(method='post', url=template_list_url, data=json.dumps(template_list_data)), 'template_id')
        # require_push_data = {
        #     "n": {
        #         "job_form_id": response_template_list[0],  # 选择应聘登记表
        #         "end_time": getTime().get_Daytime(days=10),
        #         "plan_type": [self._get_comboBox(data=_comboBox_data['ZPFL'], value='value')[0]],  # 招聘分类
        #         "start_time": getTime().get_Daytime(),
        #         "plan_show_type": self._get_comboBox(data=_comboBox_data['ZPBQ'], value='value'),  # 发布平台
        #         "value": "",
        #         "require_id": require_id[0]
        #     },
        #     "a": {
        #         "source": "1284"
        #     },
        #     "v": self.session_id
        # }
        # push_detail_url = self.hrmapi + "/hrm/code/query/detail"  # 判断编码生成规则
        # push_detail_adta = {"a": {"source": "1284"}, "n": {"code_type": "578"}, "v": self.session_id}
        # response_push_detail = send_requests(method='post', url=push_detail_url, data=json.dumps(push_detail_adta))
        # if getJson(response_push_detail, 'rule_type')[0] == '774':
        #     require_push_data['n']['plan_id'] = getTime.now_time.strftime("%Y%m%d%H%M%S")
        #
        # require_push_url = self.hrmapi + "/hrm/recruit/require/info/push"
        # response_require_push = send_requests(method='post', url=require_push_url, data=json.dumps(require_push_data))
        # log.info('发布用人需求结果--->{0}'.format(getJson(response_require_push, 'message')[0]))

        log.info('''添加招聘计划''')
        plan_name = "招聘计划名称_" + self.faker.text(max_nb_chars=10)
        plan_add_url = self.hrmapi + "/hrm/recruit/plan/add"
        plan_add_data = {
            "a": {
                "source": "1284"
            },
            "n": {
                "plan_name": plan_name,
                "year": "2021",
                "recruitment_require_collect_type": "828",
                "recruitment_require_collect_start_time": getTime().get_Daytime(1),  # getTime().get_Daytime(1),
                "recruitment_require_collect_end_time": ""
            },
            "v": self.session_id
        }
        query_detail_url = self.hrmapi + '/hrm/code/query/detail'  # 判断招聘计划编号是否需要填写
        query_detail_data = {"a": {"source": "1284"}, "n": {"code_type": "578"}, "v": self.session_id}
        response_query_detail = send_requests(method='post', url=query_detail_url, data=json.dumps(query_detail_data))
        if getJson(response_query_detail, 'rule_type')[0] == "774":
            plan_add_data['n']['plan_id'] = getTime.now_time.strftime("%Y%m%d%H%M%S")
        response_plan_add = send_requests(method='post', url=plan_add_url, data=json.dumps(plan_add_data))
        self.is_true(response_plan_add, '添加招聘计划')

        log.info('''发布招聘计划''')
        plan_query_url = self.hrmapi + "/hrm/recruit/plan/query"
        plan_query_data = {
            "a": {
                "source": "1284"
            },
            "n": {
                "plan_status": "",
                "plan_year": "",
                "plan_name": plan_name
            },
            "v": self.session_id,
            "f": {
                "indexpage": 1,
                "repaging": "1",
                "pagesize": 10
            }
        }
        response_plan_query = send_requests(method='post', url=plan_query_url, data=json.dumps(plan_query_data))
        self.is_true(response_plan_query, '招聘计划查询')

        if getJson(response_plan_query, 'plan_name'):
            plan_id = getJson(response_plan_query, 'plan_id')[0]
            template_list_url = self.gcgateway + "/unify_users/module/template/info/query/list"  # 获取应聘登记表
            template_list_data = {"a": {"source": "1284"}, "n": {"template_type": "297"}, "v": self.session_id}
            response_template_list = send_requests(method='post', url=template_list_url, data=json.dumps(template_list_data))
            self.is_true(response_template_list, '获取应聘登记表')
            templates_id = random.choice(getJson(response_template_list, 'template_id'))

            log.info('''关联用人需求''')
            position_query_url = self.hrmapi + "/hrm/recruit/plan/position/simple/filter/query"
            position_query_data = {
                "a": {
                    "source": "1284"
                },
                "n": {
                    "plan_id": plan_id,
                    "recruitment_require_position_name": position_name
                },
                "v": self.session_id,
                "f": {
                    "indexpage": 1,
                    "repaging": "1",
                    "pagesize": 10
                }
            }
            response_position_query = send_requests(method='post', url=position_query_url, data=json.dumps(position_query_data))
            if getJson(response_position_query, 'require_id') is False:
                position_query_data['n']['recruitment_require_position_name'] = ''
                response_position_query = send_requests(method='post', url=position_query_url, data=json.dumps(position_query_data))
            self.is_true(response_position_query, '查询用人需求')
            require_id = getJson(response_position_query, 'require_id')[0]

            position_add_url = self.hrmapi + "/hrm/recruit/plan/position/add"
            position_add_data = {"a": {"source": "1284"}, "n": {"plan_id": plan_id, "require_infos": [{"require_id": require_id}]},
                                 "v": self.session_id}
            response_position_add = send_requests(method='post', url=position_add_url, data=json.dumps(position_add_data))
            self.is_true(response_position_add, '关联用人需求')

            recruit_limit_url = self.hrmapi + '/hrm/recruit/plan/position/query/limit'
            recruit_limit_data = {"a": {"source": "1284"}, "n": {"plan_id": plan_id}, "v": self.session_id}
            response_recruit_limit = send_requests(method='post', url=recruit_limit_url, data=json.dumps(recruit_limit_data))
            self.is_true(response_recruit_limit, '查询招聘计划发布信息')

            simple_content = "公告内容备注_" + self.faker.text(max_nb_chars=200)
            recruit_plan_push_url = self.hrmapi + '/hrm/recruit/plan/push'
            recruit_plan_push_data = {
                "a": {
                    "source": "1284"
                },
                "n": {
                    "is_repeat_push": "0",
                    "announcement_content": simple_content,
                    "simple_content": simple_content,
                    "demand_agency": "",  # 需求机构
                    "push_time": getTime().get_Daytime(0).split(" ")[0],
                    "end_time": getTime().get_Daytime(30),
                    "job_form_id": templates_id,
                    "plan_column": self._get_comboBox(data=_comboBox_data['PUSH_TYPE'], value='value'),  # 发布栏目
                    "plan_id": plan_id,
                    "plan_name": plan_name,
                    "plan_type": self._get_comboBox(data=_comboBox_data['ZPFL'], value='value'),  # 招聘分类,
                    "recruitment_file_id": templates_id,
                    "plan_show_type": self._get_comboBox(data=_comboBox_data['ZPBQ'], value='value'),  # 发布平台,
                    "plan_out_name": "公告标题_" + plan_name
                },
                "v": self.session_id,
                "f": {
                    "indexpage": "1",
                    "repaging": "1",
                    "pagesize": "10"
                }
            }
            if self._get_comboBox(data=_comboBox_data['XQJG'], value='value'):
                recruit_plan_push_data['n']['demand_agency'] = random.choice(self._get_comboBox(data=_comboBox_data['XQJG'], value='value'))
            response_recruit_plan_push = send_requests(method='post', url=recruit_plan_push_url, data=json.dumps(recruit_plan_push_data))
            self.is_true(response_recruit_plan_push, '发布招聘计划')

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

    def is_true(self, obj, msg):
        if self.assertTrue(getJson(obj, 'message')[0], '成功'):
            log.info(msg + "成功")
        else:
            log.error('{0}失败,失败信息--->{1}'.format(msg, obj))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase('test_run', 'test', 'GC0200074603961341'))
    unittest.TextTestRunner(verbosity=2).run(suite)
