from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import feedparser

bot_token = ""
app_token = ""
feed_link = "https://ysws.hackclub.com/feed.xml"
bot = App(token = bot_token)

def feed_send(say):
    feed = feedparser.parse(feed_link)
    out = ""
    for entry in feed.entries:
        title = entry.get("title")
        link = entry.get("link")
        desc = entry.get("description")
        desc_start_key = "![CDATA["
        desc_end_key = "</p>"
        desc_start = desc.find(desc_start_key) + 4
        desc_end = desc.find(desc_end_key)
        description = desc[desc_start:desc_end]
        dead_start_key = "</strong>"
        dead_end_key = "2025"
        end_key2 = "2026"
        dead_start = desc.find(dead_start_key) + 10
        dead_end = desc.find(dead_end_key) + 4
        dead_end2 = desc.find(end_key2) + 4
        deadline = (desc[dead_start:dead_end])
        deadline2 = (desc[dead_start:dead_end2])
        out += "\n• <" + link + "|" + title + ">\n" + "*Description:* " + description
        if len(deadline.strip()) > 0:
            out += "\n*Deadline:* " + deadline + deadline2
        out += "\n" + 90 * "─"
    out += "\nFull site: https://ysws.hackclub.com/"
    say(out)

@bot.event("app_mention")
def mention_event(event,say):
    user = event.get("user")
    say(
        text = "Hello <@" + user + ">Select option:",
        blocks = [
            {
                "type":"section",
                "text":{"type":"mrkdwn","text":"Hello <@" + user + "> \nPlease select an option:"},
            },
            {
                "type":"actions",
                "elements":[
                    {
                        "type":"button",
                        "text":{"type": "plain_text","text":"YSWS"},
                        "action_id":"ysws_button",
                    }
                ]
            }
        ]
    )

@bot.action("ysws_button")
def handle_ysws_click(ack,body,say):
    ack()
    user_id = body["user"]["id"]
    say("<@" + user_id + "> *You Ship We Ship Programs:-*")
    feed_send(say)

@bot.message("YSWS")
def handle_ysws(message,say):
    user_id = message.get("user")
    say("<@" + user_id + "> *You Ship We Ship Programs:-*")
    feed_send(say)

if __name__ == "__main__":
    handler=SocketModeHandler(bot,app_token)
    handler.start()