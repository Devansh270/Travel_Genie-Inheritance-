from fastapi import FastAPI
from pydantic import BaseModel
import torch

app = FastAPI()

# Global model references (loaded once at startup)
model = None
tokenizer = None


# ----------- Load Model on Startup -----------
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


# ----------- STRICT LLM Function -----------
def call_llm(prompt: str):
    if model is None or tokenizer is None:
        return "Model not loaded."

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.0,          # deterministic
            do_sample=False,          # no creativity
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)

    # Remove the original prompt from output
    result = decoded[len(prompt):].strip()

    return result


# ----------- Chat Endpoint -----------
@app.post("/chat")
def chat_endpoint(payload: Query):
    query = payload.query

    # Safe fallback if model failed
    if model is None:
        return {
            "city": "TestCity",
            "days": 3,
            "itinerary": f"Test response for: {query}"
        }

    from .helpers import (
        extract_city,
        extract_days,
        extract_budget,
        extract_category,
        generate_itinerary,
        format_itinerary
    )

    city = extract_city(query)
    if not city:
        return {"error": "City not specified"}

    days = extract_days(query)
    budget = extract_budget(query)
    category = extract_category(query)

    itin_df = generate_itinerary(city, days, budget, category)

    if itin_df.empty:
        return {"error": "No matching places found in dataset"}

    base_itin = format_itinerary(itin_df)

    # 🔥 STRICT PROMPT CONTROL
    prompt = f"""
You are a strict formatting engine.

Follow these rules strictly:
- Output ONLY the itinerary lines.
- Do NOT add explanations.
- Do NOT add addresses.
- Do NOT add extra sentences.
- Do NOT repeat the instructions.
- Do NOT modify place names.

Return EXACTLY this:

{base_itin}

Output:
"""

    clean_output = call_llm(prompt)

    return {
        "city": city,
        "days": days,
        "itinerary": clean_output
    }
