from groq import Groq # Import Groq library
import os
import json
import time
import re
import math
import sys

# --- Configuration ---
# !!! GET YOUR API KEY FROM console.groq.com !!!
API_KEY = "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"
if not API_KEY:
    raise ValueError("Please set the GROQ_API_KEY environment variable.")

# Choose a Groq model (Check console.groq.com for available models)
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"  # Powerful Llama 3 model
# Other options: "mixtral-8x7b-32768", "gemma-7b-it"

# Your list of detailed input descriptions (Paste the 20 descriptions here)
input_descriptions = [
    # === PASTE THE 20 DESCRIPTIONS FROM THE PREVIOUS ANSWER HERE ===
        """Rice - Blast: The image shows multiple leaves of a rice plant during the tillering stage. Many leaves exhibit diamond-shaped lesions, approximately 1-2 cm long, with grayish-white centers and distinct dark brown borders. Some lesions are merging, causing larger blighted areas. No insects are visible.
Cotton - Bollworm: Close-up view of a developing cotton boll. Several small (<1cm), pinkish-white larvae are seen boring into the boll surface near the bracts. Small entry holes with some dark, granular frass (excrement) are visible. The surrounding leaves appear relatively healthy.
Maize - Nitrogen Deficiency: Image displays the lower leaves of a young maize plant. The leaves show distinct yellowing starting at the leaf tip and progressing down the midrib in a characteristic V-shape pattern. The leaf margins remain relatively green initially. Upper leaves appear greener.
Tomato - Early Blight: Several lower leaves of a mature tomato plant are shown. They exhibit circular to irregular dark brown lesions, 0.5-1.5 cm in diameter. Many lesions display characteristic concentric rings, giving a 'target board' appearance. Significant yellowing (chlorosis) surrounds the lesions, and some affected leaves are starting to wither.
Wheat - Stripe Rust: Picture shows the upper leaves of a wheat plant nearing the flag leaf stage. Numerous small, bright yellow-orange pustules are arranged in distinct, long stripes running parallel to the leaf veins. When touched, a yellowish powder (spores) rubs off.
Chili - Leaf Curl Virus: The image focuses on the growing tip of a chili plant. The young leaves are severely deformed, showing upward curling, puckering, and twisting. The leaves appear thickened and brittle, and veins are sometimes noticeably thicker. Plant growth appears stunted overall. Tiny whitefly insects may be subtly present but are not the primary focus.
Groundnut - Tikka Disease (Leaf Spot): Several leaves of a groundnut plant are displayed. They are covered with numerous circular, dark brown to black spots, about 2-8 mm wide. Each spot is surrounded by a distinct yellow halo. Some older spots on lower leaves might lack the clear halo.
Soybean - Healthy: Image shows a section of a healthy, vigorously growing soybean plant canopy during the vegetative stage. The leaves are uniformly deep green, fully expanded, and show no signs of spotting, yellowing, mosaic patterns, insect feeding, or wilting. Stems appear sturdy.
Mango - Anthracnose on Fruit: A near-ripe mango fruit is shown. It displays several sunken, irregular-shaped black spots on the peel. Some spots appear to be coalescing into larger dark lesions. In humid conditions, pinkish spore masses might be visible in the center of older spots (though not clearly visible here).
Sugarcane - Early Shoot Borer Damage: Focus is on the base of young sugarcane tillers (shoots). The central whorl of leaves is dried up, creating a characteristic "dead heart" symptom, which can be easily pulled out. Small bore holes may be visible near the base of the affected shoot.
Potato - Late Blight: Image shows potato leaves with large, irregular, water-soaked lesions, often starting at the leaf margins or tips. The lesions rapidly turn dark brown to black. A fuzzy white fungal growth (sporangiophores) might be visible on the underside of the leaves near the edge of the lesions, especially in moist conditions.
Brinjal (Eggplant) - Aphid Infestation: Close-up shows the underside of several young brinjal leaves and stems. They are heavily infested with clusters of small, pear-shaped insects, mostly greenish or blackish in color. Some shiny, sticky honeydew secretions might be visible on the leaf surfaces below the infestation.
Okra (Lady's Finger) - Yellow Vein Mosaic Virus: The image shows several leaves of an okra plant. The veins of the leaves are prominently yellow, and the yellow network extends into the surrounding green leaf tissue, creating a distinct mosaic pattern. The leaves might be slightly reduced in size.
Cabbage - Diamondback Moth Larvae: Several outer leaves of a cabbage head are shown. Small (around 1 cm), greenish larvae with a slightly tapered body are visible, actively feeding on the leaf tissue. They have created irregular holes or "window panes" (where only one layer of the leaf epidermis is left). Some silken threads might be present.
Pigeon Pea (Tur/Arhar) - Pod Borer Damage: Image shows several developing pigeon pea pods. Some pods have distinct circular bore holes on the surface. One pod is broken open slightly, revealing a visible greenish or brownish larva feeding inside on the developing seeds. Frass might be present near the holes.
Mustard - White Rust: Focus is on mustard leaves and potentially flower stalks. White, blister-like pustules, somewhat raised and initially smooth, are scattered on the underside of the leaves. Corresponding yellow spots may be visible on the upper leaf surface. Affected flower parts can become swollen and distorted.
Apple - Powdery Mildew: Young leaves and shoot tips of an apple sapling are shown. They are covered with a characteristic white to grayish powdery fungal growth. Affected leaves may appear distorted, curled, or stunted.
Grapes - Downy Mildew: Image displays the upper surface of grape leaves showing distinct, angular, yellowish-green spots ("oil spots"). On the underside of the leaf, corresponding to these spots, a white, downy fungal growth is visible, especially under humid conditions.
Papaya - Mealybug Infestation: Close-up on the stem and leaf petioles of a papaya plant, especially near the growing point. Clusters of white, cottony masses are visible, covering small, oval, soft-bodied insects (mealybugs). Ants may also be present, attracted to the honeydew secreted by the mealybugs.
Banana - Sigatoka Leaf Spot: Several mature banana leaves are shown. They exhibit numerous small, elliptical spots parallel to the leaf veins. Initially yellowish-green, the spots enlarge, become dark brown or black, and often develop a grayish center surrounded by a dark border and a yellow halo. Severe spotting leads to leaf necrosis.
""",
    "The image shows multiple leaves of a rice plant during the tillering stage. Many leaves exhibit diamond-shaped lesions, approximately 1-2 cm long, with grayish-white centers and distinct dark brown borders. Some lesions are merging, causing larger blighted areas. No insects are visible.",
    "Close-up view of a developing cotton boll. Several small (<1cm), pinkish-white larvae are seen boring into the boll surface near the bracts. Small entry holes with some dark, granular frass (excrement) are visible. The surrounding leaves appear relatively healthy.",
    "Image displays the lower leaves of a young maize plant. The leaves show distinct yellowing starting at the leaf tip and progressing down the midrib in a characteristic V-shape pattern. The leaf margins remain relatively green initially. Upper leaves appear greener.",
    "Several lower leaves of a mature tomato plant are shown. They exhibit circular to irregular dark brown lesions, 0.5-1.5 cm in diameter. Many lesions display characteristic concentric rings, giving a 'target board' appearance. Significant yellowing (chlorosis) surrounds the lesions, and some affected leaves are starting to wither.",
    "Picture shows the upper leaves of a wheat plant nearing the flag leaf stage. Numerous small, bright yellow-orange pustules are arranged in distinct, long stripes running parallel to the leaf veins. When touched, a yellowish powder (spores) rubs off.",
    "The image focuses on the growing tip of a chili plant. The young leaves are severely deformed, showing upward curling, puckering, and twisting. The leaves appear thickened and brittle, and veins are sometimes noticeably thicker. Plant growth appears stunted overall. Tiny whitefly insects may be subtly present but are not the primary focus.",
    "Several leaves of a groundnut plant are displayed. They are covered with numerous circular, dark brown to black spots, about 2-8 mm wide. Each spot is surrounded by a distinct yellow halo. Some older spots on lower leaves might lack the clear halo.",
    "Image shows a section of a healthy, vigorously growing soybean plant canopy during the vegetative stage. The leaves are uniformly deep green, fully expanded, and show no signs of spotting, yellowing, mosaic patterns, insect feeding, or wilting. Stems appear sturdy.",
    "A near-ripe mango fruit is shown. It displays several sunken, irregular-shaped black spots on the peel. Some spots appear to be coalescing into larger dark lesions. In humid conditions, pinkish spore masses might be visible in the center of older spots (though not clearly visible here).",
    "Focus is on the base of young sugarcane tillers (shoots). The central whorl of leaves is dried up, creating a characteristic \"dead heart\" symptom, which can be easily pulled out. Small bore holes may be visible near the base of the affected shoot.",
    "Image shows potato leaves with large, irregular, water-soaked lesions, often starting at the leaf margins or tips. The lesions rapidly turn dark brown to black. A fuzzy white fungal growth (sporangiophores) might be visible on the underside of the leaves near the edge of the lesions, especially in moist conditions.",
    "Close-up shows the underside of several young brinjal leaves and stems. They are heavily infested with clusters of small, pear-shaped insects, mostly greenish or blackish in color. Some shiny, sticky honeydew secretions might be visible on the leaf surfaces below the infestation.",
    "The image shows several leaves of an okra plant. The veins of the leaves are prominently yellow, and the yellow network extends into the surrounding green leaf tissue, creating a distinct mosaic pattern. The leaves might be slightly reduced in size.",
    "Several outer leaves of a cabbage head are shown. Small (around 1 cm), greenish larvae with a slightly tapered body are visible, actively feeding on the leaf tissue. They have created irregular holes or \"window panes\" (where only one layer of the leaf epidermis is left). Some silken threads might be present.",
    "Image shows several developing pigeon pea pods. Some pods have distinct circular bore holes on the surface. One pod is broken open slightly, revealing a visible greenish or brownish larva feeding inside on the developing seeds. Frass might be present near the holes.",
    "Focus is on mustard leaves and potentially flower stalks. White, blister-like pustules, somewhat raised and initially smooth, are scattered on the underside of the leaves. Corresponding yellow spots may be visible on the upper leaf surface. Affected flower parts can become swollen and distorted.",
    "Young leaves and shoot tips of an apple sapling are shown. They are covered with a characteristic white to grayish powdery fungal growth. Affected leaves may appear distorted, curled, or stunted.",
    "Image displays the upper surface of grape leaves showing distinct, angular, yellowish-green spots (\"oil spots\"). On the underside of the leaf, corresponding to these spots, a white, downy fungal growth is visible, especially under humid conditions.",
    "Close-up on the stem and leaf petioles of a papaya plant, especially near the growing point. Clusters of white, cottony masses are visible, covering small, oval, soft-bodied insects (mealybugs). Ants may also be present, attracted to the honeydew secreted by the mealybugs.",
    "Several mature banana leaves are shown. They exhibit numerous small, elliptical spots parallel to the leaf veins. Initially yellowish-green, the spots enlarge, become dark brown or black, and often develop a grayish center surrounded by a dark border and a yellow halo. Severe spotting leads to leaf necrosis."
    # === END OF DESCRIPTION LIST ===
]

