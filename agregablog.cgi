#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use DateTime;

my $cgi = CGI->new;
my $nombre_usuario = $cgi->param('nombre_usuario');
my $titulo = $cgi->param('titulo');
my $contenido = $cgi->param('contenido');

my $conexiondb = DBI->connect('DBI:MariaDB:database=dbusuarios;host=localhost','useradmin','admin');

my $fecha = DateTime->now(time_zone => 'local');
my $fechaformat = $fecha->strftime('%Y-%m-%d %H:%M:%S');
$conexiondb->do("INSERT INTO blogentries VALUES (\"$nombre_usuario\",\"$fechaformat\",\"$titulo\",\"$contenido\")");
$conexiondb->disconnect();

print $cgi->redirect("http://192.168.1.148/cgi-bin/verblog.cgi?nombre_usuario=$nombre_usuario");
