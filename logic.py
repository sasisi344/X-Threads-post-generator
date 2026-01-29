import requests
from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_article(url):
    """
    Scrapes the content of the given URL using Jina Reader API.
    Returns the markdown content or an error message.
    """
    try:
        jina_url = f"https://r.jina.ai/{url}"
        response = requests.get(jina_url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error scraping URL: {str(e)}"

def generate_posts(content, api_key=None, persona="blogger"):
    """
    Generates X and Threads posts using Gemini 2.0 Flash.
    Returns a dictionary with 'x_post' and 'threads_post'.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        return {"error": "Gemini API Key is missing."}

    # Persona definitions
    personas = {
        "influencer": "You are a popular social media influencer with an energetic, trendy, and relatable writing style. Use emojis strategically, speak directly to the audience, and create FOMO.",
        "cmo": "You are a Chief Marketing Officer with a professional, data-driven, and strategic writing style. Focus on value propositions, ROI, and business insights. Be authoritative yet approachable.",
        "blogger": "You are an experienced blogger with a conversational, informative, and SEO-aware writing style. Balance personality with useful information. Include clear takeaways.",
        "general": "You are an everyday person sharing interesting content. Use casual, natural language. Be authentic and relatable without trying too hard.",
        "geek": "You are a passionate tech enthusiast and gadget geek. You have deep knowledge of IT devices and technology. Your writing style is enthusiastic and detail-oriented, sharing genuine excitement about products you believe in. You explain technical features in an accessible way while maintaining your passion."
    }
    
    persona_instruction = personas.get(persona, personas["blogger"])

    client = genai.Client(api_key=key)

    prompt = f"""
    {persona_instruction}
    
    IMPORTANT: You MUST output the posts in the SAME LANGUAGE as the blog content. If the blog is in Japanese, output in Japanese. If in English, output in English.
    
    Based on the following blog content (in Markdown), generate two types of posts:
    1. X (Twitter): Maximum 140 characters, bullet points, conclusion-first, includes relevant hashtags.
    2. Threads: Around 400 characters, empathetic, story-driven, engaging tone.

    Output the result STRICTLY in JSON format with the following keys:
    "x_post": "...",
    "threads_post": "..."

    Blog Content:
    {content}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"Error generating posts: {str(e)}"}