OUTPUT_FILENAME = "agri_synthetic_data_generated_groq.jsonl" # Changed filename
DESCRIPTIONS_PER_BATCH = 5
# Consider slightly higher temperature for variation across runs, but check quality
GENERATION_TEMPERATURE = 0.7 # Groq defaults often work well
# Adjust sleep time based on API rate limits (Groq free tier limits are per day/week/month often)
SLEEP_TIME_PER_API_CALL = 5 # Groq is fast, but API limits still apply. Start low and increase if needed.

# --- Prompt Templates (Remain the same conceptually) ---
# template_detailed, template_short, template_easy...
# (These template strings remain identical to the previous script)
template_detailed = """... (same as before) ..."""
template_short = """... (same as before) ..."""
template_easy = """... (same as before) ..."""
templates = { "detailed": template_detailed, "short": template_short, "easy": template_easy }
user_prompts_for_template = {
     "detailed": "Analyze the provided description of plant symptoms and provide a detailed technical diagnosis and recommendations.",
     "short": "Briefly identify the problem shown in the description and give the main point.",
     "easy": "Explain what might be wrong based on this description, using simple words, and what I should do first."
}


# --- Load Existing Data (Remains the same) ---
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
client = Groq(api_key=API_KEY) # Instantiate Groq client

total_entries_generated_this_run = 0
num_duplicates_skipped_this_run = 0
num_batches = math.ceil(len(input_descriptions) / DESCRIPTIONS_PER_BATCH)

