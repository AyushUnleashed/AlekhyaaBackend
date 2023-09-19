import os

from chat_bot.gpt_bot import append_reply_to_chat_history, fetch_paid_openai_response,SYSTEM_PROMPT
from chat_bot.bot_choser import get_gpt_response
from clean_script import extract_visual_and_voiceover_arrays


def load_text_from_file(file_path):
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def prepare_llm_prompt(press_release_dump: str) -> str:
    # Prepare the prompt for LLM.
    llm_prompt = SYSTEM_PROMPT
    llm_prompt += press_release_dump
    return llm_prompt

def prepare_llm_prompt_paid(press_release_dump: str) -> str:
    llm_prompt = press_release_dump
    return llm_prompt



def get_script_from_press_release(press_release_dump: str):
    response = get_gpt_response(prepare_llm_prompt_paid(press_release_dump), paid=True)
    if response is None:
        print("Sever is down")
        return
    return response


def clean_script(video_script):
    # Call the extraction function
    visuals, voiceovers, cleaned_voiceover = extract_visual_and_voiceover_arrays(video_script)
    return cleaned_voiceover

def get_clean_text_for_t2s(file_path):
    file_contents = load_text_from_file(file_path)

    if file_contents:
        video_script = get_script_from_press_release(file_contents)
        cleaned_voiceover = clean_script(video_script)
        print("cleaned_voiceover:\n", cleaned_voiceover)

        if not os.path.exists('assets'):
            os.mkdir('assets')

        with open('assets/cleaned_voiceover.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(cleaned_voiceover)
        return cleaned_voiceover
    else:
        print("Failed to load file.")
        return None


if __name__ == "__main__":
    file_path = 'webpage_text.txt'  # Replace with the path to your text file
    get_clean_text_for_t2s(file_path)