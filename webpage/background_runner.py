# background_runner.py
# from flask_mail import Message
import time
import uuid
import os


class BackgroundRunner:
    def __init__(self, executor):
        self.executor = executor
        # self.upload_key=upload_key

    def do_task(self, upload_key):
        inpath=f"/home/saksham/Desktop/RED_HEN/RedHenAnonymizer/webpage/static/upload/{upload_key}/swap_output_elon.mp4"
        # facepath=""
        outpath=f"/home/saksham/Desktop/RED_HEN/RedHenAnonymizer/webpage/static/upload/{upload_key}/swap_output_elon.mp4"
        pitch="-4"
        cmd=f"python /home/saksham/Desktop/RED_HEN/RedHenAnonymizer/rha.py --inpath {inpath} --outpath {outpath} --pitch {pitch} --anonymize 'audiovideo' --visual_anonymization 'hider'"
        print(cmd)
        error = os.system(cmd)
        if error:
            raise Exception(f'unable to swap faces. Check fsgan. error code: {error}')
        
        print("Done")


    def do_task_async(self, upload_key):
        task_id = upload_key  
        self.executor.submit_stored(task_id, self.do_task, upload_key)
        return task_id

    def task_status(self, task_id):
        if not self.executor.futures.done(task_id):
            return "running"
        self.executor.futures.pop(task_id)
        return "completed"