#! /usr/bin/env python

#print "Content-type: text/html"
#print

import cgi
import sys
import os
import urllib, urllib2
import cPickle

TAGS_TO_REMOVE = {"img":["<img ",">"],"font":["<font ",">"],"p":["<p ",">"],\
                  "span":["<span",">"],"div":["<div",">"],"script":["<script",">"], "h-something":["<h",">"]}


def JointLines(lines, begin_line_index, end_line_index):
    output = ''
    for i in range(begin_line_index, end_line_index):
        try:
            output += lines[i]
        except:
            break
    return output

def IsASublistOfB(list_a, list_b):
    len_a = len(list_a)
    len_b = len(list_b)
    list_a_name_and_pos = map(lambda x: x[0:2], list_a)
    list_b_name_and_pos = map(lambda x: x[0:2], list_b)
    for i in range(len_b):
        if len_a+i>len_b:
            return False
        if list_a_name_and_pos==list_b_name_and_pos[i:i+len_a]:
            return True
    return False

def DuplicateLists(lists):
    output_lists = []
    for l in lists:
        output_lists.append(map(lambda x: x, l))
    return output_lists

def ReadLinesFromStr(line):
    splitters = ['\r\n','\n\r','\n','\r','<br>','<br/>','<br />',\
                 '<Br>','<BR>','<Br/>','<Br />','<BR/>','<BR/>']
    splitters = filter(lambda x: x in line, splitters)
    splitters.sort(lambda x, y: len(y)-len(x))
    splitter = splitters[0]

    return line.split(splitter)

def RemoveTag(input_text, begin_tag, end_tag, is_debug_mode=0):
    output_text = input_text
    begin_pos = output_text.find(begin_tag)
    while (begin_pos!=-1):
        end_pos = output_text[begin_pos:].find(end_tag)+begin_pos+len(end_tag)
        text_to_remove = output_text[begin_pos:end_pos]
        if is_debug_mode:
            print "text_to_remove for " + begin_tag + " = "+ text_to_remove
        output_text = output_text.replace(text_to_remove, "")
        begin_pos = output_text.find(begin_tag)	
    return output_text


###remove photos, hyper links, and fonts###
def RemoveTags(input_text,tags_to_remove = TAGS_TO_REMOVE, is_debug_mode=False):
    if is_debug_mode:
        print "removing tags for " + input_text[:20] + " ..."
    output_text = input_text.replace("<br />","\n").replace("<br/>","\n").replace("<br>","\n").replace("<p>","\n").replace("\n\n","\n")

    if is_debug_mode:
        print "starting for loop..."

        
    for tag_type in tags_to_remove.keys():
        begin_tag = tags_to_remove[tag_type][0]
        end_tag = tags_to_remove[tag_type][1]
        output_text = RemoveTag(output_text, begin_tag, end_tag, is_debug_mode)

    output_text = output_text.replace("\n,","\n").replace("&nbsp;","")
    if is_debug_mode:
        print "starting while loop..."

    output_text = output_text.replace("&hellip;","").replace("</a>","").replace("</font>","").replace("</p>","").replace("</table>","")
    output_text = output_text.replace("<strong>","").replace("</strong>","").replace("</div>","").replace("</script>","")
    output_text = output_text.replace("&spades;","").replace("<li>","").replace("</ol>","").replace("</li>","").replace("</span>","")
    #output_text = output_text.replace("<","").replace(">","")
    while "\n\n" in output_text:
        output_text = output_text.replace("\n\n","\n")
    return output_text

