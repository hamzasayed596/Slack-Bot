import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import feedparser
import requests



bot_token = os.environ.get("SLACK_BOT_TOKEN")
app_token = os.environ.get("SLACK_APP_TOKEN")
ysws_feed_link = "https://ysws.hackclub.com/feed.xml"
toolbox_feed_link = "https://raw.githubusercontent.com/hackclub/toolbox/main/manifest.js"
bot = App(token = bot_token)



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
                    },
                    {
                        "type":"button",
                        "text":{"type": "plain_text","text":"Toolbox"},
                        "action_id":"toolbox_button",
                    }
                ]
            }
        ]
    )



def ysws_feed_send(say):
    feed = feedparser.parse(ysws_feed_link)
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

@bot.action("ysws_button")
def handle_ysws_click(ack,body,say):
    ack()
    user_id = body["user"]["id"]
    say("<@" + user_id + "> *You Ship We Ship Programs:-*")
    ysws_feed_send(say)

@bot.message("YSWS")
def handle_ysws(message,say):
    user_id = message.get("user")
    say("<@" + user_id + "> *You Ship We Ship Programs:-*")
    ysws_feed_send(say)



def toolbox_feed_send(say):
    response = requests.get(toolbox_feed_link)
    out = ""
    past_title = None
    past_desc = None
    past_link = None
    for line in response.text.splitlines():
        s = line.strip()
        if "name:" in s:
            start = s.find("'")
            if start == -1:
                start = s.find('"')
            if start != -1:
                end = s.find(s[start], start + 1)
                if end != -1:
                    past_title = s[start + 1:end]
        if "description:" in s:
            start = s.find("'")
            if start == -1:
                start = s.find('"')
            if start != -1:
                end = s.find(s[start], start + 1)
                if end != -1:
                    past_desc = s[start + 1:end]
        if "url:" in s:
            start = s.find("'")
            if start == -1:
                start = s.find('"')
            if start != -1:
                end = s.find(s[start], start + 1)
                if end != -1:
                    past_link = s[start + 1:end]
                    title = past_title if past_title else past_link
                    desc = past_desc if past_desc else past_link
                    if past_link.find("http") != -1:
                        out += "\n• <" + past_link + "|" + title + ">\n"
    say(out)

@bot.action("toolbox_button")
def handle_toolbox_click(ack,body,say):
    ack()
    user_id = body["user"]["id"]
    say("<@" + user_id + "> *Toolbox:-*")
    toolbox_feed_send(say)

@bot.message("Toolbox")
def handle_toolbox(message, say):
    user_id = message.get("user")
    say("<@" + user_id + "> *Toolbox:-*")
    toolbox_feed_send(say)



if __name__ == "__main__":
    handler=SocketModeHandler(bot,app_token)
    handler.start()

