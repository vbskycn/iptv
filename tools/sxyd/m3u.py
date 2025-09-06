class Channel:
    def __init__(self, tvg_id: str, tvg_name: str, tvg_logo: str, group_title: str, m3u8: str):
        self.tvg_id = tvg_id
        self.tvg_name = tvg_name
        self.tvg_logo = tvg_logo
        self.group_title = group_title
        self.m3u8 = m3u8

class M3u:
    def __init__(self, channels: list[Channel]):
        self.channels = channels

    def generate_text(self) -> str:
        text = "#EXTM3U\n"
        
        for channel in self.channels:
            text += f'#EXTINF:-1 tvg-id="{channel.tvg_id}" tvg-name="{channel.tvg_name}" tvg-logo="{channel.tvg_logo}" group-title="{channel.group_title}",{channel.tvg_name}\n'
            text += f"{channel.m3u8}\n"
            
        return text 