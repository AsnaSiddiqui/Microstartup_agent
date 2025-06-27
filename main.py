import os
import random
from dotenv import load_dotenv
import chainlit as cl

from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled

# Load environment
load_dotenv()
set_tracing_disabled(True)

# OpenRouter setup
provider = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1/"
)

model = OpenAIChatCompletionsModel(
    model="mistralai/mistral-7b-instruct",  
    openai_client=provider,
)


# Tools
@function_tool
def get_idea(skill: str, time: int, preference: str) -> str:
    skill = skill.lower()
    if "design" in skill:
        return "Start a logo design or Canva template shop on Etsy."
    elif "graphic" in skill:
        return "Offer social media post designs for small brands."
    elif "ui" in skill or "ux" in skill:
        return "Design UI kits and sell them on Gumroad or your portfolio site."
    elif "web" in skill or "html" in skill or "css" in skill:
        return "Build portfolio websites or local business landing pages."
    elif "tailwind" in skill:
        return "Build and sell Tailwind-based UI templates or websites."
    elif "react" in skill:
        return "Create small web apps for freelancers and sell on CodeCanyon."
    elif "javascript" in skill:
        return "Build interactive widgets and plugins for websites."
    elif "python" in skill:
        return "Create automation scripts or small data tools for businesses."
    elif "coding" in skill or "developer" in skill:
        return "Build custom tools or websites for local startups."
    elif "flutter" in skill or "mobile" in skill:
        return "Create custom mobile apps for local businesses."
    elif "ai" in skill or "prompt" in skill:
        return "Sell AI prompt packs or build prompt-based mini tools."
    elif "chatgpt" in skill:
        return "Start a service that builds ChatGPT bots for businesses."
    elif "writing" in skill or "content" in skill:
        return "Offer blog or website content writing services."
    elif "copywriting" in skill:
        return "Write sales pages or ads for digital product sellers."
    elif "seo" in skill:
        return "Help small sites optimize pages with SEO reports."
    elif "data" in skill or "excel" in skill:
        return "Create Excel dashboards or data analysis reports."
    elif "analytics" in skill:
        return "Setup Google Analytics or dashboards for clients."
    elif "photography" in skill:
        return "Offer event shoots or sell presets and editing services."
    elif "video" in skill or "editing" in skill:
        return "Edit reels, YouTube videos, or make intro animations."
    elif "animation" in skill:
        return "Create explainer videos for SaaS or local products."
    elif "voice" in skill or "podcast" in skill:
        return "Offer voiceover or podcast cleanup services."
    elif "translation" in skill or "language" in skill:
        return "Offer document/video translation services."
    elif "urdu" in skill:
        return "Offer Urdu content creation or translation services."
    elif "english" in skill:
        return "Offer spoken English tutoring online."
    elif "teaching" in skill or "tutoring" in skill:
        return "Start online group classes for your subject."
    elif "math" in skill:
        return "Offer math tutoring or exam prep services."
    elif "science" in skill:
        return "Make digital notes and sell or teach via Zoom."
    elif "commerce" in skill or "accounts" in skill:
        return "Offer business studies or accounting tutoring."
    elif "digital marketing" in skill:
        return "Run ads for local shops or manage social media."
    elif "social media" in skill:
        return "Offer Instagram page management service."
    elif "blogging" in skill:
        return "Start a niche blog and earn via ads or affiliates."
    elif "affiliates" in skill:
        return "Build affiliate review pages or Instagram stories."
    elif "finance" in skill:
        return "Help people manage budget spreadsheets or save money."
    elif "crypto" in skill:
        return "Start a newsletter explaining crypto trends."
    elif "canva" in skill:
        return "Create Canva templates and sell on marketplaces."
    elif "notion" in skill:
        return "Design Notion templates for productivity or students."
    elif "wordpress" in skill:
        return "Build business websites using Elementor or themes."
    elif "shopify" in skill:
        return "Setup online stores for people with products."
    elif "dropshipping" in skill:
        return "Start a store selling low-competition products."
    elif "email marketing" in skill:
        return "Write email sequences or newsletters for small brands."
    elif "project management" in skill:
        return "Offer project tracking templates or training."
    elif "typing" in skill:
        return "Do transcription work or data entry freelance."
    elif "research" in skill:
        return "Do online research for students or writers."
    elif "linkedin" in skill:
        return "Optimize LinkedIn profiles for professionals."
    elif "resume" in skill:
        return "Make aesthetic resumes using Canva or Figma."
    elif "figma" in skill:
        return "Design UI mockups and sell or pitch to dev teams."
    elif "illustrator" in skill:
        return "Create illustrations for books or websites."
    elif "photoshop" in skill:
        return "Do image retouching or banner design gigs."
    elif "sales" in skill:
        return "Teach cold email writing or sales call basics."
    elif "law" in skill or "legal" in skill:
        return "Provide contract templates or offer legal insights."
    else:
        return "Start a freelance or micro-consulting service based on your skill."

@function_tool
def earning_model(skill: str) -> str:
    return random.choice([
        "Freelancing via Upwork or Fiverr",
        "Monthly subscription model",
        "Sell via WhatsApp or Instagram",
        "Online course or PDF via Gumroad"
    ])

@function_tool
def next_steps(skill: str) -> list:
    return [
        f"1. Research what others in {skill} are offering.",
        "2. Create a sample of your service.",
        "3. Share in 3 WhatsApp groups or online platforms."
    ]

# Agent
agent = Agent(
    name="MicroStartupAgent",
    instructions="Suggest startup idea in detail 4 to 5 lines, earning model, and steps based on skill, time, and preference.",
    tools=[get_idea, earning_model, next_steps],
    model=model
)

# Heading + Input + Response
@cl.on_chat_start
async def start_chat():
    await cl.Message(content="# MicroStartup Agent\n*By Asna — powered with Chainlit + AI*").send()

@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content="Please wait, generating your startup idea...").send()

    prompt = f"""
You're a professional startup advisor AI.

The user wants to start a micro-startup based on their own skills.

Here is the user's info:
Skill: {message.content}
Available Time per week: {message.content} hours
Work Preference: {message.content}

Based on this information:

1. Give a **detailed and practical startup idea**.
   - Why this idea suits their skill
   - How it can be done in their available time
   - What kind of clients or customers will benefit
   - Tools/Platforms they might use

2. Suggest a suitable **earning model** (freelancing, course selling, templates, etc.).

3. Provide **3 simple but important first steps** to begin their journey.

Make sure the advice is practical, encouraging, and easy for a beginner to follow.
"""

    result = await Runner.run(agent, prompt)
    await cl.Message(content=result.final_output).send()
