import re
def extract_visual_and_voiceover_arrays(text):
    try:
        visual_matches = re.findall(r'\[(?:\s*(?:\w+\s+)*?)?Visual:\s*(.*?)\]\s*Voiceover:\s*(.*?)\n', text, re.DOTALL)

        visuals = []
        voiceovers = []

        for visual, voiceover in visual_matches:
            visuals.append(visual.strip())
            voiceovers.append(voiceover.strip())

        # Create a single cleaned voiceover string by joining all voiceovers
        cleaned_voiceover = '\n\n'.join(voiceovers)

        return visuals,voiceovers,cleaned_voiceover

    except Exception as e:
        print(f"Error while extract_visual_and_voiceover_arrays: {str(e)}")
        raise e



def main():
    # Input text
    input_text = """
    [Opening Visual: Aerial view of Raipur, Chhattisgarh]
    Voiceover: In a significant development, the fourth and final meeting of the G20 Framework Working Group, under the Indian G20 Presidency, successfully concluded today in the vibrant city of Raipur, Chhattisgarh.
    
    [Visual: Representatives from G20 countries gathered for the meeting]
    Voiceover: This two-day meeting, held on the 18th and 19th of September 2023, was co-chaired by Ms. Chandni Raina, Adviser, Ministry of Finance, Government of India, and Ms. Sam Beckett, Chief Economic Adviser, HM Treasury, UK. It witnessed the participation of approximately 65 delegates from G20 member countries, invitee countries, and various international and regional organizations.
    
    [Visual: Representatives from G20 countries gathered for the meeting]
    Voiceover: This two-day meeting, held on the 18th and 19th of September 2023, was co-chaired by Ms. Chandni Raina, Adviser, Ministry of Finance, Government of India, and Ms. Sam Beckett, Chief Economic Adviser, HM Treasury, UK. It witnessed the participation of approximately 65 delegates from G20 member countries, invitee countries, and various international and regional organizations.
    
    [Closing Visual: G20 Logo]
    Voiceover: For more updates on this and other significant events, stay tuned to Alekhyaa. Don't forget to like, share, and subscribe for the latest news and insights. Thank you for watching.
    """

    # Call the extraction function
    visuals, voiceovers, cleaned_voiceover = extract_visual_and_voiceover_arrays(input_text)

    # Print the results

    print("Cleaned Voiceover:", cleaned_voiceover)

    # for i in range(len(visuals)):
    #     print("Visual:", visuals[i])
    #     print("Voiceover:", voiceovers[i])

if __name__ == "__main__":
    main()



