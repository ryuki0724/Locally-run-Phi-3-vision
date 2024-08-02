import sys
import os
import time
import threading
from PIL import Image
import torch
from transformers import AutoModelForCausalLM, AutoProcessor
import shlex


def loading_animation():
    animation = "|/-\\"
    idx = 0
    while loading:
        print(f"\rProcessing {animation[idx % len(animation)]}", end="")
        idx += 1
        time.sleep(0.1)
    
    print("\r", end="")


def print_slowly(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()


if __name__ == '__main__':
    # Load the model
    model_path = "phi-3-vision-128k-instruct"

    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    processor = AutoProcessor.from_pretrained(
        model_path, trust_remote_code=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch_dtype, low_cpu_mem_usage=True, trust_remote_code=True, device_map="cuda:0", attn_implementation="flash_attention_2").cuda()

    user_prompt = '<|user|>\n'
    assistant_prompt = '<|assistant|>\n'
    prompt_suffix = "<|end|>\n"

    chat_history = []

    os.system('cls')

    while (True):

        input_text = input(
            "Please input your question (use --path to add images): ")

        images = []
        image_tags = ""

        if input_text.lower() == "exit":
            loading = False
            loading_thread.join()
            sys.exit(0)

        if "--path" in input_text:
            parts = input_text.split("--path")
            input_text = parts[0].strip()
            image_paths = shlex.split(parts[1].strip())

            print(f"image_: {image_paths}\n")

            for i, path in enumerate(image_paths, start=1):
                print(f"image_{i}: {path}")
                try:
                    images.append(Image.open(path))
                    image_tags += f"<|image_{i}|>"
                except IOError as e:
                    print(f"Error opening image {path}: {e}")
                    continue

            image_tags += "\n"

        current_message = {"role": "user", "content": f"{image_tags}{input_text}"}
        chat_history.append(current_message)

        full_prompt = processor.tokenizer.apply_chat_template(
            chat_history, tokenize=False, add_generation_prompt=True)

        if full_prompt.endswith("<|endoftext|>"):
            full_prompt = full_prompt.rstrip("<|endoftext|>")

        print(f">>> Full Prompt\n{full_prompt}")
        # print(f">>> Full Prompt\n{input_text}")

        loading = True
        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.start()

        try:
            inputs = processor(full_prompt, images=images if images else None,
                               return_tensors="pt").to("cuda:0")

            generate_ids = model.generate(**inputs,
                                          max_new_tokens=1000,
                                          eos_token_id=processor.tokenizer.eos_token_id,
                                          )

            generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
            response = processor.batch_decode(generate_ids,
                                              skip_special_tokens=True,
                                              clean_up_tokenization_spaces=False)[0]
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            continue
        finally:
            loading = False
            loading_thread.join()

        print(">>> Response\n")
        print_slowly(response)

        # print(f'>>> Response\n{response}')

        chat_history.append({"role": "assistant", "content": response})

        images.clear()

        print("\n\n")
