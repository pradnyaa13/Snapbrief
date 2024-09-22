from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
#flask instance created 
app = Flask(__name__)
#define a route for the summary endpoint
@app.get('/summary')
def summary_api():
    #extract url from request string
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    summary = get_summary(get_transcript(video_id))
    return summary, 200 
#function to get the transcript of video
def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    #join the transcript of each transcript entry into a single string
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript
#function to generate the summary from the transcript
def get_summary(transcript):
    summariser = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

if __name__ == '__main__':
    app.run()