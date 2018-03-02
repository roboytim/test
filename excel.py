# -*- coding: utf-8 -*-
#导入Excel读取模块
import xlrd
#导入Excel写入模块
import xlwt
'''
import sys
if __name__=='__main__':
    print ()
add = []
for a in range(1,len(sys.argv)):
	add.append(str(sys.argv[a]))
path = add[0]
'''
#Excel文件路径
path = r'/Users/roboytim/Desktop/work/exceltest/test.nmon.xlsx'
#梯度数量
num = 10
#实例化工作表，打开制定excel文件
book = xlrd.open_workbook(path)
#打印改文件的所有工作表名称
print (book.sheet_names())
#通过工作表索引获取sheet对象
sheetbyindex = book.sheet_by_index(1)
print (sheetbyindex.name)
#通过工作表名称获取sheet对象
CPUsheet = book.sheet_by_name('CPU_ALL')
MEMsheet = book.sheet_by_name('MEM')
#打印工作表名称，工作表行数，工作表列数
print ('工作表名称：%s,工作表行数：%d，工作表列数：%d' % (CPUsheet.name,CPUsheet.nrows,CPUsheet.ncols))
#计算每个梯度包含的行数
rownum = int((CPUsheet.nrows-3)/num)
#rownum = (CPUsheet.nrows-3)/num
print (rownum)
#定义一个名称为CPU的数组
CPU = []
MEM = []
#打印输出工作表最后一列的数据
for j in range(num):
    CPU_sum = 0
    MEM_sum = 0
    for i in range(rownum):
        #print (CPUsheet.cell_value(i+1,CPUsheet.ncols-1))
        CPU_sum = CPU_sum + CPUsheet.cell_value(rownum * j + i + 1,CPUsheet.ncols-1)
        # 打印内存使用率 公式为：(memtotal-memfree-cached-buffers)/memtotal*100
        MEM_sum = MEM_sum + (MEMsheet.cell_value(rownum * j + i + 1, 1) - MEMsheet.cell_value(rownum * j + i + 1, 5) - MEMsheet.cell_value(rownum * j + i + 1,10) - MEMsheet.cell_value(rownum * j + i + 1, 13)) / MEMsheet.cell_value(rownum * j + i + 1, 1) * 100
    CPU.append(str(CPU_sum))
    MEM.append(str(MEM_sum))

for i in range(len(CPU)):
    print (i,CPU[i])
    print (i,MEM[i])