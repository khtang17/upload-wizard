#!/usr/bin/perl -w
# ustatus.pl - update status of a Upload-Wizard job
#
#
#

my $RUNAS = "www";
use POSIX;
use strict;
use DBI;
use Getopt::Long;

my $example = "update_zincload_status.pl <status_id>";

if ($ARGV[1]) {
	my $dir = $ARGV[1];
	chdir "$dir";
}
my $str = `pwd`;
$str =~ s/.*_//;
chomp $str;
my ($job_id) = (split "/", $str)[1];

print `pwd`;
print "debug job id $job_id\n";

my $dsn = "DBI:Pg:dbname=uploaddb;host=mem"; # production machine
my $un = "uploadwrite";

my $dbh = DBI->connect ($dsn, $un, "", {RaiseError => 1});
$dbh->{PrintError} = 0;

my $newstatus = $ARGV[0];

my $cmd2 = "update history set status_id = ? where id = ?";
my $cmd3 = "update history set last_updated = now() where id = ?";
#my $last_updated=unix_timestamp();
my $last_updated = time;
my $sth2 = $dbh->prepare($cmd2);
my $row2 = $sth2->execute($newstatus, $job_id);
my $sth3 = $dbh->prepare($cmd3);
my $row3 = $sth3->execute($job_id); 

print "updating job $job_id with status_id $newstatus\n";

$sth2->finish();
$sth3->finish();
$dbh->disconnect();
