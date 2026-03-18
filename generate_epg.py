import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_multi_channel_epg():
    # 1. Configuration: Your 10 Channels
    channels = [
        {"id": "INFO.bud", "name": "SYSTEM INFO / DISCORD"},
        {"id": "Channel1.bud", "name": "Action Movies"},
        {"id": "Channel2.bud", "name": "Classic TV"},
        {"id": "Channel3.bud", "name": "Sci-Fi Zone"},
        {"id": "Channel4.bud", "name": "Comedy Central Clone"},
        {"id": "Channel5.bud", "name": "Documentary Hub"},
        {"id": "Channel6.bud", "name": "News 24/7"},
        {"id": "Channel7.bud", "name": "Sports Replays"},
        {"id": "Channel8.bud", "name": "Music Hits"},
        {"id": "Channel9.bud", "name": "Kids Club"}
    ]
    
    CUSTOM_MESSAGES = [
        "DISCORD: https://discord.gg/fnsWGDy2mm",
        "UPDATE: EPG Light Project v2.0 is now live.",
        "NOTICE: Maintenance scheduled for Sunday at 02:00.",
        "TIP: Use Tivimate for the best experience with this guide."
    ]
    
    # 2. Generate the ID Reference File (epg_ids.txt)
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    timestamp_str = now_utc.strftime('%Y%m%d%H%M') # Matches your example: 202603181136 
    
    with open("epg_ids.txt", "w", encoding="utf-8") as f:
        f.write(f"{timestamp_str}\n\n\n")
        f.write("-- epg_ripper_DUMMY_CHANNELS --\n\n")
        for ch in channels:
            f.write(f"{ch['id']}\n")
    
    # 3. Create XML Root
    tv = ET.Element('tv')
    
    # 4. Add Channel Definitions
    for ch in channels:
        chan_elem = ET.SubElement(tv, 'channel', id=ch["id"])
        ET.SubElement(chan_elem, 'display-name').text = ch["name"]
    
    # 5. Generate Programming
    base_start = now_utc.replace(minute=0, second=0, microsecond=0)
    update_timestamp = now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')
    
    for ch in channels:
        if ch["id"] == "INFO.bud":
            # 24-HOUR BLOCK
            prog_start = base_start
            prog_stop = base_start + datetime.timedelta(hours=24)
            start_str = prog_start.strftime('%Y%m%d%H%M%S +0000')
            stop_str = prog_stop.strftime('%Y%m%d%H%M%S +0000')
            
            prog = ET.SubElement(tv, 'programme', start=start_str, stop=stop_str, channel=ch["id"])
            ET.SubElement(prog, 'title', lang="en").text = "SYSTEM STATUS & DISCORD INFO"
            full_description = "\n".join(CUSTOM_MESSAGES) + f"\n\nLAST REGEN: {update_timestamp}"
            ET.SubElement(prog, 'desc', lang="en").text = full_description
            
        else:
            # 2-HOUR BLOCKS
            for i in range(12):
                prog_start = base_start + datetime.timedelta(hours=i*2)
                prog_stop = prog_start + datetime.timedelta(hours=2)
                start_str = prog_start.strftime('%Y%m%d%H%M%S +0000')
                stop_str = prog_stop.strftime('%Y%m%d%H%M%S +0000')
                
                prog = ET.SubElement(tv, 'programme', start=start_str, stop=stop_str, channel=ch["id"])
                ET.SubElement(prog, 'title', lang="en").text = f"{ch['name']} - Block {i+1}"
                ET.SubElement(prog, 'desc', lang="en").text = "Continuous automated programming."

    # 6. Save XML
    xml_string = ET.tostring(tv, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")
    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print("Successfully generated epg.xml and epg_ids.txt")

if __name__ == "__main__":
    generate_multi_channel_epg()
