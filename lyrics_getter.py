from bs4 import BeautifulSoup
import httplib #HTTPConnection
import sys
import time

def escape(str_value):
    return '%20'.join(str_value.split())
def get_lyrics(artist,title):
    conn = httplib.HTTPConnection("api.chartlyrics.com")
    conn.request("GET", "/apiv1.asmx/SearchLyric?artist=%s&song=%s"%(escape(artist),escape(title)) )
    r1 = conn.getresponse()
    if r1.status != 200:
        raise Exception("Status code is %d. Should be 200" % (r1.status))
    data1 = r1.read()
    soup = BeautifulSoup(data1, "xml")
    id = soup.ArrayOfSearchLyricResult.SearchLyricResult.LyricId.text
    chksum = soup.ArrayOfSearchLyricResult.SearchLyricResult.LyricChecksum.text

    # resets connection otherwise
    time.sleep(0.55)
    conn.request("GET","/apiv1.asmx/GetLyric?lyricId=%s&lyricCheckSum=%s" % (str(id),str(chksum)) )
    r2 = conn.getresponse()
    if r2.status != 200:
        raise Exception("Status code is %d. Should be 200" % (r2.status))
    data2 = r2.read()
    soup2 = BeautifulSoup(data2, "xml")
    conn.close()
    return soup2.GetLyricResult.Lyric.text


if __name__ == '__main__':
    print (get_lyrics(sys.argv[1],sys.argv[2]))
