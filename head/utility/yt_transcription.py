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
            transcripts = YouTubeTranscriptApi.list_transcripts(self.code)
            transcript_lang = transcripts.find_transcript(['en'])
            transcript_list = transcript_lang.fetch()

            # Convert to plain text
            transcript_text = " ".join(
                chunk.text for chunk in transcript_list
            )

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            # chunks = splitter.split_text(transcript_text)

            # return chunks

            texts = splitter.split_text(transcript_text)

            documents = [
                Document(
                    page_content=text,
                    metadata={"source": self.url}
                )
                for text in texts
            ]
            return documents


        except TranscriptsDisabled:
            return "No captions available for this video."

        except NoTranscriptFound:
            return "English transcript not available."

        except VideoUnavailable:
            return "Video unavailable or private."
