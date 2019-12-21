<?php

date_default_timezone_set("Asia/Calcutta");
$date = '10/17/2019 07:28:34 pm';
echo $date;

$date2 = date('m/d/Y h:i:s a', time());
$date=strtotime($date);
// print_r($date);
echo "<br>";
$date2=strtotime($date2);
print_r(abs($date-$date2));


// $inter=abs($sent-$cur);
?>