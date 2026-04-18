# RecipeAI
A Youtube cooking video summarizer.
<img width="1101" height="525" alt="Screenshot 2026-04-19 at 01 55 28" src="https://github.com/user-attachments/assets/15d6e82a-c86b-4b71-9699-25b3781d2388" />

## Motivation

Millions of cooking videos are uploaded to YouTube and other platforms every day. As users save more and more video recipes, keeping track of them becomes nearly impossible. Unlike text‑based recipes, video content is not easily searchable, scannable, or comparable. This leads to several practical problems:

- **Information overload** – You forget what recipes you have already seen or saved.
- **Repetitive effort** – You have to re‑watch the same video to recall a single step or quantity.
- **Lack of structure** – There is no standard format to compare ingredients or cooking times across different videos.

The goal of this project is to solve these problems by converting long videos to clean recipes. 

## Approach

This module trains a language model to transform real‑world cooking video transcripts (from YouTube and similar platforms) into a **standardized, executable recipe format** containing:

- Dish name  
- Ingredient list  
- Step‑by‑step instructions  
- Summary / conclusion  

Raw transcripts are highly colloquial, filled with disfluencies, off‑topic narration, and long‑context dependencies. Off‑the‑shelf LLMs often fail to produce stable structured outputs from such inputs. Manual annotation of “transcript → structured recipe” pairs is expensive and suffers from low consistency across annotators. Therefore, we adopt a **teacher‑student synthetic labeling approach**:

- A **Teacher LLM** (external, more powerful) rewrites raw transcripts into high‑quality structured recipes.  
- These synthetic input–output pairs are used as the training set for supervised fine‑tuning (SFT).

This strategy rapidly scales the training dataset while explicitly enforcing the desired output format.

- **Framework**: [Unsloth](https://github.com/unslothai/unsloth) – optimized for faster LoRA fine‑tuning with reduced memory usage.  
- **Base model**: Llama series (Llama 2 / Llama 3).  
- **Fine‑tuning method**: LoRA (Low‑Rank Adaptation) – parameter‑efficient and suitable for long‑context scenarios.  
- **Objective**: Improve structured output stability, reduce hallucination of irrelevant narrative content, and maintain performance even with long transcripts.

A fine‑tuned Llama model that reliably converts messy, spoken‑language cooking video transcripts into clean, searchable, and executable recipes — enabling users to build a personal, structured recipe library from any video they watch.

Video Demo: https://www.youtube.com/watch?v=wmzBDZWGfv0
