# ResumeMaker
Django-Resume Maker WebApp

This WebApp is a CRUD based web-application for making resumes/CV's
with they <b>Fundamental idea</b> of <b>uploading user documents</b><br>

<b>User can upload</b> his/her documents to the website.
Also the Resume will have a QR-Code and a Hyper-Link that can redirect the reviewer to a webpage where he/she can check/see the user documents<br>

This will reduce the time and third party interferance to document checking related to Resume
An easy intervention can be done for the document checking, on the same website<br>
<hr>
Key Features:
-> Email Verifiation at login,register,forget-password 
    -> a dynamic link will be sent to set password,login, ..
-> Document preview in base64 format
    -> As the fundamental idea, user upload their document, but while previewing it to reviewer, the system show it in 'src base64' format
<hr>
The website is built on Django framework,
website gives service to --
-> create new resume
-> add custom field (achievements, certification)
-> download resume
-> modify
-> view
-> upload document

<br>
The Resume reviewer can click on the hyper-link or scan the qr-code and he/she
will be redirected to a page where he/she can view the uploaded documents.
