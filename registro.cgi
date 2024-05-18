#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use Email::Send::SMTP::Gmail;

my $cgi = CGI->new;
my $nombre_usuario = $cgi->param('nombre_usuario');
my $contrasena = $cgi->param('contrasena');
my $nombre = $cgi->param('nombre');
my $apellido = $cgi->param('apellido');
my $email = $cgi->param('email');
my $correo_postal = $cgi->param('correo_postal');
my $tipo_usuario = $cgi->param('tipo_usuario');

my $conexiondb = DBI->connect('DBI:MariaDB:database=dbusuarios;host=localhost','useradmin','admin');
my $query = $conexiondb->prepare("SELECT username FROM userdata WHERE username=\"$nombre_usuario\"");
my $resultado = $query->execute();
my @ref = $query->fetchrow_array();

if($ref[0] eq $nombre_usuario){
	#Error usuario existe
	print $cgi->redirect("http://192.168.1.148/usuarioexiste.html");
	exit;
}

my $nombre_grupo = $tipo_usuario eq "alumno" ? "alumnos" : "profesores";

print `sudo useradd -G $nombre_grupo,sftp_users -p $contrasena $nombre_usuario`;
print `sudo setquota -u $nombre_usuario 0 81920 0 100 /dev/sda1`;

$conexiondb->do("INSERT INTO userdata VALUES (\"$nombre_usuario\",\"$contrasena\",\"$nombre\",\"$apellido\",\"$email\",\"$correo_postal\",\"$tipo_usuario\")");
$conexiondb->disconnect();

my ($mail,$error) = Email::Send::SMTP::Gmail->new( -port=>587,
	-smtp=>'smtp.gmail.com',
	-login=>'nafnimda@gmail.com',
	-pass=>'cmbglwsscvkcalsw');

my $contCorr = '<h1>Bienvenidx al Departamento de Informática y automática USAL</h1>
	<p>Se te ha proveído de un correo de la plataforma, acceso FTP a apuntes y ficheros personales, un blog personal y acceso a Moodle</p>
	<p>No olvides respetar las normas y usar la plataforma con responsabilidad</p>';

$mail->send(-to=>$email, -subject=>'Bienvenidx', -body=>$contCorr, -contenttype=>'text/html');
$mail->bye;
print $cgi->redirect("http://192.168.1.148/index.html");
