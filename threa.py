import threading

start,end = 0, 10000

def cal_sum(start, end):
    result = sum(range(start, end+1))
    print(result)

begin, finish = 10000,20000

def total(begin,finish):
    total = sum(range(begin, finish+1))
    print(total)

thread1 = threading.Thread(target=cal_sum,args=(start, end))
thread2 = threading.Thread(target= total, args=(begin, finish))
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()