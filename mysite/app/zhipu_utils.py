import requests
from zhipuai import ZhipuAI
import re
import json

ZHIPU_AI_KEY = 'e8f5bd8291fd2c8f8d95e4e2783c5535.A2nRLLgFusbcY37y'

def code_explain(code):
    """
    代码解释
    """
    prompt = f'''
你是一名精通`C++`、`C语言`代码的程序员，请你解释一下下面的代码的含义：

```c
{code}
```
    '''
    
    client = ZhipuAI(api_key=ZHIPU_AI_KEY) # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-3-turbo", # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

def code_check(code):
    """
    代码检查
    """
    prompt = f'''
你是一名精通`C++`、`C语言`代码的程序员，请你检查一下下面的代码，是否有明显的语法错误或者可以改进的地方：

```c
{code}
```
    '''
    
    client = ZhipuAI(api_key=ZHIPU_AI_KEY) # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-3-turbo", # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

# 判题
def homework_judge(name, code):
    """
    判题
    """
    prompt = f'''
你是一名精通`C++`、`C语言`代码的程序员，现在有一道题目，题目是：

```txt
{name}
```

下面的代码是某个人提交的答案

```c
{code}
```

请你结合题目，对该代码进行评分以及评价，评分区间是60到100分，评价需要比较简单的语句，请用JSON的形式返回数据，比如

```JSON
{{"score": 95, "remark": "做得还行"}}
```

'''
    print(prompt)
    client = ZhipuAI(api_key=ZHIPU_AI_KEY) # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-3-turbo", # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content
    print(content)
    # 解析结果
    # 正则提取{}中的内容
    result = re.search(r'{"(.*?)"}', content).group().strip()
    result = json.loads(result)
    return result

def qa(q):
    """
    智能答疑
    """
    prompt = f'''
你是一名精通`C++`、`C语言`代码的程序员，请你回答以下问题，答案请尽量简短。

问题：

```txt
{q}
```
    '''
    client = ZhipuAI(api_key=ZHIPU_AI_KEY) # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-3-turbo", # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def test_homework_judge():
    name = '用C语言写一个冒泡排序'
    code = '''
    #include <stdio.h>

    void bubbleSort(int arr[], int n) {
        int i, j, temp;
        for (i = 0; i < n - 1; i++) {      
            for (j = 0; j < n - i - 1; j++) { 
                if (arr[j] > arr[j + 1]) {
                    temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
    '''
    r = homework_judge(name, code)
    print(r)

if __name__ == '__main__':
    test_homework_judge()


