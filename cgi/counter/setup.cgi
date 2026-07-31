#!/usr/bin/perl -w

############################################################
################## Home Page Hit Counter ###################
############################################################
####### Counter script written by Brandon Ramirez. #########
############################################################

#####################################################################
# HPH Counter Copyright (C) 2000 Brandon Ramirez. For information
# on how to use this program, look at readme.txt. for a copy of
# the GNU General Public Liscence, look at gpl.txt.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#######################################################################

print "Content-type: text/html\n\n";

print qq~<html>
<head>
<style type="text/css">
<!--
 a:link    {text-decoration:none}
 a:visited {text-decoration:none}
 a:hover   {text-decoration:underline}
-->
</style>
<title>Counter Setup</title>
<script language="JavaScript">
<!--
 function setDate(){
  window.document.forms[0].date.value = new Date();
 }
//-->
</script>
</head>

<body bgcolor="#000000" text="#FFFFFF" link="#FFFFFF" vlink="#FFFFFF">
<p align="center"><img src="http://www.siliconshadow.com/\~renegade/counter.gif"></p>
<hr noshade color="#FF0000">
~;

# Declare global variables.
use vars qw($cgi $action $readme @saltchars $salt);

@saltchars = ('A' .. 'Z', 0 .. 9, 'a' .. 'z', '.', '/');
$salt      = join('', @saltchars[rand 64, rand 64]);

use CGI;
$cgi    = new CGI;
$action = $cgi->param('action');

if($action eq 'set-text'){
    &set_text;
}elsif($action eq 'set-date'){
    &set_date;
}elsif($action eq 'set-pass'){
    &set_pass;
}elsif($action eq 'finish'){
    &finish;
}else{
    &start;
}

sub start{
    print qq~
     <div align="center">
      <h1>Welcome to Counter Setup!</h1>
       <form method="get" action="$ENV{'SCRIPT_NAME'}">
       <input type="hidden" name="action" value="set-text">
       <input type="submit" value="Start Setup >>">
       </form>
      </div>
    ~;
}

sub set_text{
    my $text = $cgi->param('text');

    if($text){
        &set_date;
    }else{
        print qq~
         <h1>Set Counter Text</h1>
         <form method="post" action="$ENV{'SCRIPT_NAME'}">
         <input type="hidden" name="action" value="set-date">
         Enter the text displayed in the counter below. You may use
         the following variables:<br>
         %NUM%  - Represents the number of visits (counter is useless without this)<br>
         %DATE% - Represents the date since the last time you reset the counter.<br>
         Example: You are visitor number %NUM% since %DATE%.<br>
         <br>
         <input type="text" name="text" size="35"><br>
         <input type="submit" value="Next Step>>">
         </form>
        ~;
    }
}

sub set_date{
    my $date = $cgi->param('date');
    my $text = $cgi->param('text');

    if(!$text){
        &set_text;
    }else{
        if($date){
            &set_pass;
        }else{
            print qq~
             <h1>Set Date</h1>
             <script language="JavaScript">
              <!--
               window.onload=setDate;
              //-->
             </script>
             <form method="post" action="$ENV{'SCRIPT_NAME'}">
             <input type="hidden" name="action" value="set-pass">
             <input type="hidden" name="text" value="$text">
             Enter today's date: <input type="text" name="date" size="40"><br>
             <input type="submit" value="Next Step>>">
             </form>
            ~;
        }
    }
}

sub set_pass{
    my $pass = $cgi->param('pass');
    my $date = $cgi->param('date');
    my $text = $cgi->param('text');

    if(!$text){
        &set_text;
    }else{
        if(!$date){
            &set_date;
        }else{
            print qq~
             <h1>Set Password</h1>
             <form method="post" action="$ENV{'SCRIPT_NAME'}">
             <input type="hidden" name="action" value="finish">
             <input type="hidden" name="text" value="$text">
             <input type="hidden" name="date" value="$date">
             Please enter the password you would like to use to manage your counter:
             <input type="password" name="pass"> <input type="submit" value="Finish Setup">
             </form>
            ~;
        }
    }
}

sub finish{
    my $pass = $cgi->param('pass');
    my $date = $cgi->param('date');
    my $text = $cgi->param('text');

    unless(($pass)and($date)and($text)){
        print qq~
         <h1>Setup Error</h1>
         You left out an option somewhere.
         <a href="$ENV{'SCRIPT_NAME'}">Please start the setup process again</a>.
        ~;
    }

    my $cpass = crypt($pass, $salt);

    print "<h1>Setup Conclusion</h1>\n";
    print "Building configuration file...<br>\n";
    open(CONFIG, ">./config.dat") || &cgierr("Couldn't create the configuration file: $!");
    print CONFIG "num_file``num.dat\n";
    print CONFIG "pass``$cpass\n";
    print CONFIG "text``$text\n";
    print CONFIG "date``$date";
    close CONFIG;
    print "Configuration file successfully created.<br>\n";

    print qq~<br>
     The default data file for tracking the visitors is num.dat. You can change this
     in the config.dat file. You may change your settings <a href="admin.cgi">here</a>.
    ~;
}

sub cgierr{
    $error = shift;

    print $error;
    die $error;
}

print qq~
    <hr noshade color="#FF0000">
    </body>
    </html>
~;