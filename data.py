import os
import json
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
    
def get_leetcode_problem_info():
    return 0

def get_grepp_problem_info():
    return 0
    
def select_leetcode_problems():
    return 0
    
def select_grepp_problems():
    return 0

def load_test_data(plat, n_sample):
    return 0
    
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
