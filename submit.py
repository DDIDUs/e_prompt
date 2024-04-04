import os
import time
import openai
import subprocess

from data import *

openai.api_key = ""

init_prompt = '''
For the problem below, configure prompts to help LLM understand the problem in detail and write code.
There are many ways to organize prompts, and you can add any elements you think are necessary.

Problem
‘’’
{}
‘’’

Code template
‘’’
{}
‘’’

Requirement
	- Generate only prompts.
	- Consider what errors might occur when running the generated code.
	- The generated prompt should include a description of the problem, a description of any errors that might occur when running the code, and a code template, and examples
'''

def gpt_4_submit(instruction):
    messages = [
            {"role": "user", "content": f"{instruction}"},
        ]

    response = openai.ChatCompletion.create(    
        model="gpt-4-turbo",
        messages=messages
    )
    
    return response["choices"][0]["message"]["content"], response["usage"]["total_tokens"]

def get_error_promt(prob_desc, code_snippet):
    prompt = init_prompt.format(prob_desc, code_snippet)
    error_prompt, _ = gpt_4_submit(prompt)
    
    return error_prompt
    
def get_code_from_prompt(prompt, log_path, p_info, max_retries=5, delay=60):
    retries = 0
    
    while retries < max_retries:
        try:
            code, token_count = gpt_4_submit(prompt)
            class_code = extract_class_code(code)
            if token_count >= 4000:
                time.sleep(60)
            elif class_code.startswith("class"):
                class_code.replace("\n", "\\n")
                break
            else:
                time.sleep(30)
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {delay} seconds.")
            retries += 1
            time.sleep(delay)
            
    data = {'error_prompt' : prompt, 'generated_code' : class_code}
    
    save_result(log_path, p_info, data)
    
    return class_code

def submit(class_code, p_info, platform, sub_result_path):
    if platform == "leetcode":
        result = leetcode_submit(class_code, p_info, sub_result_path)
    else:
        result = grepp_submit(class_code, p_info, sub_result_path)
    
    save_result(sub_result_path, p_info, result)
    return result
    
def leetcode_submit(class_code, p_info, sub_result_path):   
    _, p_name, _ = p_info
    
    with open("./{}.py".format(p_name), "w") as f:
        f.write(class_code)
    
    result = subprocess.run("leetcode submit {}".format(p_name), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.decode("utf-8")
    
    os.remove("./{}.py".format(p_name))
    
    data = {'submit_reult' : result}
    save_result(sub_result_path, p_info, data)
    
    time.sleep(10)
    
    return data

def grepp_submit(class_code, p_info, sub_result_path):
    result = "asdf"
    time.sleep(10)
    return result
