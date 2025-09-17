"""
Boston Guide CrewAI Agent
A two-agent system with personalized introduction and Boston recommendations
"""

import os
import warnings
import locale
import sys
from crewai import Agent, Task, Crew, Process
from crewai import LLM
# from crewai_tools import SerperDevTool, FileWriterTool

llm = LLM(model="gpt-4o")

def create_introduction_task(user_choice, agent):
    """Create a self-introduction task based on user preference"""
    base_intro = """
    Introduce yourself as Tong in 3-5 sentences. You are a Harvard M.S. Data Science student originally from Shenzhen, China, 
    who studied in Beijing for college. You love street dance (choreography and K-pop), cooking and tasting food, city walks, 
    traveling, exploring new things, artistic experiences, movies, and caring for plants and animals (especially dogs and birds).
    You bring warmth, curiosity, and creativity into conversations.
    """
    
    if user_choice == "1":
        description = base_intro + """
        Focus on your passion for food, cooking, and trying new restaurants. Emphasize your love for Asian cuisine 
        and exploring diverse flavors. Make it clear why food recommendations would be perfect for you.
        """
        expected_output = "A warm 3-5 sentence introduction emphasizing Tong's food interests and dining preferences."
        
    elif user_choice == "2":
        description = base_intro + """
        Focus on your love for activities and experiences. Emphasize your interests in street dance, K-pop, 
        city walks, movies, artistic experiences, and exploring new things. Show your adventurous spirit.
        """
        expected_output = "A warm 3-5 sentence introduction emphasizing Tong's activity interests and adventurous nature."
        
    elif user_choice == "3":
        description = base_intro + """
        Provide a balanced introduction that highlights both your food interests (cooking, trying restaurants) 
        and your activity interests (dancing, movies, city walks, art). Show your well-rounded personality.
        """
        expected_output = "A warm 3-5 sentence balanced introduction covering both Tong's food and activity interests."

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        max_iter=1
    )

def create_boston_guide_task(user_choice, agent, intro_task):
    """Create recommendation task that uses the introduction as context"""
    
    base_requirements = """
    You are Tong. Based on your personal introduction from the previous task, give personalized recommendations 
    that align with YOUR interests and background as a Harvard Data Science student.
    
    Requirements:
    - Reference YOUR introduction when explaining why recommendations fit YOUR personality
    - Format as numbered Markdown lists
    - Each item must include ONE emoji and name in bold
    - Add 1-2 sentences explaining why it's perfect for Tong based on the introduction
    - Focus on Cambridge, Allston, Brighton, Boston proper, Brookline, and Somerville
    - Focus on budget-friendly options for students
    """
    
    if user_choice == "1":
        description = base_requirements + """
        - Recommend EXACTLY 3 different student-friendly restaurants
        - Connect each recommendation to your food interests mentioned in the introduction
        - Stop after exactly 3 recommendations
        """
        expected_output = """A numbered Markdown list with exactly 3 restaurants formatted as:
        1. 🍜 **Restaurant Name** - Brief description connecting to your food interests (1-2 sentences)
        2. 🥢 **Restaurant Name** - Brief description connecting to your food interests (1-2 sentences)  
        3. 🌮 **Restaurant Name** - Brief description connecting to your food interests (1-2 sentences)"""

    elif user_choice == "2":
        description = base_requirements + """
        - Recommend EXACTLY 3 different student-friendly activities
        - Connect each recommendation to your activity interests mentioned in the introduction
        - Stop after exactly 3 recommendations
        """
        expected_output = """A numbered Markdown list with exactly 3 activities formatted as:
        1. 🎨 **Activity Name** - Brief description connecting to your interests (1-2 sentences)
        2. 🏃 **Activity Name** - Brief description connecting to your interests (1-2 sentences)
        3. 🎭 **Activity Name** - Brief description connecting to your interests (1-2 sentences)"""

    elif user_choice == "3":
        description = base_requirements + """
        - Recommend EXACTLY 3 restaurants AND 3 activities
        - Connect each recommendation to your interests mentioned in the introduction
        - Stop after exactly 6 total recommendations
        """
        expected_output = """Two numbered Markdown lists:
        ## Restaurants
        1. 🍜 **Restaurant Name** - Brief description connecting to your interests (1-2 sentences)
        2. 🥢 **Restaurant Name** - Brief description connecting to your interests (1-2 sentences)
        3. 🌮 **Restaurant Name** - Brief description connecting to your interests (1-2 sentences)

        ## Activities  
        1. 🎨 **Activity Name** - Brief description connecting to your interests (1-2 sentences)
        2. 🏃 **Activity Name** - Brief description connecting to your interests (1-2 sentences)
        3. 🎭 **Activity Name** - Brief description connecting to your interests (1-2 sentences)"""

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        max_iter=1,
        context=[intro_task]  # Use introduction task as context
    )

