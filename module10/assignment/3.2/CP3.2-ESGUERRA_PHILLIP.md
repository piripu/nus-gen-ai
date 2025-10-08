# Module 10 - Capstone Project Part 3.1

> Submitted by Phillip Amir Esguerra

## Implementation

The code is implemented as follows:

``` python
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
```

The `run_model` function calls the replicate `run` method using the supplied parameters `model`, `prompt`, `seed`, `steps` and `format`, another parameter `filename` is used to save the output locally. The `filename`  acts as the base file name and other parameters are appended in the file for better documentation of output.

## Outputs

### Experimenting with Parameters

> Prompt: "a white siamese cat"

| Parameter | Output |
|---|---|
| Seed: `42`, Steps: `20` | ![cat1](cat_seed42_steps20.png) |
| Seed: `42`, Steps: `30` | ![cat2](cat_seed42_steps30.png) |
| Seed: `42`, Steps: `40` | ![cat3](cat_seed42_steps40.png) |
| Seed: `42`, Steps: `50` | ![cat4](cat_seed42_steps50.png) |

Changing the steps doesn't seem to have any noticable changes in the output

| Parameter | Output |
|---|---|
| Seed: `69`, Steps: `30` | ![cat1](cat_seed69_steps30.png) |
| Seed: `420`, Steps: `30` | ![cat2](cat_seed420_steps30.png) |
| Seed: `42069`, Steps: `30` | ![cat3](cat_seed42069_steps30.png) |

However, changing the seed parameter provides variations in the output.

### Experimenting with Prompts

| Prompt | Output |
|---|---|
| "a white siamese cat, studio lighting" | ![cat-studio](cat-studio_seed42_steps30.png) |
| "a white siamese cat, dramatic lighting, dark background" | ![cat-dramatic](cat-dramatic_seed42_steps30.png) |
| "a white siamese cat, outdoor setting, natural light" | ![cat-outdoor](cat-outdoor_seed42_steps30.png) |

Testing out different variations of the prompt, and the model follows the simple prompts easily. Although the cat in the outdoor setting doesn't seem to be a siamese cat, it's more orange cat.

#### Personal Prompt

> Prompt: "a white siamese cat, riding a horse in an american civil war battle scene"

| Parameter | Output |
|---|---|
| Seed: `42`, Steps: `30` | ![cat1](cat-civil-war_seed42_steps30.png) |
| Seed: `42`, Steps: `40` | ![cat2](cat-civil-war_seed42_steps40.png) |
| Seed: `42`, Steps: `50` | ![cat3](cat-civil-war_seed42_steps50.png) |

Same with this prompt, changing the steps doesn't provide any noticeable changes in the output.

| Parameter | Output |
|---|---|
| Seed: `69`, Steps: `30` | ![cat1](cat-civil-war_seed69_steps30.png) |
| Seed: `420`, Steps: `30` | ![cat2](cat-civil-war_seed420_steps30.png) |
| Seed: `42069`, Steps: `30` | ![cat3](cat-civil-war_seed42069_steps30.png) |

Changing the seed on the other hand changes the output dramatically. At seed 420, an output error can be seen that the horse is anatomically incorrect in it's posing and can be seen that it has 5 legs. At step 42069, it's a horse that looks like a cat.

<style>
td > img {
    width: 400px;
}
</style>