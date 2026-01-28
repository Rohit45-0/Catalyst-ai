"""
LangGraph State Definition

This module defines the shared state that flows through all agents
in the marketing content generation workflow.
"""

from typing import TypedDict, List, Annotated, Optional
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """
    The global state shared across all agents in the workflow.
    
    This acts as a "whiteboard" where each agent can read from and write to,
    enabling seamless communication between specialized agents.
    """
    
    # Conversation history between agents
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Original user inputs
    product_image_path: str
    product_description: str
    
    # Vision analysis results
    product_data: dict  # Structured data from Vision Analyzer
    
    # Marketing strategy
    brand_persona: Optional[dict]
    campaign_goal: Optional[str]
    target_audience: Optional[str]
    
    # Generated content for different platforms
    generated_content: dict  # Keys: 'blog', 'instagram', 'reel', etc.
    generated_images: List[dict]  # List of generated images with metadata
    market_data: dict  # Data from Market Research Agent
    
    # Workflow control
    current_step: str  # Tracks which agent is currently active
    review_status: Optional[str]  # 'approved', 'needs_revision', 'pending'
    
    # Error handling
    errors: Annotated[List[str], operator.add]


class ProductData(TypedDict):
    """Structured output from Vision Analyzer Agent"""
    product_name: str
    category: str
    primary_colors: List[str]
    material: Optional[str]
    key_features: List[str]
    target_demographic: str
    visual_style: str  # e.g., "minimalist", "luxury", "playful"
    selling_points: List[str]


class GeneratedContent(TypedDict):
    """Container for all generated marketing content"""
    blog_post: Optional[dict]  # {'title': str, 'content': str, 'seo_keywords': List[str]}
    instagram_post: Optional[dict]  # {'caption': str, 'hashtags': List[str]}
    instagram_reel: Optional[dict]  # {'script': str, 'hooks': List[str], 'cta': str}
    linkedin_post: Optional[dict]
    facebook_post: Optional[dict]
