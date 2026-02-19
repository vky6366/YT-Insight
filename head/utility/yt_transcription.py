from .yt_url_parser import yt_parser
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class Transcription:
    def __init__(self, url):
        self.url = url
        self.code = yt_parser(self.url).get_youtube_id()

    def transcript(self):

        if not self.code or not isinstance(self.code, str):
            return "Invalid or missing YouTube video ID."

        try:
            ytt_api = YouTubeTranscriptApi()
            fetched_transcript = ytt_api.fetch(self.code)

            documents = []

            for snippet in fetched_transcript:
                documents.append(
                    Document(
                        page_content=snippet.text,
                        metadata={
                            "source": self.url,
                            "start": snippet.start,
                            "duration": snippet.duration,
                            "video_id": self.code,
                            "language": fetched_transcript.language_code
                        }
                    )
                )

            return documents

        except TranscriptsDisabled:
            return "No captions available for this video."

        except NoTranscriptFound:
            return "English transcript not available."

        except VideoUnavailable:
            return "Video unavailable or private."

