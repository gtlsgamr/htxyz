const EMAIL = 'hittarththummarcoc@gmail.com';
const SITE = 'ht.xyz';

var script = document.createElement('script');
script.src = "https://cdnjs.cloudflare.com/ajax/libs/showdown/1.9.1/showdown.min.js";
document.head.appendChild(script)

function commenthtmlgen(header,time,content){
			var txt = `
			<div class='comments-dest'>
				<p class='comments-header'>
					${header}
				</p>
				<p class='comments-time'>
					${time}
				</p>
				<hr>
			<div class='comments-content'>
				${content}
			</div>
			<hr class='class-1'>
			</div>`;

	return txt;
}

function displaycomments(){
	var url = window.location.pathname;
	for(let i=0;i<commentsdata.length;i++){
			if(commentsdata[i].postId == url){
			var commentslist = 	document.getElementById("solution");
			var converter = new showdown.Converter();
			var cd = commentsdata[i];
			txt = commenthtmlgen(cd.alias,cd.time,converter.makeHtml(cd.body));
			console.log(txt);
			commentslist.innerHTML += txt;
	}
}
}

function postcomments(){
	var alias = document.getElementById('alias').value;
	var comment = document.getElementById('comment').value;
	var url = window.location.pathname;
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
