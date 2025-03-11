# from rasa_sdk import Action, Tracker
# from rasa_sdk.events import SlotSet
# from rasa_sdk.executor import CollectingDispatcher
# from typing import Any, Dict, List, Text
# import re
# import random

# class ActionAskAge(Action):
#     def name(self) -> Text:
#         return "action_ask_age"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(text="Can you please tell me your age?")
#         return []

# class ActionProvideAge(Action):
#     def name(self) -> Text:
#         return "action_provide_age"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # Extract age from the message using regex
#         message = tracker.latest_message.get('text', '')
#         age_match = re.search(r'\b(\d+)\b', message)
        
#         if age_match:
#             age = age_match.group(1)
#             dispatcher.utter_message(text=f"Thank you for sharing your age: {age}")
#             return [SlotSet("age", age)]
#         else:
#             dispatcher.utter_message(text="I couldn't understand your age. Can you please provide it as a number?")
#             return []

# class ActionRecommendActivity(Action):
#     def name(self) -> Text:
#         return "action_recommend_activity"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         age = tracker.get_slot("age")
        
#         if not age:
#             dispatcher.utter_message(text="I don't know your age yet. Can you tell me your age first?")
#             return []
        
#         try:
#             age = int(age)
            
#             if age < 18:
#                 activities = [
#                     "Educational games like Minecraft Education",
#                     "Learning a new language with Duolingo",
#                     "Supervised social media usage",
#                     "Coding for kids with Scratch"
#                 ]
#             elif age < 30:
#                 activities = [
#                     "Fitness apps like Nike Training Club",
#                     "Learning platforms like Coursera",
#                     "Networking events in your industry",
#                     "Travel planning apps for weekend getaways"
#                 ]
#             elif age < 50:
#                 activities = [
#                     "Career development courses",
#                     "Financial planning apps",
#                     "Family activity planners",
#                     "Mindfulness and meditation apps"
#                 ]
#             else:
#                 activities = [
#                     "Health tracking apps",
#                     "Brain training games",
#                     "Virtual museum tours",
#                     "Community volunteer platforms"
#                 ]
                
#             recommendations = random.sample(activities, 2)
#             response = f"Based on your age ({age}), I recommend: {recommendations[0]} and {recommendations[1]}"
#             dispatcher.utter_message(text=response)
#             return []
            
#         except ValueError:
#             dispatcher.utter_message(text="I couldn't process your age. Please provide a valid number.")
#             return []

# class ActionHandleHealthQuery(Action):
#     def name(self) -> Text:
#         return "action_handle_health_query"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         age = tracker.get_slot("age")
        
#         if not age:
#             dispatcher.utter_message(text="To provide personalized health information, I need to know your age first.")
#             return []
        
#         try:
#             age = int(age)
#             health_info = self.get_health_info_by_age(age)
#             dispatcher.utter_message(text=health_info)
#             return []
#         except ValueError:
#             dispatcher.utter_message(text="I couldn't process your age. Please provide a valid number.")
#             return []
            
#     def get_health_info_by_age(self, age):
#         if age < 18:
#             return "For your age group, regular physical activity, balanced nutrition, and adequate sleep are important. Remember that health advice should be discussed with your doctor or parents."
#         elif age < 30:
#             return "For adults in their 20s, establishing healthy habits is key. Regular exercise (150 minutes/week), balanced diet, regular check-ups, and mental health awareness are recommended."
#         elif age < 50:
#             return "For adults in their 30s and 40s, regular health screenings become more important. Maintain physical activity, manage stress, and be aware of changing nutritional needs."
#         else:
#             return "For adults 50+, regular health screenings, bone health, heart health monitoring, and staying physically and mentally active are particularly important."




# ========================================


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ActionAskAge(Action):
    def name(self) -> Text:
        return "action_ask_age"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Check if we already have the age
        age = tracker.get_slot("age")
        if age is not None:
            logger.debug(f"Age already provided: {age}")
            return []
            
        dispatcher.utter_message(response="utter_ask_age")
        return []

class ActionProvideAge(Action):
    def name(self) -> Text:
        return "action_provide_age"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract age from entities
        age = next(tracker.get_latest_entity_values("age"), None)
        logger.debug(f"Extracted age entity: {age}")
        
        # If no entity found, try to extract from text
        if age is None:
            text = tracker.latest_message.get("text", "").lower()
            logger.debug(f"Trying to extract age from text: {text}")
            if "i am " in text and "years old" in text:
                try:
                    age_text = text.split("i am ")[1].split("years old")[0].strip()
                    if age_text.isdigit():
                        age = age_text
                        logger.debug(f"Extracted age from text: {age}")
                except Exception as e:
                    logger.error(f"Error extracting age from text: {e}")
        
        # If still no age, ask directly
        if age is None:
            dispatcher.utter_message(text="I didn't catch your age. Could you please tell me how old you are?")
            return []
        
        # Acknowledge the age
        dispatcher.utter_message(text=f"Thank you for sharing your age: {age}")
        
        # Return an event to set the slot
        logger.debug(f"Setting age slot to: {age}")
        return [SlotSet("age", age)]

