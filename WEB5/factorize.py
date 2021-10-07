import copy
import time
import multiprocessing


number = [128, 255, 99999, 10651060]

def factorize(number):
    start = time.perf_counter()
    final_list = []
    for element in number:
        result = []
        for prob in range(1, element + 1):
            if element % prob == 0:
                result.append(prob)
        final_list.append(copy.deepcopy(result))
    finish = time.perf_counter()
    print(f"The process took {finish - start} sec")
    return final_list
    raise NotImplementedError()

# def Process(number):
#     print("Process started...")
#     results = []
#     for i in number:
#         p = multiprocessing.Process()
#         results.append(p.start())
#         p.join()
#     return results

def Pool(number):
    print("Pool started...")
    with multiprocessing.Pool() as Pool:
        result = Pool.map(factorize, (number,))
    return result[0]


if __name__ == '__main__':
    print(factorize(number))
    # print(Process(number))
    print(Pool(number))
    a, b, c, d  = Pool(number)
    print(a)
    print(b)
    print(c)
    print(d)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
