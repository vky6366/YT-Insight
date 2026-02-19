from .yt_url_parser import yt_parser
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter

class transcription():
    def __init__(self, url):
        self.url = url
        self.code = yt_parser(self.url).get_youtube_id()

    def transcript(self):
        if not self.code or not isinstance(self.code, str):
            return "Invalid or missing YouTube video ID."
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(self.code, languages=["en"])

            # Flatten it to plain text
            transcript = " ".join(chunk["text"] for chunk in transcript_list)
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.create_documents([transcript])
            return chunks


        except TranscriptsDisabled:
            return "No captions available for this video."