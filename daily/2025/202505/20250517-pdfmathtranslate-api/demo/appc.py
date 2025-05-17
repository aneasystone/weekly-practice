import time

params = {
    'lang_in': 'en',
    'lang_out': 'zh',
    'service': 'google',
    'thread': 4
}

filepath = '/Users/aneasystone/Downloads/2504.08748v1/2504.08748v1.pdf'

from pdf2zh.backend import translate_task

with open(filepath, 'rb') as f:
    task = translate_task.delay(f.read(), params)
    print(task.id)
    
    while True:
        time.sleep(1)
        if str(task.state) == "PROGRESS":
            print('state: ', task.state, 'info: ', task.info)
        else:
            print('state: ', task.state)
        if str(task.state) == "SUCCESS":
            break

    doc_mono, doc_dual = task.get()
    with open('./dual.pdf', 'wb') as dual:
        dual.write(doc_dual)
