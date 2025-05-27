import requests
import os
import json
import time
import re
import sys
import math
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# Set LM Studio API URL - default is local server
LMSTUDIO_API_URL = os.environ.get("LMSTUDIO_API_URL", "http://localhost:1234/v1/chat/completions")

# Choose a model loaded in your LM Studio instance
MODEL_NAME = "default"  # LM Studio uses loaded model by default

# Your list of detailed input descriptions
input_descriptions = [
    "Rice - Blast: The image shows multiple leaves of a rice plant during the tillering stage. Many leaves exhibit diamond-shaped lesions, approximately 1-2 cm long, with grayish-white centers and distinct dark brown borders. Some lesions are merging, causing larger blighted areas. No insects are visible.",
    "Cotton - Bollworm: Close-up view of a developing cotton boll. Several small (<1cm), pinkish-white larvae are seen boring into the boll surface near the bracts. Small entry holes with some dark, granular frass (excrement) are visible. The surrounding leaves appear relatively healthy.",
    "Maize - Nitrogen Deficiency: Image displays the lower leaves of a young maize plant. The leaves show distinct yellowing starting at the leaf tip and progressing down the midrib in a characteristic V-shape pattern. The leaf margins remain relatively green initially. Upper leaves appear greener.",
    "Tomato - Early Blight: Several lower leaves of a mature tomato plant are shown. They exhibit circular to irregular dark brown lesions, 0.5-1.5 cm in diameter. Many lesions display characteristic concentric rings, giving a 'target board' appearance. Significant yellowing (chlorosis) surrounds the lesions, and some affected leaves are starting to wither.",
    "Wheat - Stripe Rust: Picture shows the upper leaves of a wheat plant nearing the flag leaf stage. Numerous small, bright yellow-orange pustules are arranged in distinct, long stripes running parallel to the leaf veins. When touched, a yellowish powder (spores) rubs off.",
    "Chili - Leaf Curl Virus: The image focuses on the growing tip of a chili plant. The young leaves are severely deformed, showing upward curling, puckering, and twisting. The leaves appear thickened and brittle, and veins are sometimes noticeably thicker. Plant growth appears stunted overall. Tiny whitefly insects may be subtly present but are not the primary focus.",
    "Groundnut - Tikka Disease (Leaf Spot): Several leaves of a groundnut plant are displayed. They are covered with numerous circular, dark brown to black spots, about 2-8 mm wide. Each spot is surrounded by a distinct yellow halo. Some older spots on lower leaves might lack the clear halo.",
    "Soybean - Healthy: Image shows a section of a healthy, vigorously growing soybean plant canopy during the vegetative stage. The leaves are uniformly deep green, fully expanded, and show no signs of spotting, yellowing, mosaic patterns, insect feeding, or wilting. Stems appear sturdy.",
    "Mango - Anthracnose on Fruit: A near-ripe mango fruit is shown. It displays several sunken, irregular-shaped black spots on the peel. Some spots appear to be coalescing into larger dark lesions. In humid conditions, pinkish spore masses might be visible in the center of older spots (though not clearly visible here).",
    "Sugarcane - Early Shoot Borer Damage: Focus is on the base of young sugarcane tillers (shoots). The central whorl of leaves is dried up, creating a characteristic \"dead heart\" symptom, which can be easily pulled out. Small bore holes may be visible near the base of the affected shoot.",
    "Potato - Late Blight: Image shows potato leaves with large, irregular, water-soaked lesions, often starting at the leaf margins or tips. The lesions rapidly turn dark brown to black. A fuzzy white fungal growth (sporangiophores) might be visible on the underside of the leaves near the edge of the lesions, especially in moist conditions.",
    "Brinjal (Eggplant) - Aphid Infestation: Close-up shows the underside of several young brinjal leaves and stems. They are heavily infested with clusters of small, pear-shaped insects, mostly greenish or blackish in color. Some shiny, sticky honeydew secretions might be visible on the leaf surfaces below the infestation.",
    "Okra (Lady's Finger) - Yellow Vein Mosaic Virus: The image shows several leaves of an okra plant. The veins of the leaves are prominently yellow, and the yellow network extends into the surrounding green leaf tissue, creating a distinct mosaic pattern. The leaves might be slightly reduced in size.",
    "Cabbage - Diamondback Moth Larvae: Several outer leaves of a cabbage head are shown. Small (around 1 cm), greenish larvae with a slightly tapered body are visible, actively feeding on the leaf tissue. They have created irregular holes or \"window panes\" (where only one layer of the leaf epidermis is left). Some silken threads might be present.",
    "Pigeon Pea (Tur/Arhar) - Pod Borer Damage: Image shows several developing pigeon pea pods. Some pods have distinct circular bore holes on the surface. One pod is broken open slightly, revealing a visible greenish or brownish larva feeding inside on the developing seeds. Frass might be present near the holes.",
    "Mustard - White Rust: Focus is on mustard leaves and potentially flower stalks. White, blister-like pustules, somewhat raised and initially smooth, are scattered on the underside of the leaves. Corresponding yellow spots may be visible on the upper leaf surface. Affected flower parts can become swollen and distorted.",
    "Apple - Powdery Mildew: Young leaves and shoot tips of an apple sapling are shown. They are covered with a characteristic white to grayish powdery fungal growth. Affected leaves may appear distorted, curled, or stunted.",
    "Grapes - Downy Mildew: Image displays the upper surface of grape leaves showing distinct, angular, yellowish-green spots (\"oil spots\"). On the underside of the leaf, corresponding to these spots, a white, downy fungal growth is visible, especially under humid conditions.",
    "Papaya - Mealybug Infestation: Close-up on the stem and leaf petioles of a papaya plant, especially near the growing point. Clusters of white, cottony masses are visible, covering small, oval, soft-bodied insects (mealybugs). Ants may also be present, attracted to the honeydew secreted by the mealybugs.",
    "Banana - Sigatoka Leaf Spot: Several mature banana leaves are shown. They exhibit numerous small, elliptical spots parallel to the leaf veins. Initially yellowish-green, the spots enlarge, become dark brown or black, and often develop a grayish center surrounded by a dark border and a yellow halo. Severe spotting leads to leaf necrosis."
]

