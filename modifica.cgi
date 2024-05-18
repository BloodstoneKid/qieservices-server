#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use DBI;

my $cgi = CGI->new;
my $nombre_usuario = $cgi->param('nombre_usuario');
my $contrasena = $cgi->param('contrasena');
my $nombre = $cgi->param('nombre');
my $apellido = $cgi->param('apellido');
my $email = $cgi->param('email');
my $correo_postal = $cgi->param('correo_postal');

my $conexiondb = DBI->connect('DBI:MariaDB:database=dbusuarios;host=localhost','useradmin','admin');

if($contrasena){
	print `echo "$nombre_usuario:$contrasena"|sudo chpasswd`;
	$conexiondb->do("UPDATE userdata SET contrasena=\"$contrasena\" WHERE username=\"$nombre_usuario\"");
}
if($nombre){
        $conexiondb->do("UPDATE userdata SET nombre=\"$nombre\" WHERE username=\"$nombre_usuario\"");
}
if($apellido){
        $conexiondb->do("UPDATE userdata SET apellido=\"$apellido\" WHERE username=\"$nombre_usuario\"");
}
if($email){
        $conexiondb->do("UPDATE userdata SET email=\"$email\" WHERE username=\"$nombre_usuario\"");
}
if($correo_postal){
        $conexiondb->do("UPDATE userdata SET correo_postal=\"$correo_postal\" WHERE username=\"$nombre_usuario\"");
}

$conexiondb->disconnect();

print $cgi->redirect("http://192.168.1.148/index.html");
