<?php
declare(strict_types=1);
ini_set('display_errors', '0');
header('Content-Type: text/html; charset=UTF-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
header("Content-Security-Policy: default-src 'none'; style-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'");
try {
    require dirname(__DIR__, 2) . '/private/app/bootstrap.php';
} catch (Throwable $error) {
    http_response_code(503);
    echo '<!doctype html><html lang="cs"><meta charset="utf-8"><title>Formulář není dostupný</title><p>Zprávu se nepodařilo předat. Zkuste to prosím později.</p><a href="/">Zpět na úvod</a></html>';
}
