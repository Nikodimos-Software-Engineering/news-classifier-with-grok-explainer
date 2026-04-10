import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_explanation(headline, article, category, score):

	if not GROQ_API_KEY:
		return "Groq API key not configured."


	excerpt = article[:200]

	confidence_pct = f"{score:.1f}%" if isinstance(score, (int, float)) else str(score)

	prompt = f"Headline: {headline}. Article excerpt: {excerpt}. My machine learning model is {confidence_pct} certain this article belongs to the '{category}' news category. In 1-2 sentences, explain why this article fits '{category}' news. Do not mention the confidence score or percentages in your explanation."

	headers = {
		"Authorization" : f"Bearer {GROQ_API_KEY}",
		"Content-Type" : "application/json"
	}

	data = {
		"model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 100
	}

	async with httpx.AsyncClient(timeout=30.0) as client:
		try:
			response = await client.post(GROQ_URL, json=data, headers=headers)
			print(f"Groq status: {response.status_code}")
			response_text = response.text
			print(f"Groq response: {response_text[:500]}")  # First 500 chars
			if response.status_code != 200:
				return f"API error ({response.status_code})"

			result = response.json()
			explanation = result["choices"][0]["message"]["content"].strip()
			return explanation
		except Exception as e:
			print(f"Groq exception: {type(e).__name__}: {e}")
			return "Explanation temporarily unavailable."