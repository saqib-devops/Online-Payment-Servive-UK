# Online-Payment-Servive-UK
Assignment
An Online Payment Service
1. Introduction
This assignment is about the design and implementation of a web-based, multi-user
payment service using the Django framework. The system is a much-simplified
version of PayPal. Through a web interface, users should be able to send money to
other registered users (e.g., using their registered email address as their unique
identifier), request money from other registered users and manage their own account
(e.g., look at their recent transactions). Super-users (i.e., admins) should be able to
access all user accounts and transactions.
After successfully completing the assignment, you will have demonstrated that you
can:
• design and implement user interfaces using Templates
• design and implement business logic using Views
• design and implement data access using Models
• design and implement a secure multi-user system
2. Project Description
Online payment services, such as PayPal, allow users to connect their online accounts
to their bank accounts, debit and credit cards. In such systems, users can usually
transfer money from their bank accounts to the online account, receive payments to
this account from other users, push money from the online account to their bank
accounts, among others.
For simplicity, we will assume in this project that all registered users start with a
specific amount of money (e.g., £1000) and no connections to bank accounts exist.
Note: This is pretended money, and no connection to real sources of money should exist.
To register, a user must provide a username, a first and last name, an email address
and a password. Each user has a single online account whose currency is selected
upon registration. Users can choose to have their account in GB Pounds, US dollars
or Euros. In any case, the system should make the appropriate conversion to assign
the right initial amount of money (e.g., if the baseline is £1000, then the initial amount
should be 1000 * GBP_to_USD_rate US dollars).
A user can instruct the system to make a direct payment to another user. If this
request is accepted (i.e., the recipient of the payment exists and there are enough
funds), money is transferred (within a single Django transaction) to the recipient
immediately. Users should be able to check for notifications regarding payments in
their accounts.
A user can instruct the system to request payment from some other user. A user
should be able to check about such notifications for payment requests. They can
reject the request or, in response to it, make a payment to the requesting user.
Users can access all their transactions, that is, sent and received payments and
requests for payments as well as their current account balance.
An administrator can see all user accounts and all transactions.
A separate RESTful web service must implement currency conversion. The exchange
rates will be statically assigned (hard-coded) in the RESTful service source code.
3. Penalties
You will receive 0 marks for your submission if it does not respect the following
THREE requirements.
1. You should use these naming conventions:
database: db.webapps
context path: /webapps2023
2. The submitted IntelliJ Django project should follow this structure:
webapps2023
│ db.webapps
│ manage.py
│
├───templates
│
├───register
│ │ admin.py
│ │ apps.py
│ │ models.py
│ │ tests.py
│ │ views.py
│ │ __init__.py
│ │
│ └───migrations
│ __init__.py
│
├───webapps2023
│ asgi.py
│ settings.py
│ urls.py
│ wsgi.py
│ __init__.py
│
├───payapp
│ ...
3. Your IntelliJ Django project should compile without any errors.
• A penalty of 4% will be applied if the source code is not well-formatted
and self-documentingLinks to an external site. (or well-documented).
4. System Architecture and Mark Allocation
4.1. The Presentation Layer (20%)
The presentation layer consists of a set of templates through which users and
administrators interact with the web application.
Users should be able to:
• View all their transactions
• Make direct payments to other registered users
• Request payments from registered users
Administrators should be able to see:
• user accounts
• all payment transactions
and register new administrators
4.1.1 Mark Allocation
• 10% - Full marks will be given if all required templates are written and
correctly connected with view functions in a way that makes sense even if
no other functionality is implemented at the business logic and data access
layers. The set of correctly implemented templates includes .html pages
required to perform security-related actions.
• 5% - Full marks will be given if all required conversions and validations are
done. This highly depends on the way you design your pages. In most
cases, standard validations and conversions should be enough. Full marks
will be given to assignments that support full and correct page navigation
by explicitly specifying navigation rules in URLConf modules.
• 5% - The appearance of web pages will be marked. It is advisable to
use crispy forms and bootstrap.
4.2. The Business Logic Layer (20%)
The business logic layer consists of views containing the logic that accesses the
model(s) and defers to the appropriate template(s). Views should support transactions
so that data integrity is preserved. You only need to annotate your views with the
appropriate transaction attributes (or leave the default behaviour, if appropriate). It is
also necessary to guarantee the ACID properties.
4.2.1 Mark Allocation
Full marks will be given if all required business logic is implemented in a set of views,
which must include appropriate annotations for supporting transactions if and when
required.
Users should be able to (15%):
• View all their transactions
• Make direct payments to other registered users
• Request payments from registered users
Administrators should be able to (5%):
• View all user accounts and balances
• View all payment transactions
• Register more administrators
4.3. The Data Access Layer (15%)
The data access layer consists of models containing anything and everything about
the data. To simplify deployment and configuration, you must use SQLite as your
Relational DataBase Management System (RDBMS). SQLite is an RDBMS that is
included in Python.
Your model should contain the essential fields and behaviours of the data being
stored. After installing the app, Django can create a database schema and a Python
database-access API for accessing your objects.
4.3.1 Mark Allocation
15% Full marks will be given if all access to application data is handled through
models and properly relating tables to each other.
4.4. The Security Layer (25%)
The online payment service is a multi-user web application. A user must be logged in
to interact with the system. Users should not be able to see other users' information
nor access pages and functionality for administrators. Administrators access their
own set of pages, through which can have access to all users' information. Users and
administrators should be able to log out from the web application.
You will need to implement and support the following:
• Authentication functionality (i.e., registration, login, and logout)
• Access control to restrict access to web pages to non-authorised users
• Communication on top of HTTPS for every interaction with users and
admins
• Cross-site scripting (XSS), Cross-site request forgery (CSRF), SQL injection,
and Clickjacking protection
4.4.1 Mark Allocation
10% - Authentication functionality
• Full marks will be given if users can register, login and logout. An admin
must be registered in the system upon activating the models
4% - Access control when navigating through templates
• Access to templates must be restricted to authorised actors (users and
admin).
5% - HTTPS functionality
• Communication with the web application using HTTPS
5% - Web security protection functionality
• Protection against cross-site scripting (XSS), cross-site request forgery
(CSRF), SQL injection, and clickjacking attacks needs to be in place
1% - Initial administration registration
• Upon activating the models, a single administrator account
(username: admin1, password: admin1) must be present. Only an
administrator can register more administrators through the restricted admin
pages.
4.5. Web Services (10%)
You must implement a REST Service to be accessed by the business logic layer. The
service will be deployed on the same server but accessed from the business logic
layer in the standard way, i.e., through HTTP.
A currency conversion RESTful web service that responds only to GET requests. The
exported resource should be named conversion in a path such as the following:
baseURL/conversion/{currency1}/{currency2}/{amount_of_currency1}
The RESTful web service should return an HTTP response with the conversion rate
(currency1 to currency2) or the appropriate HTTP status code if one or both of the
provided currencies are not supported.
4.5.1 Mark Allocation
10% - Full marks will be given if the REST web service is correctly implemented.
4.6 Report (10%)
• 4% - The report should include five sections: Presentation, Business Logic
Layer, Data Access Layer, Security Layer, and Web Services In each
section, you need to specify what has been fully or partially implemented
or if any requirement has not been implemented.
• 6% - The report should include a user manual to assist users in using your
application. This can be one of these two options:
o a list of screenshots of running your project. You need to show
all the working parts, e.g., the main interface, the user/admin
registration, request payment, payment transaction, REST
service, etc. These screenshots should show all the user
interfaces and any related data in the database.
o or a short walkthrough video/demo that shows all the working
parts.
5. (Optional) Deployment on the Cloud (7%
bonus)
You can optionally deploy your application on the Cloud and get an extra 7%. The
maximum mark you can get for this assignment is 100% (i.e. you will still get 100%,
and not 107%, even if your submission is perfect and you deployed your application
on the Cloud). To do so, you must successfully deploy and run the application on, e.g.,
Amazon EC2 virtual machine (any other framework would work fine, too). To get full
marks, you must submit screenshots of the commands you issued on the console to
run your Django web application and screenshots of the application running on the
cloud where the URI of the application is shown. To verify that you have indeed
deployed the application, the tutor may ask you, during the marking period, to run the
server and deploy your application for it to be tested. You will be invited to join AWS
Academy, where you will get access to the required AWS resources. Sussex is an
active member of AWS Academy, which means you will be given some free credits to
use AWS. These credits will be enough to deploy this project. Some tutorials on using
AWS will be provided in the lab classes later in this module.
6. Comments about marking
The coursework requires you to bring together several independent pieces of
functionality. It is highly recommended that you consider the service design BEFORE
you start implementation. Consider which parts are necessary to implement the core
functionality.
Some parts of this assignment are independent. For example, one could implement
the system without the REST web service (losing the marks mentioned in the marking
criteria) by just hard-coding the currency conversion functionality in a view.
Along the same lines, one could ignore the data access layer (losing 15% of the marks)
by storing data in Lists and Sets appropriately in a Singleton Class (just like we did
during the views' lab class).
Some other functionality cuts through the whole system architecture vertically. That
means that if, for example, the requesting money functionality is not implemented
(nor the templates and any potentially required persistence data), marks will be
removed from all three layers.
Security is mostly independent and orthogonal to the rest of the system.
7. Submission
The assignment submission will be through the separate UG and PGR Canvas sites.
Your submission should be a zip file containing:
• a zipped copy of the IntelliJ Django project containing well-formatted
source code (including all .python, .html and all required configuration
files)
• the report
Failure to submit the source code as described in the first bullet will result in a zero
mark, as the tutor will not be able to assess your programming effort. The submitted
source code must be part of an IntelliJ Django project that can be compiled and
deployed locally on any computer. Projects implemented using other technologies
(e.g., Java EE, Payara, MySQL Server, PHP, etc.) will not get any marks.
8. Plagiarism and Collusion
The coursework you submit is supposed to have been produced by you and you
alone. This means that you should not:
• work together with anyone else on this assignment
• give code for the assignment to other students
• request help from external sources
• do anything that means that the work you submit for assessment is not
wholly your own work, but consists in part or whole of other people’s
work, presented as your own, for which you should in fairness get no credit
• if you need help, ask your tutor
The University considers it misconduct to give or receive help other than from your
tutors or to copy work from uncredited sources. If any suspicion arises that this has
happened, formal action will be taken. Remember that in cases of collusion (students
helping each other on assignments) the student giving help is regarded by the
University as just as guilty as the person receiving help and is liable to receive the
same penalty.
Also bear in mind that suspicious similarities in student code are surprisingly easy to
spot and sadly the procedures for dealing with them are stressful and unpleasant.
Academic misconduct also upsets other students, who complain to us about
unfairness. So please don’t collude or plagaries
