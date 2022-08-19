#!/usr/bin/env python3
import os
import markdown
import shutil
from html import escape
from datetime import date
from csscompressor import compress

CONTENT_DIR = "./content"
PUBLIC_DIR = "./public"
CSS_FILE = "./content/static/css/sp.css"

sitetitle = "ht's website."
sitename = "ht.xyz"
siteurl = "https://hitarththummar.xyz"
footer = "Copyright © 2022 - Hitarth Thummar"
css = compress(open(CSS_FILE,'r').read())
sitevars = {"sitetitle": sitetitle, "sitename": sitename, "footer": footer,"css":css}
NAV_BAR_VALUES = {
    "home": "/",
    "projects": "/projects",
    "blog": "/blog",
    "artwork": "/artwork",
    "poems": "/poems",
}


def init_dir_structure():
    """
    create the needed directories
    """
    for directory in os.listdir(CONTENT_DIR):
        if os.path.isdir(os.path.join(CONTENT_DIR, directory)):
            os.makedirs(os.path.join(PUBLIC_DIR, directory), exist_ok=True)


def gen_navbar(nav_bar_items):
    """
    generates the html code for the navbar
    """
    navbar_html = []
    navbar_html.append("<ul>")
    for link_name, link_path in nav_bar_items.items():
        navbar_html.append(
            f"\t\t\t\t\t<li> <a href='{escape(link_path)}'>{escape(link_name)}</a></li>"
        )
    navbar_html.append("\t\t\t\t</ul>")
    return "\n".join(navbar_html)


def generate_layout(var):
    """
    generate the layout template file
    """
    TEMPLATE_FILE = "./templates/layout.html"
    with open(TEMPLATE_FILE, "r") as f:
        master_layout = f.read()
    for var_key, var_value in var.items():
        master_layout = master_layout.replace(f"${var_key}$", var_value)
    return master_layout


init_dir_structure()
sitevars['navbar'] = gen_navbar(NAV_BAR_VALUES)
master_layout = generate_layout(sitevars)

def get_sorted_index(path):
    """
    get a list of all markdown files sorted by date : in the 'path' directory
    """
    filelist = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith((".md", ".html")):
                file = os.path.join(root, name)
                with open(file, "r") as f:
                    variable, text = read_vars(f.read())
                if "date" in variable:
                    filelist.append(
                        [
                            os.path.join(os.path.splitext(file)[0]),
                            variable["date"],
                            variable["title"],
                            variable["description"],
                        ]
                    )
    return sorted(filelist, key=lambda x: date.fromisoformat(x[1]), reverse=True)


def read_vars(text):
    """
    get the variables from a markdown front matter
    """
    variables = dict()
    textarr = text.splitlines()
    i = 0
    while textarr[i].strip() != "+++":
        v = textarr[i].split("=")
        variables[v[0]] = v[1].replace('"', "")
        i += 1
    text = "\n".join(textarr[i + 1 :])  # This gives the text without the front matter
    return variables, text


def generate_home_page():
    """
    special function to generate the home page because we only want to show the first five items
    """
    homepage = os.path.join(CONTENT_DIR, "home.md")

    variables , markdowntext = read_vars(open(homepage,'r').read())
    htmltext = markdown.markdown(markdowntext)
    layout = master_layout.replace("<h3 id='articletitle'>$title$</h3>", "")  ## if it is the home page, remove the title and date, edge case
    layout = layout.replace("<small>$date$</small>", "")

    for key, value in variables.items():
        layout = layout.replace(f"${key}$", value)

    layout = layout.replace(f"$mdtext$", htmltext)

    homeindex = ""
    index_dict = get_sorted_index(CONTENT_DIR)
    for i in index_dict[0:5]:
        htmllink = '/'.join(i[0].replace(".md",".html").split("/")[2:])
        homeindex += (
            f"<p> <a href='/{htmllink}'>{i[2]}</a> -  &thinsp;{i[1]} </p>\n"
        )
    layout = layout.replace(f"$listindex$", homeindex)

    with open(os.path.join(PUBLIC_DIR, "index.html"), "w") as f:
        f.write(layout)


# same as above, but for ALL the pages :)
def generate_page(path):
    layout = master_layout

    if os.path.basename(path) == "home.md":
        generate_home_page()
        return

    variables, markdowntext = read_vars(open(path,'r').read())
    htmltext = markdown.markdown(markdowntext)
    layout = layout.replace(f"$mdtext$", htmltext)

    ## if it is an index page, remove the date and create index

    if os.path.basename(path) == "index.md":
        layout = layout.replace("<small>$date$</small>", "")
        index_list = get_sorted_index(os.path.dirname(path))
        index_html = ""
        for i in index_list:
            htmllink = '/'.join(i[0].replace(".md",".html").split("/")[2:])
            index_html += (
                f"<p><a href='/{htmllink}'>{i[2]}</a> -  &thinsp;{i[1]}</p>\n"
            )
        layout = layout.replace(f"$listindex$", index_html)

    for i in variables.items():
        layout = layout.replace(f"${i[0]}$", i[1])

    output_name = path.replace("./content", "./public").replace(".md",".html")
    with open(output_name, "w") as w:
        w.write(layout)

def generate_rss():
    feed = ""
    for i in get_sorted_index(CONTENT_DIR):
        link = i[0].replace("./content/","")
        feed += f"\n\t\t<item>\n\t\t\t<title>{i[2]}</title>\n\t\t\t<link>{siteurl}/{link}</link>\n\t\t\t<pubDate>{i[1]}</pubDate>\n\t\t\t<description>{i[3]}</description>\n\t\t</item>"
    rsslayout = open("./templates/rss.xml", "r").read().replace("$rssfeed$", feed)
    with open("./public/rss.xml", "w") as w:
        w.write(rsslayout)


if __name__ == "__main__":
    filelist = []
    for root, dirs, files in os.walk("./content", topdown=False):
        for name in files:
            if name.endswith((".md",".html")):
                generate_page(os.path.join(root, name))
    shutil.copytree("./content/static", "./public/static", dirs_exist_ok=True)
    generate_rss()
