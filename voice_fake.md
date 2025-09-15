[Home](./index.html)

Akshay Gulabrao 13 September 2025

# introduction to the world of voice synthesis

*This is not a serious introduction to voice synthesis. This is my attempt to become familiar with the field.*

Voice synthesis refers to the deep learning task of converting one voice speaking a specific utterance to a different voice. It is significantly easier than face generation because the data has far lower dimensionality. Azzuni et al. published a comprehensive survey of voice cloning, so I will begin there. [^1]

Reading the introduction to they paper, the papers they cite mainly involve TTS speech synthesis, however, I'm mainly interested in speech to speech synthesis. An arxive search of speech synthesis yielded the interesting paper by Quamer et al. [^2] The author uses the CommonVoice dataset.[^3]

Another interesting paper that I found by Luo et al. innovates on a codec framework with a subspace orthogonal projection module that splits the input into 2 subspaces where 1 correlates to speech and another correlates to the background. 


## Blog


**September 14, 2025**
Downloading and indexing the Open Voice dataset was extremely slow—listing all ~2.5 million clips took over 30 minutes. Since clips are processed alphabetically, I used the first digit of the clip name as a rough progress indicator. The dataset only advertises clip count, not size or download time, which makes planning difficult. I ended up switching to a smaller dataset due to resource constraints. I plan to publish a preprocessed version on Hugging Face to make it easier for others to use.

**September 13, 2025**
Downloaded Common Voice and started drafting the intro. Parsing is still in progress. I’ve been exploring Tinygrad as a core framework, possibly using PyTorch for utilities. I might build a small wrapper library around Tinygrad to streamline experimentation.

[^1]: Azzuni et al. [Voice Cloning: A Comprehensive Survey.](https://arxiv.org/pdf/2505.00579) 2025. arxiv. 
[^2]: Quamer et al. [DarkStream: real-time speech anonymization with low latency](https://arxiv.org/pdf/2509.04667) 2025. arxiv.
[^3]: Ardila, R., Branson, M., Davis, K., Henretty, M., Kohler, M., Meyer, J., Morais, R., Saunders, L., Tyers, F. M. and Weber, G. (2020) [Common Voice: A Massively-Multilingual Speech Corpus](https://arxiv.org/pdf/1912.06670). Proceedings of the 12th Conference on Language Resources and Evaluation (LREC 2020). pp. 4211—4215
[^4]: Wenhan Yao, Fen Xiao, Xiarun Chen, Jia Liu, YongQiang He, Weiping Wen. [Pureformer-VC: Non-parallel Voice Conversion with Pure Stylized Transformer Blocks and Triplet Discriminative Training](https://arxiv.org/pdf/2506.08348). IJCNN2025.
[^5]: [babyvedat/VCTK](https://huggingface.co/datasets/badayvedat/VCTK)
