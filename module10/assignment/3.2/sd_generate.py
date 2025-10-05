from dotenv import load_dotenv

load_dotenv()

import replicate
import os
from time import sleep

def run_model(
    model: str, 
    prompt: str, 
    seed:int, 
    steps:int, 
    format:str, 
    filename:str=None):
    
    result = replicate.run(
        model,
        input={
            "prompt": prompt,
            "seed": seed,
            "steps": steps,
            "format": format
        }
    )
    
    output = create_parameterized_output_name(filename, seed, steps, format)
    print(f"Saving output {result} to {output}")
    
    with open(output, 'wb') as f:
        f.write(result.read())

    return result

def create_parameterized_output_name(
    base_name: str, 
    seed: int, 
    steps: int, 
    format: str) -> str:
    
    name, ext = os.path.splitext(base_name)
    return f"{name}_seed{seed}_steps{steps}.{format}"

def create_experiments():
    return [
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat", 
            "seed": 42, "steps": 30, "format": "png", "filename": "cat"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat", 
            "seed": 42069, "steps": 30, "format": "png", "filename": "cat"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat", 
            "seed": 420, "steps": 30, "format": "png", "filename": "cat"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat", 
            "seed": 69, "steps": 30, "format": "png", "filename": "cat"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat", 
            "seed": 42, "steps": 20, "format": "png", "filename": "cat"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat", 
            "seed": 42, "steps": 30, "format": "png", "filename": "cat"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat", 
            "seed": 42, "steps": 40, "format": "png", "filename": "cat"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat", 
            "seed": 42, "steps": 50, "format": "png", "filename": "cat"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, studio lighting", 
            "seed": 42, "steps": 30, "format": "png", "filename": "cat-studio"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, dramatic lighting, dark background", 
            "seed": 42, "steps": 30, "format": "png", "filename": "cat-dramatic"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, outdoor setting, natural light", 
            "seed": 42, "steps": 30, "format": "png", "filename": "cat-outdoor"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, riding a horse in an american civil war battle scene", 
            "seed": 42, "steps": 30, "format": "png", "filename": "cat-civil-war"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, riding a horse in an american civil war battle scene", 
            "seed": 42, "steps": 40, "format": "png", "filename": "cat-civil-war"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, riding a horse in an american civil war battle scene", 
            "seed": 42, "steps": 50, "format": "png", "filename": "cat-civil-war"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, riding a horse in an american civil war battle scene", 
            "seed": 420, "steps": 30, "format": "png", "filename": "cat-civil-war"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, riding a horse in an american civil war battle scene", 
            "seed": 69, "steps": 30, "format": "png", "filename": "cat-civil-war"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, riding a horse in an american civil war battle scene", 
            "seed": 42069, "steps": 30, "format": "png", "filename": "cat-civil-war"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, wearing a samurai armor in an action shot, cinematic lighting, akira kurosawa style", 
            "seed": 42, "steps": 30, "format": "png", "filename": "cat-samurai"
        },
        { 
            "model": "stability-ai/stable-diffusion-3.5-medium", 
            "prompt": "a white siamese cat, wearing a shinobi outfit while kneeling holding a katana sword, dramatic lighting with ginko leaves in the background, akira kurosawa style", 
            "seed": 42, "steps": 30, "format": "png", "filename": "cat-shinobi"
        }
    ]

if __name__ == "__main__":
    
    experiments = create_experiments()
    for exp in experiments:
        model = exp["model"]
        prompt = exp["prompt"]
        seed = exp["seed"]
        steps = exp["steps"]
        format = exp["format"]
        filename = exp["filename"]

        print(f"Running model {model} with seed {seed} and steps {steps}")
        
        run_model(model, prompt, seed, steps, format, filename)
        
        # To avoid hitting rate limits
        sleep(1)  