import boto.swf.layer2 as swf

DOMAIN = 'boto_tutorial'
VERSION = '1.0'
TASKLIST = 'goodbye'

class GoodByeWorker(swf.ActivityWorker):
    domain = DOMAIN
    version = VERSION
    task_list = TASKLIST

    def run(self):
        activity_task = self.poll()
        print(activity_task)
        if 'activityId' in activity_task:
            print 'GoodBye, World!'
            self.complete()
            return True

