import google.generativeai as genai
import os
import json
import time
import re
import math
import sys # To check for file existence and handle errors

# --- Configuration ---
API_KEY = "AIzaSyChwTleVWKrti4nQmFJAA5aFLuZPXYf7ds"
if not API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

MODEL_NAME = "gemini-1.5-flash-latest" # Or "gemini-1.5-pro-latest"

# Your list of detailed input descriptions (Keep the full list here)
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

OUTPUT_FILENAME = "agri_synthetic_data_generated.jsonl"
DESCRIPTIONS_PER_BATCH = 5
# Consider slightly higher temperature for variation across runs, but check quality
GENERATION_TEMPERATURE = 0.5
# Adjust sleep time based on API rate limits (seconds)
SLEEP_TIME_PER_API_CALL = 20

# --- Prompt Templates (Remain the same as previous script) ---
# template_detailed, template_short, template_easy...
template_detailed = """
You are an AI assistant generating synthetic fine-tuning data for an agricultural LLM (Gemma-3). You act as a **senior agricultural scientist**. You will be given {num_descriptions} distinct text descriptions simulating field observations. For **EACH** description, you must generate a corresponding **detailed and technically accurate** diagnosis and management strategy, formatted **exactly** as specified.

**INPUT DESCRIPTIONS:**
{input_descriptions_formatted}

**TASK:**
For **EACH** of the {num_descriptions} Input Descriptions provided above, generate a **single output string** strictly following the Gemma-3 format. The response part within each string should contain your detailed, technical diagnosis and recommendations based *only* on the corresponding Input Description.

**OUTPUT FORMAT (Generate one block containing all {num_descriptions} strings consecutively, separated by '---'):**
{output_format_structure}

**Formatting & Constraints:**
*   Generate **one single continuous block of text** containing all {num_descriptions} formatted `OUTPUT_STRING` sections.
*   Use `\\n---\\n` as a separator between each formatted string output.
*   Each of the {num_descriptions} output strings MUST individually adhere strictly to the `<bos>...<end_of_turn>` structure.
*   Ensure the correct description is pasted inside the user turn for each corresponding output string.
*   Base diagnosis/recommendations ONLY on the corresponding Input Description.
*   Responses should be thorough and use appropriate technical terms.
*   Do NOT add any extra text outside this structure.
--- Produce only the final formatted block based on the Input Descriptions. ---
"""
template_short = """
You are an AI assistant generating synthetic fine-tuning data for an agricultural LLM (Gemma-3). You act as a **quick diagnostic assistant**. You will be given {num_descriptions} distinct text descriptions simulating field observations. For **EACH** description, you must generate a corresponding **very brief identification** and key point, formatted **exactly** as specified.

**INPUT DESCRIPTIONS:**
{input_descriptions_formatted}

**TASK:**
For **EACH** of the {num_descriptions} Input Descriptions provided above, generate a **single output string** strictly following the Gemma-3 format. The response part within each string should contain your extremely concise identification and key point/action (1-3 sentences max) based *only* on the corresponding Input Description.

**OUTPUT FORMAT (Generate one block containing all {num_descriptions} strings consecutively, separated by '---'):**
{output_format_structure}

**Formatting & Constraints:**
*   Generate **one single continuous block of text** containing all {num_descriptions} formatted `OUTPUT_STRING` sections.
*   Use `\\n---\\n` as a separator between each formatted string output.
*   Each of the {num_descriptions} output strings MUST individually adhere strictly to the `<bos>...<end_of_turn>` structure.
*   Ensure the correct description is pasted inside the user turn for each corresponding output string.
*   Base identification ONLY on the corresponding Input Description.
*   Responses should be extremely concise.
*   Do NOT add any extra text outside this structure.
--- Produce only the final formatted block based on the Input Descriptions. ---
"""
template_easy = """
You are an AI assistant generating synthetic fine-tuning data for an agricultural LLM (Gemma-3). You act as a **friendly local agricultural advisor**. You will be given {num_descriptions} distinct text descriptions simulating field observations. For **EACH** description, you must generate a corresponding explanation and recommendation in **simple, easy-to-understand language**, formatted **exactly** as specified.

**INPUT DESCRIPTIONS:**
{input_descriptions_formatted}

**TASK:**
For **EACH** of the {num_descriptions} Input Descriptions provided above, generate a **single output string** strictly following the Gemma-3 format. The response part within each string should explain the likely problem and suggest first steps in **simple, non-technical language** suitable for an Indian farmer, based *only* on the corresponding Input Description.

**OUTPUT FORMAT (Generate one block containing all {num_descriptions} strings consecutively, separated by '---'):**
{output_format_structure}

**Formatting & Constraints:**
*   Generate **one single continuous block of text** containing all {num_descriptions} formatted `OUTPUT_STRING` sections.
*   Use `\\n---\\n` as a separator between each formatted string output.
*   Each of the {num_descriptions} output strings MUST individually adhere strictly to the `<bos>...<end_of_turn>` structure.
*   Ensure the correct description is pasted inside the user turn for each corresponding output string.
*   Base explanation ONLY on the corresponding Input Description.
*   Use simple phrasing, avoid jargon.
*   Do NOT add any extra text outside this structure.
--- Produce only the final formatted block based the Input Descriptions. ---
"""
templates = { "detailed": template_detailed, "short": template_short, "easy": template_easy }
user_prompts_for_template = {
     "detailed": "Analyze the provided description of plant symptoms and provide a detailed technical diagnosis and recommendations.",
     "short": "Briefly identify the problem shown in the description and give the main point.",
     "easy": "Explain what might be wrong based on this description, using simple words, and what I should do first."
}

