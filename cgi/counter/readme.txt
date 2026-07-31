/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
\/\/\/\/\/\/\/\/\/\/\/\/\/ C O U N T E R \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
/\/\/\/\/\/\/\/\/\/\/\/\/\ ============= /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

DESCRIPTION
===========
HPH Counter is a cgi program created in perl for tracking the
number of visits to a web page. By simply inserting a small
code into a web page, the page will display the number of
times the page has been accessed since the last time you
reset the counter.

INSTALLATION
============
What makes HPH Counter different from any other page counter
script is that HPH Counter features an easy-to-use admin panel,
small and fast counting process, and best of all, an extremely
easy-to-use setup wizard. Below are the steps to installing
the HPH Counter, with examples after each step:

 1) Set the correct path to perl at the top of the source files.
 2) Create a new directory called counter or something similar.
    For the purpose of keeping things simple, I'll assume you're
    installing this in a folder called counter in your cgi-bin.
 3) Chmod the new folder you created to 777 (666 will NOT work!).
 4) Upload all of the files to the new folder and set the
    permissions to 755.
 5) Go to http://www.yourhost.com/cgi-bin/counter/setup.cgi
    (url will vary) and click on Start Setup.
That's it, just follow the on-screen instructions and you're all set :)

HOW TO USE
==========
To actually put the counter on your page, you've got 2 options:
  1) Use SSI to include (/cgi-bin/counter/counter.cgi).
  2) Place the following code in your page:
       <script language="JavaScript"
       src="http://www.myhost.com/cgi-bin/counter/counter.cgi?js">
       </script>
Again, your URL/paths will vary.

CHANGING SETTINGS
=================
To change settings, such as resetting, changing the text, or
changing your password, go to
http://www.myhost.com/cgi-bin/counter/admin.cgi and click on
the option you want.

MORE HELP
=========
If you are having any kind of problems, remember that you have all
the right in the world to modify the script, so long as you don't
take credit for it and sell it.
If you need personal help, you can email me at renegade@siliconshadow.com
or on icq at 28387303. I use ReNeGaDeSm on AIM, but I don't use that
program too much, you'll have better luck with icq.