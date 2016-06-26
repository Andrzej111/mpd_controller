#!/usr/bin/perl
use v5.18;
my $uri ='';
while (my $x = shift @ARGV){
    $uri=$uri.$x.'+';
}
$_ = $uri;
#`xdotool search --name firefox windowkill`;

s/.$//;
#split @ARGV;
my @response = `curl -k https://www.youtube.com/results?search_query=$_ 2>/dev/null`;
for (@response){
    chomp; 
    next unless m/yt-lockup-content/;
    m/a\shref=\"(\S+)"/; 
    if (length($1)>10 && length($1)<40){
        print "youtube.com$1";
        exit;
    }

}
