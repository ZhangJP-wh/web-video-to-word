from pathlib import Path
from huggingface_hub import snapshot_download
from resemblyzer import VoiceEncoder
from reader import ffmpeg
root = Path(__file__).resolve().parent
path = snapshot_download("Qwen/Qwen3-ASR-1.7B", cache_dir=str(root / "work/model-cache"),
                         allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model"])
print("Qwen 模型下载完成：", path)
VoiceEncoder(device="cpu", verbose=False)
print("声纹模型可加载；FFmpeg 路径：", ffmpeg())
