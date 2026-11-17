<?php
$host = getenv('MYSQL_HOST') ?: 'mariadb';
$db   = getenv('MARIADB_DATABASE') ?: 'mydb';
$user = getenv('MARIADB_USER') ?: 'app_user';
$pass = getenv('MARIADB_PASSWORD') ?: 'app_password';

$status = 'unreachable';
try {
    $pdo = new PDO(
        "mysql:host={$host};dbname={$db};charset=utf8mb4",
        $user,
        $pass,
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
    $status = 'connected';
} catch (Throwable $e) {
    $status = 'error: ' . $e->getMessage();
}
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>PHP Apache MariaDB</title>
</head>
<body>
  <h1>PHP + Apache + MariaDB</h1>
  <p>Database status: <?php echo htmlspecialchars($status, ENT_QUOTES, 'UTF-8'); ?></p>
</body>
</html>
