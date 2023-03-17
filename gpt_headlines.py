import re
import openai

# Load API key from file
with open("gptkey.txt", "r") as f:
    openai.api_key = f.read().strip()

# Load headlines from file
with open("headlines.txt", "r") as f:
    headlines = [line.strip() for line in f.readlines()]

# Define the prompt
prompt_template = "Make a headline similar to {} and make sure the headline is unique from previous entries. Please also make sure that generated headlines use the same numbers."
headline_history = []

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
                generated_numbers = re.findall(r'[0-9]+', generated_headline)
                if(len(generated_numbers) == 0):
                    print("Error: No numbers found in generated headline")
                elif(generated_numbers[0] != numbers):
                    print("MISMATCH ALERT! {} vs {}".format(headline, generated_headline))
                    print("Regex Replacing...")
                    # replace generated numbers with original numbers
                    generated_headline = generated_headline.replace(generated_numbers[0], numbers)
            
            headline_history.append(generated_headline)

            # check if generated headline is unique
            while(generated_headline in headline_history):
                print("Error: Duplicate headline found")
                print("Regenerating headline...")
                # generate new headline
                replace_prompt = "Make a headline similar to {} and make sure the headline is unique from previous entries. Please also make sure that generated headlines use the same numbers."
                responses = openai.Completion.create(
                        engine="text-davinci-002",
                        prompt=prompt,
                        max_tokens=60,
                        n=1,
                        stop=None,
                        temperature=0.8,)
                generated_headline = responses.choices[0].text.strip().format(numbers) if numbers else responses.choices[0].text.strip()
                if numbers:
                    generated_numbers = re.findall(r'[0-9]+', generated_headline)
                    if(len(generated_numbers) == 0):
                        print("Error: No numbers found in generated headline {}".format(generated_headline))
                    elif(generated_numbers[0] != numbers):
                        print("MISMATCH ALERT! {} vs {}".format(headline, generated_headline))
                        print("Regex Replacing...")
                        # replace generated numbers with original numbers
                        generated_headline = generated_headline.replace(generated_numbers[0], numbers)
            headline_history.append(generated_headline)
            f.write(f"{generated_headline}\n")
        f.write("\n")

print("Done!")
