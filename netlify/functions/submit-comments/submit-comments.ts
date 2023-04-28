import { Handler } from '@netlify/functions';
import { Octokit } from '@octokit/rest';
import querystring from 'querystring';

interface Comment {
	alias: string;
	url: string;
	time: string;
	body: string;
}

const handler: Handler = async (event, context) => {
  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

  // Parse the form data from the request body
  const formData = querystring.parse(event.body) as Comment;

  // Construct the comment object
  const comment: Comment = {
    alias: formData.alias,
    url: formData.url,
    time: formData.time,
    body: formData.body,
  };

  console.log(comment)
  // Push comment to GitHub repo
  await octokit.repos.createOrUpdateFileContents({
    owner: 'gtlsgamr',
    repo: 'htxyz',
    path: '/content/static/comments.json',
    message: 'Add new comment',
    content: Buffer.from(JSON.stringify(comment)).toString('base64'),
  });

  return {
    statusCode: 200,
    body: 'Comment submitted successfully!',
  };
};

export { handler };
