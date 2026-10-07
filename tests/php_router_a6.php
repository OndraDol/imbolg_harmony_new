<?php
// Local PHP server only: emulate the release ErrorDocument directive.
// This file is never part of dist/release or a production endpoint.
declare(strict_types=1);
$root = realpath($_SERVER['DOCUMENT_ROOT']);
$url = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$file = realpath($root . '/' . rawurldecode(is_string($url) ? $url : '/'));
if ($file !== false && ($file === $root || str_starts_with($file, $root . DIRECTORY_SEPARATOR))) {
    if (is_file($file) || (is_dir($file) && is_file($file . '/index.html'))) {
        return false;
    }
}
http_response_code(404);
header('Content-Type: text/html; charset=UTF-8');
readfile($root . '/404.html');
