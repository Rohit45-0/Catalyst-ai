"""
Agent Orchestrator - Manages the multi-agent workflow

This orchestrator integrates with your existing LangGraph agents:
1. Vision Analyzer
2. Market Research Agent
3. Content Writer Agent
4. Image Generator Agent

It manages job creation, execution, and result storage.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import Project, Job, Asset
import uuid
import json
import asyncio


class AgentOrchestrator:
    """
    Orchestrates the multi-agent marketing content generation pipeline.
    
    Workflow:
    1. VISION_ANALYSIS - Analyze product image
    2. MARKET_RESEARCH - Research market and competitors
    3. CONTENT_GENERATION - Generate platform-specific content
    4. IMAGE_GENERATION - Create marketing images (optional)
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def start_workflow(self, project_id: uuid.UUID) -> Dict[str, Any]:
        """
        Start the complete agent workflow for a project.
        
        Args:
            project_id: UUID of the project to process
            
        Returns:
            Dict with workflow status and job IDs
        """
        project = self.db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            return {"status": "error", "message": "Project not found"}
        
        # Update project status
        project.status = "processing"
        self.db.commit()
        
        try:
            # Step 1: Vision Analysis
            vision_job = await self._run_vision_analysis(project)
            
            if vision_job.status == "failed":
                project.status = "failed"
                self.db.commit()
                return {
                    "status": "failed",
                    "message": "Vision analysis failed",
                    "error": vision_job.error_message
                }
            
            # Step 2: Market Research
            research_job = await self._run_market_research(project, vision_job)
            
            if research_job.status == "failed":
                project.status = "failed"
                self.db.commit()
                return {
                    "status": "failed",
                    "message": "Market research failed",
                    "error": research_job.error_message
                }
            
            # Step 3: Content Generation
            content_job = await self._run_content_generation(project, vision_job, research_job)
            
            if content_job.status == "failed":
                project.status = "failed"
                self.db.commit()
                return {
                    "status": "failed",
                    "message": "Content generation failed",
                    "error": content_job.error_message
                }
            
            # Step 4: Image Generation (optional)
            image_job = None
            if project.image_path:  # Only if we have a base image
                image_job = await self._run_image_generation(project, vision_job, research_job)
            
            # Update project status
            project.status = "completed"
            self.db.commit()
            
            return {
                "status": "success",
                "message": "Workflow completed successfully",
                "jobs": {
                    "vision_analysis": str(vision_job.id),
                    "market_research": str(research_job.id),
                    "content_generation": str(content_job.id),
                    "image_generation": str(image_job.id) if image_job else None
                }
            }
            
        except Exception as e:
            project.status = "failed"
            self.db.commit()
            return {
                "status": "error",
                "message": f"Workflow failed: {str(e)}"
            }
    
    async def _run_vision_analysis(self, project: Project) -> Job:
        """
        Run Vision Analysis Agent
        
        This agent analyzes the product image to extract:
        - Product name and category
        - Visual features (colors, style)
        - Target demographic
        - Key selling points
        """
        job = Job(
            project_id=project.id,
            job_type="VISION_ANALYSIS",
            status="running",
            input_payload={
                "image_path": project.image_path,
                "product_name": project.product_name,
                "description": project.description
            },
            started_at=datetime.utcnow()
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        
        try:
            # Use real agent via wrapper
            from app.core.agent_wrapper import get_agent_wrapper
            agent_wrapper = get_agent_wrapper()
            
            output = agent_wrapper.run_vision_analysis(
                image_path=project.image_path or "",
                product_name=project.product_name,
                description=project.description or ""
            )
            
            job.output_payload = output
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            self.db.commit()
            
            return job
            
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            self.db.commit()
            return job
    
    async def _run_market_research(self, project: Project, vision_job: Job) -> Job:
        """
        Run Market Research Agent
        
        This agent researches:
        - Competitor products
        - Market trends
        - Customer reviews and pain points
        - Pricing strategies
        """
        job = Job(
            project_id=project.id,
            job_type="MARKET_RESEARCH",
            status="running",
            input_payload={
                "product_name": project.product_name,
                "brand_name": project.brand_name,
                "vision_data": vision_job.output_payload
            },
            started_at=datetime.utcnow()
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        
        try:
            # Use real agent via wrapper
            from app.core.agent_wrapper import get_agent_wrapper
            agent_wrapper = get_agent_wrapper()
            
            output = agent_wrapper.run_market_research(
                product_name=project.product_name,
                brand_name=project.brand_name or "",
                product_data=vision_job.output_payload
            )
            
            job.output_payload = output
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            self.db.commit()
            
            return job
            
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            self.db.commit()
            return job
    
    async def _run_content_generation(
        self, 
        project: Project, 
        vision_job: Job, 
        research_job: Job
    ) -> Job:
        """
        Run Content Writer Agent
        
        This agent generates platform-specific content:
        - LinkedIn posts
        - Facebook/Instagram posts
        - Blog posts for Medium
        - Ad copy
        """
        job = Job(
            project_id=project.id,
            job_type="CONTENT_GENERATION",
            status="running",
            input_payload={
                "product_data": vision_job.output_payload,
                "market_data": research_job.output_payload,
                "campaign_goal": project.campaign_goal,
                "target_audience": project.target_audience,
                "brand_persona": project.brand_persona
            },
            started_at=datetime.utcnow()
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        
        try:
            # Use real agent via wrapper
            from app.core.agent_wrapper import get_agent_wrapper
            agent_wrapper = get_agent_wrapper()
            
            generated_content = agent_wrapper.run_content_generation(
                product_data=vision_job.output_payload,
                market_data=research_job.output_payload,
                campaign_goal=project.campaign_goal,
                target_audience=project.target_audience,
                brand_persona=project.brand_persona
            )
            
            job.output_payload = generated_content
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            self.db.commit()
            
            # Create assets from generated content
            await self._create_assets_from_content(project.id, generated_content)
            
            return job
            
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            self.db.commit()
            return job
    
    async def _run_image_generation(
        self, 
        project: Project, 
        vision_job: Job, 
        research_job: Job
    ) -> Job:
        """
        Run Image Generator Agent (Optional)
        
        This agent generates marketing images using DALL-E
        """
        job = Job(
            project_id=project.id,
            job_type="IMAGE_GENERATION",
            status="running",
            input_payload={
                "product_data": vision_job.output_payload,
                "market_data": research_job.output_payload
            },
            started_at=datetime.utcnow()
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        
        try:
            # TODO: Integrate with your ImageGeneratorAgent
            # from agents.image_generator import ImageGeneratorAgent
            # image_agent = ImageGeneratorAgent()
            # result = image_agent.generate_images(state)
            
            # Mock output for now
            output = {
                "generated_images": [
                    {
                        "type": "social_media_post",
                        "url": "https://example.com/image1.jpg",
                        "prompt": "Marketing image for social media"
                    }
                ]
            }
            
            job.output_payload = output
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            self.db.commit()
            
            return job
            
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            self.db.commit()
            return job
    
    async def _create_assets_from_content(
        self, 
        project_id: uuid.UUID, 
        generated_content: Dict[str, Any]
    ):
        """
        Create Asset records from generated content
        """
        # LinkedIn post
        if "linkedin_post" in generated_content:
            linkedin_asset = Asset(
                project_id=project_id,
                asset_type="linkedin_post",
                content=json.dumps(generated_content["linkedin_post"])
            )
            self.db.add(linkedin_asset)
        
        # Meta (Facebook/Instagram) post
        if "meta_post" in generated_content:
            meta_asset = Asset(
                project_id=project_id,
                asset_type="meta_post",
                content=json.dumps(generated_content["meta_post"])
            )
            self.db.add(meta_asset)
        
        # Blog post
        if "blog_post" in generated_content:
            blog_asset = Asset(
                project_id=project_id,
                asset_type="blog_post",
                content=json.dumps(generated_content["blog_post"])
            )
            self.db.add(blog_asset)
        
        self.db.commit()
    
    def get_workflow_status(self, project_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get the current status of the workflow for a project
        """
        project = self.db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            return {"status": "error", "message": "Project not found"}
        
        jobs = self.db.query(Job).filter(Job.project_id == project_id).all()
        
        return {
            "project_status": project.status,
            "jobs": [
                {
                    "id": str(job.id),
                    "type": job.job_type,
                    "status": job.status,
                    "started_at": job.started_at.isoformat() if job.started_at else None,
                    "completed_at": job.completed_at.isoformat() if job.completed_at else None,
                    "error": job.error_message
                }
                for job in jobs
            ]
        }
