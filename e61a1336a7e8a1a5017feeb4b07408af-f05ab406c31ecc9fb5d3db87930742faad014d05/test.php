<?php
  $secretKey = $_POST["sk"];
//   $postData = array(
//   "appId" => $_POST["aid"],
//   "orderId" => $_POST["oid"],
//   "orderAmount" => $_POST["oa"],
//   "orderCurrency" => $_POST["oc"],
//   "orderNote" => $_POST["on"],
//   "customerName" => $_POST["cn"],
//   "customerPhone" => $_POST["cp"],
//   "customerEmail" => $_POST["ce"],
//   "returnUrl" => $_POST["rurl"],
//   "notifyUrl" => $_POST["nurl"],
// );
//  // get secret key from your config
//  ksort($postData);
//  $signatureData = "";
//  foreach ($postData as $key => $value){
//       $signatureData .= $key.$value;
//  }
 $signature = hash_hmac('sha256', $_POST["dwefsad"], $secretKey,true);
 $signature = base64_encode($signature);

 echo $signature;

 ?>