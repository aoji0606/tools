import multiprocessing
import traceback


def run(thread_id, data):
    for item in data:
        try:
            # do ***
            print(thread_id, item)
        except:
            traceback.print_exc()
    

data = list(range(100))
data_size = len(data)
thread_num = 10
chunk_size = data_size // thread_num
processes = []
for i in range(thread_num):
    start_index = i * chunk_size
    end_index = start_index + chunk_size if i < thread_num - 1 else data_size
    chunk = data[start_index:end_index]
    processes.append(multiprocessing.Process(target=run, args=(i, chunk)))
    print(f"processes:{i} size:{len(chunk)}")
for i in processes:
    i.start()
for i in processes:
    i.join()
