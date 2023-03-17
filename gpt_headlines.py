import re
import openai

# Load API key from file
with open("gptkey.txt", "r") as f:
    openai.api_key = f.read().strip()

# Load headlines from file
with open("headlines.txt", "r") as f:
    headlines = [line.strip() for line in f.readlines()]

# Define the prompt
prompt_template = "make a headline similar to {} and make sure all headlines are unique"

# Loop through each headline and generate 3 similar headlines
with open("gpt_headlines.txt", "w") as f:
    for headline in headlines:
        # Check if the headline has numbers
        match = re.search(r"\d+", headline)
        if match:
            # Extract the numbers from the original headline
            numbers = match.group(0)
            # Replace the numbers in the prompt with a placeholder
            prompt = prompt_template.format(re.sub(r"\d+", "{}", headline))
        else:
            prompt = prompt_template.format(headline)
            numbers = None  # No numbers in the original headline
        
        responses = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=60,
            n=3,
            stop=None,
            temperature=0.8,
        )

        f.write(f"Original Headline: {headline}\n")
        for i, response in enumerate(responses.choices):
            # Replace the placeholder with the extracted numbers, if any
            generated_headline = response.text.strip().format(numbers) if numbers else response.text.strip()
            # Ensure that the numbers in the generated headline are the same as the numbers in the original headline
            if numbers:
                generated_numbers = re.search(r"\d+", generated_headline).group(0)
                generated_headline = generated_headline.replace(generated_numbers, numbers)
            f.write(f"{generated_headline}\n")
        f.write("\n")

print("Done!")
