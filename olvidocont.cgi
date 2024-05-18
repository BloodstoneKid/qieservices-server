#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use Email::Send::SMTP::Gmail;

my $cgi = CGI->new;
my $email = $cgi->param('email');

my $conexiondb = DBI->connect('DBI:MariaDB:database=dbusuarios;host=localhost','useradmin','admin');
my $query = $conexiondb->prepare("SELECT email FROM userdata WHERE email=\"$email\"");
my $resultado = $query->execute();
my @ref = $query->fetchrow_array();

if($ref[0] ne $email){
	#No está registrado ese correo
	print $cgi->redirect("http://192.168.1.148/index.html");
	exit;
}

my @chars = ("A".."z","a".."z");
my $randpass;
$randpass .= $chars[rand @chars] for 1..8;
print `echo "$nombre_usuario:$randpass"|sudo chpasswd`;
$conexiondb->do("UPDATE userdata SET contrasena=\"$randpass\" WHERE email=\"$email\"");

$conexiondb->disconnect();

my ($mail,$error) = Email::Send::SMTP::Gmail->new( -port=>587,
	-smtp=>'smtp.gmail.com',
	-login=>'nafnimda@gmail.com',
	-pass=>'cmbglwsscvkcalsw');

my $contCorr = "<h1>Recuperación contraseña</h1>
	<p>Se te ha generado automáticamente la contraseña $randpass . Asegúrate de no perderla. Podrás cambiar tu contraseña en tu página personal</p>";

$mail->send(-to=>$email, -subject=>'Recuperación contraseña', -body=>$contCorr, -contenttype=>'text/html');
$mail->bye;
print $cgi->redirect("http://192.168.1.148/index.html");

