# ResumeMaker
Django-Resume Maker WebApp<br><br>

This WebApp is a CRUD based web-application for making resumes/CV's<br>
with they <b>Fundamental idea</b> of <b>uploading user documents</b><br>

<b>User can upload</b> his/her documents to the website.<br>
Also the Resume will have a QR-Code and a Hyper-Link that can redirect the reviewer to a webpage where he/she can check/see the user documents<br>

This will reduce the time and third party interferance to document checking related to Resume<br>
An easy intervention can be done for the document checking, on the same website<br>
<hr>
Key Features:<br>
<ul>
    <li>Email Verifiation at login,register,forget-password
        <ul>
            <li>a dynamic link will be sent to set password,login, ..</li>
        </ul>
    </li>
    <li>Document preview in base64 format
    <ul>
        <li>As the fundamental idea, user upload their document, but while previewing it to reviewer, the system show it in 'src base64' format</li>
        </ul>
    </li>
</ul>
    <hr>
The website is built on Django framework,<br>
website gives service to --<br>
<ul>
    <li>create new resume</li>
    <li>add custom field (achievements, certification)</li>
<li>download resume</li>
<li>modify</li>
<li>view</li>
<li>upload document</li>
</ul>
<br>
The Resume reviewer can click on the hyper-link or scan the qr-code and he/she<br>
will be redirected to a page where he/she can view the uploaded documents.<br>
