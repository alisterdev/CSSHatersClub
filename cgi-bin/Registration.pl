#!/usr/bin/perl

use CGI qw(:standard);

my $name = escapeHTML(param('name'));
my $username = escapeHTML(param('username'));
my $password = escapeHTML(param('password'));

$error = "";

	print "Content-Type: text/html\n\n";
	$pageHTML = <<'END_MESSAGE';
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Registration | CSS Haters Club</title>	
</head>
<body bgcolor='#0070e0'>
	<font size='5' color='white' face='Helvetica Neue, Arial'>		
		<table align='center'>					
END_MESSAGE

if ((defined $name and length $name) and (defined $username and length $username) and (defined $password and length $password)) {
	
	$userExists = 1;
	$file = "members.csv";

	open(INFO, "<$file");
	@lines = <INFO>;
	close(INFO);

	foreach $line (@lines) {	
		@fields = split(" " , $line);
		if ($fields[1] eq $username) {	
			$pageHTML .= "<tr><td align='center'><br/><br/><br/><br/><br/><br/><br/><br/>Sorry, the username is already taken!<br/></td></tr><tr><td align='center'>Please <a href='../register.html'><font color='white'>try again</font></a>!</td></tr>";	
			$userExists = 1;
			last;		
		} else {
			$userExists = 0;
		}
	}

	if ($userExists eq 0) {
		open(my $fh, '>>', $file) or die "Could not open file '$file' $!";
		print $fh "$name $username $password\n";
		close $fh;
		$pageHTML .= "<tr><td align='center'><br/><br/><br/><br/><br/><br/><br/><br/>Registration successful!<br/></td></tr><tr><td align='center'>You can now login <a href='../index.html'><font color='white'>here</font></a>!</td></tr>";
	}

} else {
	$error .= "<tr><td align='center'><br/><br/><br/><br/><br/><br/><br/><br/>Make sure to fill in all the fields!<br/></td></tr><tr><td align='center'>Please <a href='../register.html'><font color='white'>try again</font></a>!</td></tr>";
}
print $pageHTML . $error . "</table></font></body></html>";