OUTPUT_FILENAME = "agri_synthetic_data_generated_lmstudio.jsonl"
GENERATION_TEMPERATURE = 0.7
SLEEP_TIME_PER_API_CALL = 1  # LM Studio is local, so we can typically be a bit faster

# --- Prompt Template ---
single_prompt_template = """
You are an AI assistant generating fine-tuning data for an agricultural diagnosis chatbot.
Your task is to generate a response in a specific format based on the provided plant symptom description and the user's implied question style.

Follow these instructions STRICTLY:

1.  Analyze the User Question Style: Understand the level of detail requested by the user prompt ({user_question_style}).
2.  Analyze the Input Description: Carefully read the provided plant symptom description.
3.  Generate the Response: Create a helpful and accurate response that directly addresses the user's question style, based *only* on the information in the input description.
4.  Format the Output EXACTLY as specified below and make sure to include ALL the tags, especially the final <end_of_turn> tag:

<bos><start_of_turn>user
{user_question}
{input_description}<end_of_turn>
<start_of_turn>model
[YOUR GENERATED RESPONSE HERE BASED ON THE DESCRIPTION AND QUESTION STYLE]<end_of_turn>

IMPORTANT: Make sure your response includes all required tags, especially ending with <end_of_turn>

--- Input Data ---

User Question Style: {user_question_style}
User Question: {user_question}
Input Description:
{input_description}

--- Generate the Output Below ---
"""

# Define the different user question styles
user_prompts_for_style = {
     "detailed": "Analyze the provided description of plant symptoms and provide a detailed technical diagnosis and recommendations.",
     "short": "Briefly identify the problem shown in the description and give the main point.",
     "easy": "Explain what might be wrong based on this description, using simple words, and what I should do first."
}

