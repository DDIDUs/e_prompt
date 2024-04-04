from data import *
from submit import *

import argparse
from tqdm import tqdm

def test(args):
    
    platform = args.platform
    num_samples = args.num_sample
    
    test_data = load_test_data(platform, num_samples)
    
    prompt_path, sub_result_path = init_logpath("./result", platform)
    
    for problem in tqdm(test_data):
        p_disc, code_snippet, p_info = problem
        
        prompt = get_error_promt(p_disc, code_snippet)
        gen_code = get_code_from_prompt(prompt, prompt_path, p_info)
        
        result = submit(gen_code, p_info, platform, sub_result_path)
        print(result)
    
    return 0
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="info")
    parser.add_argument('-platform', type=str, default="leetcode", choices=['leetcode', 'grepp'], help="Problem platform")
    parser.add_argument('-num_sample', type=int, default=30, help="The number of problem")
    config = parser.parse_args()
    
    test(config)