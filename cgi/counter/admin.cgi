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
<title>Counter Admin</title>
</head>

<body bgcolor="#000000" text="#FFFFFF" link="#FFFFFF" vlink="#FFFFFF">
<p align="center"><img src="http://www.siliconshadow.com/\~renegade/counter.gif"></p>
<hr noshade color="#FF0000">
~;

# Global variables
use vars qw(%form %config $name $value);

# Get HTTP parameters
use CGI;
$cgi = new CGI;
foreach($cgi->param()){
    ($name, $value) = split(/=/);
    $form{$name} = $value;
}

# Get configuration data.
open(CFG, "./config.dat") || &cgierr("An error occured opening the config file: $!");
while(<CFG>){
    ($name, $value) = split(/``/);
    $config{$name} = $value;
}
close CFG;

foreach $conf(keys %config){
    $config{$conf} =~ s/\n$//;
    $config{$conf} =~ s/\r$//;
}

if($cgi->param('action') eq 'reset'){
    &reset;
}elsif($cgi->param('action') eq 'set-text'){
    &set_text;
}elsif($cgi->param('action') eq 'chg-pass'){
    &change_pass;
}else{
    &menu;
}

sub reset{
    my $buffer;
    my $date     = $cgi->param('date');
    my $password = $cgi->param('password');

    if(crypt($password, $config{'pass'}) eq $config{'pass'}){
        if($date){
            open(CFG, "config.dat") ||
                &cgierr("An error occured opening config file: $!");
            while(<CFG>){
                $buffer .= $_ unless m|^date``|;
            }
            close CFG;
            $buffer .= "\ndate``$date";
            open(CFG, ">config.dat") ||
                &cgierr("An error occured updating the config file. $!");
            print CFG $buffer;
            close CFG;
            open(NUM, ">$config{'num_file'}") ||
                &cgierr("An error occured opening the num file. $!");
            print NUM "0";
            close NUM;
            print "Counter successfully reset!\n";
        }else{
            print <<"HTML";
<h1>Reset Form</h1>
<form method="post" action="admin.cgi">
<input type="hidden" name="action" value="reset">
<input type="hidden" name="password" value="$password">
<p>Please enter the date you would like displayed in the counter:
<input type="text" name="date" size="35"> <input type="submit" value="Reset"></p>
</form>
HTML
        }
    }else{
        print <<"PASS";
<h1>Password required</h1>
<form method="post" action="admin.cgi">
<input type="hidden" name="action" value="reset">
<p>Enter password: <input type="password" name="password">
<input type="submit" value="Login"></p>
</form>
PASS
    }
}

sub set_text{
    my $buffer;
    my $text     = $cgi->param('text');
    my $password = $cgi->param('password');

    if(crypt($password, $config{'pass'}) eq $config{'pass'}){
        if($text){
            open(CFG, "config.dat") ||
                &cgierr("An error occured opening config file: $!");
            while(<CFG>){
                $buffer .= $_ unless m|^text``|;
            }
            close CFG;
            $buffer .= "\ntext``$text";
            open(CFG, ">config.dat") ||
                &cgierr("An error occured updating the config file. $!");
            print CFG $buffer;
            close CFG;
            print "Text successfully updated!\n";
        }else{
            print <<"HTML";
<h1>Update Text</h1>
<form method="post" action="admin.cgi">
<input type="hidden" name="action" value="set-text">
<input type="hidden" name="password" value="$password">
<p>Please enter the text you would like displayed in the counter:
<input type="text" name="text" size="35"> <input type="submit" value="Update Text"></p>
</form>
HTML
        }
    }else{
        print <<"PASS";
<h1>Password required</h1>
<form method="post" action="admin.cgi">
<input type="hidden" name="action" value="set-text">
<p>Enter password: <input type="password" name="password">
<input type="submit" value="Login"></p>
</form>
PASS
    }
}

sub change_pass{
    my $buffer, $cpass;
    my $pass      = $cgi->param('pass');
    my $password  = $cgi->param('password');
    my @saltchars = ('A' .. 'Z', 0 .. 9, 'a' .. 'z', '.', '/');
    my $salt      = join('', @saltchars[rand 64, rand 64]);

    if(crypt($password, $config{'pass'}) eq $config{'pass'}){
        if($pass){
        $cpass = crypt($pass, $salt);
            open(CFG, "config.dat") ||
                &cgierr("An error occured opening config file: $!");
            while(<CFG>){
                $buffer .= $_ unless m|^pass``|;
            }
            close CFG;
            $buffer .= "\npass``$cpass";
            open(CFG, ">config.dat") ||
                &cgierr("An error occured updating the config file. $!");
            print CFG $buffer;
            close CFG;
            open(NUM, ">$config{'num_file'}") ||
                &cgierr("An error occured opening the num file. $!");
            print NUM "0";
            close NUM;
            print "Password successfully changed!\n";
        }else{
            print <<"HTML";
<h1>Change Password</h1>
<form method="post" action="admin.cgi">
<input type="hidden" name="action" value="chg-pass">
<input type="hidden" name="password" value="$password">
<p>Please enter your new password for admin functions:
<input type="password" name="pass" size="35"> <input type="submit" value="Reset"></p>
</form>
HTML
        }
    }else{
        print <<"PASS";
<h1>Password required</h1>
<form method="post" action="admin.cgi">
<input type="hidden" name="action" value="chg-pass">
<p>Enter password: <input type="password" name="password">
<input type="submit" value="Login"></p>
</form>
PASS
    }
}

sub menu{
    print qq~
    <div align="center">
     <h1>Counter Admin</h1>
     <form method="get" action="admin.cgi">
     <input type="hidden" name="action" value="reset">
     <input type="submit" value="Reset Counter">
     </form>
     <form method="get" action="admin.cgi">
     <input type="hidden" name="action" value="set-text">
     <input type="submit" value="Set Counter Text">
     </form>
     <form method="get" action="admin.cgi">
     <input type="hidden" name="action" value="chg-pass">
     <input type="submit" value="Change Password">
     </form>
    </div>
    ~;
}

print qq~
    <hr noshade color="#FF0000">
    <div align="center">
     <div id="links" style="border: 2px solid #FF0000;border-top:1px solid #000000;width:450"
     align="center">
      <font size="+1" face="Verdana, Arial"><u>Menu</u></font><br>
      <a href="admin.cgi">Admin Home</a> | <a href="admin.cgi?action=reset">Reset Counter</a> |
      <a href="admin.cgi?action=set-text">Set Counter Text</a> |
      <a href="admin.cgi?action=chg-pass">Change Password</a>
     </div>
    </div>
    </body>
    </html>
~;