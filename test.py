#-*-coding:utf-8-*-
import ctypes #引入python调用dll的支持库 
import json
import sys

from ctypes import c_char_p,c_int,create_string_buffer,string_at


dll = ctypes.WinDLL("qsapi.dll")#加载DLL

#以下为定义参数类型
dll.readid.argtypes = [c_char_p]
dll.signin.argtypes = [c_char_p,c_char_p,c_char_p]
dll.transaction.argtypes = [c_char_p,c_char_p,c_int,c_char_p,c_char_p,c_char_p]
dll.query.argtypes = [c_char_p,c_char_p,c_int]
dll.quotation.argtypes = [c_char_p]
dll.revoke.argtypes = [c_char_p,c_char_p,c_char_p]

#以下为定义返回值类型
dll.readid.restype = c_char_p
dll.signin.restype = c_char_p
dll.transaction.restype = c_char_p
dll.query.restype = c_char_p
dll.quotation.restype = c_char_p
dll.revoke.restype = c_char_p

#readid 取券商id————————————————————————————————————————————————————————————————
qsmc = create_string_buffer(bytes("东莞证券","gb2312"))#券商名称改成自己的
qsid = string_at(dll.readid(qsmc))#readid 参数1 券商名称 返回券商id
if qsid == b"":
	print("不支持的券商")
	sys.exit(0)

#signin 登录—————————————————————————————————————————————————————————————————————
qszh = create_string_buffer(b"123456789")#账号改成自己的
qsmm = create_string_buffer(b"123456")#密码改成自己的
str = string_at(dll.signin(qsid,qszh,qsmm)).decode('gb2312')#signin的参数 1.券商id 2.账号 3.密码 返回登录结果
Title = json.loads(str)['Title']
if Title != "登录成功":
	print(str)
	sys.exit(0)
print(str)#打印登录结果

#query 查询———————————————————————————————————————————————————————————————————————
str = ctypes.string_at(dll.query(qsid,qszh,0)).decode('gb2312')#query函数是查询   参数4是查询类型 0查持仓及资产 1查成交 2查委托
print(str)#打印查询结果

#transaction 下单————————————————————————————————————————————————————————————————————
gpdm = create_string_buffer(b"000001")#股票代码
mmjg = create_string_buffer(b"13.50")#买卖价格
mmsl = create_string_buffer(b"100")#买卖数量
str = string_at(dll.transaction(qsid, qszh, 0, gpdm, mmjg, mmsl)).decode('gb2312')#参数4 0为买 1为卖
print(str)#打印下单结果

#quotation 股票行情——调用的是新浪接口——————————————————————————————————————————————————
str = string_at(dll.quotation(gpdm)).decode('gb2312')#参数传六位股票代码
print(str)#打印五档行情
#返回数据可参考https://blog.csdn.net/fangquan1980/article/details/80006762

#revoke 撤单——————————————————————————————————————————————————————————————————————————
htdm = create_string_buffer(b"13")#合同单号可在查委托里看到 可能是纯数字 也可能字母开头  各大券商有所不同
str = string_at(dll.revoke(qsid,qszh,htdm)).decode('gb2312')
print(str)#打印撤单结果

#暂时只支持以上功能     后期会考虑加入打新
#使用出现问题可以来群里咨询
#QQ群724065449
