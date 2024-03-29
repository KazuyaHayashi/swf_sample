import boto.swf.layer2 as swf
from boto.swf.exceptions import SWFTypeAlreadyExistsError, SWFDomainAlreadyExistsError

DOMAIN = 'boto_tutorial'
VERSION = '1.0'

registerables = []
registerables.append(swf.Domain(name=DOMAIN))

for workflow_type in ('HelloWorkflow', 'SerialWorkflow', 'ParallelWorkflow'):
    registerables.append(swf.WorkflowType(domain=DOMAIN, name=workflow_type, version=VERSION, task_list='default'))

for activity_type in ('HelloWorld', 'ActivityA', 'ActivityB', 'ActivityC'):
    registerables.append(swf.ActivityType(domain=DOMAIN, name=activity_type, version=VERSION))

for swf_entity in registerables:
    try:
        swf_entity.register()
        print swf_entity.name, 'registered successfully'
    except (SWFDomainAlreadyExistsError, SWFTypeAlreadyExistsError):
        print swf_entity.__class__.__name__, swf_entity.name, 'already exists'

