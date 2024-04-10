from diffusers import DiffusionPipeline

def openjourney(enhanced_query,file_name,path):

    pipe = DiffusionPipeline.from_pretrained("prompthero/openjourney")
    pipe = pipe.to("cuda")

    # Recommended if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()

    #prompt = "In 'Top Gun Maverick,' Tom Cruise's Maverick engages in a thrilling aerial duel, his determined face visible inside the cockpit amidst rugged canyons and vast skies."

    image = pipe(enhanced_query).images[0]
    image.save(path + "/q1.png")