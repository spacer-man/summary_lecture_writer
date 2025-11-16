from io import BytesIO


class AudioConverter(object):
    @staticmethod
    def opus_to_wav(origins: BytesIO) -> BytesIO:
        import ffmpeg

        origins.seek(0)
        
        # Use ffmpeg to convert
        process = (
            ffmpeg
            .input('pipe:0')
            .output('pipe:1', format='wav')
            .run_async(
                pipe_stdin=True,
                pipe_stdout=True,
                pipe_stderr=True,
                quiet=True)
        )
        
        wav_data, _ = process.communicate(input=origins.read())
        
        return BytesIO(wav_data)
