#!/usr/bin/perl

BEGIN { push @INC, '/var/www/cgi-bin/perl' }

use warnings;
use strict;
use IoTClock;
use Data::Dumper;
use CGI qw(:standard);

$ENV{TERM} = "xterm-256color";


my $content;
my $query = CGI->new;
my $menu = $query->param('menu') || 0;
my $settings = do 'settings.cfg';
my $statusMsg = $query->param('statusMsg') || 0;

my $param;
my $otherParam;

sub overview() {
	IoTClock::get_train();
	
	$settings = do 'settings.cfg';
	
	$content .= "<div class=\"container\">";
	$content .= "  <div class=\"starter-template\">";
	$content .= "    <h2>Train</h2>";
	$content .= "<ul class=\"list-group\">";
	
	my $departure_hour;
	my $departure_minute;
	my $arrival_hour;
	my $arrival_minute;
	
	if(length((localtime($settings->{selection}->{0}->{departure}->{time}))[2])< 2) {
		$departure_hour .= "0";
	}
	
	if(length((localtime($settings->{selection}->{0}->{departure}->{time}))[1])< 2) {
		$departure_minute .= "0";
	}
	
	if(length((localtime($settings->{selection}->{0}->{arrival}->{time}))[2])< 2) {
		$arrival_hour .= "0";
	}
	
	if(length((localtime($settings->{selection}->{0}->{arrival}->{time}))[1])< 2) {
		$arrival_minute .= "0";
	}
	
	$departure_hour .= (localtime($settings->{selection}->{0}->{departure}->{time}))[2];
	$departure_minute .= (localtime($settings->{selection}->{0}->{departure}->{time}))[1];
	$arrival_hour .= (localtime($settings->{selection}->{0}->{arrival}->{time}))[2];
	$arrival_minute .= (localtime($settings->{selection}->{0}->{arrival}->{time}))[1];
	
	
	$content .= "  <li class=\"list-group-item\">Departure from <b>".$settings->{selection}->{0}->{departure}->{station}."</b>&nbsp;<span class=\"label label-default\">Platf ".$settings->{selection}->{0}->{departure}->{platform}."</span>&nbsp;<span class=\"label label-success\">".$departure_hour.":".$departure_minute."</span></li>";
	$content .= "  <li class=\"list-group-item\">Arrival at <b>".$settings->{selection}->{0}->{arrival}->{station}."</b>&nbsp;<span class=\"label label-default\">Platf ".$settings->{selection}->{0}->{arrival}->{platform}."</span>&nbsp;<span class=\"label label-danger\">".$arrival_hour.":".$arrival_minute."</span></li>";
	$content .= "</ul>";
	$content .= "<br/>";
	$content .= "    <h2>Alarm</h2>";
	$content .= "<ul class=\"list-group\">";
	
	my $alarm = IoTClock::get_alarm_time();
	
	$content .= "  <li class=\"list-group-item\">The alarm will ring at <span class=\"label label-success\">".(substr $alarm,0,2).":".(substr $alarm,2,2)."</span></li>";
	$content .= "</ul>";
	$content .= "  </div>";
	$content .= "</div><!-- /.container -->";
}

