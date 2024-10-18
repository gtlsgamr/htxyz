#!/usr/bin/env python3
import os,html,markdown,shutil,json,time
from datetime import date, datetime
from string import Template
import concurrent.futures


CONTENT_DIR = "./content"
PUBLIC_DIR = "./public"
CSS_FILE = "./content/static/css/sp.css"
COMMENTS_FILE = "./content/static/comments.json"

comments = json.loads(open(COMMENTS_FILE).read())
sitetitle = "personal website and blog"
sitename = "ht.xyz"
siteurl = "https://hitarththummar.xyz"
footer = "Copyright © 2022 - Hitarth Thummar"
sitevars = {"sitetitle": sitetitle, "sitename": sitename, "footer": footer}

NAV_BAR_VALUES = {
    "home": "/",
    "blog": "/blog",
    "artwork": "/artwork.html",
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
    navbar_html = ["<ul>"]
    navbar_html += [f"\t\t\t\t\t<li> <a href='{html.escape(link_path)}'>{html.escape(link_name)}</a></li>" for link_name, link_path in nav_bar_items.items()]
    navbar_html.append(' <li><div id="theme-toggle"></div></li>')
    navbar_html.append("\t\t\t\t</ul>")
    return "\n".join(navbar_html)

def generate_layout(var):
    """
    generate the layout template file
    """
    TEMPLATE_FILE = "./templates/layout.html"
    with open(TEMPLATE_FILE, "r") as f:
        master_layout = f.read()
    template = Template(master_layout)
    master_layout = template.safe_substitute(var)
    return master_layout


init_dir_structure()
sitevars["navbar"] = gen_navbar(NAV_BAR_VALUES)
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
    text = "\n".join(textarr[i + 1:])  # This gives the text without the front matter
    return variables, text


def generate_home_page():
    """
    special function to generate the home page because we only want to show the
    first five items
    """
    homepage = os.path.join(CONTENT_DIR, "home.md")

    variables, markdowntext = read_vars(open(homepage, "r").read())
    htmltext = markdown.markdown(markdowntext, extensions=['markdown.extensions.extra'])


    layout = master_layout.replace('					<h1 id="articletitle">${title}</h1>', "")  
    # if it is the home page, remove the title and date, edge case
    layout = layout.replace('					<small id="date">${date}</small>', "")

    template = Template(layout)
    layout = template.safe_substitute({"mdtext": htmltext}, **variables)

    homeindex = ""
    index_dict = get_sorted_index(CONTENT_DIR)
    for i in index_dict[0:5]:
        htmllink = "/".join(i[0].replace(".md", ".html").split("/")[2:])
        homeindex += f"<p> <a href='/{htmllink}'>{i[2]}</a> -  &thinsp;{i[1]} </p>\n"
    layout = layout.replace(f"$listindex$", homeindex)
    c = [f"<div><span style='font-family:monospace; font-weight:bold;'>{x['alias']}:</span>{x['body']}</div>" for x in comments if x['url'] == "/"]

    layout = layout.replace("$comments$","\n".join(c))
    with open(os.path.join(PUBLIC_DIR, "index.html"), "w") as f:
        f.write(layout)


# same as above, but for ALL the pages :)
def generate_page(path):
    layout = master_layout

    if os.path.basename(path) == "home.md":
        generate_home_page()
        return

    filename = os.path.basename(path).replace(".md","")
    variables, markdowntext = read_vars(open(path, "r").read())
    htmltext = markdown.markdown(markdowntext, extensions=['markdown.extensions.extra'])

    template = Template(layout)
    layout = template.safe_substitute({"mdtext": htmltext}, **variables)

    if os.path.basename(path) == "artwork.md" or os.path.basename(path) == "404.md":
        layout = layout.replace('<small id="date">${date}</small>', "")

    ## if it is an index page, remove the date and create index
    if os.path.basename(path) == "index.md":
        layout = layout.replace('<small id="date">${date}</small>', "")
        index_list = get_sorted_index(os.path.dirname(path))
        index_html = ""
        for i in index_list:
            htmllink = "/".join(i[0].replace(".md", ".html").split("/")[2:])
            index_html += f"<p><a id='listitems' href='/{htmllink}'>{i[2]}</a> -  &thinsp;{i[1]}</p>\n"
        layout = layout.replace(f"$listindex$", index_html)

    output_name = path.replace("./content", "./public").replace(".md", ".html")
    c = [f"<div><span style='font-family:monospace; font-weight:bold;'>{x['alias']}:</span>{x['body']}</div>" for x in comments if filename in x['url']]
    layout = layout.replace("$comments$","\n".join(c))
    with open(output_name, "w") as w:
        w.write(layout)


# Generate RSS
def generate_rss():
    feed = ""
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    for i in get_sorted_index(CONTENT_DIR):
        link = i[0].replace("./content/", "")
        with open(f"./content/{link}.md", "r") as scan:
            z = scan.read()
            markdowntext = read_vars(z)[1]
        feed = "".join([
            feed,
            f"""
                <entry>
                    <title>{i[2]}</title>
                    <link href='{siteurl}/{link}'/>
                    <id>{siteurl}/{link}</id>
                    <updated>{datetime.strptime(i[1],"%Y-%m-%d").isoformat()}Z</updated>
                    <summary>"{i[3]}"</summary>
                    <content type="html">
                        {html.escape(markdown.markdown(markdowntext, extensions=['markdown.extensions.extra']))}
                    </content>
                </entry>
            """
        ])
    rsslayout = open("./templates/atom.xml", "r").read().replace("$rssfeed$", feed).replace("$updated$",date)
    with open("./public/atom.xml", "w") as w:
        w.write(rsslayout)


def generate_all_pages():
    page_count = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(CONTENT_DIR, topdown=False):
            for name in files:
                if name.endswith((".md", ".html")):
                    executor.submit(generate_page, os.path.join(root, name))
                    page_count += 1
    return page_count

def count_static_files():
    static_file_count = 0
    for root, dirs, files in os.walk(CONTENT_DIR + "/static"):
        static_file_count += len(files)
    return static_file_count

def print_message(message, message_type="INFO"):
    """
    Print formatted messages with a consistent style.
    """
    color_codes = {
        "INFO": "\033[94m",  # Blue
        "SUCCESS": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "ENDC": "\033[0m",  # Reset
    }
    color_code = color_codes.get(message_type, "\033[0m")
    print(f"{color_code}[{message_type}] {message}{color_codes['ENDC']}")

if __name__ == "__main__":
    start_time = time.time()
    print_message("Start building sites …")
    try:
        page_count = generate_all_pages()
        static_file_count = count_static_files()
        shutil.copytree(CONTENT_DIR + "/static", PUBLIC_DIR + "/static", dirs_exist_ok=True)
        generate_rss()
        end_time = time.time()
        print_message(f"Pages            | {page_count}", "SUCCESS")
        print_message(f"Static files     | {static_file_count}", "SUCCESS")
        print_message(f"Total in {(end_time - start_time) * 1000} ms", "SUCCESS")
    except Exception as e:
        print_message(f"An error occurred: {e}", "ERROR")
