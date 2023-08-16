# background_runner.py
# from flask_mail import Message
import time
import uuid


class BackgroundRunner:
    def __init__(self, executor):
        self.executor = executor

    def do_task(self):
        time.sleep(1000)
        print("DOne")


    def do_task_async(self, upload_key):
        task_id = upload_key  # Generate a unique task ID
        self.executor.submit_stored(task_id, self.do_task)
        return task_id

    def task_status(self, task_id):
        if not self.executor.futures.done(task_id):
            return "running"
        self.executor.futures.pop(task_id)
        return "completed"