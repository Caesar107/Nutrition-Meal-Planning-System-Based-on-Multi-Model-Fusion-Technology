"""

# 千帆AI
pip install qianfan


"""

import os
import qianfan

os.environ["QIANFAN_AK"] = "mdCdGjnGKrlSYgO68ZLbe4mB"
os.environ["QIANFAN_SK"] = "uWAVT4smF6DSBORaQMChG4ZqXhpQobiT"

os.environ["QIANFAN_AK"] = "eNqnXBfmSfL1Vvli4pESO0nn"
os.environ["QIANFAN_SK"] = "LTTI6A8TjFcz7jQj21tacUdVQzGqoQeb"


# 判题
def homework_judge(name, code):
    """
    判题
    """
    prompt = f'''
你是一名精通`C语言`代码的程序员，现在有一道题目，题目是：

```txt
{name}
```

下面的代码是某个人提交的答案

```c
{code}
```

请你结合题目，对该代码进行分析，判断对错，并给出错误原因以及修改意见

'''
    
    print(prompt)
    chat_comp = qianfan.ChatCompletion(model="ERNIE-Bot")
    resp = chat_comp.do(messages=[{
                "role": "user",
                "content": prompt
                }], top_p=0.8, temperature=0.9, penalty_score=1.0)

    print(resp["result"])
    return resp["result"]

if __name__ == '__main__':
    name = '写一个冒泡排序'
    code = '''

#include <stdio.h>

void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) { // 外层循环控制遍历轮数
        for (int j = 0; j < n - i - 1; j++) { // 内层循环控制每轮比较的次数
            if (arr[j] > arr[j + 1]) { // 如果前一个元素大于后一个元素，则交换它们
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(arr) / sizeof(arr[0]); // 获取数组长度

    printf("Original array: ");
    printArray(arr, n);

    bubbleSort(arr, n); // 对数组进行冒泡排序

    printf("Sorted array: ");
    printArray(arr, n);

    return 0;
}
    '''
    homework_judge(name, code)

