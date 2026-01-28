"""
Agent Wrapper - Adapts LangGraph agents to work with the backend

This module provides a simplified interface to your existing agents,
handling the conversion between backend data structures and agent state.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path


class AgentWrapper:
    """
    Wrapper class that adapts your LangGraph agents to work with the backend.
    
    This handles:
    - Converting backend Project data to AgentState
    - Running agents with proper error handling
    - Extracting results from AgentState
    """
    
    def __init__(self):
        self.use_mock = os.getenv("USE_MOCK_AGENTS", "false").lower() == "true"
        
        # Only import agents if not using mocks
        if not self.use_mock:
            try:
                # Import your actual agents
                from app.agents.vision_analyzer import VisionAnalyzerAgent
                from app.agents.market_research import MarketResearchAgent
                from app.agents.content_writer import ContentWriterAgent
                from app.agents.image_generator import ImageGeneratorAgent
                
                self.vision_agent = VisionAnalyzerAgent()
                self.research_agent = MarketResearchAgent()
                self.content_agent = ContentWriterAgent()
                self.image_agent = ImageGeneratorAgent()
                
                print("✅ Real agents loaded successfully")
            except Exception as e:
                print(f"⚠️  Failed to load real agents: {e}")
                print("📝 Falling back to mock agents")
                self.use_mock = True
    
    def run_vision_analysis(self, image_path: str, product_name: str, description: str = "") -> Dict[str, Any]:
        """
        Run vision analysis on a product image.
        
        Args:
            image_path: Path to the product image
            product_name: Name of the product
            description: Optional product description
            
        Returns:
            Product data dictionary
        """
        if self.use_mock:
            return self._mock_vision_analysis(product_name)
        
        try:
            # Use your actual agent
            result = self.vision_agent.analyze_product_image(image_path, description)
            return result
        except Exception as e:
            print(f"Vision analysis error: {e}")
            return self._mock_vision_analysis(product_name)
    
    def run_market_research(
        self, 
        product_name: str, 
        brand_name: str,
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run market research for a product.
        
        Args:
            product_name: Name of the product
            brand_name: Brand name
            product_data: Vision analysis results
            
        Returns:
            Market research data dictionary
        """
        if self.use_mock:
            return self._mock_market_research(product_name)
        
        try:
            # Create minimal state for the agent
            from app.agents.state import AgentState
            
            state = AgentState(
                messages=[],
                product_image_path="",
                product_description="",
                product_data=product_data,
                market_data={},
                generated_images=[],
                generated_content={},
                errors=[]
            )
            
            # Run the agent
            updated_state = self.research_agent(state)
            return updated_state.get("market_data", {})
            
        except Exception as e:
            print(f"Market research error: {e}")
            return self._mock_market_research(product_name)
    
    def run_content_generation(
        self,
        product_data: Dict[str, Any],
        market_data: Dict[str, Any],
        campaign_goal: Optional[str] = None,
        target_audience: Optional[str] = None,
        brand_persona: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate marketing content.
        
        Args:
            product_data: Vision analysis results
            market_data: Market research results
            campaign_goal: Campaign objective
            target_audience: Target demographic
            brand_persona: Brand voice/personality
            
        Returns:
            Generated content dictionary
        """
        if self.use_mock:
            return self._mock_content_generation(product_data.get("product_name", "Product"))
        
        try:
            from app.agents.state import AgentState
            
            state = AgentState(
                messages=[],
                product_image_path="",
                product_description="",
                product_data=product_data,
                market_data=market_data,
                campaign_goal=campaign_goal,
                target_audience=target_audience,
                brand_persona={"voice": brand_persona} if brand_persona else None,
                generated_images=[],
                generated_content={},
                errors=[]
            )
            
            # Run the agent
            updated_state = self.content_agent(state)
            return updated_state.get("generated_content", {})
            
        except Exception as e:
            print(f"Content generation error: {e}")
            return self._mock_content_generation(product_data.get("product_name", "Product"))
    
    def run_image_generation(
        self,
        product_data: Dict[str, Any],
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate marketing images (optional).
        
        Args:
            product_data: Vision analysis results
            market_data: Market research results
            
        Returns:
            Generated images data
        """
        if self.use_mock:
            return self._mock_image_generation()
        
        try:
            from app.agents.state import AgentState
            
            state = AgentState(
                messages=[],
                product_image_path="",
                product_description="",
                product_data=product_data,
                market_data=market_data,
                generated_images=[],
                generated_content={},
                errors=[]
            )
            
            # Run the agent
            updated_state = self.image_agent(state)
            return {
                "generated_images": updated_state.get("generated_images", [])
            }
            
        except Exception as e:
            print(f"Image generation error: {e}")
            return self._mock_image_generation()
    
    # ============================================
    # MOCK IMPLEMENTATIONS (Fallback)
    # ============================================
    
    def _mock_vision_analysis(self, product_name: str) -> Dict[str, Any]:
        """Mock vision analysis for testing without API keys"""
        return {
            "product_name": product_name,
            "category": "General Product",
            "primary_colors": ["Blue", "White"],
            "material": "Premium materials",
            "key_features": [
                "High quality construction",
                "Modern design",
                "User-friendly interface"
            ],
            "target_demographic": "General consumers",
            "visual_style": "Modern and professional",
            "selling_points": [
                "Quality craftsmanship",
                "Innovative features",
                "Great value"
            ]
        }
    
    def _mock_market_research(self, product_name: str) -> Dict[str, Any]:
        """Mock market research for testing"""
        return {
            "competitors": ["Competitor A", "Competitor B"],
            "market_trends": [
                "Growing demand for quality products",
                "Shift towards sustainable options"
            ],
            "customer_pain_points": [
                "Need for better quality",
                "Looking for value"
            ],
            "pricing_insights": {
                "average_price": "$500-$1000",
                "price_range": "Mid to premium"
            },
            "metadata": {
                "total_results": 10,
                "total_reviews": 50,
                "total_features": 15
            }
        }
    
    def _mock_content_generation(self, product_name: str) -> Dict[str, Any]:
        """Mock content generation for testing"""
        return {
            "linkedin_post": {
                "title": f"Introducing {product_name}",
                "content": f"We're excited to announce {product_name}! "
                          f"This innovative product combines quality, design, and functionality. "
                          f"Perfect for professionals who demand the best. #Innovation #Quality",
                "hashtags": ["#Innovation", "#Quality", "#NewProduct"]
            },
            "meta_post": {
                "caption": f"🚀 Check out {product_name}! The perfect blend of style and substance. "
                          f"Available now! #NewProduct #Innovation",
                "hashtags": ["#NewProduct", "#Innovation", "#Quality"]
            },
            "blog_post": {
                "title": f"Introducing {product_name}: Innovation Meets Design",
                "content": f"# {product_name}\n\n"
                          f"We're thrilled to introduce {product_name}, our latest innovation "
                          f"that combines cutting-edge technology with elegant design.\n\n"
                          f"## Key Features\n"
                          f"- Premium quality construction\n"
                          f"- Modern, user-friendly design\n"
                          f"- Exceptional value\n\n"
                          f"Experience the difference today!",
                "seo_keywords": ["innovation", "quality", product_name.lower()]
            }
        }
    
    def _mock_image_generation(self) -> Dict[str, Any]:
        """Mock image generation for testing"""
        return {
            "generated_images": [
                {
                    "type": "social_media_post",
                    "url": "https://via.placeholder.com/1200x630/4A90E2/ffffff?text=Social+Media+Post",
                    "prompt": "Marketing image for social media"
                },
                {
                    "type": "blog_header",
                    "url": "https://via.placeholder.com/1920x1080/7B68EE/ffffff?text=Blog+Header",
                    "prompt": "Blog post header image"
                }
            ]
        }


# Global instance
_agent_wrapper = None

def get_agent_wrapper() -> AgentWrapper:
    """Get or create the global agent wrapper instance"""
    global _agent_wrapper
    if _agent_wrapper is None:
        _agent_wrapper = AgentWrapper()
    return _agent_wrapper