sub trains() {
	my $stations_data_xml = IoTClock::list_stations();
	
	$content .= "<div class=\"container\">";
	$content .= "  <div class=\"starter-template\">";
	$content .= "    <h2>Train information</h2>";
	$content .= "    <p class=\"lead\">Configure the relevant parameters to find a valid train connection.</p>";
	$content .= "    <h3>From: </h3>";
	$content .= "    <div class=\"btn-group\">";
	$content .= "  <select class=\"btn btn-default dropdown-toggle\" name=\"from\"";

	foreach my $e (@{$stations_data_xml->{station}}) {
		if($settings->{trains}->{0}->{from} eq $e->{content}){
			$content .= "    <option selected value=\"$e->{content}\">$e->{content}</option>";
		} else {
			$content .= "    <option value=\"$e->{content}\">$e->{content}</option>";
		}
	}
	
	$content .= "  </select>";
	$content .= "    </div>";
	$content .= "    <br/>";
	$content .= "<h3>To: </h3>";
	$content .= "<div class=\"btn-group\">";
	$content .= "  <select class=\"btn btn-default dropdown-toggle\" name=\"to\"";

	foreach my $e (@{$stations_data_xml->{station}}) {
		if($settings->{trains}->{0}->{to} eq $e->{content}){
			$content .= "    <option selected value=\"$e->{content}\">$e->{content}</option>";
		} else {
			$content .= "    <option value=\"$e->{content}\">$e->{content}</option>";
		}
	}
	
	$content .= "  </select>";
	$content .= "</div>";
	$content .= "	<br/>";

	$content .= "<h3>Arrival: </h3>";
	$content .= "<div class=\"btn-group\">";
	
	my $hour = substr $settings->{trains}->{0}->{arrival}, 0, 2;
	
	$content .= "  <select class=\"btn btn-default dropdown-toggle\" name=\"hour\"";

	for (my $e=0;$e<24;$e++) {
		$e = sprintf("%02d", $e);
		
		if($hour eq $e) {
			$content .= "    <option selected value=\"$e\">$e</option>";
		} else {
			$content .= "    <option value=\"$e\">$e</option>";
		}
	}

	$content .= "  </select>";
	$content .= "</div>";
	$content .= "&nbsp;:&nbsp;";
	$content .= "<div class=\"btn-group\">";
	
	my $minutes = substr $settings->{trains}->{0}->{arrival}, 2, 2;
	
	$content .= "  <select class=\"btn btn-default dropdown-toggle\" name=\"minutes\"";

	for (my $e=0;$e<60;$e++) {
		$e = sprintf("%02d", $e);
		
		if($minutes eq $e) {
			$content .= "    <option selected value=\"$e\">$e</option>";
		} else {
			$content .= "    <option value=\"$e\">$e</option>";
		}
	}

	$content .= "  </select>";
	$content .= "</div>";
	$content .= "	<br/>";
	$content .= "	<br/>";
	$content .= "	<button type=\"submit\" class=\"btn btn-success\" name=\"save_train\">";
	$content .= "	  <span class=\"glyphicon glyphicon-ok-circle\"></span>";
	$content .= "	  Save";
	$content .= "	</button>";
	$content .= "	<button type=\"submit\" class=\"btn btn-danger\" name=\"cancel_train\">";
	$content .= "	  <span class=\"glyphicon glyphicon-ban-circle\"></span>";
	$content .= "	  Cancel";
	$content .= "	</button>";
	$content .= "	<br/><br/>";
	
	if($statusMsg == 1){
		$content .= "	<div class=\"alert alert-success\">Settings saved successfully</div>";
	} elsif($statusMsg == 2){
		$content .= "	<div class=\"alert alert-danger\">Something went wrong, settings not saved</div>";
	}
	$content .= "  </div>";
	$content .= "</div><!-- /.container -->";
}

sub sounds(){
	$content .= "    <div class=\"container\">";
	$content .= "      <div class=\"starter-template\">";
	$content .= "        <h1>Sounds</h1>";
	$content .= "        <p class=\"lead\">Manage the sounds used by the alarm clock.</p>";
	$content .= "		<div class=\"panel panel-default\">";
	$content .= "		  <!-- Default panel contents -->";
	$content .= "		  <div class=\"panel-heading\">Sound</div>";
	$content .= "		  <!-- Table -->";
	$content .= "		  <table class=\"table\">";
	$content .= "		    <tr><th>Name</th><th>Path/Link</th></tr>";
	
	
	foreach my $i (keys %$settings->{sounds}) {
		$content .= "			<tr><td>".$settings->{sounds}->{$i}->{name}."</td><td>".$settings->{sounds}->{$i}->{file}."</td></tr>";
	}
	
	$content .= "		  </table>";
	$content .= "		</div>";
	$content .= "		<br/>";
	$content .= "		<h3>Add new sound</h3>";
	$content .= "		<br/>";
	$content .= "		<div class=\"input-group\">";
	$content .= "		  <span class=\"input-group-addon\">Name:</span>";
	$content .= "		  <input name=\"sound_name\" type=\"text\" class=\"form-control\" placeholder=\"Sound name, e.g. 'Q-Music'\">";
	$content .= "		</div>";
	$content .= "		<br/>";
	$content .= "		<div class=\"input-group\">";
	$content .= "		  <span class=\"input-group-addon\">Path/Link:</span>";
	$content .= "		  <input name=\"sound_file\" type=\"text\" class=\"form-control\" placeholder=\"Path or link to sound, e.g. 'http://www.q-music.be'\">";
	$content .= "		</div>";
	$content .= "		<br/>";
	$content .= "		<button type=\"submit\" class=\"btn btn-success\" name=\"save_sound\">";
	$content .= "		  <span class=\"glyphicon glyphicon-ok-circle\"></span>";
	$content .= "		  Save";
	$content .= "		</button>";
	$content .= "		<button type=\"submit\" class=\"btn btn-danger\" name=\"cancel_sound\">";
	$content .= "		  <span class=\"glyphicon glyphicon-ban-circle\"></span>";
	$content .= "		  Cancel";
	$content .= "		</button>";
	$content .= "		<br/><br/>";
	
	if($statusMsg == 1){
		$content .= "	<div class=\"alert alert-success\">Settings saved successfully</div>";
	} elsif($statusMsg == 2){
		$content .= "	<div class=\"alert alert-danger\">Something went wrong, settings not saved</div>";
	}
	
	$content .= "      </div>";
	$content .= "    </div><!-- /.container -->	";
}

