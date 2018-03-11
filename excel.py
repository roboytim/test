# -*- coding: utf-8 -*-
#导入Excel读取模块
import xlrd
#导入Excel写入模块
import xlwt
#Excel文件路径
path = r'/Users/roboytim/Desktop/work/exceltest/test.nmon.xlsx'
#梯度数量
num = 2
#实例化工作表，打开制定excel文件
book = xlrd.open_workbook(path)
#打印改文件的所有工作表名称
#print (book.sheet_names())
#通过工作表索引获取sheet对象
sheetbyindex = book.sheet_by_index(1)
#print (sheetbyindex.name)
#获取解析后的系统类型Linux||AIX
for i in range(book.sheet_by_name('BBBP').nrows-1):
    #print (type(book.sheet_by_name('BBBP').cell_value(i,1)))
    #if "Linux" in book.sheet_by_name('BBBP').cell_value(i,1):
    if book.sheet_by_name('BBBP').cell_value(i,1).find("Linux") == -1:
        OS = 'Linux'
    else:
        OS = 'AIX'
#print (OS)
#通过工作表名称获取sheet对象
CPUsheet = book.sheet_by_name('CPU_ALL')
#如果系统为linux，内存计算使用MEM工作表，如果为AIX，使用MEMNEW工作表
if OS == 'Linux':
    MEMsheet = book.sheet_by_name('MEM')
else:
    MEMsheet = book.sheet_by_name('MEMNEW')
DISKsheet = book.sheet_by_name('DISKBUSY')
#print (DISKsheet.nrows,DISKsheet.ncols)
#获取DISKBUSY工作表中有数据的列数
DISKend=0
for j in range(DISKsheet.ncols):
    #print (DISKsheet.cell_value(0,j))
    if DISKsheet.cell_value(0,j)=='':
        break
    DISKend=DISKend+1
DISKindex = DISKend-1
#获取DISKBUSY中总和最大的列
DISKmax=0
for i in range(DISKindex-1):
    DISKtotal = 0
    for j in range(DISKsheet.nrows-6):
        DISKtotal = DISKtotal + DISKsheet.cell_value(j+1,i+1)
        if DISKtotal > DISKmax:
            DISKmax = DISKtotal
            DISKclos = i+1
#打印工作表名称，工作表行数，工作表列数
#print ('工作表名称：%s,工作表行数：%d，工作表列数：%d' % (CPUsheet.name,CPUsheet.nrows,CPUsheet.ncols))
#计算每个梯度包含的行数
rownum = int((CPUsheet.nrows-3)/num)
#rownum = (CPUsheet.nrows-3)/num
#print (rownum)
#定义一个名称为CPU的数组
CPU = []
MEM = []
DISK = []
#打印输出工作表最后一列的数据
for j in range(num):
    CPU_sum = 0
    MEM_sum = 0
    DISK_sum = 0
    for i in range(rownum):
        #print (CPUsheet.cell_value(i+1,CPUsheet.ncols-1))
        CPU_sum = CPU_sum + CPUsheet.cell_value(rownum * j + i + 1,CPUsheet.ncols-2)
        # 打印内存使用率 公式为：(memtotal-memfree-cached-buffers)/memtotal*100
        MEM_sum = MEM_sum + (MEMsheet.cell_value(rownum * j + i + 1, 1) - MEMsheet.cell_value(rownum * j + i + 1, 5) - MEMsheet.cell_value(rownum * j + i + 1,10) - MEMsheet.cell_value(rownum * j + i + 1, 13)) / MEMsheet.cell_value(rownum * j + i + 1, 1) * 100
        DISK_sum = DISK_sum + DISKsheet.cell_value(rownum * j + i + 1,DISKclos)
    CPU.append(CPU_sum/rownum)
    MEM.append(MEM_sum/rownum)
    DISK.append(DISK_sum/rownum)
print("梯度\tCPU\tMEM\tDISKBUSY")
for i in range(len(CPU)):
    #print (type(CPU[i]))
    print ("%d\t%.2f\t%.2f\t%.2f" % (i,CPU[i],MEM[i],DISK[i]))