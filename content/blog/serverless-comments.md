title="Implementing comments on your static website using Netlify"
description="Get comments working on your blog using netlify functions."
date=2023-04-28
+++

## Backstory

**If you just want the procedure, skip this part.**

I have been working on this site for the past two-ish years and comments have
been the part of it that is constantly changing. At first when I did not have
hosting I used [comments](https://github.com/gtlsgamr/comments), some
javascript code that took comments from a form formatted them according to my
needs and opened the user's mail client with a prepared mail to my E-mail. I
would then review those emails and put the json in a comments.json file which
would then be read by each page of my site to display their comments. This was
a very crude solution in my opinion. 

Fortunately I started [~tildevarsh](https://tildevarsh.in) and had
access to hosting so I moved on to
[addcomment.c](https://github.com/gtlsgamr/addcomment.c). It was a CGI script
written in C that took the comments, formatted them and moved them to a buffer
file in my site directory. Periodically I would download that file and copy
comments to my comments.json file. This was okay too, but it still required me
to check the file and move the comments. At some point I removed the code that
dynamically placed comments on pages and integrated it into my static site
generator. So now the comments were placed at build time and no javascript was
needed to display comments.

Now we come to the current scenario. I have managed to integrate [netlify
functions](https://www.netlify.com/products/functions/) to manage comments on
my website, which ensures that I don't need to manually review the comments.
Below I will show you how you can do that same for your website if you want a
solution that works and does not store your comments somewhere else.

## The method

There are four main steps for this.

- User comments on the website.
- The comment gets submitted to the netlify function.
- The function parses the comment for malicious content and pushes the content to the comments.json file on the github repo.
- The push causes netlify CD to deploy the site, this time with the new comment.

Here is what the html form on my site looks like.

    <form
       name="comments"
       id="formcomments"
       action="/.netlify/functions/submit-comments"
       method="POST"
       >
       <div>
          <h2>Post a Comment</h2>
       </div>
       <div>
          <input
             type="text"
             class="comment-field"
             name="alias"
             placeholder="Your Alias"
             id="alias"
             required
             />
          <input type="hidden" id="texturl" name="url" />
          <input type="hidden" id="textdate" name="time" />
       </div>
       <div>
          <textarea
             maxlength="500"
             name="body"
             placeholder="Enter your comment here (Max 500 words)"
             id="comment"
             required
             ></textarea>
       </div>
       <div>
          <button
             type="button"
             id="comment-button"
             onclick="tesubmit()"
             >
          Comment
          </button>
       </div>
    </form>
    <script>
    function tesubmit() {
        document
            .getElementById("texturl")
            .setAttribute("value", window.location.pathname);
        document.getElementById("texturl").value =
            window.location.pathname;
        document
            .getElementById("textdate")
            .setAttribute("value", new Date().toString());
        document.getElementById("formcomments").submit();
    }
    </script>

Once you are done with this, you will need to create a netlify function. You can do that by using the netlify cli.

First install the netlify cli.

    npm install -g netlify-cli

Then go inside your site directory and link the site to netlify.

    netlify link

This will give you some text prompts, which you can choose by yourself.

Next you will create a netlify function.

    netlify functions:create

This will give you some prompts as well, you can select by yourself, it is not complicated. The function name should be submit-comments, according to the html form. If you need it to be something else, make sure change it in the form as well.

Once done with this, you will have a netlify directory in your site root. Go to netlify/functions/submit-comments, and you can see it has created everything for you.

Now this is what my submit-comments.ts looks like

    import { Handler } from '@netlify/functions';
    import fetch from "node-fetch";
    import querystring from 'querystring';
    import { Octokit } from '@octokit/rest';

    interface Comment {
      alias: string;
      url: string;
      time: string;
      body: string;
    }

    function validateInput(input: string): boolean {
      if(textisinvalid){
      return false;
      }
      return true; // Input passed all tests
    }

    const handler: Handler = async (event, context) => {
      const formData = querystring.parse(event.body) as Comment;

      if(!validateInput(formData.alias) || !validateInput(formData.body)){
          return {
            statusCode: 400,
            body: "You tried some funny business didn'tcha?! I'm gonna ignore your comment.",
          };
      }

      // Get existing comments
      const response = await fetch('https://raw.githubusercontent.com/gtlsgamr/htxyz/main/content/static/comments.json');
      const existingComments: Comment[] = await response.json();

      // Add new comment
      existingComments.push(formData);

      // Update comments file on GitHub
      const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
      const content = Buffer.from(JSON.stringify(existingComments)).toString('base64');
      const sha = await octokit.repos.getContent({
        owner: 'gtlsgamr',
        repo: 'htxyz',
        path: 'content/static/comments.json',
      }).then((response) => response.data.sha);

      await octokit.repos.createOrUpdateFileContents({
        owner: 'gtlsgamr',
        repo: 'htxyz',
        path: 'content/static/comments.json',
        message: `Add new comment, by ${formData.alias}`,
        content,
        sha,
      });

      return {
      statusCode: 200,
      headers: {
        'Content-type': 'text/html; charset=UTF-8',
      },
        body: 'Your comment has been posted! It will show up soon. :) <a href="javascript:history.back()">Go Back</a>',
    }
    };

    export { handler };

The validateInput function performs some validations on the text which I did not post here. You can do your own validations if you wish. In netlify itself, you will have to add GITHUB_TOKEN environment variable, whose value you can get from github.

This workflow is simple, and easy to use and keeps the comments on your own repo. Please suggest improvements, if any.
