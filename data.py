import os
import json
import time
import pickle
import subprocess

from tqdm import tqdm
from random import shuffle
from collections import OrderedDict

def extract_class_code(result):
    code = ""
    for line in result.split("\n"):
        if "class" not in line and code == "":
            continue
        if "    " in line or line.startswith("class"):
            code += line + "\n"
    if code == "":
        return -1
    else:
        return code
    
def get_leetcode_problem_info(prob_num, plat, diff):
    
    result = subprocess.run("leetcode show {} -g -x -l python3".format(prob_num), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.decode("utf-8")
    time.sleep(10)
    tmp = result.split("\n")
    
    p_name = tmp[0][7:-2]

    for t in tmp:
        if "* Source Code:       " in t:
            file_name = t[t.find(str(prob_num)):t.find(".py")+3]
            break
        
    prob_disc = ""
    code_snippet = ""
    
    with open ("./" + file_name, "r") as f:
        lines = f.readlines()

        disc_flag = False
        code_flag = False
        
        for line in lines:
            if "# Testcase Example:" in line:
                disc_flag = True
                continue
            elif "# @lc code=start" in line:
                code_flag = True
                disc_flag = False
                continue
            elif "# @lc code=end" in line:
                break
            
            if disc_flag:
                prob_disc += line[1:]
            if code_flag:
                code_snippet += line
                
    os.remove("./" + file_name)
                
    return [prob_disc, code_snippet, [diff, p_name, plat]]

def get_grepp_problem_info():
    return 0
    
def select_leetcode_problems(p_list, n_sample, diff):
    s_list = []
    for n in range(n_sample):
        line = p_list[n]
        t = line.find("]")
        p_num = line[t-4:t]
        s_list.append([p_num, diff])
    return s_list
    
def select_grepp_problems():
    return 0

def load_test_data(plat, n_sample):
    if os.path.exists("./prob.pkl"):
        with open("./result/problem.pkl","wb") as f:
            test_data = pickle.load(f)
        shuffle(test_data)
        return test_data
    
    p_dlist= []
    diff = ["h", "m", "e"]
    
    test_data = []
    
    if plat == "leetcode":
        for d in diff:
            result = subprocess.run("leetcode list -q {}L -s".format(d), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.decode("utf-8")
            time.sleep(10)
            p_dlist.append(select_leetcode_problems(result.split("\n"), n_sample, d))

        for p_list in p_dlist:
            for prob in tqdm(p_list):
                p_num, dif = prob
                test_data.append(get_leetcode_problem_info(p_num, plat, dif))
    
    shuffle(test_data)
    
    with open("./result/problem.pkl","wb") as f:
        pickle.dump(test_data, f)

    return test_data                                                     # prob_desc, code, p_info
    
def save_result(log_path, problem_info, data):
    p_diff, p_name, platform = problem_info
    
    result_path = log_path + "/{}_{}.json".format(platform, p_diff)
    
    f_data = OrderedDict()
    f_data["difficulty"] = p_diff
    f_data["problem_name"] = p_name
    f_data["data"] = data                                         # type(data) == dict

    if os.path.exists(result_path):
        with open(result_path, 'r') as file:
            file_data = json.load(file, object_pairs_hook=OrderedDict)
        file_data["result"].append(f_data)
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(file_data, f, ensure_ascii=False, indent="\t")
    else:
        root = OrderedDict()
        tmp = []
        tmp.append(f_data)
        root["result"] = tmp
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(root, f, ensure_ascii=False, indent="\t")
        
def init_logpath(default_path, platform):
    
    prompt_path = default_path + "/gen_prompt_{}".format(platform)
    sub_result_path = default_path + "/submit_result_{}".format(platform)
    
    if not os.path.exists(default_path):
        os.mkdir(default_path)
        os.mkdir(prompt_path)
        os.mkdir(sub_result_path)
    else:
        if not os.path.exists(prompt_path):
            os.mkdir(prompt_path)
        elif not os.path.exists(sub_result_path):
            os.mkdir(sub_result_path)
            
    return prompt_path, sub_result_path
