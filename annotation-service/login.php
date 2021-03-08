<?php
session_start();

function update_table($conn, $sql_command, string $types , ...$vars ) {
$sql2 = $sql_command; // Add flag that current claim is taken. Need to be freed when evidence is submitted,
$stmt= $conn->prepare($sql2);
$stmt->bind_param($types, ...$vars);
$stmt->execute();
}

$id = $_GET["id"];
$pw_md5 = $_GET["pw"];
//
// $id = $argv[1];
// $pw_md5 = $argv[2];
#
//
// echo($id);
// echo($pw_md5);
$db_params = parse_ini_file( dirname(__FILE__).'/db_params.ini', false);


$servername = "localhost";
$username = $db_params['user'];
$password = $db_params['password'];
$dbname = $db_params['database'];

$conn = new mysqli($servername, $username, $password, $dbname);


if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT id,annotation_mode, finished_calibration FROM Annotators WHERE password_md5 = ? AND id = ?";
$stmt= $conn->prepare($sql);
$stmt->bind_param("si", $pw_md5, $id);
$stmt->execute();

$result = $stmt->get_result();
$credentials_match = $result->num_rows > 0;
if ($credentials_match) {
  $row = $result->fetch_assoc();
  $_SESSION["user"] = $id;
  $_SESSION["annotation_mode"] = $row['annotation_mode'];
  $_SESSION["finished_calibration"] = $row['finished_calibration'];

  $output =  array($credentials_match, $row['annotation_mode'], $row['finished_calibration']);
  update_table($conn, "UPDATE Annotators SET number_logins=number_logins+1 WHERE id=?", 'i', $id);
  echo(json_encode($output));
}else{
  echo 0;
}

$conn->close();
?>
