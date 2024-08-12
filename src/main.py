import asyncio
from server import Server
from faster_whisper_asr import FasterWhisperASR
from pyannote_vad import PyannoteVAD


def main():
    vad_pipeline = PyannoteVAD("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")
    asr_pipeline = FasterWhisperASR()

    server = Server(vad_pipeline, asr_pipeline, host="0.0.0.0", port=4000, sampling_rate=16000, samples_width=2)

    print("Websocket URL: ws://127.0.0.1:4000")

    asyncio.get_event_loop().run_until_complete(server.start())
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
