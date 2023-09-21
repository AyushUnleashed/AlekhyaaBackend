# Import modules
from fastapi import FastAPI, Query
import requests, json

# Create FastAPI app
app = FastAPI()

# Define API route
@app.get("/api/imagesearch")
def image_search(query: str): # Change this line
    # Check if query is valid
    if not query:
        return {"error": "Please provide a query parameter"}
    # Construct GET request to Custom Search JSON API
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": "AIzaSyCsWAb0PSkUA_hdU8BHwcw_RwxtrBPo2tY",
        "cx": "60e8c83068bc84aeb",
        "q": query, # Query parameter from user
        "searchType": "image",
        "num": 10
    }
    response = requests.get(url, params=params)
    # Check if response is valid
    if response.status_code != 200:
        return {"error": response.json().get("error")}
    # Parse JSON response and extract relevant information
    data = response.json()
    items = data.get("items")
    results = []
    for item in items:
        result = {
            "image_url": item.get("link"),
            "title": item.get("title"),
        }
        results.append(result)
        
    # Create a JSON output file from the results
    with open("results.json", "w") as outfile:
        json.dump(results, outfile)

    # Return results as JSON object
    return {"results": results}

# Add this part to ask for user input and run the function
while True: # Start a loop
    query = input("Enter a query for image search or type 'exit' to quit: ") # Prompt the user for a query or exit command
    if query.lower() == "exit": # Check if the user wants to exit
        print("Bye!")
        break # Break the loop and end the program
    else: # Otherwise, run the function with the query
        print(image_search(query))