# --- Load Existing Data ---
existing_texts = set()
if os.path.exists(OUTPUT_FILENAME):
    print(f"Loading existing entries from {OUTPUT_FILENAME} to avoid duplicates...")
    try:
        with open(OUTPUT_FILENAME, 'r', encoding='utf-8') as infile:
            for line in infile:
                try:
                    data = json.loads(line)
                    if 'text' in data:
                        existing_texts.add(data['text'])
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"  Skipping invalid line: {line.strip()} - Error: {e}")
        print(f"Loaded {len(existing_texts)} unique existing entries.")
    except Exception as e:
        print(f"Error loading existing file: {e}. Starting fresh.")
else:
    print(f"Output file {OUTPUT_FILENAME} not found. Starting fresh.")

# --- Main Generation Logic ---
total_entries_generated_this_run = 0
num_duplicates_skipped_this_run = 0
total_api_calls = len(input_descriptions) * len(user_prompts_for_style)
current_api_call = 0

print(f"\nStarting data generation for {len(input_descriptions)} descriptions...")
print(f"Will make {total_api_calls} individual API calls via LM Studio.")
print(f"Output will be appended to: {OUTPUT_FILENAME}")
print(f"Using LM Studio model: {MODEL_NAME}, Temperature: {GENERATION_TEMPERATURE}")
print(f"Pausing {SLEEP_TIME_PER_API_CALL} seconds between API calls.")

