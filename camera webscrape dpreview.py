import unicodecsv
import time
import re
from lxml import html
from bs4 import BeautifulSoup

def cycle_links():
    r = requests.get("https://www.dpreview.com/products/cameras/all?sort=alphabetical&view=list")
    webpage = html.fromstring(r.content)
    links=webpage.xpath('//a/@href')

    links_length=len(links)

    gudlinks=[]

    for i in range(24,links_length):
        if "buy" not in links[i]:
            gudlinks.append(links[i])

    final_links=gudlinks[::2]

    for link in final_links:
        scrape_details(link)
        time.sleep(1)


def scrape_details(link):
    indiv = requests.get(link)
    soup = BeautifulSoup(indiv.content, "lxml")

    name=(soup.title).text
    m = re.search("(.+?):", name)
    if m:
        m=m.group(1)
    else: return

    if "review" in str.lower(m):
        return

    td = soup.find_all("td", class_="value")
    tdname = soup.find_all("td", class_="label")

    n=0
    bodytype=maxres=effectivepixels=sensorsize=sensortype=lensmount=focallength=artLCD=maxaperture=screensize=iso=screendots=maxshutterspeed=myformat=storagetypes=usb=weight=dim=gps="NA"

    for col in tdname:
        if col.text == "Body type":
            bodytype=td[n].text
        if col.text == "Max resolution":
            maxres=td[n].text
        if col.text == "Effective pixels":
            effectivepixels=td[n].text
        if col.text == "Sensor Size":
            sensorsize=td[n].text
        if col.text == "Sensor type":
            sensortype=td[n].text
        if col.text == "Lens mount":
            lensmount=td[n].text
        if "Focal length" in col.text:
            focallength=td[n].text
        if col.text == "Articulated LCD":
            artLCD=td[n].text
        if col.text == "Max aperture":
            maxaperture=td[n].text
        if col.text == "Screen size":
            screensize=td[n].text
        if col.text == "ISO":
            iso=td[n].text
        if col.text == "Screen dots":
            screendots=td[n].text
        if col.text == "Max shutter speed":
            maxshutterspeed=td[n].text
        if col.text == "Format":
            myformat=td[n].text
        if col.text == "Storage types":
            storagetypes=td[n].text
        if col.text == "USB":
            usb=td[n].text
        if "Weight" in col.text:
            weight=td[n].text
        if col.text in "Dimensions":
            dim=td[n].text
        if col.text in "GPS":
            gps=td[n].text
        n=n+1
        
    writer.writerow([m.lstrip(), bodytype.lstrip(), maxres.lstrip(), effectivepixels.lstrip(), sensorsize.lstrip(), sensortype.lstrip(), focallength.lstrip(), lensmount.lstrip(), artLCD.lstrip(), maxaperture.lstrip(), screensize.lstrip(), iso.lstrip(), screendots.lstrip(), maxshutterspeed.lstrip(), myformat.lstrip(), storagetypes.lstrip(), usb.lstrip(), weight.lstrip(), dim.lstrip(), gps.lstrip()])


f = open("dpreview_camera_scrape.csv", "wb")
writer = unicodecsv.writer(f)
writer.writerow(["camera name", "body type", "max resolution", "effective pixels", "sensor size", "sensor type", "focal length", "lens mount", "articulated LCD", "maximum aperture", "screen size", "iso", "screen dots", "max shutter speed", "format", "storage types", "usb", "weight", "dimension", "gps"])
cycle_links()
f.close()
