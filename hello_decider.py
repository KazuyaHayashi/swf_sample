import boto.swf.layer2 as swf

DOMAIN = 'boto_tutorial'
ACTIVITY = 'HelloWorld'
ACTIVITY_A = 'ActivityA'
VERSION = '1.0'
TASKLIST = 'default'

class HelloDecider(swf.Decider):
    domain = DOMAIN
    task_list = TASKLIST
    version = VERSION

    def run(self):
        history = self.poll()
        if 'events' in history:
            workflow_events = [e for e in history['events']
                if not e['eventType'].startswith('Decision')]
            last_event = workflow_events[-1]

            decisions = swf.Layer1Decisions()
            if last_event['eventType'] == 'WorkflowExecutionStarted':
                decisions.schedule_activity_task('saying_hi', ACTIVITY, VERSION, task_list=TASKLIST)
            elif last_event['eventType'] == 'ActivityTaskCompleted':
                last_event_attrs = last_event['activityTaskCompletedEventAttributes']
                completed_activity_id = last_event_attrs['scheduledEventId'] - 1

                activity_data = history['events'][completed_activity_id]
                activity_attrs = activity_data['activityTaskScheduledEventAttributes']
                activity_name = activity_attrs['activityType']['name']

                result = last_event['activityTaskCompletedEventAttributes'].get('result')

                if activity_name == ACTIVITY:
                    decisions.schedule_activity_task('saying_goodbye', ACTIVITY_A, VERSION, task_list='goodbye', input=result)
                elif activity_name == ACTIVITY_A:
                    decisions.complete_workflow_execution()

            self.complete(decisions=decisions)
            return True
