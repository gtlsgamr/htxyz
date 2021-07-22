const EMAIL = 'hittarththummarcoc@gmail.com';
const SITE = 'ht.xyz';

var script = document.createElement('script');
script.src = "https://cdnjs.cloudflare.com/ajax/libs/showdown/1.9.1/showdown.min.js";
document.head.appendChild(script)

function displaycomments(){
	var url = encodeURI(window.location.href.split('#')[0]);
	for(let i=0;i<commentsdata.length;i++){
			//do the comment display thing
			var commentslist = 	document.getElementById("solution");
			var converter = new showdown.Converter();
			var txt = `
			<div class='comments-dest'>
				<p class='comments-header'>
					${commentsdata[i].alias}
				</p>
				<p class='comments-time'>
					${commentsdata[i].time}
				</p>
				<hr>
			<div class='comments-content'>
				${converter.makeHtml(commentsdata[i].body)}
			</div>
			<hr class='class-1'>
			</div>`;
		console.log(txt);
			commentslist.insertAdjacentHTML("beforeend",txt);
	}
}

function postcomments(){
	var alias = document.getElementById('alias').value;
	var comment = document.getElementById('comment').value;
	var url = encodeURI(window.location.href.split('#')[0]);
	var result = {
		"postId": url,
		"time": new Date().toString(),
		"alias": alias,
		"body": comment,
	};
	var message = JSON.stringify(result);
	var place = document.getElementById('comment');
	var text = place.value;
	place.value = message;
	place.select();
	place.setSelectionRange(0, 99999);
	document.execCommand("copy");
	place.value = text;
	if (confirm("Comment posted, press OK to open mail client and send mail to the site owner for approval.")) {
		var mail = `mailto:${EMAIL}?subject=[${SITE}] New%20Comment%20from%20%20${alias}&body=${message}`
		window.open(mail);
	}
	else {
		alert("The message has been copied to your clipboard, you can email it to owner if you wish.")//cancel
	}
	console.log(JSON.stringify(result));
}

displaycomments();
