from dotenv import load_dotenv
import os
from crewai.tools import BaseTool

import google.generativeai as genai
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import YoutubeVideoSearchTool, SerperDevTool

#parent directery that contain one subfolder per skill (each with skill.md)
_SKILLS_ROOT = Path(__file__).resolve().parent / "skills"
# load env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# tools
youtube_research_tool = YoutubeVideoSearchTool()
web_research_tool = SerperDevTool()
# LLM (Gemini)
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=api_key,
    temperature=0.7
)
print("Loaded API Key:", api_key[:10])
print("Model:", llm.model)



class GeminiImageTool(BaseTool):
    name: str = "Gemini Image Generator"
    description: str = "Generates AI image prompts using Gemini"

    def _run(self, prompt: str) -> str:

        model = genai.GenerativeModel(
            "gemini-2.0-flash-exp"
        )

        response = model.generate_content(
            f"""
            Create a professional AI image concept.

            Prompt:
            {prompt}

            Return:
            - detailed cinematic image prompt
            - colors
            - composition
            - style
            """
        )

        return response.text


# agent
web_research_agent = Agent(

    role="Web Researcher",
    goal="Find the latest and most insightful information about{topic} from the web",
    backstory=""" You are a senior research analyst who excels at finding high-quality resend 
    information from the internet.You focus on finding unique insight,statics,
    expert opinions,and real_world examples that would make great talking points for
    a linkdin Post.You are fluff and focus on substance.""",
    tools=[web_research_tool],
    llm=llm,
    verbose=True
   
)
youtube_research_agent = Agent(
    role="Youtube Researcher",
    goal="Extract the most valuable insights from YouTube video about{topic}",
    backstory="""You are expert at analyzing video content and extracting the key takeaway
    that audiences find most valuable.You focus on unique prespectives,memorable 
    quotes,frameworks,and actionable advice shared in the video.You always note
    the speaker's main argument and supporting points.""",
    # tools=[youtube_research_tool],
    llm=llm,
    verbose=True
)
linkedin_writer_agent = Agent(
    role="Linkedin Writer",
    goal="Write a viral Linkedin post about {topic} that gets high engagement",
    backstory="""You are a viral LinkedIn ghostwriter for top tech creators. You know how to stop the scroll with a powerful hook in the first line. You write in short, punchy paragraphs and turn boring technical topics into engaging stories. You often share real-world experiences, lessons, and insights that feel personal, relatable, and highly shareable.
     you never write generic fluffy_every post has personality and edge.  """,
    skills=[str(_SKILLS_ROOT / "linkedin-writing")],
    llm=llm,
    verbose=True
)

image_creator_agent = Agent(
    role="AI Image Creator",

    goal="Create visually engaging AI-generated images for LinkedIn posts about {topic}",

    backstory="""You are a professional AI visual designer who creates
    modern, futuristic, and attention-grabbing visuals for LinkedIn content.

    You specialize in:
    - AI-themed illustrations
    - futuristic graphics
    - minimal professional branding
    - tech content visuals
    - social media graphics
    """,

    tools=[GeminiImageTool()],

    llm=llm,
    verbose=True
)
# tasks define
web_research_task = Task(
    description = """ Research the topic '{topic}' on the web.
    Find:
    - 3-5 key insights or trend about the topic
    - Any interesting statistics or data points
    - Expert opinions or hot takes
    - Real-woeld examples or case studies
    
    Focus on recent,high-quality sources. This research will be used to write a Linkedin""",
    expected_output = """ A research brief with 3-5 key insight should be a short paragraph.""",
    agent=web_research_agent
    )
youtube_research_task = Task(
    description= """ Analyze the youtube video at {youtube_video_url} about the topic '{topic}' youtube.
    Extract:
    - The speaker's main argument or thesis 
    - 3 most valuable takeaways from the video
    - Any memorable quotes or frameworks mentioned
    - Practical advice or actionable tips shared

    This research will be used to write a Linkedin post.
    """,
    expected_output= """ A summary of the video's key insights including the main arguments,top 3 takeways,
    noteable quotes,and actionable advice.""",
    agent=youtube_research_agent
    )


linkedin_research_task=Task( 
    description=""" Using the web research and youtube video insight provide to you,
    Post requarements:
    - Start with a strong hook(first line should stop the scroll)
    - Keep it between 150-300 words
    - Use short paragraphs (1-2 sentences each)
    - Include insights from Both the web research and the video
    - End with a question or call-to-action to drive comments
    - Add 3-5 professional but conversational,opinionated,not generic

    Do NOT use emojis excessively.Max 2-3 emojis in the entire post.

    """,
    expected_output="""A ready-to-push Linkedin post between 150-300 words,with 
    insight from  research and a closing CTA.Include hashtag at the end.""",
    agent=linkedin_writer_agent,
    # human_input=True,
    output_file="linkedin_post.md",
    context = [web_research_task,youtube_research_task])

image_generation_task = Task(
    description="""
Create a cinematic LinkedIn AI visual.

The image should:
- look futuristic
- ultra realistic
- modern LinkedIn aesthetic
- blue/purple lighting
- professional tech branding
- visually engaging
- social media optimized 

    Generate an image that matches the LinkedIn post.
    """,

    expected_output="""
A detailed futuristic AI image concept suitable for LinkedIn,
including cinematic prompt, colors, composition, and style.
""",

    agent=image_creator_agent,
    context=[linkedin_research_task]
)


#define crew
crew = Crew(
agents = [web_research_agent,youtube_research_agent, linkedin_writer_agent,image_creator_agent],

tasks=[web_research_task,youtube_research_task,linkedin_research_task,image_generation_task],
process=Process.sequential,
)


result = crew.kickoff(
    inputs={
        "topic": "AI Agents",
        "youtube_video_url": "https://www.youtube.com/watch?v=HsQ9szWv1kM"
    }
)