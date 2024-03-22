from AIDevs import AIDevsTasks


dev_task = AIDevsTasks('helloapi', debug=True)

task = dev_task.task()
hint = dev_task.hint()

answer = {
    'answer': task['cookie']
}

result = dev_task.send_answer(answer)

assert result['code'] == 0
