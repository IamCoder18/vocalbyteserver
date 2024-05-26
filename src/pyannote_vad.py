from os import remove
import os

from pyannote.core import Segment
from pyannote.audio import Model
from pyannote.audio.pipelines import VoiceActivityDetection

from src.audio_utils import save_audio_to_file


class PyannoteVAD():
    def __init__(self, auth_token):
        model_name = "pyannote/segmentation"
        if auth_token is None:
            raise ValueError("Missing required env var in PYANNOTE_AUTH_TOKEN or argument in --vad-args: 'auth_token'")
        pyannote_args = {"onset": 0.5, "offset": 0.5, "min_duration_on": 0.3, "min_duration_off": 0.3}
        self.model = Model.from_pretrained(model_name, use_auth_token=auth_token)
        self.vad_pipeline = VoiceActivityDetection(segmentation=self.model)
        self.vad_pipeline.instantiate(pyannote_args)

    async def detect_activity(self, client):
        audio_file_path = await save_audio_to_file(client.scratch_buffer, client.get_file_name())
        vad_results = self.vad_pipeline(audio_file_path)
        remove(audio_file_path)
        vad_segments = []
        if len(vad_results) > 0:
            vad_segments = [
                {"start": segment.start, "end": segment.end, "confidence": 1.0}
                for segment in vad_results.itersegments()
            ]
        return vad_segments
