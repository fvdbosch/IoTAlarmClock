package IoTClock;

use warnings;
use strict;

use LWP::Simple;
use XML::Simple;
use Data::Dumper;
use Date::Parse;
use POSIX qw(strftime);

sub read_file {
	my $file = shift;
	my $content;
	
	open (FILE, $file);
	while (<FILE>) {
	        chomp;
	        $content .= $_;
	}
	close (FILE);

	return $content;
}

sub get_train() {
	my $settings = do 'settings.cfg';

	my $from = $settings->{trains}->{0}->{from};
	my $to = $settings->{trains}->{0}->{to};
	my $when = strftime "%d%m%y", localtime;
	my $time = $settings->{trains}->{0}->{arrival};

	my $trains_api_url = "http://api.irail.be/connections/?to=$to&from=$from&date=$when&time=$time&timeSel=arrive&typeOfTransport=train";

	my $trains_data_raw = get $trains_api_url or die "Couldn't get $trains_api_url";
	my $trains_data_xml = new XML::Simple (KeyAttr=>[])->XMLin($trains_data_raw);
	
	my $train_departure_time = 0;

	foreach my $e (@{$trains_data_xml->{connection}}) {
		if((($e->{departure}->{time}->{content} + $e->{departure}->{delay}) > $train_departure_time)) {#&& (($e->{arrival}->{time}->{content} + $e->{arrival}->{delay}) <= $time) 
			$settings->{selection}->{0}->{departure}->{time} = $e->{departure}->{time}->{content};
			#($train_departure_min, $train_departure_hour) = (localtime($train_departure_time))[1,2]; 
			$settings->{selection}->{0}->{departure}->{delay} = $e->{departure}->{delay}/60;
			$settings->{selection}->{0}->{departure}->{platform} = $e->{departure}->{platform}->{content};
			$settings->{selection}->{0}->{departure}->{station} = $e->{departure}->{station}->{standardname};

			$settings->{selection}->{0}->{arrival}->{time} = $e->{arrival}->{time}->{content};
			#($train_arrival_min, $train_arrival_hour) = (localtime($train_arrival_time))[1,2];
			$settings->{selection}->{0}->{arrival}->{delay} = $e->{arrival}->{delay}/60;
			$settings->{selection}->{0}->{arrival}->{platform} = $e->{arrival}->{platform}->{content};
			$settings->{selection}->{0}->{arrival}->{station} = $e->{arrival}->{station}->{standardname};
		}
	}
	
	open FILE, "> settings.cfg" or return 0;
	print FILE Dumper($settings);
	close FILE;
	
	return 1;
}

sub list_stations() {
	my $stations_api_url = "http://api.irail.be/stations/";
	
	my $stations_data_raw = get $stations_api_url or die "Couldn't get $stations_api_url";
	my $stations_data_xml = new XML::Simple (KeyAttr=>[])->XMLin($stations_data_raw);
	
	return $stations_data_xml;
}

sub get_alarm_time() {
	my $settings = do 'settings.cfg';

	my $preparation_time = $settings->{ready}->{0}->{duration};
	my $train_departure_time = $settings->{selection}->{0}->{departure}->{time};
	my ($train_departure_min, $train_departure_hour) = (localtime($train_departure_time))[1,2];
	my $time_in_seconds = ((localtime($train_departure_time))[1]*60) + ((localtime($train_departure_time))[2]*3600);
	my $train_departure_delay = $settings->{selection}->{0}->{departure}->{delay};
	
	my $alarm_time = $time_in_seconds + $train_departure_delay - $preparation_time;
	my $alarm_hours = ($alarm_time - ($alarm_time % 3600)) / 3600;
	my $alarm_minutes = ($alarm_time % 3600)/60;
	
	$alarm_hours = sprintf("%02d", $alarm_hours);
	$alarm_minutes = sprintf("%02d", $alarm_minutes);	
	
	return "$alarm_hours$alarm_minutes";
}

1;