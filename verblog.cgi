#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);use DBI;

my $cgi = CGI->new;
my $nombre_usuario = $cgi->param('nombre_usuario');

my $conexiondb = DBI->connect('DBI:MariaDB:database=dbusuarios;host=localhost','useradmin','admin');
my $query = $conexiondb->prepare("SELECT titulo,fecha,contenido FROM blogentries WHERE username=\"$nombre_usuario\"");
my $resultado = $query->execute();
print $cgi->header("text/html");

print "<html>
    <head>
	<style>
	body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }
        .blog-container {
            width: 60%;
            max-width: 800px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            padding: 20px;
            overflow-y: auto;
            max-height: 500px;
        }
        .blog-entry {
            border-bottom: 1px solid #e0e0e0;
            padding: 10px 0;
        }
        .blog-entry:last-child {
            border-bottom: none;
        }
        .blog-title {
            font-size: 1.2em;
            font-weight: bold;
            margin: 0;
        }
        .blog-meta {
            font-size: 0.9em;
            color: #666;
        }
	</style>
	<meta charset=\"UTF-8\">
	<link rel=\"stylesheet\" href=\"../style.css\">
        <title>Blog de $nombre_usuario</title>
    </head>
    <body>
	<div class=\"blog-container\">";
while (my @ref = $query->fetchrow_array()){
	print "<div class=\"blog-entry\">
            <p class=\"blog-title\">$ref[0]</p>
            <p class=\"blog-meta\">Por $nombre_usuario - $ref[1]</p>
	    <p>$ref[2]</p>
        </div>";
}
print " <h2>Añadir una entrada</h2>
        <form action=\"agregablog.cgi?nombre_usuario=$nombre_usuario\" method=\"post\">
            <label for=\"titulo\">Titulo</label>
            <input type=\"text\" id=\"titulo\" name=\"titulo\" maxlength=\"20\"><br>
            <label for=\"contenido\">Contenido</label>
            <input type=\"text\" id=\"contenido\" name=\"contenido\" maxlength=\"200\"><br>
	    <input type=\"submit\" value=\"Publicar\">
        </form>
    </body>
</html>";

$conexiondb->disconnect();