# --- Helper Function (Remains the same) ---
# format_prompt_for_batch function... (kept concise for brevity, same as before)

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
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

generation_config = genai.GenerationConfig(
    temperature=GENERATION_TEMPERATURE,
    # Add other parameters if needed
)
safety_settings = [ # Adjust as needed
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

total_entries_generated_this_run = 0
num_duplicates_skipped_this_run = 0
num_batches = math.ceil(len(input_descriptions) / DESCRIPTIONS_PER_BATCH)

print(f"\nStarting data generation for {len(input_descriptions)} descriptions...")
print(f"Will process in {num_batches} batches of up to {DESCRIPTIONS_PER_BATCH}.")
print(f"Output will be appended to: {OUTPUT_FILENAME}")
print(f"Using model: {MODEL_NAME}, Temperature: {GENERATION_TEMPERATURE}")
print(f"Pausing {SLEEP_TIME_PER_API_CALL} seconds between API calls.")

try:
    # Open file in append mode
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

                # --- Format the prompt (using the same logic as previous script) ---
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

                # --- Call the API (with retries) ---
                # (API call logic with retries remains the same as previous script)
                api_call_successful = False
                retry_count = 0
                max_retries = 2
                response_text = None # Initialize response_text
                while not api_call_successful and retry_count <= max_retries:
                    try:
                        print(f"    Sending request to Gemini (Attempt {retry_count + 1})...")
                        response = model.generate_content(
                            formatted_prompt,
                            generation_config=generation_config,
                            safety_settings=safety_settings
                        )
                        # Check for empty response or potential errors in the response object itself
                        if response.parts:
                             response_text = response.text
                        else:
                             # Handle cases where the response might be blocked or empty
                             print("    WARNING: Received response with no processable parts. Checking prompt feedback.")
                             if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                                 print(f"    Prompt Feedback: {response.prompt_feedback}")
                             response_text = None # Treat as failure for processing
                             # Decide if this is a retryable error or skip
                             if response.prompt_feedback and response.prompt_feedback.block_reason:
                                  print("      Response blocked, skipping.")
                                  break # Exit retry loop for blocked content
                             else:
                                 print("      Empty response, retrying...")


                        # If response_text is valid, mark successful
                        if response_text:
                            api_call_successful = True
                        elif not api_call_successful and retry_count < max_retries: # Only retry if not blocked and retries left
                            raise ValueError("Empty or non-text response part received") # Trigger retry
                        elif not api_call_successful: # Max retries reached or blocked
                             break # Exit retry loop

                    except Exception as e:
                        retry_count += 1
                        print(f"    ERROR during API call (Attempt {retry_count}): {e}")
                        if retry_count > max_retries:
                            print("    Max retries reached. Skipping this batch/template.")
                            response_text = None
                            break
                        print(f"    Retrying in {SLEEP_TIME_PER_API_CALL} seconds...")
                        time.sleep(SLEEP_TIME_PER_API_CALL)

                # --- Process and Save Response (with duplicate check) ---
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
                                # *** Check for duplicates ***
                                if cleaned_text not in existing_texts:
                                    data_entry = {"text": cleaned_text}
                                    json.dump(data_entry, f, ensure_ascii=False)
                                    f.write('\n')
                                    existing_texts.add(cleaned_text) # Add to set *after* writing
                                    total_entries_generated_this_run += 1
                                    generated_count_in_batch += 1
                                else:
                                    num_duplicates_skipped_this_run += 1
                                    skipped_count_in_batch += 1
                                    # print(f"    Skipped duplicate entry.") # Optional: uncomment for verbose logging
                            else:
                                print(f"    WARNING: Invalid format detected in generated entry part:\n{cleaned_text[:100]}...")
                        print(f"    Processed batch for '{template_key}': Saved {generated_count_in_batch} new entries, Skipped {skipped_count_in_batch} duplicates.")
                    else:
                         print(f"    WARNING: Expected {actual_batch_size} parts but got {len(split_parts)} for '{template_key}'. Skipping save for this malformed batch response.")
                         print(f"    Raw response snippet:\n{response_text[:500]}...")

                elif api_call_successful and not response_text:
                     print("    WARNING: API call successful but received empty/blocked response, no entries saved.")
                # else: (Handled by retry loop failure message)
                #    pass

                # --- Rate Limiting Pause ---
                print(f"    Pausing for {SLEEP_TIME_PER_API_CALL} seconds...")
                time.sleep(SLEEP_TIME_PER_API_CALL)

except Exception as e:
    print(f"\nAn unexpected error occurred outside the main loop: {e}")
    import traceback
    traceback.print_exc() # Print full traceback for debugging

finally:
    print(f"\n--- Run Finished ---")
    print(f"Entries generated in THIS run: {total_entries_generated_this_run}")
    print(f"Duplicates skipped in THIS run: {num_duplicates_skipped_this_run}")
    print(f"Total unique entries now in {OUTPUT_FILENAME}: {len(existing_texts)}") # Reflects total after run completion