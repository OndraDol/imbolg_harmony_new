<?php
declare(strict_types=1);
namespace Imbolg;
require __DIR__ . '/form.php';
require __DIR__ . '/rate.php';
require __DIR__ . '/transport.php';

$private = dirname(__DIR__);
$values = [];
try {
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        header('Allow: POST');
        render(405, 'Formulář přijímá pouze odeslání metodou POST.');
        return;
    }
    if ((int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 65536) {
        render(413, 'Odeslaná data jsou příliš velká. Zkraťte prosím text.');
        return;
    }
    if (strtolower(trim(explode(';', $_SERVER['CONTENT_TYPE'] ?? '')[0])) !== 'application/x-www-form-urlencoded') {
        render(415, 'Formulář nepřijímá přílohy ani tento formát dat.');
        return;
    }
    // Read at most the allowed bytes, even if Content-Length is absent or false.
    $stream = fopen('php://input', 'rb');
    $raw = stream_get_contents($stream, 65537);
    fclose($stream);
    if ($raw === false || strlen($raw) > 65536) {
        render(413, 'Odeslaná data jsou příliš velká.');
        return;
    }
    parse_str($raw, $input);
    [$values, $errors] = validate($input);
    require $private . '/vendor/autoload.php';
    $config = require $private . '/config.php';
    if (!is_array($config)) { throw new \RuntimeException('Invalid configuration'); }
    $peer = $_SERVER['REMOTE_ADDR'] ?? '';
    $config = configuration($config, $peer);
    // REMOTE_ADDR only; X-Forwarded-For is deliberately ignored.
    if (!rateAllowed($private . '/var', $peer, $config['rate_key'], $config['rate_limit'], $config['rate_window'])) {
        header('Retry-After: ' . $config['rate_window']);
        render(429, 'Příliš mnoho pokusů. Vyčkejte prosím a zkuste to později.', $values);
        return;
    }
    if (isset($errors['website']) || $values['website'] !== '') {
        render(422, 'Požadavek byl odmítnut ochranou formuláře.', $values);
        return;
    }
    if ($errors !== []) {
        render(422, 'Zkontrolujte prosím označená pole.', $values, $errors);
        return;
    }
    $summary = deliver(message($values, $config), $config, $private);
    render(200, $summary, [], [], false);
} catch (\Throwable $error) {
    // No exception details, credentials or message contents in public output/logs.
    render(503, 'Zprávu se nepodařilo předat. Zkuste to prosím později.', $values);
}
