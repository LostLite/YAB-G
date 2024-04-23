from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import BlogPost
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
from datetime import datetime
from .models import BlogPost

# Create your views here.
@login_required
def index(request):
    return render(request, 'ai_generator/index.html', {})

@csrf_exempt
def generate_blog(request):
    """
    This is the function that generates the actual blog
    It is Responsible for fetching the clip from YouTube link and 
    processing it accordingly.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']

        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data method.'}, status=400)

        # get video title using pytube
        yt = YouTube(yt_link)
        title = yt.title

        # download audio file from YouTube Video
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        video = yt.streams.filter(only_audio=True).first()
        output_file = video.download(output_path=settings.MEDIA_ROOT, filename_prefix=str(current_datetime))
        base, ext = os.path.splitext(output_file)
        new_file = f'{base}.mp3'
        os.rename(output_file, new_file)
        
        # get transcript
        config = aai.TranscriptionConfig(speaker_labels=True)
        aai.settings.api_key = settings.ASSEMBLY_AI_API_KEY
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(new_file,config=config)

        # if transcript.status == aai.TranscriptStatus.error:
        #     print(transcript.error)
        # else:
        #     # print(transcript.text)
        #     for utterance in transcript.utterances:
        #         print(f"Speaker {utterance.speaker}: {utterance.text}")
        if transcript.status == aai.TranscriptStatus.error:
            return JsonResponse({'error': f'{transcript.error}'}, status=500)

        # use OpenAI t generate the blog

        #save blog article to the database
        request.user.blogs.create(title=title, source_url=yt_link,youtube_title=title, generated_content=transcript.text)

        # return blog article as a response
        return JsonResponse({'content': ''}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@login_required
def all_blogs(request):
    return render(request, 'ai_generator/blogs.html')

@login_required
def single_blog(request, id):
    blog = BlogPost.objects.get(id=id)

    if blog is None:
        return redirect('home')
    return render(request, 'ai_generator/single.html', {'blog':blog})

