from work.process import call
def handler(event, context):
    return call(event, context)