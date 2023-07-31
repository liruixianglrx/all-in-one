import os
from multiprocessing import Process, Pool

from eco_baseline.parser.parser import VerilogParser

passed = True

dataset_path = "./dataset/"
contest_list = ["ICCAD2017", "ICCAD2021"]

def parse_file(case_path, test_file):
    global passed

    try:
        print(f"Parsing: {case_path}/{test_file}")
        verilog_parser = VerilogParser()
        verilog_parser.read_file(os.path.join(case_path, test_file))

    except:
        print(f"Parse Error at: {case_path}/{test_file}")
        passed = False


if __name__ == "__main__":
    pool = Pool(6)

    for contest in contest_list:
        test_path = os.path.join(dataset_path, contest)
        test_cases = os.listdir(test_path)

        for test_case in test_cases:
            case_path = os.path.join(test_path, test_case)
            for test_file in os.listdir(case_path):
                if test_file.endswith(".v"):
                    pool.apply_async(func=parse_file, args=(case_path, test_file))
                    # parse_file(case_path, test_file)

    pool.close()
    pool.join()

    if passed:
        print("Test passed!")
    else:
        print("Test failed.")
