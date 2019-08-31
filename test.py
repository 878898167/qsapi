#-*-coding:utf-8-*-
import ctypes #引入ctypes调用dll的支持库 
import json
import sys
from ctypes import c_char_p 
from ctypes import c_int 
from ctypes import c_int 
 
dll = ctypes.WinDLL("qsapi.dll")#加载DLL
 
#以下为定义参数类型
dll.readid.argtypes = [c_char_p]
dll.signin.argtypes = [c_char_p,c_char_p,c_char_p]
 
dll.transaction.argtypes = [c_char_p,c_char_p,c_int,c_char_p,c_char_p,c_char_p]
dll.query.argtypes = [c_char_p,c_char_p,ctypes.c_int]
 
#以下为定义返回值类型
dll.readid.restype = ctypes.c_char_p
dll.signin.restype = ctypes.c_char_p
dll.transaction.restype = ctypes.c_char_p
dll.query.restype = ctypes.c_char_p
 
qsmc = ctypes.create_string_buffer(bytes("东莞证券","gb2312"))#券商名称改成自己的
qsid = ctypes.string_at(dll.readid(qsmc))#readid 参数1 券商名称 返回券商id
if qsid == b"":
    print("不支持的券商")
    sys.exit(0)
 
qszh = ctypes.create_string_buffer(b"123456789")#账号改成自己的
qsmm = ctypes.create_string_buffer(b"123456")#密码改成自己的
str = ctypes.string_at(dll.signin(qsid,qszh,qsmm)).decode('gb2312')#signin的参数 1.券商id 2.账号 3.密码 返回登录结果
 
Title = json.loads(str)['Title']
if Title != "登录成功":
    print(str)
    sys.exit(0)
print(str)#打印登录结果
 
str = ctypes.string_at(dll.query(qsid,qszh,0)).decode('gb2312')#query函数是查询   参数4是查询类型 0查持仓及资产 1查成交 2查委托
print(str)#打印查询结果
 
gpdm = ctypes.create_string_buffer(b"000001")#股票代码
mmjg = ctypes.create_string_buffer(b"13.50")#买卖价格
mmsl = ctypes.create_string_buffer(b"100")#买卖数量
#下面是下单函数
str = ctypes.string_at(dll.transaction(qsid, qszh, 0, gpdm, mmjg, mmsl)).decode('gb2312')#参数4 0为买 1为卖
print(str)#打印下单结果
