from datetime import datetime
import xml.etree.ElementTree as ET

class Channel:
    def __init__(self, channel_id: str, display_name: str, programme_title: str, 
                 programme_start: datetime, programme_stop: datetime):
        self.channel_id = channel_id
        self.display_name = display_name
        self.programme_title = programme_title
        self.programme_start = programme_start
        self.programme_stop = programme_stop

class Xmltv:
    def __init__(self, channels: list[Channel]):
        self.channels = channels

    def generate_text(self) -> str:
        tv = ET.Element("tv")
        tv.set("generator-info-name", "GITV")
        
        # 添加频道信息
        for channel in self.channels:
            channel_element = ET.SubElement(tv, "channel")
            channel_element.set("id", channel.channel_id)
            
            display_name = ET.SubElement(channel_element, "display-name")
            display_name.text = channel.display_name
            
            # 添加节目信息
            programme = ET.SubElement(tv, "programme")
            programme.set("channel", channel.channel_id)
            programme.set("start", channel.programme_start.strftime("%Y%m%d%H%M%S +0800"))
            programme.set("stop", channel.programme_stop.strftime("%Y%m%d%H%M%S +0800"))
            
            title = ET.SubElement(programme, "title")
            title.text = channel.programme_title

        return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tv, encoding='unicode', xml_declaration=False) 