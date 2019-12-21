<?php
// Import PHPMailer classes into the global namespace
// These must be at the top of your script, not inside a function
$result=['c'=>false,'ef'=>false,'sent'=>false,"inem"=>false];
if(!filter_var($_POST['email'],FILTER_VALIDATE_EMAIL)){
  $result['ef']=true;
  $result=json_encode($result);
print_r($result);
   exit();
}

$email=$_POST['email'];
$name = $_POST['name'];
$sub=$_POST['subject'];
$addr=$_POST['address'];
require("./phpmailer/SMTP.php");
require("./phpmailer/Exception.php");
require("./phpmailer/PHPMailer.php");
require('./versions/2/wizard/clientZone/connection.php');
// use phpmailer\PHPMailer\PHPMailer\SMTP;
date_default_timezone_set("Asia/Calcutta");
// use phpmailer\PHPMailer\PHPMailer\PHPMailer;
// use phpmailer\PHPMailer\PHPMailer\Exception;

// Load Composer's autoloader
// require 'vendor/autoload.php';

// Instantiation and passing `true` enables exceptions
$mail = new PHPMailer\PHPMailer\PHPMailer();
// print_r($mail);
$em=$email;
if(!$con){
   $result['c']=false;
}else{
   $result['c']=true;
//    $res=mysqli_query($con,"select * from users where email='$email'");
   // $result['res']=$email;
//    if(mysqli_num_rows($res)==1){
$date = date('m/d/Y h:i:s a', time());
// mysqli_query($con,"delete from resendPassword where email='$email'");
mysqli_query($con,"insert into contact values('$name','$email','$sub','$addr','$date')");
mysqli_commit($con);
try {
    //Server settings
   //  $mail->SMTPDebug = 4;                      // Enable verbose debug output
    $mail->isSMTP();                                            // Send using SMTP
    $mail->Host       = 'smtp.gmail.com';                    // Set the SMTP server to send through
    $mail->SMTPAuth   = true;                                   // Enable SMTP authentication
    $mail->Username   = 'wasche.services@gmail.com';                     // SMTP username
    $mail->Password   = 'kpanhdgzakdemdsg';                                     // SMTP password
    $mail->SMTPSecure = 'ssl';                               
    // $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;         // Enable TLS encryption; `PHPMailer::ENCRYPTION_SMTPS` also accepted
    $mail->Port       = 465;                                    // TCP port to connect to

    //Recipients
    $mail->setFrom('wasche.services@gmail.com','Wasche Services');
    $mail->addAddress($email);
        // Add a recipient
    $mail->addAddress('sahithbrahmam@yahoo.com');               // Name is optional
    // $mail->addReplyTo('info@example.com', 'Information');
    // $mail->addCC('cc@example.com');
    // $mail->addBCC('bcc@example.com');

    // Attachments
    // $mail->addAttachment('/var/tmp/file.tar.gz');         // Add attachments
    // $mail->addAttachment('/tmp/image.jpg', 'new.jpg');    // Optional name

    // Content
    $mail->isHTML(true);     
   
   //  $em2=urlencode("https://wasche-services.herokuapp.com/resendP#".$em);
   //  echo $em;
   //  echo "href=".$em;
    $btn="<div style='display:block;width:fit-content;margin-top:20px;'><a href='#' onclick='console.log(\"Sdsad\");' style='cursor:pointer;padding:10px;text-transform:uppercase;font-size:14px;color:white;background:#019875;outline:none;border-radius:5px;border:1px solid #019875;text-decoration:none;'><span>Contact Information.</sapn></a></p></div>";
    $msg="<style>@import url('https://fonts.googleapis.com/css?family=Open+Sans&display=swap');</style>";       
    $msg=$msg."<div style=\"font-family:'Open Sans',Arial,sans-serif;\"><div style='min-height:4rem;width:100%;display:block;border-bottom:1px solid #c5c5c5;margin-bottom:10px;'><div style='width:fit-content;height:fit-content;margin:auto;display:flex;justify-content:center;align-content:center;'><a href='https://wasche-services.herokuapp.com' style='color:black;font-size:1.6rem;text-decoration:none;text-transform:uppercase;letter-spacing:2px;font-weight:bold;padding:0;margin:0;text-shadow:1px 1px 1px rgba(0,0,0,0.1);'>Wasche</a></div></div>";
    $msg=$msg."<h3 style='margin-bottom:5px;padding:5px;'>Thank you for contacting us.</h3><h5> We will be in touch with you shortly.<br>In the mean time explore our services.<br><br>Thank you.</div>";                      // Set email format to HTML
    // $msg=$msg."<div style='width:fit-content;margin:auto;'><p style='font-size:14px;'><b><span style='font-size:18px'>Hello,</span></b><br><br>We recieved a request to reset your password.<br><br>Click on the below link in order to reset your password.<br><b>Note : </b>This link will expire in another 30 minutes.<br><br> https://wasche-services.herokuapp.com/resendP#$em <br><br></p></div><br><br><p style='font-size:15px;margin:auto;width:fit-content;'>Than you, <b>Wasche Services.</b></p></div> ";
    $mail->Subject = 'Password Reset';
    $mail->Body    = $msg;
   //  echo $em;
   //  print_r($em);
    $mail->AltBody = "Wasche\n\nHello,\n>We recieved your details.\n\nThank you for contacting us.\n\nWe will be in touch with you in short time.";
    if(!$mail->Send()) {
        $result['sent']=false;
     } else {
        $result['sent']=true;
     }
} catch (Exception $e) {
   $result['sent']=false;
}

}
$result=json_encode($result);
print_r($result);
?>