sub alarms(){
	$content .= "    <div class=\"container\">";
	$content .= "      <div class=\"starter-template\">";
	$content .= "        <h1>Alarms</h1>";
	$content .= "        <p class=\"lead\">Manage the alarms.</p>";
	$content .= "		<div class=\"panel panel-default\">";
	$content .= "		  <!-- Default panel contents -->";
	$content .= "		  <div class=\"panel-heading\">Sound</div>";
	$content .= "		  <!-- Table -->";
	$content .= "		  <table class=\"table\">";
	$content .= "		    <tr><th>Enabled</th><th>Time</th><th>Days</th><th>Sound</th></tr>";
	
	foreach my $i (keys %$settings->{alarms}) {
		my $enabled;
		my $time = (substr $settings->{alarms}->{$i}->{time}, 0, 2).":".(substr $settings->{alarms}->{$i}->{time}, 2, 2);
		my ($mon, $tue, $wed, $thu, $fri, $sat, $sun);
		$mon = (substr $settings->{alarms}->{$i}->{days}, 0, 1) ? "checked" : "";
		$tue = (substr $settings->{alarms}->{$i}->{days}, 1, 1) ? "checked" : "";
		$wed = (substr $settings->{alarms}->{$i}->{days}, 2, 1) ? "checked" : "";
		$thu = (substr $settings->{alarms}->{$i}->{days}, 3, 1) ? "checked" : "";
		$fri = (substr $settings->{alarms}->{$i}->{days}, 4, 1) ? "checked" : "";
		$sat = (substr $settings->{alarms}->{$i}->{days}, 5, 1) ? "checked" : "";
		$sun = (substr $settings->{alarms}->{$i}->{days}, 6, 1) ? "checked" : "";
		
		my $days = "<input type=\"checkbox\" $mon>&nbsp;Mon</input>&nbsp;<input type=\"checkbox\" $tue>&nbsp;Tue</input>&nbsp;<input type=\"checkbox\" $wed>&nbsp;Wed</input>&nbsp;<input type=\"checkbox\" $thu>&nbsp;Thu</input>&nbsp;<input type=\"checkbox\" $fri>&nbsp;Fri</input>&nbsp;<input type=\"checkbox\" $sat>&nbsp;Sat</input>&nbsp;<input type=\"checkbox\" $sun>&nbsp;Sun</input>";

		
		if($settings->{alarms}->{$i}->{enabled}) {
			$enabled = "<input type=\"checkbox\" checked>&nbsp;Enabled</input>";
		} else {
			$enabled = "<input type=\"checkbox\">&nbsp;Enabled</input>";
		}
		
	
		
		$content .= "			<tr><td>".$enabled."</td><td>".$time."</td><td>".$days."</td><td>".$settings->{sounds}->{$settings->{alarms}->{$i}->{sound}}->{name}."</td></tr>";
	}
		
	$content .= "		  </table>";
	$content .= "		</div>";
	$content .= "		<br/>";
	$content .= "		<h3>Add new alarm</h3>";
	$content .= "		<br/>";

	$content .= "<div class=\"btn-group\">";
	$content .= "  <select class=\"btn btn-default dropdown-toggle\" name=\"alarm_hour\"";

	for (my $e=0;$e<24;$e++) {
		$e = sprintf("%02d", $e);
		$content .= "    <option value=\"$e\">$e</option>";
	}

	$content .= "  </select>";
	$content .= "</div>";
	$content .= "&nbsp;:&nbsp;";
	$content .= "<div class=\"btn-group\">";	
	$content .= "  <select class=\"btn btn-default dropdown-toggle\" name=\"alarm_minutes\"";

	for (my $e=0;$e<60;$e++) {
		$e = sprintf("%02d", $e);
		$content .= "    <option value=\"$e\">$e</option>";
	}

	$content .= "  </select>";
	$content .= "</div>";
	
	$content .= "&nbsp;&nbsp;or&nbsp;&nbsp;<input type=\"checkbox\">&nbsp;Automatic</input>";
	
	$content .= "<br/><br/>";
	$content .= "<input type=\"checkbox\">&nbsp;Mon</input>&nbsp;<input type=\"checkbox\">&nbsp;Tue</input>&nbsp;<input type=\"checkbox\">&nbsp;Wed</input>&nbsp;<input type=\"checkbox\">&nbsp;Thu</input>&nbsp;<input type=\"checkbox\">&nbsp;Fri</input>&nbsp;<input type=\"checkbox\">&nbsp;Sat</input>&nbsp;<input type=\"checkbox\">&nbsp;Sun</input>";
	$content .= "<br/><br/>";
	
		$content .= "    <div class=\"btn-group\">";
	$content .= "  <select class=\"btn btn-default dropdown-toggle\" name=\"from\"";

	foreach my $i (keys %$settings->{sounds}) {
		$content .= "    <option value=\"$i\">$settings->{sounds}->{$i}->{name}</option>";
	}
	
	$content .= "  </select>";
	$content .= "    </div>";
	
	$content .= "    <br/><br/><br/>";
	
	$content .= "		<button type=\"submit\" class=\"btn btn-success\" name=\"save_alarm\">";
	$content .= "		  <span class=\"glyphicon glyphicon-ok-circle\"></span>";
	$content .= "		  Save";
	$content .= "		</button>";
	$content .= "		<button type=\"submit\" class=\"btn btn-danger\" name=\"cancel_alarm\">";
	$content .= "		  <span class=\"glyphicon glyphicon-ban-circle\"></span>";
	$content .= "		  Cancel";
	$content .= "		</button>";
	$content .= "		<br/><br/>";
	
	if($statusMsg == 1){
		$content .= "	<div class=\"alert alert-success\">Settings saved successfully</div>";
	} elsif($statusMsg == 2){
		$content .= "	<div class=\"alert alert-danger\">Something went wrong, settings not saved</div>";
	}
	
	$content .= "      </div>";
	$content .= "    </div><!-- /.container -->	";
}

