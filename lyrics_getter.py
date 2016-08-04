from bs4 import BeautifulSoup
import httplib #HTTPConnection
import sys
import time
from text_search.main import DocumentSearcher

searcher = DocumentSearcher()

def escape(str_value):
    return '%20'.join(str_value.split())
def get_lyrics(artist,title):
    # stupid python2 workaround
    artist = u''+artist
    title = u''+title
    conn = httplib.HTTPConnection("api.chartlyrics.com")
    conn.request("GET", "/apiv1.asmx/SearchLyric?artist=%s&song=%s"%(escape(artist),escape(title)) )
    r1 = conn.getresponse()
    if r1.status != 200:
        raise Exception("Status code is %d. Should be 200" % (r1.status))
    data1 = r1.read()
    soup = BeautifulSoup(data1, "xml")
    title_id_chksum_map = {}
    for result_node in soup.find_all('SearchLyricResult'):
        try:
#            print ('SONG: ',result_node.find('Song').text)
            title_id_chksum_map[result_node.find('Song').text]= result_node.find('LyricId').text, result_node.find('LyricChecksum').text
        except Exception as e:
            print (e)
    id = None
    chksum = None
    print (title_id_chksum_map)
    if len(title_id_chksum_map.keys()) > 1:
        with searcher as s:
            s.set_documents(title_id_chksum_map.keys())
            for k,v in s.search( title ):
                print ('RESULT: ',k,v)
            _ , best_title = s.get_best_match( title )
            id, chksum = title_id_chksum_map[best_title]
    elif len(title_id_chksum_map.keys()) == 1:
        id, chksum = title_id_chksum_map[title_id_chksum_map.keys()[0]]

    if id is None or chksum is None:
        return None
    # resets connection otherwise
    time.sleep(0.65)
    req = "/apiv1.asmx/GetLyric?lyricId=%s&lyricCheckSum=%s" % (str(id),str(chksum))
    print (req)
    conn.request("GET", req )
    r2 = conn.getresponse()
    if r2.status != 200:
        raise Exception("Status code is %d. Should be 200" % (r2.status))
    data2 = r2.read()
    soup2 = BeautifulSoup(data2, "xml")
    conn.close()
    return soup2.GetLyricResult.Lyric.text


if __name__ == '__main__':
    print (get_lyrics(sys.argv[1],sys.argv[2]))
