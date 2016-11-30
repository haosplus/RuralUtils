#encoding: utf-8
'''
            用来监控app的的内存和cpu使用状况；
            指定android设备的serial和需要监控的app包名
            执行：monitor_app.py --package xxx
    @author: haos
'''
import time
import os
import platform
from optparse import OptionParser


cpu_data = []
memory_data = []

find_key = None
if platform.system() == "Linux":
    find_key = "grep"
else:
    find_key = "findstr"
    

def get_argument():
    parser = OptionParser()
    parser.add_option('--serial', action='store', dest='serial_num', help='device serial number, adb devices')
    parser.add_option('--package', action='store', dest='package', help='the package that monitor app')
    (options, args) = parser.parse_args()
    if options.package is None:
        print parser.format_help()
        print parser.exit(msg="Please point the package name ")
    return options, args
     

def monitor():
    (options, args) = get_argument()
    global package_name
    package_name = options.package
    if options.serial_num is None:
        cmd = "adb shell top -d 1 -n 1 | %s %s"%(find_key, package_name);
    else:
        cmd = "adb -s %s shell top -d 1 -n 1 | %s %s"%(options.serial_num, find_key, package_name)    
    print cmd
    while True:
        content = getoutput(cmd)
        a =  content.split("\n")
        power_cpu = 0
        power_mem = 0
        for line in a:
            power_array = line.strip().split()
            power_cpu += int(power_array[2].split("%")[0])
            power_mem += int(power_array[6].split("K")[0])/1024
        cpu_data.append(power_cpu)
        memory_data.append(power_mem)
        print "CPU: %s  Memory: %sM"%(str(power_cpu)+"%", power_mem)


def getoutput(cmd):
    pipe = os.popen(cmd, "r")
    text = pipe.read()
    sts = pipe.close()
    if sts is None: sts = 0
    if text[-1:] == '\n': text = text[:-1]
    return text

def save_data():
    script_file = os.path.abspath(__file__)
    parent_dir = os.path.split(script_file)[0]
    from xlwt import Workbook
    w = Workbook()    
    ws = w.add_sheet("power")  
    ws.write(0, 2, package_name)  
    ws.write(0, 0, "CPU(%)") 
    cpu_count = len(cpu_data)
    for i in range(cpu_count):
        ws.write(i+1, 0, cpu_data[i])
    ws.write(0, 1, "Memory(M)") 
    mem_count = len(memory_data)
    for i in range(mem_count):
        ws.write(i+1, 1, memory_data[i])
    w.save(os.path.join(parent_dir, time.strftime("%Y%m%d%H%M%S")+".xls"))
    

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        save_data()