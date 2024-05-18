use Sys::Statistics::Linux;
use Email::Send::SMTP::Gmail;

open(FH,'>',"stats.txt")or die $!;
my $lxs = Sys::Statistics::Linux->new(
	cpustats => 1,
	memstats => 1,
	diskstats => 1,
	diskusage => 1,
	filestats => 1
);

sleep 1;

my $stats = $lxs->get;

print FH "CPU:\n";
foreach my $key ($stats->cpustats){
	print FH "$key:\n";
	foreach my $key2 ($stats->cpustats($key)){
	print FH $key2," ",$stats->cpustats($key,$key2),"\n";
	}
}
print FH "\n\n";
print FH "Memoria:\n";
foreach my $key ($stats->memstats){
	print FH $key," ",$stats->memstats($key),"\n";
}
print FH "\n\n";
print FH "Uso de disco:\n";
foreach my $key ($stats->diskusage){
	print FH "$key:\n";
	foreach my $key2 ($stats->diskusage($key)){
	print FH $key2," ",$stats->diskusage($key,$key2),"\n";
	}
}

close(FH);

my ($mail,$error)=Email::Send::SMTP::Gmail->new(
	-port=>587,
	-smtp=>'smtp.gmail.com',
	-login=>'nafnimda@gmail.com',
	-pass=>'zwhmesrttbpcvnza'
);

print "Error creacion: $error\n" unless ($mail=!-1);

$mail->send(-to=>'andresperdomo737@gmail.com', -subject=>'Auditoria diaria',
	-body=>'A continuacion se presentan las estadisticas y registros del dia.',
	-contenttype=>'text/html',
	-attachments=>'/opt/monitor/stats.txt,/opt/monitor/logs.txt');
$mail->bye;
