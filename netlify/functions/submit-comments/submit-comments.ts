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

const handler: Handler = async (event, context) => {
  const formData = querystring.parse(event.body) as Comment;

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
    body: 'Your comment has been recorded for approval. <a href="javascript:history.back()">Go Back</a>',
  };
};

export { handler };