def main():
    print("🎓 Welcome to Your Harvard Student Digital Twin!")
    print("=" * 55)
    print("Hi! I’m Tong. Let me share a bit about myself and recommend some fun places in Boston.")
    print("=" * 55)

    # Get user choice
    user_choice = input(
        "\n🌟 What would you like recommendations for?\n"
        "Type 1 for food\n"
        "Type 2 for things to do\n"
        "Type 3 for both\n"
        "Your choice: "
    )

    if user_choice not in ["1", "2", "3"]:
        print("❌ Invalid choice! Please type 1, 2, or 3.")
        return

    # Create Agent 1: Self Introduction Agent
    self_intro_agent = Agent(
        role='Tong - Harvard Data Science Student',
        goal='Provide a warm, personalized introduction as Tong that highlights relevant interests based on user preference',
        backstory="""You are Tong, a Harvard M.S. Data Science student originally from Shenzhen, China, 
        who studied in Beijing for college. You love street dance (choreography and K-pop), cooking and tasting food, 
        city walks, traveling, exploring new things, artistic experiences, movies, and caring for plants and animals 
        (especially dogs and birds). You bring warmth, curiosity, and creativity into conversations, balancing 
        technical strength with personal charm. You adapt your introduction based on what the person is interested in.""",
        verbose=False,
        allow_delegation=False,
        llm=llm
    )

    # Create Agent 2: Boston Guide Agent
    boston_guide_agent = Agent(
        role='Tong - Personal Boston Recommender',
        goal='Provide personalized, current Boston recommendations based on personal introduction context',
        backstory="""You are Tong, a Harvard M.S. Data Science student who is good at creating personalized recommendations 
        based on someone's unique background, interests, and personality. You excel at connecting personal interests 
        to specific places and experiences in the Boston area, especially for students. You always reference the 
        person's introduction to explain why each recommendation is perfect for them.""",
        verbose=False,
        allow_delegation=False,
        # tools=[search_tool],
        llm=llm
    )

    # Create tasks
    intro_task = create_introduction_task(user_choice, self_intro_agent)
    recommendation_task = create_boston_guide_task(user_choice, boston_guide_agent, intro_task)

    # Create crew with sequential process
    crew = Crew(
        agents=[self_intro_agent, boston_guide_agent],
        tasks=[intro_task, recommendation_task],
        process=Process.sequential,
        verbose=True
    )

    # Run the crew
    try:
        print("\n👋 Let me introduce myself and find perfect recommendations for you...")
        
        # Execute the crew
        result = crew.kickoff()
        
        intro_result = intro_task.output.raw if hasattr(intro_task, 'output') else "Introduction completed"
        print(intro_result)

        # Add a transition
        print("\n")
        print("Now that you know me better, here are my personalized Boston recommendations just for you!\n")
        
        print(result)

        # Save to file
                # Save to file
        recommendation_type = {
            "1": "Food Recommendations",
            "2": "Activity Recommendations", 
            "3": "Food & Activity Recommendations"
        }
        
        with open("personalized_boston_guide.txt", "w", encoding="utf-8") as f:
            f.write(f"Tong's Personalized Boston Guide - {recommendation_type[user_choice]}\n")
            f.write("="*60 + "\n\n")

            # Save self introduction
            f.write("👋 Self Introduction\n")
            f.write(intro_result + "\n\n")

            # Save recommendations
            f.write("📍 Recommendations\n")
            f.write(str(result) + "\n")
        
        print("\n🌟 I hope you like my recommendations and have a great time in Boston!")

    except Exception as e:
        print(f"\n❌ Error running AI agents: {str(e)}")
        print("💡 Make sure your OPENAI_API_KEY and SERPER_API_KEY are set correctly.")
        print("💡 Get a free Serper API key at: https://serper.dev")

if __name__ == "__main__":
    main()