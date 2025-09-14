[Home](./index.html)

Akshay Gulabrao 13 September 2025

# introduction to the world of deepfakes

*This is not a serious introduction to deepfakes. This is my attempt to become familiar with the field.*

Face synthesis, aka *deepfakes*, uses deep learning to convert a video of 1 person talking to look like another person talking. Because of it's potential for misuse, it's not a very well published idea in the deep learning community.

Pei et al. 2024 [^1]covers a benchmark and survey of deepfake generation and detection. Conceptually, given input frames, audio, or text, we want to convert it to output of output frames, audio, and text. There are 4 subtasks in deepfakes: Face swapping, face reenactment, talking face generation, and facial attribute editing. I'm mainly interested in talking face generation, so I will be focusing on that. There are 2 frontier methods for this task involve Diffusion based and NeRFS.

Xu et al. proposes direct learning from a single image and audio [^2]. They use the VoxCeleb2 dataset [^3]. I will attempt to reproduce their experiments with


[^1]: [Pei et al. Deepfake Generation and Detection: A Benchmark and Survey. 2024](https://arxiv.org/pdf/2403.17881)
[^2]: [Xu et al. VASA-1: Lifelike Audio-Driven Talking Faces Generated in Real Time. 2024](https://arxiv.org/pdf/2404.10667)
[^3]: [J.S. Chung. The VoxCeleb2 Dataset](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox2.html)