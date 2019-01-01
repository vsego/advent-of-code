#!/usr/bin/env perl

$ws = $ARGV[0] || 5;
$min = $ARGV[1] || 61;

map {
    /Step (\w) must be finished before step (\w) can begin./;
    $gt->{$2}->{$1} = $all->{$1} = $all->{$2} = 1;
} <STDIN>;
$r = join("", map {
    $f = (sort { $a cmp $b } grep { ! ($gt->{$_} and grep { $all->{$_} } keys %{$gt->{$_}}) } keys %$all)[0];
    delete $all->{$f};
    $f
} keys %$all);
print "Part 1: $r\n";

$t = 0;
@w = map { { "t" => 0, "s" => undef } } (1..$ws);
@todo = split(//, $r);
while (@todo) {
    unless ($ns) {
        @cando = grep { $todo = $_; !($u->{$todo} || grep { $gt->{$todo}->{$_} } @todo) } @todo;
        $ns = (sort { $a cmp $b } @cando)[-1] if @cando;
        $u->{$ns} = 1;
    }
    $ne = (grep { !$_->{"s"} } @w)[0];
    if ($ns && $ne && !grep { $_->{"s"} && $gt->{$ns}->{$_->{"s"}} } @w) {
        $ne->{"t"} = $t + ord($ns) - 65 + $min;
        $ne->{"s"} = $ns;
        $ns = undef;
    } else {
        $fe = (sort { $a->{"t"} <=> $b->{"t"} } grep { $_->{"s"} } @w)[0];
        @todo = grep { $_ ne $fe->{"s"} } @todo;
        $t = $fe->{"t"} if $t < $fe->{"t"};
        $fe->{"s"} = undef;
    }
}
print "Part 2: $t\n";
