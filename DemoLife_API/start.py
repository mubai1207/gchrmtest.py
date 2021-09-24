# _*_ coding:utf-8 _*_


from DemoLife_API.testcase.life_makerOder import maker_main
from DemoLife_API.testcase.life_mealOut import business_main
from DemoLife_API.testcase.life_takeMeal import take_main
from DemoLife_API.testcase.life_inSorting import sorting_main
from DemoLife_API.testcase.life_doCheck import check_main
from DemoLife_API.testcase.life_beDeliveredIn import deliver_main
from DemoLife_API.testcase.life_deliveryOrder import OrderList_main


def start():
    login_PATH = 'gray'  # （默认lsmart，可选择lsmart/gray/pro）
    school_code = '12061'  # yunmalife
    num = 1
    """取配置文件中登录手机号"""
    maker_main(login_PATH=login_PATH, school_code=school_code, num=1)  # 创建订单
    business_main(login_PATH=login_PATH, user_pwd='a111112')  # 商家出餐
    take_main(login_PATH=login_PATH, user_pwd='a111112')  # 取餐员取餐
    sorting_main(login_PATH=login_PATH, user_pwd='a111112')  # 取餐员送达分拣中心（单个送达）
    check_order_data = OrderList_main(login_PATH=login_PATH, user_pwd='a111111', statue=60)
    check_main(login_PATH=login_PATH, user_pwd='a111111')  # 扫码核验
    deliver_order_data = OrderList_main(login_PATH=login_PATH, user_pwd='a111111', statue=70)
    deliver_main(login_PATH=login_PATH, user_pwd='a111111')  # 扫码送达


if __name__ == '__main__':
    start()
