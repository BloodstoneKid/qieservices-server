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
	<style>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
    color: #333;
}

header {
    background-color: #004080;
    color: white;
    padding: 15px;
    text-align: center;
}

nav {
    display: flex;
    justify-content: center;
    background-color: #0066cc;
    padding: 10px;
}

nav a {
    color: white;
    margin: 0 15px;
    text-decoration: none;
    font-size: 18px;
}

nav a:hover {
    text-decoration: underline;
}

.container {
    padding: 20px;
    background-color: white;
    margin: 20px auto;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    max-width: 600px; /* Ancho máximo ajustado */
}

/* Estilos para formularios */
form {
    display: flex;
    flex-direction: column;
}

form label {
    margin-top: 10px;
}

form input, form textarea {
    width: calc(100% - 20px); /* Para que no ocupe toda la pantalla */
    padding: 10px;
    margin: 5px 10px; /* Margen ajustado */
    border: 1px solid #ccc;
    border-radius: 4px;
}

form button {
    background-color: #004080;
    color: white;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    margin: 10px auto; /* Para centrar el botón */
    border-radius: 4px;
    max-width: 150px; /* Ancho máximo del botón */
}

form button:hover {
    background-color: #003366;
}

/* Estilo para hipervínculos */
a {
    color: #004080;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Página de Quiénes Somos */
.about-section {
    padding: 20px;
    background-color: white;
    margin: 20px auto;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    max-width: 800px;
}

.about-section h2 {
    color: #004080;
}
</style>
        <title>Home de $nombre_usuario</title>
        <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    </head>
    <body>
        <h1>Bienvenidx de vuelta, $nombre_usuario</h1>
        <p>Accede a tu blog personal, correo electrónico o la plataforma Moodle</p>
        <p>Puedes acceder a tus ficheros personales y al fichero público de apuntes desde tu cliente SFTP preferido</p>
       	<a href=\"verblog.cgi?nombre_usuario=$usuario\">Mi blog</a>
	<a href=\"../correo\">Correo</a>
	<a href=\"../moodle\">Moodle</a>
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
    </body>
</html>";
