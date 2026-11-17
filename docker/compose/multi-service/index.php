<?php
function ping(string $label, callable $fn): string
{
    try {
        return $label . ': ' . $fn();
    } catch (Throwable $e) {
        return $label . ': error (' . $e->getMessage() . ')';
    }
}

$checks = [];

$checks[] = ping('MariaDB', function () {
    $host = getenv('MYSQL_HOST') ?: 'mariadb';
    $db = getenv('MARIADB_DATABASE') ?: 'mydb';
    $user = getenv('MARIADB_USER') ?: 'app_user';
    $pass = getenv('MARIADB_PASSWORD') ?: 'app_password';
    new PDO(
        "mysql:host={$host};dbname={$db};charset=utf8mb4",
        $user,
        $pass,
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
    return 'ok';
});

$checks[] = ping('PostgreSQL', function () {
    $host = getenv('POSTGRES_HOST') ?: 'postgres';
    $user = getenv('POSTGRES_USER') ?: 'app_user';
    $pass = getenv('POSTGRES_PASSWORD') ?: 'app_password';
    $db = getenv('POSTGRES_DB') ?: 'mydb';
    if (!extension_loaded('pdo_pgsql')) {
        return 'driver missing (expected in full stack exercises)';
    }
    new PDO(
        "pgsql:host={$host};dbname={$db}",
        $user,
        $pass,
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
    return 'ok';
});

$checks[] = ping('Redis host', function () {
    $host = getenv('REDIS_HOST') ?: 'redis';
    $errno = 0;
    $errstr = '';
    $fp = @fsockopen($host, 6379, $errno, $errstr, 2);
    if (!$fp) {
        throw new RuntimeException($errstr ?: 'unreachable');
    }
    fclose($fp);
    return 'reachable';
});
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Multi-service stack</title>
</head>
<body>
  <h1>Multi-service stack</h1>
  <ul>
    <?php foreach ($checks as $line): ?>
      <li><?php echo htmlspecialchars($line, ENT_QUOTES, 'UTF-8'); ?></li>
    <?php endforeach; ?>
  </ul>
</body>
</html>
