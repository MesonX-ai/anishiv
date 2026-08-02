<?php
declare(strict_types=1);

$uri = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
$uri = is_string($uri) ? $uri : '/';

if ($uri === '/' || $uri === '') {
    readfile(__DIR__ . '/index.htm');
    return true;
}

if ($uri === '/contact') {
    include __DIR__ . '/contact_submit.php';
    return true;
}

$target = __DIR__ . $uri;
if (is_file($target)) {
    return false;
}

http_response_code(404);
header('Content-Type: text/plain; charset=UTF-8');
echo "Not Found\n";
return true;
