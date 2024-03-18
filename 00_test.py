from AIDevs import AIDevsTasks, API_KEY


dev_task = AIDevsTasks(API_KEY, 'helloapi', debug=True)

task = dev_task.task()
hint = dev_task.hint()

answer = {
    'answer': task['cookie']
}

result = dev_task.send_answer(answer)

assert result['code'] == 0
