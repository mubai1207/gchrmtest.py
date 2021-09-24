# coding=utf-8
# import torch._utils
# try:
#     torch._utils._rebuild_tensor_v2
# except AttributeError:
#     def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
#         tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
#         tensor.requires_grad = requires_grad
#         tensor._backward_hooks = backward_hooks
#         return tensor
#     torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2


#
#
# data = {"statusCode": 0, "message": "操作成功",
#         "data": {"id": 2002101258526037, "schoolCode": "yq025", "schoolName": "杭州亿云网络科技有限公司", "qrcodePayType": 0, "account": "12222202001", "mobilePhone": "122****2001", "sex": 1,
#                  "realNameStatus": 0, "regiserTime": "2020-02-10 12:58:52", "nickName": "122****2001", "bindCardStatus": 0, "lastLogin": "2020-09-04 16:09:21",
#                  "headImg": "http://fastdfs.lsmart.wanguser_default_head_img", "deviceId": "357612083023375,357613083023373", "testAccount": 1, "payUser": "TEST385558715311595",
#                  "token": "4358858da9834447975406959a47260d", "realUserName": "苏娜", "realIdentityNo": "**************8325", "joinNewactivityStatus": 1, "isNew": 1,
#                  "createStatus": 0, "eacctStatus": 0, "schoolClasses": 1, "schoolNature": 1, "platform": "YUNMA_APP", "realNameTime": "2020-02-14 13:50:05",
#                  "uuToken": "YT3tLvFFuVPH/ZQQugmVbCeIHNI/ewM4NvY4dC7ZXjf+SP2jiwrmzKL+1zt4IQ1adY6gd1DQaZYJWGhF9+qklQ==",
#                  "qrcodePublicKey": "************************************************************************************************************************************************************************************************************************",
#                  "qrcodePrivateKey": "MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBALybEsyEUJ5au5w02/FGPz5+sWIVXHbgnkagM9Bx4IQ29qJLW7REV73s3WRSPsbgT61r/cjYSjJq+Cct2Xv2MDCLKXUfEap2XHgbxuLZCpV9rBlCVYGy6l1GXFUBxSl24S7KrY+nTOxJtp2hjH1k0hlju6/EIh/8TCU4ZcKHzoU5AgMBAAECgYEAt2iKAG5PQ57yQHY6yEdKq0hi0QH61/OYlw+lM3f6IDie4LYtqICpXp1fsfY07AsoEHoq4kxK4vqY9OimTODcfDuEMgx/+g3twgjWU0wkT+Qt/v5LHYd00yHR6MgDAEgHYRiHIcH5UorF934t6q9vFh7MOjzwiR4E68FcNjhvOfECQQDvGh5Xs/IGLWq9JT8yAH2O/etwoKBmI4YhwzhkixeUe2iL/Z7tQTVcfALhJ+Q7Xo/SlKwzwCyiFiAuNHjpqntdAkEAye9dyAt7B0qrH1Da7UzgyFb1rptKCre37uZ1XhYY9T37jqyvffwou43ZbSdI/dZAA6oQibD/pVWpXYjzH6SvjQJBAJ5mhj2B98/B3NnLyC7/Bi9p5sUplLm1xRGu/DgXsZprm1pKvjPdpFVNzraNL/Vo8w0F84MhSDBlShJyLrxWdf0CQQCbinSCEdXB2BHXHUCEaCL8LX8v7w0pFDnpGjptLjgrLoMFcp36PLBjRu+i1A+09cJ5EBWM+XjwsPqzwTkDtqZBAkAC/Pij+EQ15IleEUv35vAXV3JJf5KmI4BSQTu/kchbGVFiZ2F7Jkbg8hqBZxf2z6eOSg0mcrLXzzhaS755VPlc",
#                  "bindCardRate": 2, "points": 745, "schoolIdentityType": 2, "alumniFlag": 0,
#                  "extJson": "{\"openBanks\":[{\"orgCode\":\"190201\",\"orgName\":\"科创支行\"},{\"orgCode\":\"n001\",\"orgName\":\"农行测试网点\"}]}"}, "success": True}
#
# from jsonpath_rw import jsonpath, parse
#
# # jsonpath_expr = parse('data[*].total')
# # data = {'foo': [{'baz': 'news'}, {'baz': 'music'}]}
# # print([match.value for match in jsonpath_expr.find(data)][0])
#
#
import datetime

import jsonpath

#
new_data = {'message': '操作成功', 'rows': [
    {'areaCode': '1', 'areaName': '测试校区', 'buildingCode': '01', 'buildingName': '1号楼', 'floorCode': '1001', 'floorName': '1层', 'roomCode': '101', 'roomName': '101房间'},
    {'areaCode': '1', 'areaName': '测试校区', 'buildingCode': '01', 'buildingName': '1号楼', 'floorCode': '1001', 'floorName': '1层', 'roomCode': '101', 'roomName': '101房间'}],
            'statusCode': 0, 'total': 2}

d = {}
# print(d)
message = ['areaCode', 'buildingCode', 'floorCode', 'roomCode']
l=[]
for i in message:
    # print(i)
    # print(jsonpath.jsonpath(new_data,"$..buildingName"))
    value = jsonpath.jsonpath(new_data, "$..%s" % i)[0]
    # print(key)
    l.append(value)
print(message,l)
print(dict(zip(message,l)))
# print(d)
# # new_data.update({
# #     "id": jsonpath.jsonpath(data, "$..id")[0],
# #     "token": jsonpath.jsonpath(data, "$..token")[0],
# # })
#
#
# #
# # jsonpath_expr = parse('data[*].id')
# #
# # print([match.value for match in jsonpath_expr.find(data)])
title = ['name','age']
item = ['xiaowang','15']
itemZip = zip(title,item)
print(dict(itemZip))


print(datetime.datetime.now())