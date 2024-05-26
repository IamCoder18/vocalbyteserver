import asyncio
from server import Server
from src.faster_whisper_asr import FasterWhisperASR
from src.pyannote_vad import PyannoteVAD


def main():
    vad_pipeline = PyannoteVAD("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")
    asr_pipeline = FasterWhisperASR()

    server = Server(vad_pipeline, asr_pipeline, host="0.0.0.0", port=5050, sampling_rate=16000, samples_width=2)

    asyncio.get_event_loop().run_until_complete(server.start())
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
