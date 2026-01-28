import sys
import traceback

with open("agent_results.log", "w", encoding="utf-8") as log:
    def print_log(msg):
        print(msg)
        log.write(msg + "\n")

    print_log("Checking agent imports...")


    try:
        print_log("1. Importing VisionAnalyzerAgent...")
        from app.agents.vision_analyzer import VisionAnalyzerAgent
        print_log("   ✅ Success")
    except Exception as e:
        print_log(f"   ❌ Failed: {e}")
        traceback.print_exc(file=log)

    try:
        print_log("2. Importing MarketResearchAgent...")
        from app.agents.market_research import MarketResearchAgent
        print_log("   ✅ Success")
    except Exception as e:
        print_log(f"   ❌ Failed: {e}")
        traceback.print_exc(file=log)

    try:
        print_log("3. Importing ContentWriterAgent...")
        from app.agents.content_writer import ContentWriterAgent
        print_log("   ✅ Success")
    except Exception as e:
        print_log(f"   ❌ Failed: {e}")
        traceback.print_exc(file=log)

    try:
        print_log("4. Importing ImageGeneratorAgent...")
        from app.agents.image_generator import ImageGeneratorAgent
        print_log("   ✅ Success")
    except Exception as e:
        print_log(f"   ❌ Failed: {e}")
        traceback.print_exc(file=log)
