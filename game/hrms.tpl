%{
username=`{get_cookie username | escape_html}
userdir=etc/users/`{get_cookie id | sed 's/[^a-z0-9]//g'}

if(! ~ $"post_arg_email '')
    email=`{echo $post_arg_email | sed 's/[^0-9]//g'}
if not
    email=`{ls -trp $userdir/emails | tail -n 1}
%}

<style>
body {
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
    margin: 0;
    overflow: hidden;
}

div {
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
}

table {
    height: calc(100vh - 64px);
    border-collapse: collapse;
}
td {
    vertical-align: baseline;
    box-shadow: 0px 0px 0px 1px #d4dbde inset;
    padding: 6px;
}
td.noborder {
    padding: 0;
    box-shadow: none;
}
tr {
    height: 0;
}
tr:last-child {
    height: auto;
}

#header {
    width: 100%;
    height: 64px;
    padding: 0;
    overflow: hidden;
    background-color: #2f3a3f;
}
#username {
    color: #fff;
    font-size: 32px;
    padding: 7px 16px;
}

#maintable {
    position: absolute;
    top: 64px;
    right: 0;
    bottom: 0;
    left: 0;
}

#emaildetails td {
    box-shadow: none;
    padding: 0 6px 0 0;
}
#emailbody {
    padding: 0 1.5em 0.5em 1.5em;
}

.emailBtn:hover {
    background-color: #ebf9ff;
    cursor: pointer;
}
.active {
    background-color: #ebf9ff;
    box-shadow: 3px 0px 0px #9ddfff inset;
}

#actions {
    text-align: center;
}
#actions input {
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 16px 24px;
    margin: 0.5em 0.2em 1em;
    font-size: 175%;
}
#actions input:hover {
    opacity: 0.75;
    cursor: pointer;
}
#actions input.hire {
    background-color: #4caf50;
    border: 3px solid #419544;
}
#actions input.reject {
    background-color: #f44336;
    border: 3px solid #cf392e;
}
</style>

<div id="header">
    <img src="img/header.png" />
    <span id="username" style="float: right"><span style="font-size: 90%">Hello,</span> <span style="font-weight: 600">%($username%).</span></span>
</div>
<table id="maintable"><tr>
<td class="noborder"><div style="width: 14vw"><table style="width: calc(100% + 1px)">
    <tr><td>
        <span>Inbox</span>
    </td></tr>
    <tr class="active"><td>
        <span><strong>Spam</strong></span>
        <span style="float: right"><strong>%(`{ls $userdir/emails | wc -l}%)</strong></span>
    </td></tr>
    <tr><td>
        <span>Sent</span>
    </td></tr>
    <tr><td>
        <span>Trash</span>
    </td></tr>
    <tr style="height: auto"><td></td></tr>
    <tr style="height: 0"><td style="text-align: center">
        <img src="img/health-%(`{cat $userdir/health}%).png" style="width: 100%; margin-top: 8px" /><br />
        <label for="health">Mental Health</label><br />
        <progress id="health" value="%(`{cat $userdir/health}%)" max="100"></progress>
    </td></tr>
</table></div></td>
<td class="noborder"><div style="width: 25vw"><table style="width: calc(100% + 1px)">
%   for(i in `{ls -tp $userdir/emails}) {
    <tr class="emailBtn %(`{if(~ $email $i) echo 'active'}%)" onclick="openEmail(%($i%))"><td>
        <span><strong>%(`{cat $userdir/emails/$i/subject}%)</strong></span><br />
        <span>%(`{cat $userdir/emails/$i/sender}%)</span>
        <span style="float: right">%(`{/bin/date -r $userdir/emails/$i/body '+%H:%M:%S %Z'}%)</span>
    </td></tr>
%   }
    <tr><td></td></tr>
</table></div></td>
<td class="noborder"><div style="width: 61vw"><table style="width: calc(100% + 1px)">
    <tr style="background-color: #f4f4f4"><td>
        <table style="height: auto" id="emaildetails">
          <tr><td style="text-align: right">From:</td><td>%(`{cat $userdir/emails/$email/sender}%)</td></tr>
          <tr><td style="text-align: right">Date:</td><td>%(`{/bin/date -r $userdir/emails/$email/body}%)</td></tr>
          <tr><td style="text-align: right">Subject:</td><td><strong>%(`{cat $userdir/emails/$email/subject}%)</strong></td></td>
        </table>
    </td></tr>
    <tr><td id="emailbody">
        %(`{tpl_handler $userdir/emails/$email/body}%)
%       switch(`{cat $userdir/emails/$email/type}) {
%       case application
        <form id="actions" method="POST" action="">
            <input name="action" type="submit" value="Hire" class="hire">
            <input name="action" type="submit" value="Reject" class="reject">
        </form>
%       }
    </td></tr>
</table></div></td>
</tr></table>

<script>
function openEmail(email) {
    var form = document.createElement("form");
    var emailVal = document.createElement("input");

    form.method = "POST";
    form.action = "";

    emailVal.name = "email";
    emailVal.value = email;
    emailVal.type = "hidden";

    form.appendChild(emailVal);
    document.body.appendChild(form);
    form.submit();
}
</script>
