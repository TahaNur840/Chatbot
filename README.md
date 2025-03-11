# Age-Based Recommendation Chatbot
A conversational AI assistant that provides personalized recommendations based on user age.

# Prerequisites
Python 3.8+
pip (Python package manager)
virtualenv (recommended)
Installation
Copy
# Clone the repository
git clone https://github.com/yourusername/age-based-recommendation-chatbot.git
cd age-based-recommendation-chatbot

# Create and activate a virtual environment
# On Windows
python -m venv venv_rasa
venv_rasa\Scripts\activate

# On macOS/Linux
python -m venv venv_rasa
source venv_rasa/bin/activate

# Install Rasa and dependencies
pip install rasa==3.6.2
pip install locust==2.33.1
pip install -r requirements.txt
Running the Chatbot
Copy
# Train the model
rasa train

# Start the Rasa server
rasa run --enable-api

# Start the actions server (in a separate terminal)
rasa run actions

# Interact with the chatbot via command line (in a separate terminal)
rasa shell
API Usage
Copy
# Example API request using curl
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "user123", "message": "Hello"}'
Testing
Copy
# Interactive testing
rasa interactive

# Load testing with Locust
locust -f locustfile.py
# Then open http://localhost:8089 in your browser

# Run the test suite
rasa test

# Age-Based Recommendation Chatbot: Documentation
# 1. Introduction
The Age-Based Recommendation Chatbot is an intelligent conversational agent designed to provide personalized recommendations and information based on a user's age. The bot leverages natural language processing to understand user inputs, maintain conversation context, and deliver tailored suggestions for activities and health information appropriate to different life stages.

# 2. Core Functionality
# 2.1 Age Collection and Storage
The chatbot begins interactions by greeting users and asking for their age. Once provided, the age is:

Extracted using entity recognition
Stored in the conversation session state
Used as a key parameter for all subsequent recommendations

# 2.2 Recommendation System
Based on the stored age, the chatbot can provide two main types of recommendations:

# Activity Recommendations: 
Suggests age-appropriate activities, tools, and applications
# Health Information: 
Offers relevant health guidance and tips specific to the user's age group

# 2.3 Context Management
The chatbot maintains conversation context throughout the interaction, allowing users to:

# Provide their age once and receive multiple recommendations without repetition
Switch between recommendation types (activities vs. health) while retaining age information
Return to the conversation after brief digressions with context intact

# 3. User Interaction Flow
# Initial Greeting:
Bot introduces itself and asks for the user's age
# Age Collection:
User provides age, which is acknowledged and stored
# Recommendation Options:
Bot offers different recommendation categories
# Personalized Suggestions:
Based on user selection and age, tailored recommendations are provided
# Follow-up Options:
User can request additional information or different recommendation types

# 4. Age-Based Recommendation Categories
The chatbot segments recommendations into different age brackets:

# Children and Teens (0-18)
# Activities: 
Educational apps, age-appropriate games, supervised social platforms
# Health: 
Growth milestones, nutrition needs, physical activity guidelines

# Young Adults (19-35)
# Activities:
Career development courses, fitness trackers, financial planning basics
# Health:
Stress management, exercise routines, preventive care

# Middle-Aged Adults (36-55)
# Activities:
Family activity planners, mindfulness apps, financial planning tools
# Health:
Regular screenings, work-life balance, nutrition guidance

# Older Adults (56+)
# Activities:
Retirement planning tools, brain training games, social connection platforms
# Health:
Health monitoring apps, chronic condition management, preventive measures

# 5. Technical Implementation
# 5.1 Architecture
The chatbot is built using the Rasa framework, which includes:

# NLU (Natural Language Understanding):
Processes and classifies user inputs
# Core Dialogue Management:
Handles conversation flow and context
# Actions:
Executes responses and retrieves recommendation data

# 5.2 Key Components
# Intents:
greet, inform_age, ask_recommendation, ask_health_info, etc.
# Entities:
age
# Slots:
user_age (stores the user's age throughout the conversation)
# Forms:
age_form (collects age information when not provided)
# Actions:
provide_activity_recommendation, provide_health_info

# 5.3 Context Management Implementation
The chatbot maintains context through:

Persistent slots that store user information across turns
State tracking to remember where in the conversation flow the user is
Memory policies that recall previous interactions to inform responses

# 6. Performance Metrics
Based on testing, the chatbot demonstrates:

# Response Accuracy: 
92.59% success rate in providing contextually appropriate responses
# Context Retention: 
Successfully maintains age information throughout conversations
# Response Time: 
Average response time of 2.1 seconds

# 7. Use Cases

# 7.1 Personal Health Management
Users can receive age-appropriate health recommendations to support wellness goals and preventive care.

# 7.2 Life Stage Planning
The bot can suggest activities and tools relevant to different life stages, from education to retirement planning.

# 7.3 Parental Guidance
Parents can use the bot to find age-appropriate activities and health information for their children.

# 7.4 Senior Support
Older adults can receive specialized recommendations for maintaining health and engagement.

# 8. Conclusion
The Age-Based Recommendation Chatbot represents an intelligent solution for providing personalized guidance across the lifespan. By understanding and remembering a user's age, it delivers relevant recommendations that can help individuals make informed choices about activities and health practices appropriate to their life stage.
