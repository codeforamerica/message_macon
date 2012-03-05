Fix Macon
=========

With [SeeClickFix](http://seeclickfix.com/macon) now integrated with the
City of Macon's Public Works department, citizens should be able to
report neighborhood issues.  This application aims to help citizens
without internet access report issues through SMS text messages.

The format for sending issues should be an **address** followed by an
**issue**.

    123 Some St. Garbage cart lid is broken and falls off cart.

These issues will then be added to SeeClickFix through the [Open311
API](http://seeclickfix.com/open311) (using the
[Three](https://github.com/codeforamerica/three) wrapper). Text messages
will be received using [SMSified](https://smsified.com).


Configuration
-------------

The application makes use of several enviornment variables -- which you
should know about if you're planning on extending or adapting it.
Currently, to get set up on Heroku, here are the ones used.

    heroku config:add OPEN311_API_KEY=seeclickfix_api_key
    heroku config:add SMS_USER=smsified_username SMS_PASS=smsified_password

Locally, you can `export` these environment variables in your terminal.

    export OPEN311_API_KEY=seeclickfix_api_key
    export SMS_USER=smsified_username
    export SMS_PASS=smsified_password
