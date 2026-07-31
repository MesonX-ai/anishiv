#!/usr/bin/perl -w

############################################################
################ Home Page Hit Counter #####################
############################################################
######## Counter script written by Brandon Ramirez. ########
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

# Global variables
use vars qw(%config $name $value);

# Get configuration data.
open(CFG, "./config.dat") || &cgierr("An error occured opening the config file: $!");
while(<CFG>){
    ($name, $value) = split(/``/);
    $value =~ s/\n$//;
    $config{$name} = $value;
}
close CFG;

&display;

sub display{
    my $text = $config{'text'};
    my $date = $config{'date'};
    my $num  = 0;

    if(-e $config{'num_file'}){
        open(NUM, $config{'num_file'}) ||
            &cgierr("An error occured opening the num file: $!");
            $num = <NUM>;
        close NUM;
    }

    # Update the data file and increment the visits number by 1.
    $num++;
    open(NUM, ">$config{'num_file'}") ||
        &cgierr("Couldn't open the num file for overwriting: $!");
    print NUM $num;
    close NUM;

    $text =~ s/%NUM%/$num/gi;
    $text =~ s/%DATE%/$date/gi;

    if($ENV{'QUERY_STRING'} eq "js"){
        $text =~ s/"/'/g;
        print "document.write(\"$text\");";
    }else{
        print $text;
    }
}

sub cgierr{
    $error = shift;

    print $error;
    die $error;
}