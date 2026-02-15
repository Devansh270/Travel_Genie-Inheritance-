from fastapi import FastAPI
from pydantic import BaseModel
import torch

app = FastAPI()

# These will hold our model and tokenizer once the app starts.
# Keeping them global so we load the model only once (not on every request).
model = None
tokenizer = None


# ----------- Load Model Safely on Startup -----------
@app.on_event("startup")
def load_model():
    """
    This runs automatically when the FastAPI app starts.
    We try to load the model here so that it's ready before
    any request hits the /chat endpoint.
    """
    global model, tokenizer
    try:
        # Importing inside the function to avoid circular import issues
        # and to make sure it only loads during startup.
        from .model import model as loaded_model, tokenizer as loaded_tokenizer
        
        model = loaded_model
        tokenizer = loaded_tokenizer
        
        print("Model loaded successfully.")
    except Exception as e:
        # If something goes wrong, we log the error.
        # The app will still run, but model-based features won’t work.
        print(" Model failed to load:", e)


# ----------- Request Schema -----------
class Query(BaseModel):
    # This defines the structure of the incoming JSON request.
    # Example:
    # {
    #   "query": "Plan a 3-day trip to Paris under 20000"
    # }
    query: str


# ----------- LLM Function -----------
def call_llm(prompt):
    """
    Sends the constructed prompt to the loaded model
    and returns the generated response.
    """
    
    # If model isn't available, return a friendly warning.
    if model is None or tokenizer is None:
        return "backend/python_service/app.pyModel not loaded."

    # Convert text prompt into tensor inputs for the model.
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Disable gradient calculation since we are only doing inference.
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=200,      # limit response length
            temperature=0.4,         # lower temperature = more controlled output
            do_sample=True,          # enable sampling for variation
            repetition_penalty=1.2,  # helps avoid repeating phrases
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    # Convert generated tokens back to readable text.
    return tokenizer.decode(out[0], skip_special_tokens=True)


# ----------- Chat Endpoint -----------
@app.post("/chat")
def chat_endpoint(payload: Query):
    """
    Main API endpoint.
    Takes user query, extracts structured data,
    generates itinerary, and enhances it using LLM.
    """
    query = payload.query

    # If model failed to load, return a basic mock response.
    # This helps during testing so the frontend doesn't break.
    if model is None:
        return {
            "city": "TestCity",
            "days": 3,
            "itinerary": f"Test response for: {query}"
        }

    # Importing helper functions only when needed.
    # This keeps startup lightweight and avoids unnecessary imports.
    from .helpers import (
        extract_city,
        extract_days,
        extract_budget,
        extract_category,
        generate_itinerary,
        format_itinerary
    )

    # Step 1: Extract structured information from user query.
    city = extract_city(query)
    if not city:
        # If city is missing, we can't proceed.
        return {"error": "City not specified"}

    days = extract_days(query)
    budget = extract_budget(query)
    category = extract_category(query)

    # Step 2: Generate a base itinerary using filtered dataset.
    itin_df = generate_itinerary(city, days, budget, category)

    # Convert dataframe into a readable text format
    # that we can pass to the language model.
    base_itin = format_itinerary(itin_df)

    # Step 3: Construct the final prompt for the LLM.
    # Important: We restrict it to ONLY use places from our dataset.
    prompt = f"""
    You are a travel itinerary generator.
    City: {city}
    Days: {days}
    Use ONLY these places:
    {base_itin}
    """

    # Step 4: Return structured response.
    return {
        "city": city,
        "days": days,
        "itinerary": call_llm(prompt)
    }