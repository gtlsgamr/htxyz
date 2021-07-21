const EMAIL = "hittarth91@gmail.com"
const SITE = "htxyz"

var url = encodeURI(window.location.href.split('#')[0]);
//Code to add comments recursively
$(document).ready(function () {
	var converter = new showdown.Converter();
	console.log(commentsobj);


		for (key of commentsobj) {
			if (key.postId == url) {
				var txt = `
				<div class='comments-dest'>
				<p class='comments-header'>
				${key.alias}
				</p>
				<p class='comments-time'>
				${key.time}
				</p>
				<hr>
				<div class='comments-content'>
				${converter.makeHtml(key.body)}
				</div>
				<hr class='class-1'>
				</div>`;
				$('#solution').insertAdjacentHTML('beforeend', txt);
			}

		}





});
function jsonCreator(alias, comment) {
	var result = {
		"postId": url,
		"time": new Date().toString(),
		"alias": alias,
		"body": comment,
	};
	//Below code does the work of copying the predefined messsage for the user and also mailing it to the site owner.
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

};
