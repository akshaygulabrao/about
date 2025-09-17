---
title: "Voice Conversion"
author: "Akshay Gulabrao"
date: "2025-September-16"
bibliography: voice_fake_references.bib
link-citations: true
---
[Home](./index.html)


This is not a serious introduction to voice synthesis. This is my attempt to become familiar with the field.

Voice synthesis refers to the deep learning task of converting one voice speaking a specific utterance to a different voice. It is significantly easier than face generation because the data has far lower dimensionality. Azzuni et al. published a comprehensive survey of voice cloning, so I will begin there [@azzuni2025voicecloning].

Reading the introduction to their paper, the papers they cite mainly involve TTS speech synthesis; however, I'm mainly interested in speech-to-speech synthesis. An arXiv search of speech synthesis yielded the interesting paper by Quamer et al. [@quamer2025darkstream]. The author uses the CommonVoice dataset [@ardila2020commonvoice].

Another interesting paper that I found by Luo et al. innovates on a codec framework with a subspace orthogonal projection module that splits the input into two subspaces—one correlates to speech and another correlates to the background [@luo2025decodec]. See also [@yao2025pureformervc; @babyvedat_vctk; @kameoka2025latentvoicegrad].

The VCTK dataset is extremely popular for voice synthesis research. It is a 10GB dataset which contains speech data for 100+ native English speakers with various accents [@yamagishi2019cstr].

## References