print(f"\nStarting data generation for {len(input_descriptions)} descriptions...")
print(f"Will process in {num_batches} batches of up to {DESCRIPTIONS_PER_BATCH}.")
print(f"Output will be appended to: {OUTPUT_FILENAME}")
print(f"Using Groq model: {MODEL_NAME}, Temperature: {GENERATION_TEMPERATURE}")
print(f"Pausing {SLEEP_TIME_PER_API_CALL} seconds between API calls.")

try:
    with open(OUTPUT_FILENAME, 'a', encoding='utf-8') as f:
        for i in range(num_batches):
            start_index = i * DESCRIPTIONS_PER_BATCH
            end_index = start_index + DESCRIPTIONS_PER_BATCH
            batch_descriptions = input_descriptions[start_index:end_index]
            actual_batch_size = len(batch_descriptions)

            print(f"\n--- Processing Batch {i+1}/{num_batches} ({actual_batch_size} descriptions) ---")

            if not batch_descriptions:
                print("Skipping empty batch.")
                continue

            for template_key in templates.keys():
                print(f"  Generating '{template_key}' style responses...")

                # --- Format the prompt ---
                # (Formatting logic remains the same as previous script)
                formatted_prompt = ""
                input_desc_block = ""
                output_struct_block = ""
                user_prompt = user_prompts_for_template[template_key]
                for idx, desc in enumerate(batch_descriptions, 1):
                     input_desc_block += f"INPUT_DESCRIPTION_{idx}:\n{desc}\n\n"
                     pasted_desc_safe = desc.replace('`', r'\`').replace('{', '{{').replace('}', '}}')
                     output_struct_block += f"OUTPUT_STRING_{idx}:\n"
                     output_struct_block += f"<bos><start_of_turn>user\n{user_prompt}\n{pasted_desc_safe}<end_of_turn>\n<start_of_turn>model\n[MODEL'S RESPONSE FOR DESCRIPTION {idx} HERE]<end_of_turn>\n"
                     if idx < actual_batch_size:
                         output_struct_block += "---\n"
                formatted_prompt = templates[template_key].format(
                    num_descriptions=actual_batch_size,
                    input_descriptions_formatted=input_desc_block.strip(),
                    output_format_structure=output_struct_block.strip()
                 )

                # --- Structure messages for Groq API ---
                messages = [
                    # Optional system prompt (can help set context)
                    # {
                    #     "role": "system",
                    #     "content": "You are an AI assistant generating synthetic fine-tuning data..."
                    # },
                    {
                        "role": "user",
                        "content": formatted_prompt # The entire detailed instruction set goes here
                    }
                ]

                # --- Call the Groq API (with retries) ---
                api_call_successful = False
                retry_count = 0
                max_retries = 2
                response_text = None
                while not api_call_successful and retry_count <= max_retries:
                    try:
                        print(f"    Sending request to Groq (Attempt {retry_count + 1})...")
                        chat_completion = client.chat.completions.create(
                            messages=messages,
                            model=MODEL_NAME,
                            temperature=GENERATION_TEMPERATURE,
                            # max_tokens=4096, # Optional: Specify max output tokens if needed
                            # top_p=..., # Optional
                        )
                        # Extract response content
                        if chat_completion.choices and chat_completion.choices[0].message:
                            response_text = chat_completion.choices[0].message.content
                            api_call_successful = True
                        else:
                           # Handle unexpected empty or malformed response from Groq
                           print("    WARNING: Received unexpected response structure from Groq.")
                           print(f"    Raw completion object: {chat_completion}")
                           response_text = None
                           raise ValueError("Invalid Groq response structure") # Trigger retry

                    except Exception as e:
                        retry_count += 1
                        print(f"    ERROR during Groq API call (Attempt {retry_count}): {e}")
                        if retry_count > max_retries:
                            print("    Max retries reached. Skipping this batch/template.")
                            response_text = None
                            break
                        print(f"    Retrying in {SLEEP_TIME_PER_API_CALL} seconds...")
                        time.sleep(SLEEP_TIME_PER_API_CALL)


                # --- Process and Save Response (with duplicate check) ---
                # (This logic remains identical to the previous script)
                if api_call_successful and response_text:
                    split_parts = re.split(r'\n---\n', response_text.strip())
                    generated_count_in_batch = 0
                    skipped_count_in_batch = 0

                    if len(split_parts) == actual_batch_size:
                        for entry_text in split_parts:
                            cleaned_text = entry_text.strip()
                            if cleaned_text.startswith("OUTPUT_STRING_"):
                                cleaned_text = cleaned_text.split('\n', 1)[-1].strip()

                            if cleaned_text.startswith("<bos>") and cleaned_text.endswith("<end_of_turn>"):
                                if cleaned_text not in existing_texts:
                                    data_entry = {"text": cleaned_text}
                                    json.dump(data_entry, f, ensure_ascii=False)
                                    f.write('\n')
                                    existing_texts.add(cleaned_text)
                                    total_entries_generated_this_run += 1
                                    generated_count_in_batch += 1
                                else:
                                    num_duplicates_skipped_this_run += 1
                                    skipped_count_in_batch += 1
                            else:
                                print(f"    WARNING: Invalid format detected in generated entry part:\n{cleaned_text[:100]}...")
                        print(f"    Processed batch for '{template_key}': Saved {generated_count_in_batch} new entries, Skipped {skipped_count_in_batch} duplicates.")
                    else:
                         print(f"    WARNING: Expected {actual_batch_size} parts but got {len(split_parts)} for '{template_key}'. Skipping save for this malformed batch response.")
                         print(f"    Raw response snippet:\n{response_text[:500]}...")

                elif api_call_successful and not response_text:
                     print("    WARNING: API call successful but received empty response, no entries saved.")
                # else: No need for else, handled by retry logic

                # --- Rate Limiting Pause ---
                print(f"    Pausing for {SLEEP_TIME_PER_API_CALL} seconds...")
                time.sleep(SLEEP_TIME_PER_API_CALL)

except Exception as e:
    print(f"\nAn unexpected error occurred outside the main loop: {e}")
    import traceback
    traceback.print_exc()

finally:
    print(f"\n--- Run Finished ---")
    print(f"Entries generated in THIS run: {total_entries_generated_this_run}")
    print(f"Duplicates skipped in THIS run: {num_duplicates_skipped_this_run}")
    print(f"Total unique entries now in {OUTPUT_FILENAME}: {len(existing_texts)}")