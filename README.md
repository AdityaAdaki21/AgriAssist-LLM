---
title: "AgriLlama: Plant Disease Information Assistant"
description: "AgriLlama is a fine-tuned large language model based on Llama3.2:1B, designed to assist Indian farmers with plant disease identification and management."
version: "1.0"
author: "Sike Aditya"
repository: "https://huggingface.co/sikeaditya/agri_assist_llm"
tags:
  - Agriculture
  - Plant Disease
  - LLM
  - AI
  - India
model:
  base: "meta/Llama3.2:1B"
  fine_tuning_dataset: "1000 samples focusing on plant diseases in Indian agriculture"
  format: "Alpaca Instruct Format"
usage:
  - "Farmers"
  - "Agronomists"
  - "Agricultural extension workers"
installation:
  ollama: "curl -fsSL https://ollama.ai/install.sh | sh"
usage_examples:
  - command: "ollama run AgriLlama 'Explain Red Rot in sugarcane in simple terms for Indian farmers.'"
    description: "Provides an easy-to-understand explanation of Red Rot disease in sugarcane."
dataset:
  crops:
    Sugarcane:
      - "Bacterial Blight"
      - "Healthy"
      - "Red Rot"
    Maize:
      - "Blight"
      - "Common Rust"
      - "Gray Leaf Spot"
      - "Healthy"
    Cotton:
      - "Bacterial Blight"
      - "Curl Virus"
      - "Fusarium Wilt"
      - "Healthy"
    Rice:
      - "Bacterial Blight"
      - "Blast"
      - "Brownspot"
      - "Tungro"
    Wheat:
      - "Healthy"
      - "Septoria"
      - "Strip Rust"
contact:
  email: "sikeaditya@example.com"
  issues: "https://github.com/sikeaditya/agri_assist_llm/issues"
---
# AgriLlama: Plant Disease Information Assistant

AgriLlama is a fine-tuned large language model based on Llama3.2:1B, specifically designed to provide detailed, actionable information about plant diseases to Indian farmers. It offers clear, concise, and locally relevant guidance on disease identification, symptoms, causes, severity, and treatment measures across major crops such as Sugarcane, Maize, Cotton, Rice, and Wheat.

## Features

- **Tailored Guidance:** Provides comprehensive details on various plant diseases affecting Indian crops.
- **Practical Recommendations:** Offers clear instructions on treatment and prevention, helping farmers manage crop health.
- **User-Friendly:** Utilizes the Alpaca Instruct Format to generate responses in simple, accessible language.
- **Versatile Applications:** Suitable for use by farmers, agronomists, and agricultural extension workers.

## Model Details

- **Base Model:** Llama3.2:1B
- **Fine-Tuning Dataset:** Custom dataset of 200 samples focusing on plant diseases in Indian agriculture.
- **Intended Use:** Assisting in the identification, explanation, and management of plant diseases.

## Installation

To use AgriLlama, install the required libraries:

```bash
pip install transformers torch
```

## Usage

### Using Hugging Face Transformers

Here’s an example of how to use AgriLlama with the Hugging Face Transformers library:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
# Load the tokenizer and model from the Hugging Face Hub
tokenizer = AutoTokenizer.from_pretrained("your-username/AgriLlama")
model = AutoModelForCausalLM.from_pretrained("your-username/AgriLlama")
# Define a prompt
prompt = "Explain Red Rot in sugarcane in simple terms for Indian farmers."
# Tokenize and generate a response
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=256)
# Decode and print the generated response
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

*Note:* Replace `your-username/AgriLlama` with the actual path of your repository.

### Using Ollama

You can also use AgriLlama with [Ollama](https://ollama.ai), a simple way to run large language models locally.

1. Install Ollama if you haven't already:

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

2. Pull the model from Ollama [Library](https://ollama.com/sike_aditya/AgriLlama)
```bash
ollama pull sike_aditya/AgriLlama
```

3. Run the model using Ollama:

```bash
ollama run AgriLlama "Explain Red Rot in sugarcane in simple terms for Indian farmers."
```

This will generate a response based on the model’s fine-tuned dataset.

## Fine-Tuning and Training

AgriLlama was fine-tuned using a custom dataset created in the Alpaca Instruct Format. The dataset covers detailed plant disease information tailored to the Indian context and includes samples for:

- **Sugarcane:** Bacterial Blight, Healthy, Red Rot
- **Maize:** Blight, Common Rust, Gray Leaf Spot, Healthy
- **Cotton:** Bacterial Blight, Curl Virus, Fusarium Wilt, Healthy
- **Rice:** Bacterial Blight, Blast, Brownspot, Tungro
- **Wheat:** Healthy, Septoria, Strip Rust

## Dataset

The fine-tuning dataset consists of carefully curated samples that provide comprehensive, accurate information designed to help users manage crop diseases effectively.


## Contact

For questions or suggestions, please open an issue in the repository or contact the authors directly.

---

Happy farming with AgriLlama!