try:
    with open(OUTPUT_FILENAME, 'a', encoding='utf-8') as f:
        # Iterate through each description
        for i, description in enumerate(input_descriptions):
            print(f"\n--- Processing Description {i+1}/{len(input_descriptions)} ---")
            print(f"Input: {description[:100]}...") # Print snippet

            # Iterate through each prompt style for the current description
            for style_key, user_question in user_prompts_for_style.items():
                current_api_call += 1
                print(f"  Generating '{style_key}' style response ({current_api_call}/{total_api_calls})...")

                # Format the prompt
                pasted_desc_safe = description.replace('{', '{{').replace('}', '}}')
                formatted_prompt = single_prompt_template.format(
                    user_question_style=style_key,
                    user_question=user_question,
                    input_description=pasted_desc_safe
                )

                # Prepare payload for LM Studio API
                payload = {
                    "messages": [
                        {
                            "role": "user",
                            "content": formatted_prompt
                        }
                    ],
                    "temperature": GENERATION_TEMPERATURE,
                    "max_tokens": 2048,
                    "stream": False
                }

                # Call the LM Studio API (with retries)
                api_call_successful = False
                retry_count = 0
                max_retries = 3
                response_text = None
                
                while not api_call_successful and retry_count <= max_retries:
                    try:
                        print(f"    Sending request to LM Studio (Attempt {retry_count + 1})...")
                        start_time = time.time()

                        # Make the POST request to LM Studio
                        response = requests.post(
                            LMSTUDIO_API_URL,
                            json=payload,
                            headers={"Content-Type": "application/json"}
                        )

                        end_time = time.time()
                        print(f"    LM Studio API call took {end_time - start_time:.2f} seconds.")

                        # Check for HTTP errors
                        response.raise_for_status()

                        # Parse the JSON response
                        response_data = response.json()

                        # Extract response content (LM Studio format)
                        if response_data.get('choices') and len(response_data['choices']) > 0:
                            response_text = response_data['choices'][0]['message']['content']
                            print(f"    DEBUG - Last 50 chars of response: {response_text[-50:] if response_text else 'None'}")

                            # Check if response looks like expected format
                            if response_text and "<bos>" in response_text:
                                api_call_successful = True
                            else:
                                print("    WARNING: Received response doesn't contain '<bos>'. Might be malformed.")
                                print(f"    Raw Response Snippet: {response_text[:200]}...")
                                # Extract what looks like the format we want
                                if "<start_of_turn>" in response_text:
                                    # Try to extract just the formatted part
                                    pattern = r"<bos>.*?<end_of_turn>"
                                    match = re.search(pattern, response_text, re.DOTALL)
                                    if match:
                                        response_text = match.group(0)
                                        api_call_successful = True
                                        print("    Found partial match in response, extracted usable content.")
                                    else:
                                        raise ValueError("Response format incorrect")
                                else:
                                    raise ValueError("Response format incorrect")
                        else:
                            print("    WARNING: Received unexpected response structure from LM Studio.")
                            print(f"    Raw response data: {response_data}")
                            response_text = None
                            raise ValueError("Invalid LM Studio response structure")

                    except requests.exceptions.RequestException as e:
                        retry_count += 1
                        print(f"    ERROR during LM Studio API call (Attempt {retry_count}): {e}")
                        
                        wait_time = SLEEP_TIME_PER_API_CALL * (2 ** (retry_count - 1))

                        if retry_count > max_retries:
                            print(f"    Max retries reached for Description {i+1}, Style '{style_key}'. Skipping.")
                            response_text = None
                            break
                        print(f"    Retrying in {wait_time:.2f} seconds...")
                        time.sleep(wait_time)
                    except Exception as e:
                        retry_count += 1
                        print(f"    ERROR processing request/response (Attempt {retry_count}): {e}")
                        wait_time = SLEEP_TIME_PER_API_CALL * (2 ** (retry_count - 1))
                        if retry_count > max_retries:
                            print(f"    Max retries reached for Description {i+1}, Style '{style_key}'. Skipping.")
                            response_text = None
                            break
                        print(f"    Retrying in {wait_time:.2f} seconds...")
                        time.sleep(wait_time)

                # Process and Save Response
                if api_call_successful and response_text:
                    cleaned_text = response_text.strip()
                    print(f"    DEBUG - Response starts with: {cleaned_text[:50]}...")
                    print(f"    DEBUG - Response ends with: ...{cleaned_text[-50:]}")

                    # Ensure response has both starting and ending tags
                    if "<bos>" in cleaned_text:
                        # Check for end tag and add if missing
                        if "<end_of_turn>" not in cleaned_text:
                            print("    WARNING: Response missing <end_of_turn> tag. Adding it for consistency.")
                            cleaned_text = cleaned_text + "<end_of_turn>"
                        
                        # Check for duplicates
                        if cleaned_text not in existing_texts:
                            data_entry = {"text": cleaned_text}
                            json.dump(data_entry, f, ensure_ascii=False)
                            f.write('\n')
                            existing_texts.add(cleaned_text)
                            total_entries_generated_this_run += 1
                            print(f"    Saved 1 new entry for '{style_key}'.")
                        else:
                            num_duplicates_skipped_this_run += 1
                            print(f"    Skipped 1 duplicate entry for '{style_key}'.")
                    else:
                        print(f"    WARNING: Invalid format detected in final generated entry for '{style_key}'.")
                        print(f"    Failed validation. Raw text: {cleaned_text[:150]}...")

                elif not api_call_successful:
                    print(f"    Skipping save for '{style_key}' due to API call failures after retries.")

                # Rate Limiting Pause (after each API call)
                if current_api_call < total_api_calls:  # Don't sleep after the very last call
                    time.sleep(SLEEP_TIME_PER_API_CALL)

except KeyboardInterrupt:
    print("\n--- KeyboardInterrupt detected. Stopping script early. ---")
except Exception as e:
    print(f"\nAn unexpected error occurred outside the main loop: {e}")
    import traceback
    traceback.print_exc()

finally:
    print(f"\n--- Run Finished ---")
    print(f"Total API calls attempted: {current_api_call}")
    print(f"Entries generated in THIS run: {total_entries_generated_this_run}")
    print(f"Duplicates skipped in THIS run: {num_duplicates_skipped_this_run}")
    print(f"Total unique entries now in {OUTPUT_FILENAME}: {len(existing_texts)}")