import os
import json
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, SystemMessage
from openai import AzureOpenAI
from app.agents.state import AgentState
from app.utils.publisher import SocialMediaPublisher

class ContentWriterAgent:
    """
    Generates platform-specific marketing content using LLMs.
    
    Uses market research data and vision analysis to create:
    - LinkedIn Posts (Professional)
    - Medium/Blog Posts (SEO-optimized)
    - Meta (FB/IG) Posts (Engaging)
    """
    
    def __init__(self, model_name: str = None, temperature: float = 0.7):
        """Initialize with Azure OpenAI credentials."""
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_key = os.getenv("AZURE_OPENAI_KEY")
        self.deployment_name = model_name or os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")
        api_version = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
        self.temperature = temperature
        
        if not azure_endpoint or not azure_key:
            raise ValueError("Azure OpenAI credentials not found in environment.")
        
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=azure_key,
            api_version=api_version,
        )
        
        # Initialize the publisher for posting to social media
        self.publisher = SocialMediaPublisher()

    def generate_content(self, product_data: Dict, market_data: Dict) -> Dict[str, Any]:
        """Generate content for all platforms in one LLM call for efficiency."""
        
        system_prompt = """You are an expert Content Strategist and Copywriter. 
Your goal is to create high-converting, SEO-friendly marketing content for a product based on its visual analysis and market research.

Platforms to cover:
1. LinkedIn: Professional, insightful, focuses on value proposition and industry impact.
2. Medium/Blog: Informative, long-form, SEO-optimized with headings and clear structure.
3. Meta (Facebook/Instagram): Engaging, visual-focused, catchy captions, and relevant emojis.

Guidelines:
- Use the 'Key Features' and 'Selling Points' from the vision analysis.
- Incorporate 'Customer Pain Points' or 'Positive Feedback' found in market research.
- Ensure the tone is consistent with the product's visual style.
- Include SEO keywords naturally.
- Provide the output as a structured JSON object."""

        user_prompt = f"""
PRODUCT DATA:
{json.dumps(product_data, indent=2)}

MARKET RESEARCH SUMMARY:
- Search Term: {market_data.get('search_term')}
- Top Features Found: {market_data.get('features', [])[:5]}
- Review Sentiment: {market_data.get('metadata', {}).get('total_reviews', 0)} reviews analyzed.

Generate the following in JSON format:
{{
  "linkedin_post": {{
    "title": "Catchy Headline",
    "content": "Professional post body...",
    "hashtags": ["#tag1", "#tag2"]
  }},
  "blog_post": {{
    "title": "SEO Optimized Title",
    "content": "Full blog content with markdown headings...",
    "seo_keywords": ["keyword1", "keyword2"]
  }},
  "meta_post": {{
    "caption": "Catchy caption with emojis...",
    "hashtags": ["#tag1", "#tag2"]
  }}
}}
"""

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)

    def __call__(self, state: AgentState) -> AgentState:
        """LangGraph node function."""
        print("Content Writer Agent: Generating marketing content...")
        
        try:
            product_data = state.get("product_data", {})
            market_data = state.get("market_data", {})
            
            if not product_data or not market_data:
                state["errors"].append("Content Writer: Missing product or market data.")
                return state
            
            generated = self.generate_content(product_data, market_data)
            
            # Update state
            state["generated_content"] = generated
            state["current_step"] = "content_generation_complete"
            
            state["messages"].append(
                SystemMessage(content="Marketing content generated for LinkedIn, Blog, and Meta.")
            )
            
            print("Content generation complete!")
            
            # Post to LinkedIn
            print("\nContent Writer Agent: Posting to LinkedIn...")
            linkedin_post = generated.get("linkedin_post", {})
            if linkedin_post:
                image_path = state.get("product_image_path")
                # Remove emojis and special characters from content for LinkedIn
                title = linkedin_post.get("title", "").encode('ascii', 'ignore').decode('ascii')
                content = linkedin_post.get("content", "").encode('ascii', 'ignore').decode('ascii')
                linkedin_result = self.publisher.post_to_linkedin(
                    title=title,
                    content=content,
                    hashtags=linkedin_post.get("hashtags", []),
                    image_path=image_path
                )
                state["linkedin_post_result"] = linkedin_result
                
                if linkedin_result.get("status") == "success":
                    print(f"[OK] LinkedIn post published successfully!")
                    state["messages"].append(
                        SystemMessage(content=f"LinkedIn post published: {linkedin_result.get('data', {}).get('id', 'unknown')}")
                    )
                else:
                    error = linkedin_result.get("message", "Unknown error")
                    print(f"[ERROR] LinkedIn post failed: {error}")
                    state["errors"].append(f"LinkedIn posting error: {error}")
            
        except Exception as e:
            error_msg = f"Content Writer Error: {str(e)}"
            state["errors"].append(error_msg)
            print(f"Error: {error_msg}")
            
        return state