class ActionRecommendActivity(Action):
    def name(self) -> Text:
        return "action_recommend_activity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Debug logging
        logger.debug(f"All slots: {tracker.current_slot_values()}")
        
        # Get age from slot
        age = tracker.get_slot("age")
        logger.debug(f"Retrieved age from slot: {age}")
        
        # Check if age is available
        if age is None:
            # If no age in slot, try to extract from conversation history
            logger.debug("No age in slot, trying to extract from history")
            for event in reversed(tracker.events):
                if event.get("event") == "user" and event.get("text"):
                    text = event.get("text").lower()
                    logger.debug(f"Checking message: {text}")
                    if "i am " in text and "years old" in text:
                        try:
                            age_text = text.split("i am ")[1].split("years old")[0].strip()
                            if age_text.isdigit():
                                age = age_text
                                logger.debug(f"Extracted age from history: {age}")
                                # Set the slot for future use
                                return [SlotSet("age", age)]
                        except Exception as e:
                            logger.error(f"Error extracting age: {e}")
        
        # If still no age, ask for it
        if age is None:
            logger.debug("No age found, asking user")
            dispatcher.utter_message(text="Can you please tell me your age?")
            return []
        
        # Convert to int if stored as string
        try:
            age_num = int(age)
            logger.debug(f"Converted age to number: {age_num}")
        except ValueError:
            logger.error(f"Could not convert age to number: {age}")
            dispatcher.utter_message(text="I couldn't understand your age. Could you please tell me again?")
            return []
        
        # Provide recommendations based on age
        if age_num < 13:
            recommendations = "Educational games and Kid-friendly learning apps"
        elif age_num < 20:
            recommendations = "Study planning tools and Social media safety guides"
        elif age_num < 30:
            recommendations = "Career development courses and Fitness trackers"
        elif age_num < 50:
            recommendations = "Mindfulness and meditation apps and Financial planning apps"
        elif age_num < 65:
            recommendations = "Health monitoring apps and Retirement planning tools"
        else:
            recommendations = "Memory games and Community engagement platforms"
        
        logger.debug(f"Providing recommendations for age {age_num}: {recommendations}")
        dispatcher.utter_message(text=f"Based on your age ({age}), I recommend: {recommendations}")
        return []

class ActionHandleHealthQuery(Action):
    def name(self) -> Text:
        return "action_handle_health_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get age from slot
        age = tracker.get_slot("age")
        logger.debug(f"Retrieved age for health query: {age}")
        
        # Check if age is available
        if age is None:
            dispatcher.utter_message(text="To provide health information, I need to know your age first. Could you please tell me your age?")
            return []
        
        # Convert to int if stored as string
        try:
            age_num = int(age)
        except ValueError:
            dispatcher.utter_message(text="I couldn't understand your age. Could you please tell me again?")
            return []
        
        # Provide health information based on age
        if age_num < 18:
            health_info = "For your age, it's important to get regular physical activity, eat a balanced diet, and get enough sleep."
        elif age_num < 30:
            health_info = "At your age, focus on establishing good health habits like regular exercise, balanced nutrition, and stress management."
        elif age_num < 50:
            health_info = "For adults in your age range, regular health screenings, balanced diet, and regular exercise are important."
        else:
            health_info = "For your age group, regular check-ups, bone health, cardiovascular exercise, and balanced nutrition are key health priorities."
        
        dispatcher.utter_message(text=health_info)
        return []

class ActionDebug(Action):
    def name(self) -> Text:
        return "action_debug"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Log the current state
        logger.debug("=== DEBUG INFO ===")
        logger.debug(f"Sender ID: {tracker.sender_id}")
        logger.debug(f"Latest message: {tracker.latest_message}")
        logger.debug(f"All slots: {tracker.current_slot_values()}")
        logger.debug(f"Latest intent: {tracker.latest_message.get('intent', {}).get('name')}")
        logger.debug(f"Latest entities: {tracker.latest_message.get('entities', [])}")
        
        # Log recent conversation history
        logger.debug("Recent conversation history:")
        for i, event in enumerate(tracker.events[-10:]):
            if event.get("event") == "user":
                logger.debug(f"User[{i}]: {event.get('text')}")
            elif event.get("event") == "bot":
                logger.debug(f"Bot[{i}]: {event.get('text')}")
        
        logger.debug("=== END DEBUG INFO ===")
        
        # Don't send any message to the user
        return []