###find the main content###
def FindMainContent(input_text, begin_tag, end_tag,is_debug_mode=False):
    output_text = input_text 
    begin_pos = output_text.find(begin_tag)+len(begin_tag)
    end_pos = output_text[begin_pos:].find(end_tag)+begin_pos
    output_text = output_text[begin_pos:end_pos]
    if is_debug_mode:
        print "begin_tag=%s; begin_pos=%s"%(begin_tag, begin_pos)
        print "end_tag=%s; end_pos=%s"%(end_tag, end_pos)
        print "output_text="
        print output_text
    output_text = RemoveTags(output_text, TAGS_TO_REMOVE, is_debug_mode).strip()
    if output_text=='':
        print "Error: Cannot find main content...end"
        exit()
    return output_text

###find the title###
def FindTitle(input_text, begin_tag, end_tag, is_debug_mode=False):
    output_text = input_text
    begin_pos = output_text.find(begin_tag)+len(begin_tag)
    end_pos = output_text[begin_pos:].find(end_tag)+begin_pos
    output_text = output_text[begin_pos:end_pos]
    #output_text = RemoveTags(output_text, TAGS_TO_REMOVE, is_debug_mode).strip()
    if output_text=='':
        print "Error: Cannot find title...end"
        exit()
    if is_debug_mode:
        print "title found: " + output_text
    return output_text, begin_pos


###find the title###
def FindTitle(input_text, begin_tag, end_tag, is_debug_mode=False):
    output_text = input_text
    begin_pos = output_text.find(begin_tag)+len(begin_tag)
    end_pos = output_text[begin_pos:].find(end_tag)+begin_pos
    output_text = output_text[begin_pos:end_pos]
    #output_text = RemoveTags(output_text, TAGS_TO_REMOVE, is_debug_mode).strip()
    if output_text=='':
        print "Error: Cannot find title...end"
        exit()
    if is_debug_mode:
        print "title found: " + output_text
    return output_text, begin_pos


### WRETCH.CC ###
def ReadWretchArticle(raw_text,is_debug_mode=False):
    title_begin_tag = "h3 class=\"title\""
    title_end_tag = "/h3>"
    title, title_begin_pos = FindTitle(raw_text, title_begin_tag, title_end_tag, is_debug_mode)
    raw_text = raw_text[title_begin_pos:]

    begin_tag = "innertext\""
    end_tag = "div"
    main_content = FindMainContent(raw_text, begin_tag, end_tag,is_debug_mode)
    return title, main_content


### PIXNET.NET ###
def ReadPixnetArticle(raw_text,is_debug_mode=False):
    title_begin_tag = "<li class=\"title\">"
    title_end_tag = "</a>"
    title, title_begin_pos = FindTitle(raw_text, title_begin_tag, title_end_tag, is_debug_mode)
    raw_text = raw_text[title_begin_pos:]

    begin_tag = "article-content\">"
    end_tag = "/div"
    main_content = FindMainContent(raw_text, begin_tag, end_tag,is_debug_mode)
    return title, main_content


### XUITE ###
def ReadXuiteArticle(raw_text,is_debug_mode=False):
    title_begin_tag = "titlename\""
    title_end_tag = "/span>"
    title, title_begin_pos = FindTitle(raw_text, title_begin_tag, title_end_tag, is_debug_mode)
    raw_text = raw_text[title_begin_pos:]

    begin_tag = "blogbody\""
    end_tag = "/div>"
    main_content = FindMainContent(raw_text, begin_tag, end_tag,is_debug_mode)
    return title, main_content

