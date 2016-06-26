#!/usr/bin/perl
use v5.18;
use utf8;
my %commands = (
    '1' => 'play',
    '2' => 'pause',
    '3' => 'stop',
    '4' => 'next',
    '5' => 'prev'
    );
my @elements;
push @elements, $_ while ($_ = shift @ARGV);
my $search_string = join (' ',@elements);
if (length($elements[0]) == 1 && grep (/^$elements[0]$/,keys %commands)){
    `mpc $commands{$elements[0]}`;
    exit;
} 

if ($search_string ~~ m/^Volume\:\s*(\w+)/) {
    given ($1) {
        system("amixer -q set Master 5%-") when /down/;
        system("amixer -q set Master toggle") when /mute/;
        system("amixer -q set Master unmute && amixer -q set Master 5%+") when /up/;
    }
        exit;
}
if ($search_string ~~ m/^Key\:\s*(.*)$/) {
#    my $keys= join ('+',
    system("xdotool key $1");
    exit;
}
if ($search_string ~~ m/^Clip\:\s*(.*)/ms) {
#    my $keys= join ('+',
    system("DISPLAY=:0 echo \'\'\'$1\'\'\' | xclip -i -selection clipboard");
    exit;
}


`killall firefox`;
`mpc stop`;

if ($search_string ~~ m/^Radio\:\s*(\d+)/) {
        system("firefox --no-remote player.polskieradio.pl/-$1");
        exit;
}

my @search = `mpc search any "$search_string"`;
say @search;

if (scalar (@search) >0){
    for (@search){
        chomp; 
        `mpc add "$_"`; 
    }
    my $num = `mpc playlist | wc -l`; 
    chomp $num; 
    $num=$num-$#search; 
    say $num;
    `mpc play $num`;
} else {
    `find_yt_and_open.pl $search_string`;
}
#mpc search any "$1" | perl -nE 'chomp; say;'
