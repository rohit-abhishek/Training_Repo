import modal
from modal import App, Volume, Image

# Setup

# create a new app called llama 
app = modal.App("llama")

# create machine image 
image = Image.debian_slim().pip_install("torch", "transformers", "bitsandbytes", "accelerate")

# get the hugging face secret from secret file 
secrets = [modal.Secret.from_name("hf-secret")]

# we will need a machine with GPU T4 atleas fr this 
GPU = "T4"

# use llama 3.1 8B parameter base model 
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B" # "google/gemma-2-2b"



@app.function(image=image, secrets=secrets, gpu=GPU, timeout=1800)
def generate(prompt: str) -> str:

    # imports 
    import os
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, set_seed

    # Quant Config
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4"
    )

    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    # create fine tuned model 
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        quantization_config=quant_config,
        device_map="auto"
    )

    set_seed(42)
    inputs = tokenizer.encode(prompt, return_tensors="pt").to("cuda")
    attention_mask = torch.ones(inputs.shape, device="cuda")

    # we will generate the output and return the first one
    outputs = model.generate(inputs, attention_mask=attention_mask, max_new_tokens=5, num_return_sequences=1)
    return tokenizer.decode(outputs[0])
