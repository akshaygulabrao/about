[Home](./index.html)

Akshay Gulabrao 13 September 2025

# introduction to the world of voice synthesis

*This is not a serious introduction to voice synthesis. This is my attempt to become familiar with the field.*

Voice synthesis refers to the deep learning task of converting one voice speaking a specific utterance to a different voice. It is significantly easier than face generation because the data has far lower dimensionality. Azzuni et al. published a comprehensive survey of voice cloning, so I will begin there. [^1]

Reading the introduction to they paper, the papers they cite mainly involve TTS speech synthesis, however, I'm mainly interested in speech to speech synthesis. An arxive search of speech synthesis yielded the interesting paper by Quamer et al. [^2] The author uses the CommonVoice dataset.[^3]

I also looked into the Pureformer VC [^4]. Let's start with VCTK. A huggingface dataset already exists for this, so it should be quite simple with the dataloader. 

## Blog

9/13/2025: Didn't get much done today. Wrote the intro and maybe a paragraph. Downloaded common voice. Decided I'm going to start trying to get a job in ML again (even though its probably hopeless). Commonvoice is still getting parsed. Looking at tinygrad and trying to get a codebase that works for me. Will probably involve using torch for the auxillary utils and tinygrad for the core. Or maybe even start my own library. In fact tomorrow, I'll probably start my own library that just imports tinygrad.

9/14/2025: Downloading the data is taking an absurdly long time. If this finishes, my first task is to make downloading the data and building the data loader significantly faster. I find it horrible that the Open Voice dataset does nothing to advertise the length of the dataset, and they only advertise the number of clips. It took over 30 minutes just to list all the clips. There are approximately 2.5 million clips. You can use the first digit of the clip as the heuristic for how close it is to being done, since it processes them in alphabetical order. I really want to have this published on huggingface to make it faster for everyone else. If I can do that, then these entire 2 days won't have been a waste. Someone in the future will be able to quickly download and start training on this data. This was a bad idea. I should have stuck to a proof of concept first. I don't have the resources to train it even if I could download it. 

[^1]: Azzuni et al. [Voice Cloning: A Comprehensive Survey.](https://arxiv.org/pdf/2505.00579) 2025. arxiv. 
[^2]: Quamer et al. [DarkStream: real-time speech anonymization with low latency](https://arxiv.org/pdf/2509.04667) 2025. arxiv.
[^3]: Ardila, R., Branson, M., Davis, K., Henretty, M., Kohler, M., Meyer, J., Morais, R., Saunders, L., Tyers, F. M. and Weber, G. (2020) [Common Voice: A Massively-Multilingual Speech Corpus](https://arxiv.org/pdf/1912.06670). Proceedings of the 12th Conference on Language Resources and Evaluation (LREC 2020). pp. 4211—4215
[^4]: Wenhan Yao, Fen Xiao, Xiarun Chen, Jia Liu, YongQiang He, Weiping Wen. [Pureformer-VC: Non-parallel Voice Conversion with Pure Stylized Transformer Blocks and Triplet Discriminative Training](https://arxiv.org/pdf/2506.08348). IJCNN2025. 
