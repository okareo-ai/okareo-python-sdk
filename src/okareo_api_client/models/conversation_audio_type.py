from enum import Enum


class ConversationAudioType(str, Enum):
    INLINE_B64 = "inline_b64"
    URL = "url"
    VOICE_FILE_ID = "voice_file_id"

    def __str__(self) -> str:
        return str(self.value)
