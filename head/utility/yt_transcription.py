# from .yt_url_parser import yt_parser
# from youtube_transcript_api import (
#     YouTubeTranscriptApi,
#     TranscriptsDisabled,
#     NoTranscriptFound,
#     VideoUnavailable
# )
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# import os
# from googleapiclient.discovery import build

# api_key = os.getenv("YOUTUBE_API_KEY")

# class Transcription:
#     def __init__(self, url):
#         self.url = url
#         self.code = yt_parser(self.url).get_youtube_id()
#         youtube = build('youtube', 'v3', developerKey=api_key)
#     def transcript(self):

#         if not self.code or not isinstance(self.code, str):
#             return "Invalid or missing YouTube video ID."

#         try:
#             ytt_api = YouTubeTranscriptApi()
#             fetched_transcript = ytt_api.fetch(self.code)

#             documents = []

#             for snippet in fetched_transcript:
#                 documents.append(
#                     Document(
#                         page_content=snippet.text,
#                         metadata={
#                             "source": self.url,
#                             "start": snippet.start,
#                             "duration": snippet.duration,
#                             "video_id": self.code,
#                             "language": fetched_transcript.language_code
#                         }
#                     )
#                 )

#             return documents

#         except TranscriptsDisabled:
#             return "No captions available for this video."

#         except NoTranscriptFound:
#             return "English transcript not available."

#         except VideoUnavailable:
#             return "Video unavailable or private."


#     def get_captions(video_id):
#         request = youtube.captions().list(
#             part="snippet",
#             videoId=video_id
#         )
#         response = request.execute()
#         return response


from .yt_url_parser import yt_parser
from langchain_core.documents import Document
from googleapiclient.discovery import build
import os
import requests

class Transcription:
    def __init__(self, url):
        self.url = url
        self.video_id = yt_parser(url).get_youtube_id()
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def get_caption_track_id(self):
        request = self.youtube.captions().list(
            part="snippet",
            videoId=self.video_id
        )
        response = request.execute()

        if "items" not in response:
            return None

        return response["items"][0]["id"]  # first caption track

    def download_caption(self, caption_id):
        request = self.youtube.captions().download(
            id=caption_id,
            tfmt="srt"
        )
        response = request.execute()
        return response.decode("utf-8")

    def transcript(self):
        if not self.video_id:
            return "Invalid video ID"

        caption_id = self.get_caption_track_id()

        if not caption_id:
            return "No captions available"

        raw_text = self.download_caption(caption_id)

        # Convert SRT → plain text
        lines = []
        for line in raw_text.split("\n"):
            if "-->" not in line and not line.strip().isdigit():
                lines.append(line)

        full_text = " ".join(lines)

        return [
            Document(
                page_content=full_text,
                metadata={"source": self.url}
            )
        ]
