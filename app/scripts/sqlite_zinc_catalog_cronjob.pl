#!/usr/bin/perl -w
##
##set -e
##
##system("source /etc/profile.d/sge.sh");
##
## cronjob.pl - look at jobs and decide what to do.
##
##
##
##set SGE_ROOT
$ENV{SGE_ROOT}='/usr/share/gridengine';
$ENV{SGE_CELL}='ucsf.bks';



my $RUNAS = "khtang";
use POSIX;
use strict;
use DBI;
use Getopt::Long;

my $driver = "SQLite";
my $database = "/nfs/home/khtang/work/Projects/upload-wizard/app.db";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";


#my $dsn = "DBI:Pg:dbname=uploaddb;host=mem"; #production machine
#my $un = "uploadwrite";

my $dbh = DBI->connect ($dsn, $userid, $password, {RaiseError => 1});
$dbh->{PrintError} = 0;

#my $last_update = unix_timestamp();


my $newstatus = $ARGV[0];
my $newstatus_type = $ARGV[1];

#app.db
#my $cmd_1 = "select id, status_id, last_updated from history where status_id = 5 order by id";
#postgres

my $cmd_1 = "select id, short_name from user order by id";
my $cmd_2 = "select id, status_id, user_id from history where status_id = 1 order by id";
my $cmd_3 = "update history set status_id = ? where id = ?";
#my $cmd_2b = "update job_log set status_type = ? where id = ?";

my $sth1 = $dbh->prepare($cmd_1);
my $row1 = $sth1->execute();

my %short_name;

#prepare short_name dict
while (my @row = $sth1->fetchrow_array()){
	my $user_id = $row[0];
	my $name = $row[1];
	#my $status_type = $row[2];
	#my $date = $row[3];
	$short_name{$user_id}=$name;

}

my $sth2 = $dbh->prepare($cmd_2);
my $row2 = $sth2->execute();

while (my @row = $sth2->fetchrow_array()) {
        my $job_id = $row[0];
        my $status_id = $row[1];
	my $user_id = $row[2];

	#set up path to jobdir
	my $main_dir ="/nfs/home/khtang/work/Projects/upload-wizard/vendoruploads";
	my $short_name = $short_name{$user_id};
	my $dir = "$main_dir/$user_id\_$short_name/$job_id";
	print "$dir\n";
	if ($status_id == 1){
		system("sh /nfs/home/khtang/code/upload_wizard_codes/submit_catalog_job.sh $dir $short_name");

	} elsif ($status_id == 7) {
		my $sub_dir = "$dir/$short_name";
		print "Sub directory : $sub_dir\n";
		my $jobID = `cat $sub_dir/map.jid`;
		print "Checking $job_id with jobID : $jobID\n";
		my $running = length(`qstat | grep $jobID`);
		if ($running == 0){
			print "Loading is completed\n";
			print "Gathering information from outputs\n";
			
		}
		
		
	}
	
	


}	


#my $sth2a = $dbh->prepare($cmd_2a);
#my $row2a = $sth2a->execute();

