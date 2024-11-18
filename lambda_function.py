import sys
def handler(event, context):
    import librosa
    
    return 'Hello from AWS Lambda using Python' + sys.version + '! librosa version: ' + librosa.__version__