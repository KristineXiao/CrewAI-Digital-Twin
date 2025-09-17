# Personalized Boston Guide CrewAI Agent (Tong Xiao, Tech track)

A two-agent CrewAI system that creates a personalized introduction and Boston recommendations, acting as a digital twin for Tong.  

---

## 🎯 Overview
This project implements a **CrewAI digital twin lite**, consisting of:
- **Two Agents**
- **Two Sequential Tasks**
- **User-driven workflow** with input options for food, activities, or both  

The system outputs:
1. A **3–5 sentence personalized self-introduction** that adapts to the user’s preference.  
2. **Personalized Boston recommendations** (restaurants, activities, or both) based on that introduction.  

The final results are printed to the console and saved into a file (`personalized_boston_guide.txt`).  

---

## 🤖 Agents

### 1. **SelfIntroAgent**
- **Role**: Harvard M.S. Data Science student (Tong)  
- **Goal**: Provide a warm, personalized introduction based on user’s choice (food, activities, or both).  
- **Backstory**: From Shenzhen → studied in Beijing → now at Harvard. Interests include dance, food, city walks, movies, art, traveling, animals, and plants.  

### 2. **BostonGuideAgent**
- **Role**: Personal Boston recommender  
- **Goal**: Recommend **budget-friendly, student-focused restaurants and/or activities** that match Tong’s personality and introduction.  
- **Backstory**: Good at connecting personal interests with specific Boston experiences.  

---

## 📝 Tasks

### 1. **Self Introduction Task**
- Prompts the **SelfIntroAgent** to generate a 3–5 sentence intro.  
- Tailors emphasis based on user input:  
  - **1 = Food** → highlight love for food and cooking  
  - **2 = Activities** → highlight adventurous and artistic side  
  - **3 = Both** → balanced introduction  

### 2. **Boston Recommendation Task**
- Prompts the **BostonGuideAgent** to generate recommendations.  
- Takes the intro as **context**.  
- Tailored rules:  
  - **1 = Food** → exactly 3 restaurants  
  - **2 = Activities** → exactly 3 activities  
  - **3 = Both** → exactly 3 restaurants and 3 activities  
- Each recommendation:  
  - Uses **Markdown numbered list**  
  - Includes **one emoji + bolded name**  
  - Explains why it fits Tong’s interests  

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.8 or higher (the author used 3.11)
- OpenAI API key (required for the agents to function)

### Installation

1. Clone or download this example code
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

   **Note**: You can get an OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)


## 🚀 Usage

Run the main script from the terminal:

```bash
python main.py
```
When you run the program: 
1. You’ll be asked to choose a recommendation preference (`1` for food, `2` for things to do, or `3` for both).  
2. **SelfIntroAgent** runs first and generates introduction.  
3. **BostonGuideAgent** runs second, using the intro as context.  
4. Both outputs are displayed to the user.  
5. Recommendations are saved to `personalized_boston_guide.txt`.  

---
## ✅ What Worked
- Switching from free-text query parsing to **numeric input (`1/2/3`)** solved the issue of the model often giving both restaurants and activities.  
- Using **strong instructions** like *“ONLY,” “MUST,” “DO NOT”* improved task compliance.  
- Writing **clear and detailed descriptions** for tasks helped guide the output more reliably.  
- Sequential task flow worked well: introduction context was successfully passed to the recommendation step.  

---

## ⚠️ What Didn’t Work (Challenges)
- **Initial design idea**:  
  - I wanted to build a single task that dynamically adapted (food, activity, or both) based on the user’s query.  
  - In practice, the model often ignored the wording and generated both restaurants and activities anyway.  
  - Switching to numeric input and stricter prompts made it more reliable.  

- **Serper Search Tool Issue**:  
  - Tool kept throwing encoding errors:  
    ```
    Tool Usage Failed
    Name: Search the internet with Serper
    Error: 'latin-1' codec can't encode character '\u201c' ...
    ```  
  - Tried fixing with UTF-8 settings (`PYTHONIOENCODING`, `locale`, `sys.stdout.reconfigure`), but the issue persists.  
  - Currently recommendations are static (no live search). This will be fixed in future homework.

---

## 📚 Lessons Learned
- **Prompt specificity is critical**: using vague wording (e.g., “recommend restaurants or activities”) leads to unreliable outputs. Stronger phrasing with “ONLY / MUST” enforces structure.  
- **Task granularity matters**: breaking into **two sequential tasks** (intro → recommendations) was much cleaner than trying to do everything in one step.  
- **Encoding issues on Windows** can complicate tool usage; extra care is needed for UTF-8 handling.  

---

## 💾 Output Example (activity recommendations with gpt-4o)

```text
Hi there! I'm Tong, a Harvard M.S. Data Science student originally from Shenzhen, China, who has a deep passion for adventure and discovery. I love immersing myself in the world of street dance and K-pop choreography, and I find joy in exploring cities through walks that lead to new artistic experiences and hidden gems. Movies are a great love of mine, as well as experimenting with flavors while cooking and tasting new cuisines. Whether I'm dancing, mapping out urban adventures, or diving into a good film, I bring a sense of warmth and curiosity to all my pursuits.

Now that you know me better, here are my personalized Boston recommendations just for you!

1. 🎨 **Graffiti Alley in Central Square** - As someone who enjoys artistic experiences and hidden gems, the vibrant street art in Graffiti Alley offers a perfect spot for adventure and discovery. It's an ever-changing canvas that will inspire your creative side and provide plenty of opportunities for photography and exploration.

2. 🏃 **Charles River Esplanade Walks** - This scenic walking path connects you to Boston's picturesque views and is ideal for getting some exercise while discovering the city's charm. Walking along the river, you can enjoy the peace of nature and the bustle of the city — an urban adventure that matches your love for exploration.

3. 🎭 **Coolidge Corner Theatre** - This independent cinema in Brookline screens a mix of indie and classic films, aligning with your passion for movies. The historic theater coupled with diverse film selections offers a cozy and intellectually stimulating environment to enjoy and discuss films with fellow cinephiles on a budget.

🌟 I hope you like my recommendations and have a great time in Boston!
```

---

## 🤝 AI Usage Note
During this project, I used GPT to enhance readability by adding emojis to the recommendations for better visualization. I also briefly used GitHub Copilot during debugging to speed up troubleshooting.