class DiscordWebhook:
    def __init__(self, url=None, username=None):
        self.url = url
        self.username = username
    def add_embed(self, embed):
        self.embed = embed
    def execute(self):
        class Resp:
            status_code = 200
        return Resp()

class DiscordEmbed:
    def __init__(self, title=None, description=None, color=0, timestamp=None):
        self.title = title
        self.description = description
        self.color = color
        self.timestamp = timestamp
    def add_embed_field(self, name=None, value=None, inline=False):
        pass
    def set_footer(self, text=None):
        pass
    def set_thumbnail(self, url=None):
        pass
    def set_author(self, name=None):
        pass
