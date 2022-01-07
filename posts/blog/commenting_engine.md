title="[Development] My own commenting engine!"
description=""
date="2021-12-08"
+++
~~Update: I don't use this anymore because frankly it is kind of hacky. I hope people might find better use for this.~~

### How I made my own commenting engine

Well, before you go on, you might be wondering, what is a commenting engine? A commenting engine is a piece of code that handles comments on a website or app and the likes. On this website, before this point, there was no option for comments. After that I tried messing with some commenting engines such as [Disqus](https://blog.disqus.com/) and [Staticman](https://staticman.net) and many more. My core issue with most of these was that either they were hosted by third party, or they needed some sort of hosting by the site owner. I was looking for a free solution (free as in both free speech and free food), that could handle comments. Then I found [utterances!](https://utteranc.es/) It was everything I needed. It wasn't hosted by some shady third party, it was free and didn't require me to host anything. Yet, there was one ***issue***. Yes, I made that pun. *utterances* used GitHub issues to act as storage for comments. It was a very intuitive interface, but its reliance on GitHub bugged me. Hence, I set out to make my own commenting engine that was ***A FREE/Libre commenting engine that is lightweight, serverless, and possibly ~~doesn't~~ requires wonky workarounds.***

#### in the beginning

I didn't know anything about how commenting engines worked, but I had a goal in mind, to have a commenting engine that supported the given definition. I made a repo and started working. Soon I realised that the engine has to be dependent on javascript since that was the only way to have it serverless. Initially the definition contained the phrase 
>doesn't require wonky workarounds

which had to be removed, because no way in hell was I going to make something that fit that definition without workarounds. Thus was born, [comments](https://github.com/gtlsgamr/comments).

#### how it works

***comments*** basically works as a middleman to help the commenter compose the comment and the site owner to have a nicely formatted json to add to the site. 

1. The Commenter enters the comment on a post.
2. ***comments*** takes the time, date, the post on which the comment was made, nickname for the commenter and creates a json object and passes it in a `mailto` link which will open the mail client of the commenter.
3. It will have a preformatted email that the commenter just has to send.
4. The site owner receives the mail and looks at the comment. They will then copy the json and paste it inside the *comments-data.json* file in their static site directory.
5. Every time a page on the site loads, comments will parse that json file and display the comments accordingly!
	

#### how you can help!

It works fine by itself for now but I want to make it a bit more feature rich. Here are some things that might make this project a *little* bit better.

1. A github pages or some kind of landing page.
2. Nested comments and a show more button to hide comments if there are more than x amount of comments.
3. ✨ CSS Styles! ✨ Currently the default style is very basic looking (the way i prefer) but the project will be much more feature-rich if the users could have different theming options for their comments.

Honestly, it was a lot of fun making this. I hope people use it to display comments on their websites and help improve this project! 
