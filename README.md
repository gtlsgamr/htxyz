# ht.xyz
This is my website [hitarththummar.xyz](https://hitarththummar.xyz), which uses a custom shell script to generate pages. There are no "categories" and "tags" on my website because I don't need them. The css is a modified version of [SimpleCss](https://simplecss.org/) which is based on the [iceberg](https://github.com/cocopon/iceberg.vim/) colorscheme. You need the [discount](https://www.pell.portland.or.us/~orc/Code/discount/) package to make this script work if you plan to modify this for your own use. You can always replace the `markdown` command in the script with pandoc or the likes, but it is up to you.

Each and every post in the *posts* folder contains 4 lines of front matter. It is basically in the form of bash variables, i.e. name=xyz. You can use this to define various variables within each page that are replaced by the script. It is a hacky solution, but it works for me. The fourth line is just a visual seperator and can be anything, since it won't be used anyway. You can write the posts/pages in standard markdown format and they will be converted to html. For pages that act as index pages to sub-folders, a `{{listindex}}` pointer has been added. Just add that anywhere in the index page and a date-wise sorted list of the posts in that particular folder will be shown there.

The `config` file contains some standard site metadata that you may or may not want to change. I will try and explain them below.

 | key | value | 
 | --- | --- | 
 | footer | contains the footer text for the website | 
 | sitetitle | contains the site title that is shown in the tabs | 
 | sitedesc | contains the blinking text in the header of the website | 
 | navkeys | contains the names of the navigation bar buttons, in order and comma seperated | 
 | navvals | contains the links of the navigation bar buttons, in order and comma seperated | 
 | sitename | contains the site name, that is shown in the header, above sitedesc | 

This script/site comes with no warranty and is for my personal use. If you feel like using it for your own personal use, make sure you check the script for something that might mess your system up.
