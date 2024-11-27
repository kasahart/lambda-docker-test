import librosa
import sys

def call(event, context):
    return 'Hello from AWS Lambda using Python' + sys.version + '! librosa version: ' + librosa.__version__