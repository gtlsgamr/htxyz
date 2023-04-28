import { Handler } from '@netlify/functions';
import { Octokit } from '@octokit/rest';

interface Comment {
	alias: string;
	url: string;
	time: string;
	body: string;
}

const handler: Handler = async (event, context) => {
  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
  console.log("event body---"+event.body)
  const comment: Comment = JSON.parse(event.body);

  console.log("COMMENT---"+comment)
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
