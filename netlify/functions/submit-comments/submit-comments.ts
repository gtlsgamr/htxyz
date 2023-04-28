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
  // Escape HTML in input to prevent injection
  input = escapeHtml(input);

  // Check for script injection attempts
  if (/<script\b[^>]*>(.*?)<\/script>/gm.test(input)) {
    return false;
  }

  // Check for SQL injection attempts
  if (/(?:\b(ALTER|CREATE|DELETE|DROP|INSERT|REPLACE|SELECT|UPDATE)\b|\b(OR|AND)\b.*?=.*?\b\1)/gmi.test(input)) {
    return false;
  }

  // Check for profanity
  const profanityList = ["2g1c", "2 girls 1 cup", "acrotomophilia", "alabama hot pocket", "alaskan pipeline", "anal", "anilingus", "anus", "apeshit", "arsehole", "ass", "asshole", "assmunch", "auto erotic", "autoerotic", "babeland", "baby batter", "baby juice", "ball gag", "ball gravy", "ball kicking", "ball licking", "ball sack", "ball sucking", "bangbros", "bangbus", "bareback", "barely legal", "barenaked", "bastard", "bastardo", "bastinado", "bbw", "bdsm", "beaner", "beaners", "beaver cleaver", "beaver lips", "beastiality", "bestiality", "big black", "big breasts", "big knockers", "big tits", "bimbos", "birdlock", "bitch", "bitches", "black cock", "blonde action", "blonde on blonde action", "blowjob", "blow job", "blow your load", "blue waffle", "blumpkin", "bollocks", "bondage", "boner", "boob", "boobs", "booty call", "brown showers", "brunette action", "bukkake", "bulldyke", "bullet vibe", "bullshit", "bung hole", "bunghole", "busty", "butt", "buttcheeks", "butthole", "camel toe", "camgirl", "camslut", "camwhore", "carpet muncher", "carpetmuncher", "chocolate rosebuds", "cialis", "circlejerk", "cleveland steamer", "clit", "clitoris", "clover clamps", "clusterfuck", "cock", "cocks", "coprolagnia", "coprophilia", "cornhole", "coon", "coons", "creampie", "cum", "cumming", "cumshot", "cumshots", "cunnilingus", "cunt", "darkie", "date rape", "daterape", "deep throat", "deepthroat", "dendrophilia", "dick", "dildo", "dingleberry", "dingleberries", "dirty pillows", "dirty sanchez", "doggie style", "doggiestyle", "doggy style", "doggystyle", "dog style", "dolcett", "domination", "dominatrix", "dommes", "donkey punch", "double dong", "double penetration", "dp action", "dry hump", "dvda", "eat my ass", "ecchi", "ejaculation", "erotic", "erotism", "escort", "eunuch", "fag", "faggot", "fecal", "felch", "fellatio", "feltch", "female squirting", "femdom", "figging", "fingerbang", "fingering", "fisting", "foot fetish", "footjob", "frotting", "fuck", "fuck buttons", "fuckin", "fucking", "fucktards", "fudge packer", "fudgepacker", "futanari", "gangbang", "gang bang", "gay sex", "genitals", "giant cock", "girl on", "girl on top", "girls gone wild", "goatcx", "goatse", "god damn", "gokkun", "golden shower", "goodpoop", "goo girl", "goregasm", "grope", "group sex", "g-spot", "guro", "hand job", "handjob", "hard core", "hardcore", "hentai", "homoerotic", "honkey", "hooker", "horny", "hot carl", "hot chick", "how to kill", "how to murder", "huge fat", "humping", "incest", "intercourse", "jack off", "jail bait", "jailbait", "jelly donut", "jerk off", "jigaboo", "jiggaboo", "jiggerboo", "jizz", "juggs", "kike", "kinbaku", "kinkster", "kinky", "knobbing", "leather restraint", "leather straight jacket", "lemon party", "livesex", "lolita", "lovemaking", "make me come", "male squirting", "masturbate", "masturbating", "masturbation", "menage a trois", "milf", "missionary position", "mong", "motherfucker", "mound of venus", "mr hands", "muff diver", "muffdiving", "nambla", "nawashi", "negro", "neonazi", "nigga", "nigger", "nig nog", "nimphomania", "nipple", "nipples", "nsfw", "nsfw images", "nude", "nudity", "nutten", "nympho", "nymphomania", "octopussy", "omorashi", "one cup two girls", "one guy one jar", "orgasm", "orgy", "paedophile", "paki", "panties", "panty", "pedobear", "pedophile", "pegging", "penis", "phone sex", "piece of shit", "pikey", "pissing", "piss pig", "pisspig", "playboy", "pleasure chest", "pole smoker", "ponyplay", "poof", "poon", "poontang", "punany", "poop chute", "poopchute", "porn", "porno", "pornography", "prince albert piercing", "pthc", "pubes", "pussy", "queaf", "queef", "quim", "raghead", "raging boner", "rape", "raping", "rapist", "rectum", "reverse cowgirl", "rimjob", "rimming", "rosy palm", "rosy palm and her 5 sisters", "rusty trombone", "sadism", "santorum", "scat", "schlong", "scissoring", "semen", "sex", "sexcam", "sexo", "sexy", "sexual", "sexually", "sexuality", "shaved beaver", "shaved pussy", "shemale", "shibari", "shit", "shitblimp", "shitty", "shota", "shrimping", "skeet", "slanteye", "slut", "s&m", "smut", "snatch", "snowballing", "sodomize", "sodomy", "spastic", "spic", "splooge", "splooge moose", "spooge", "spread legs", "spunk", "strap on", "strapon", "strappado", "strip club", "style doggy", "suck", "sucks", "suicide girls", "sultry women", "swastika", "swinger", "tainted love", "taste my", "tea bagging", "threesome", "throating", "thumbzilla", "tied up", "tight white", "tit", "tits", "titties", "titty", "tongue in a", "topless", "tosser", "towelhead", "tranny", "tribadism", "tub girl", "tubgirl", "tushy", "twat", "twink", "twinkie", "two girls one cup", "undressing", "upskirt", "urethra play", "urophilia", "vagina", "venus mound", "viagra", "vibrator", "violet wand", "vorarephilia", "voyeur", "voyeurweb", "voyuer", "vulva", "wank", "wetback", "wet dream", "white power", "whore", "worldsex", "wrapping men", "wrinkled starfish", "xx", "xxx", "yaoi", "yellow showers", "yiffy", "zoophilia", "🖕" ]; // Add more words as needed
  const profanityRegex = new RegExp(`\\b(${profanityList.join("|")})\\b`, "gmi");
  if (profanityRegex.test(input)) {
    return false;
  }

  // Check for Unicode and null bytes
  if (/(?:%u.{4}|\+ADw-|&lt;|\x00)/gi.test(input)) {
    return false;
  }

  // Check for common exploit keywords
  const exploitList = ["onerror", "onload", "eval", "function", "img", "svg", "iframe"];
  const exploitRegex = new RegExp(`\\b(${exploitList.join("|")})\\b`, "gmi");
  if (exploitRegex.test(input)) {
    return false;
  }

  return true; // Input passed all tests
}

function escapeHtml(unsafe: string): string {
  return unsafe.replace(/[&<"']/g, function (match) {
    switch (match) {
      case "&":
        return "&amp;";
      case "<":
        return "&lt;";
      case '"':
        return "&quot;";
      case "'":
        return "&#039;";
    }
  });
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
    body: 'Your comment has been posted!. <a href="javascript:history.back()">Go Back</a>',
}
};

export { handler };