### YAM ###
def ReadYamArticle(raw_text,is_debug_mode=False):
    title_begin_tag = "post_titlediv\""
    title_end_tag = "</a>"
    title, title_begin_pos = FindTitle(raw_text, title_begin_tag, title_end_tag, is_debug_mode)
    raw_text = raw_text[title_begin_pos:]

    if "id=\"post_content\"" in raw_text:
        begin_tag = "id=\"post_content\""
    elif "<div class=\"main\">" in raw_text:
        begin_tag = "<div class=\"main\">"
    else:
        print "Error: Cannot find Begin Tag of url...end"
        exit()

    begin_pos = raw_text.find(begin_tag)+len(begin_tag)

    if "br clear=\"all\"" in raw_text and raw_text[begin_pos:].find("br clear=\"all\"")!=-1:
        end_tag = "br clear=\"all\""
    elif "<!-- " in raw_text and raw_text[begin_pos:].find("<!-- ")!=-1:
        end_tag = "<!-- "
    elif "</div>" in raw_text and raw_text[begin_pos:].find("</div>")!=-1:
        end_tag = "</div>"
    else:
        print "Error: Cannot find End Tag of url...end"
        exit()

    end_pos = raw_text[begin_pos:].find(end_tag)+begin_pos
    raw_text = raw_text[begin_pos:end_pos]
    raw_text = RemoveTags(raw_text, TAGS_TO_REMOVE, is_debug_mode).strip()
    if raw_text=='':
        print "Error: Cannot find main content...end"
        exit()
    main_content = raw_text

    return title, main_content

### UDN ###
def ReadUdnArticle(raw_text,is_debug_mode=False):
    title_begin_tag = "<span id=\"maintopic\">"
    title_end_tag = "</span>"
    title, title_begin_pos = FindTitle(raw_text, title_begin_tag, title_end_tag, is_debug_mode)
    raw_text = raw_text[title_begin_pos:]

    begin_tag = "mainbody\""
    end_tag = "</td>"
    main_content = FindMainContent(raw_text, begin_tag, end_tag,is_debug_mode)
    return RemoveTags(title, TAGS_TO_REMOVE, is_debug_mode), RemoveTags(main_content, TAGS_TO_REMOVE, is_debug_mode)    

def EncodeToUtf8(stream, is_debug_mode=0):
    charset_begin_pos = stream.find("charset=")
    charset_end_pos = stream[charset_begin_pos+8:].find("\"")+charset_begin_pos+8
    charset = stream[charset_begin_pos+8:charset_end_pos]
    if is_debug_mode:
        print "character set="+ charset
    if charset=='Big5' or charset=='big5' or charset=='BIG5':
        if is_debug_mode:
            print "encoding stream into utf-8..."
        #try:
        stream = stream.decode('big5','ignore').encode("utf-8",'ignore')
        #except:
        #    stream = stream
    return stream


def ReadBlogUrl(url, is_debug_mode=False):
    if is_debug_mode:
        print "reading path: "+ url
    stream = None
    try:
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers={'User-Agent':user_agent,} 
        request=urllib2.Request(url,None,headers)
        response = urllib2.urlopen(request)
        stream = response.read() 	
    except:
        print "cannot reach path: " + url + " ...end"
        exit()
    if is_debug_mode:
        print "success"
    return stream

def ReadArticle(url, stream, is_debug_mode=False):
    if is_debug_mode:
        print "processing derived content..."
    if '.wretch.' in url:
        title, article_text = ReadWretchArticle(stream, is_debug_mode)
    elif '.pixnet.' in url:
        title, article_text = ReadPixnetArticle(stream, is_debug_mode)
    elif '.xuite.' in url:
        title, article_text = ReadXuiteArticle(stream, is_debug_mode)
    elif '.yam.' in url:
        title, article_text = ReadYamArticle(stream, is_debug_mode)
    elif '.udn.' in url:
        title, article_text = ReadUdnArticle(stream, is_debug_mode)
    else:
        article_text = "path unrecognized...finished"
        title = ''

    return title, article_text

if __name__ == '__main__': 

    is_debug_mode = 0
    if not sys.argv[1:]:
        url = ""
    else:
        url = sys.argv[1]

    stream = ReadBlogUrl(url, is_debug_mode)
    if stream==None:
        exit()

    stream = EncodeToUtf8(stream, is_debug_mode)
    title, article_text = ReadArticle(url, stream, is_debug_mode)
    """
    ostream = open("output.html",'w')
    ostream.write(article_text)
    ostream.close()
    """
    print "title: " + title
    print "<br><br><br>"
    print article_text


