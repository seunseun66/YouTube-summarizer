# YouTube-summarizer

# Overview

I built this project to practice using AI APIs and build a backend service using Python, FastAPI, and Gemini API. The point of this project was to create a tool that could be used to take a YouTube URL and create a structured summary with key points and timestamps.

# How it works

The project starts by taking a YouTube URL through a FastAPI endpoint. The first thing it does is extract the video ID from the URL and use the YouTube transcript API to pull the video's transcript, which includes timestamps for each piece of text. Since some videos are hours long, you split them into smaller chunks (10 minutes each). Each chunk keeps track of when it starts in the video. From there, each chunk is sent to the Google Gemini API with a prompt asking it to extract 2-4 key points. Then the model is told to respond in only JSON so the response can be accurately decoded. Once every chunk has been summarized, all the key points are combined and sent to Gemini to generate an overview of the whole video. The final result shows the overview with every key point and its timestamp.

# Why I used this approach

Splitting the project into separate files (transcript.py, chunker.py, summarizer.py, main.py) instead of writing everything in one place makes it easier for me to keep track of the project by ensuring each part is pulling the transcript, splitting it into chunks, calling the AI, and handling the API route. This makes it easier for me to test each piece on its own and debug any problems

The reason why I chunked the transcript by time instead of character count is so that each summary stays tied to a specific, meaningful point in the video, rather than a sentence ending up in a random spot

I also forced the AI output into strict JSON instead of letting it return to plain text, since the code needs to actually read and organize the response.

# What I learned

- Working with gemni APi and JSON response from an LLM

- Building a real REST APi with FastAPI
  
- Debugging real world issuses like outdated libraries, changing API model names, and authentication errors
  
- Keeping API keys secure using environment variables and .gitignore

  

