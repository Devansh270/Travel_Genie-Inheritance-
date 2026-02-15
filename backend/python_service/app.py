from fastapi import FastAPI
from pydantic import BaseModel
import torch

app = FastAPI()

# Global placeholders
model = None
tokenizer = None

# ----------- Load Model Safely on Startup -----------

@app.on_event("startup")
def load_model():
    global model, tokenizer
    try:
        from .model import model as loaded_model, tokenizer as loaded_tokenizer
        model = loaded_model
        tokenizer = loaded_tokenizer
        print("✅ Model loaded successfully.")
    except Exception as e:
        print("❌ Model failed to load:", e)


# ----------- Request Schema -----------

class Query(BaseModel):
    query: str


# ----------- LLM Function -----------

def call_llm(prompt):
    if model is None or tokenizer is None:
        return "⚠️ Model not loaded."

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.4,
            do_sample=True,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    return tokenizer.decode(out[0], skip_special_tokens=True)


# ----------- Chat Endpoint -----------

@app.post("/chat")
def chat_endpoint(payload: Query):
    query = payload.query

    # If model not loaded, return test response
    if model is None:
        return {
            "city": "TestCity",
            "days": 3,
            "itinerary": f"Test response for: {query}"
        }

    # Import helpers only if model exists
    from .helpers import extract_city, extract_days, extract_budget, extract_category, generate_itinerary, format_itinerary

    city = extract_city(query)
    if not city:
        return {"error": "City not specified"}

    days = extract_days(query)
    budget = extract_budget(query)
    category = extract_category(query)

    itin_df = generate_itinerary(city, days, budget, category)
    base_itin = format_itinerary(itin_df)

    prompt = f"""
You are a travel itinerary generator.
City: {city}
Days: {days}
Use ONLY these places:
{base_itin}
"""

    return {
        "city": city,
        "days": days,
        "itinerary": call_llm(prompt)
    }