sub about(){
	
}

sub main() {
	
	if(defined $query->param('save_train')) {

		if(defined $query->param('from') && defined $query->param('to') && defined $query->param('hour') && defined $query->param('minutes')) {
			$statusMsg = 1;
			
			$settings->{trains}->{0}->{from} = $query->param('from');
			$settings->{trains}->{0}->{to} = $query->param('to');
			$settings->{trains}->{0}->{arrival} = $query->param('hour').$query->param('minutes');

			open FILE, "> settings.cfg" or ($statusMsg = 2);
			print FILE Dumper($settings);
			close FILE;
		}
	
		return print "Status: 302 Moved\nLocation: index.cgi?menu=2&statusMsg=$statusMsg\n\n";
	}
	
	if(defined $query->param('cancel_train')) {
		
		return print "Status: 302 Moved\nLocation: index.cgi?menu=2\n\n";
	}
	
	if(defined $query->param('save_sound')) {

		if(defined $query->param('sound_name') && defined $query->param('sound_file')) {
			$statusMsg = 1;
			my $size = keys %$settings->{sounds};
			
			$settings->{sounds}->{$size}->{name} = $query->param('sound_name');
			$settings->{sounds}->{$size}->{file} = $query->param('sound_file');
			
			open FILE, "> settings.cfg" or ($statusMsg = 2);
			print FILE Dumper($settings);
			close FILE;
		}
	
		return print "Status: 302 Moved\nLocation: index.cgi?menu=3&statusMsg=$statusMsg\n\n";
	}
	
	if(defined $query->param('cancel_sound')) {
		
		return print "Status: 302 Moved\nLocation: index.cgi?menu=3\n\n";
	}
	
	if(defined $query->param('save_alarm')) {

		if(defined $query->param('alarm_time') && defined $query->param('alarm_days') && defined $query->param('alarm_enabled') && defined $query->param('alarm_sound')) {
			$statusMsg = 1;
			my $size = keys %$settings->{alarms};
			
			$settings->{alarms}->{$size}->{time} = $query->param('alarm_time');
			$settings->{alarms}->{$size}->{days} = $query->param('alarm_days');
			$settings->{alarms}->{$size}->{enabled} = $query->param('alarm_enabled');
			$settings->{alarms}->{$size}->{sound} = $query->param('alarm_sound');
			
			open FILE, "> settings.cfg" or ($statusMsg = 2);
			print FILE Dumper($settings);
			close FILE;
		}
	
		return print "Status: 302 Moved\nLocation: index.cgi?menu=1&statusMsg=$statusMsg\n\n";
	}
	
	if(defined $query->param('cancel_alarm')) {
		
		return print "Status: 302 Moved\nLocation: index.cgi?menu=1\n\n";
	}
	
	$content .= IoTClock::read_file("html/header");
	$content .= IoTClock::read_file("html/navbar");
	
	$content .= $query->startform(-name=>'form',-method=>'post');
	
	if($menu == 1) {
		alarms();
	} elsif ($menu == 2) {
		trains();	
	} elsif ($menu == 3) {
		sounds();	
	} elsif ($menu == 4) {
		about();	
	} else {
		overview();
		#alarms();
	}
	
	$content .= IoTClock::read_file("html/footer");

	print $content;
}

main();