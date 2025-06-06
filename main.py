import schedule
import time
from create_post import create_instagram_post
from post_to_instagram import post_to_instagram
from quote_generator import generate_and_post_unique_quote
from telegram_alert import send_telegram_photo, wait_for_telegram_reply, send_telegram_alert
from dotenv import load_dotenv

load_dotenv()

# ✅ Optimized combined hashtag set (30 tags total)
HASHTAGS = (
    "\n\n"
    "#Motivation #Discipline #MentalToughness #HustleHard #MindsetMatters "
    "#Grit #InnerStrength #GrowthMindset #SelfDiscipline #NoExcuses "
    "#GrindMode #StrengthWithin #DailyMotivation #PushThrough #HardWorkPaysOff "
    "#WarriorMindset #TrainHard #StayFocused #NeverGiveUp #StudyMotivation "
    "#EntrepreneurMindset #BuiltNotBorn #FaithOverFear #CalmWithinStorm "
    "#RiseAndGrind #WorkHardDreamBig #FitQuote #UnbreakableSpirit "
    "#SmartWorkPaysOff #FuelYourFire"
)

def generate_and_send():
    quote = generate_and_post_unique_quote()
    image_path = create_instagram_post(quote)
    caption = f"{quote}{HASHTAGS}"

    send_telegram_photo(image_path, caption)
    return image_path, caption, quote

def run_bot():
    try:
        image_path, caption, quote = generate_and_send()

        while True:
            reply = wait_for_telegram_reply(timeout=10800)  # 3 hours

            if reply == "yes":
                post_to_instagram(image_path, caption)
                send_telegram_alert(f"✅ Post approved and uploaded:\n\n{quote}")
                print("✅ Posted successfully.")
                break

            elif reply == "no":
                send_telegram_alert("🔁 Post rejected. Generating a new one...")
                image_path, caption, quote = generate_and_send()
                continue

            elif reply == "timeout":
                send_telegram_alert("⌛ No reply in 3 hours. Skipping this post.")
                print("⌛ Timeout. Skipping.")
                break

    except Exception as e:
        print("❌ Error during post:", e)
        send_telegram_alert(f"❌ Bot crashed: {e}")

# Schedule times (UTC)
schedule.every().day.at("04:33").do(run_bot)
schedule.every().day.at("14:00").do(run_bot)
schedule.every().day.at("18:00").do(run_bot)

print("🔄 Bot is running. Waiting for scheduled posts...")

while True:
    schedule.run_pending()
    time.sleep(30)
