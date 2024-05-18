#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use DBI;

my $cgi = CGI->new;
my $nombre_usuario = $cgi->param('nombre_usuario');
my $contrasena = $cgi->param('contrasena');

my $conexiondb = DBI->connect('DBI:MariaDB:database=dbusuarios;host=localhost','useradmin','admin');
my $query = $conexiondb->prepare("SELECT username,contrasena FROM userdata WHERE username=\"$nombre_usuario\"");
my $resultado = $query->execute();
my @ref = $query->fetchrow_array();

if($ref[0] ne $nombre_usuario){
	#Error usuario no existe
	print $cgi->redirect("http://192.168.1.148/usuarionoexiste.html");
	exit;
}
if($ref[1] ne $contrasena){
	#Error contraseña equivocada
	print $cgi->redirect("http://192.168.1.148/errorpass.html");
	exit;
}

$conexiondb->disconnect();
print $cgi->header("text/html");

print "<html>
    <head>
        <title>Home de $nombre_usuario</title>
    </head>
    <body>
        <h1>Bienvenidx de vuelta, $nombre_usuario</h1>
        <p>Accede a tu blog personal, correo electrónico o la plataforma Moodle</p>
        <p>Puedes acceder a tus ficheros personales y al fichero público de apuntes desde tu cliente SFTP preferido</p>
        <h2>Modificar datos</h2>
        <form action=\"modifica.cgi?nombre_usuario=$nombre_usuario\" method=\"post\">
            <label for=\"nombre\">Nombre</label>
            <input type=\"text\" id=\"nombre\" name=\"nombre\" maxlength=\"20\"><br>
            <label for=\"apellido\">Apellido</label>
            <input type=\"text\" id=\"apellido\" name=\"apellido\" maxlength=\"20\"><br>
            <label for=\"contrasena\">Contraseña</label>
            <input type=\"password\" id=\"contrasena\" name=\"contrasena\" maxlength=\"10\"><br>
            <label for=\"email\">Correo electrónico</label>
            <input type=\"email\" id=\"email\" name=\"email\" maxlength=\"50\"><br>
            <label for=\"correo_postal\">Dirección de correo postal</label>
            <input type=\"text\" id=\"correo_postal\" name=\"correo_postal\" maxlength=\"50\"><br>
            <input type=\"submit\" value=\"Modificar\">
        </form>
	<a href=\"verblog.cgi?nombre_usuario=$nombre_usuario\">Mi blog</a>
        <a href=\"../correo\">Correo</a>
        <a href=\"../moodle\">Moodle</a>
    </body>
</html>";
