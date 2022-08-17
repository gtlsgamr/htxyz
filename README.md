# ht.xyz

This is my website [ht.xyz](https://hitarththummar.xyz), which uses
a~~shell~~ python script to generate pages.

All the content for the site goes in the *contents* folder. Routing is
handled by directories. Front matter for the site goes on top of the
markdown file which contains variables which will then be replaced in the
layout file. After you are done declaring the variables, put *+++* on the next line.

You can customize page layout by editing *templates/layout.html* in the
root of the directory.
You can write the posts/pages in standard markdown format and they will be
converted to html. For pages that act as index pages to sub-folders, a
`{{listindex}}` pointer has been added. Just add that anywhere in the index
page within a comment and a  list of the posts in that
particular folder will be placed there, sorted in descending order by date.

You can configure global site variables at the top of the script.

**This script/site comes with no warranty and is for my personal use. If you feel**
**like using it for yourself, make sure you check the script for**
**something that might mess up your system.**
