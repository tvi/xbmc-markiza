import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, sys, os, time
import cookielib

__plugin__ = "markiza"
__author__ = "Tommy"
__url__ = ""
__svn_url__ = ""
__useragent__ = ""
__credits__ = "Tommy"
__version__ = "1.5.0"
__svn_revision__ = "$Revision$"
__XBMC_Revision__ = "22965"



baseurl = 'http://video.markiza.sk/archiv-tv-markiza'
bconf = 'http://www.markiza.sk/js/flowplayer/config.js?&media='
def getHTML( url, referer, redirect=False):
        try:
                cj = cookielib.LWPCookieJar()
                req = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                req.addheaders = [('Referer', referer),
                                  ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
                response = req.open(url)
                link = response.read()
                response.close()
                reurl = response.geturl()
        except urllib2.URLError, e:
                print 'Error code: ', e.code
                return False
        else:
                if redirect==True:
                        reurl = re.compile('file=(.+?)&').findall(reurl, re.DOTALL)[0]
                        response = req.open(reurl)
                        link = response.read()
                        response.close()
                        return link
                else:
                        return link

def SEASONS():
        data = getHTML(baseurl,baseurl)
        seasons = re.compile('<a href="(.+?)"><img src="(.+?)" width=".+?" height=".+?" title="(.+?)"></a>').findall(data, re.DOTALL)
        for url, img, title in seasons:
                addDir(title,'http://video.markiza.sk'+url,1,img)             
                
def EPISODES(url):
        data = getHTML(url,baseurl)
        episodes = re.compile(""" <div class="image"><a href=".+?"><img src="(.+?)" /></a></div>
 <div class="title"><a href="(.+?)">(.+?)</a></div>
 <span>(.+?)<br/>(.+?)</span>""").findall(data, re.DOTALL)
        for image, url, title, date, pv in episodes:
                #addDir(title,bconf + url.split('/')[3],2,image)
                addDir(title +' '+date,bconf + url.split('/')[3],2,image)

def VIDEOLINKS(url,name):
         data = getHTML(url,baseurl)
         pl=xbmc.PlayList(1)
         pl.clear()
         episode = re.compile('"url":"(.+?)"').findall(data, re.DOTALL)
         for links in episode:
                if links.split('/')[4] == 'video':
                        string = links
                       
         item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')       
         item.setInfo( type="Video", infoLabels={ "Title": name})
         xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(string, item)


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        SEASONS()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1:
        print ""+url
        EPISODES(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)
