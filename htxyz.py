#!/usr/bin/env python3
import os, markdown , shutil
from datetime import date
sitetitle="ht's website."
sitename="ht.xyz"
footer="Copyright © 2022 - Hitarth Thummar"
sitevars = {
        'sitetitle':sitetitle,
        'sitename':sitename,
        'footer':footer
        }
navbarvals = {
        'home':'/',
        'projects':'/projects',
        'blog':'/blog',
        'artwork':'/artwork',
        'poems':'/poems',
        }


# create the directories needed
for i in os.listdir('./content'):
    if os.path.isdir(f"./content/{i}"):
        if not os.path.isdir(f"./public/{i}"):
            os.makedirs(f"./public/{i}")

def gen_navbar():
    navbar = "<ul>\n"
    for i,j in navbarvals.items():
        navbar+=f"\t\t\t\t\t<li> <a href='{j}'>{i}</a> </li>\n"
    navbar+="\t\t\t\t</ul>"
    sitevars['navbar'] = navbar

gen_navbar() #hence adding the stuff ;)

# generate layout
with open('./templates/layout.html','r') as f:
    master_layout = f.read()
    for i,j in sitevars.items():
        master_layout = master_layout.replace(f"${i}$",j)

# get a dict of all markdown files sorted by date : in the content directory
def get_sorted_index(path):
    filelist = []
    for root, dirs, files in (os.walk(path,topdown=False)):
        for name in files:
            filelist.append(os.path.join(root,name))
    filedict = {}
    datelist = []
    for file in filelist:
        with open(file,'r') as f:
            file_ext = file.split('.')[-1]
            if(file_ext =="md" or file_ext == "html"):
                file_contents = f.read()
                var,text = read_vars(file_contents)
                if 'date' in var:
                    if len(var['date']):
                        filedict['/'+'/'.join(file.split('/')[2:])] = [var['date'],var['title'],var['description']]
    return dict(sorted(filedict.items(), key=lambda pair: date.fromisoformat(pair[1][0]),reverse=True))



def read_vars(text):
    var = dict()
    textarr = text.split('\n')
    i=0
    while textarr[i].strip()!='+++':
        v = textarr[i].split('=')
        var[v[0]] = v[1].replace('"','')
        i+=1
    text = '\n'.join(textarr[i+1:])
    return var,text

# loop through the md files in content, first the homepage
def generate_home_page():
    homepage = './content/home.md'
    with open(homepage,'r') as f:
        var, md = read_vars(f.read())
        html = markdown.markdown(md)
        ## if it is the home page, remove the title and date
        layout = master_layout.replace("<h3 id='articletitle'>$title$</h3>","")
        layout = layout.replace("<small>$date$</small>","")
        for i,j in var.items():
            layout = layout.replace(f"${i}$",j)
        layout = layout.replace(f"$mdtext$",html)
        homeindex = ''
        index_dict = get_sorted_index('./content')
        for i in list(index_dict)[0:5]:
            htmllink = i.replace(".md",".html")
            homeindex+=f"<p><a href='{htmllink}'>{index_dict[i][1]}</a> -  &thinsp;{index_dict[i][0]}</p>\n"
        layout = layout.replace(f"$listindex$",homeindex)
    with open('./public/index.html','w') as f:
        f.write(layout)

# same as above, but for ALL the pages :)
def generate_page(path):
    layout = master_layout
    if(os.path.basename(path)=='home.md'):
        generate_home_page()
        return
    with open(path,'r') as f:
        var, md = read_vars(f.read())
        ## if it is an index page, remove the date
        if(os.path.basename(path)=='index.md'):
            layout = layout.replace("<small>$date$</small>","")
        for i in var.items():
            layout = layout.replace(f"${i[0]}$",i[1])
        html = markdown.markdown(md)
        layout = layout.replace(f"$mdtext$",html)
        if(os.path.basename(path)=='index.md'):
            index_dict = get_sorted_index(os.path.dirname(path))
            homeindex = ''
            for i in list(index_dict):
                htmllink = i.replace(".md",".html")
                homeindex+=f"<p><a href='{htmllink}'>{index_dict[i][1]}</a> -  &thinsp;{index_dict[i][0]}</p>\n"
            layout = layout.replace(f"$listindex$",homeindex)
        output_name = './public/'+('/'.join(path.split('/')[2:]).replace('.md','.html'))
    with open(output_name,'w') as w:
        w.write(layout)

def generate_rss():
    feed = ''
    for i in (get_sorted_index('./content').items()):
        feed+=f"<item><title>{i[1][1]}</title><link>{i[0]}</link><pubDate>{i[1][0]}</pubDate><description>{i[1][2]}</description></item>"
    rsslayout = open('./templates/rss.xml','r').read()
    rsslayout = rsslayout.replace("$rssfeed$",feed)
    with open('./public/rss.xml','w') as w:
        w.write(rsslayout)


if __name__=='__main__':
    filelist = []
    for root, dirs, files in (os.walk('./content',topdown=False)):
        for name in files:
            file_ext = name.split('.')[-1]
            if(file_ext =="md" or file_ext == "html"):
                generate_page(os.path.join(root,name))
    shutil.copytree('./content/static','./public/static',dirs_exist_ok=True)
    generate_rss()
