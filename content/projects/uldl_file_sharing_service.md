title="ul.dl, the no-bullshit file hosting service"
description="Creating and hosting your own cli based file hosting service!"
date="2021-12-08"
+++
You might have heard of [0x0](https://0x0.st), the no-bullshit file hosting service. It is a service for quickly sharing files right from your command line without having to point or click anywhere. What you do is, you send a POST request to the site with the file and the site will respond with a url that has the raw content of that file. 

For example, 

If you want to share a file called `test.json` with someone, all you have to do is type 

	curl -F file=@test.json 0x0.st
and it will respond with a url that will point to that file.

I myself tried hosting my own instance of 0x0 but unfortunately it was written in python and hosting a whole flask server with database was too much work for my raspberry pi. So I wrote my own version of it! It is not as nuanced as 0x0 with no file type checking or neural networks to scan for explicit content, but it does one thing and it does it good. It stores files.

You can host your own [ul.dl](https://github.com/gtlsgamr/ul.dl) instance if you want. It is a good way to quickly share files from the command line without worrying about any third party accessing it. 

I will be adding more features to it, and you can send a PR too, if you want. If you have any questions related to deploying your own instance of it, you can email me by commenting below.
