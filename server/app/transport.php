<?php
declare(strict_types=1);
namespace Imbolg;
use PHPMailer\PHPMailer\PHPMailer;

const RECIPIENT = 'kralovamarket@seznam.cz';

function configuration(array $config, string $peer): array
{
    if (!is_string($config['rate_key'] ?? null) || strlen($config['rate_key']) < 32) {
        throw new \RuntimeException('Missing rate secret');
    }
    foreach (['rate_limit' => [1, 100], 'rate_window' => [1, 86400]] as $key => [$min, $max]) {
        if (!is_int($config[$key] ?? null) || $config[$key] < $min || $config[$key] > $max) {
            throw new \RuntimeException('Invalid rate configuration');
        }
    }
    $from = $config['from'] ?? '';
    if (!is_string($from) || !filter_var($from, FILTER_VALIDATE_EMAIL) || preg_match('/[\x00-\x20\x7F]/', $from)) {
        throw new \RuntimeException('Invalid sender');
    }
    if (($config['transport'] ?? '') === 'capture') {
        if (getenv('IMBOLG_LOCAL_CAPTURE') !== '1' || !in_array($peer, ['127.0.0.1', '::1'], true)
            || !str_ends_with($from, '@example.invalid')) {
            throw new \RuntimeException('Capture is local only');
        }
        return $config;
    }
    $seznamFrom = $from === 'imbolg.harmony.formular@seznam.cz';
    if (($config['transport'] ?? '') !== 'smtp' || ($config['from_verified'] ?? false) !== true
        || (!str_ends_with(strtolower($from), '@imbolg-harmony.cz') && !$seznamFrom)) {
        throw new \RuntimeException('Production disabled');
    }
    $smtp = $config['smtp'] ?? [];
    if (!is_array($smtp) || ($smtp['enabled'] ?? false) !== true
        || !is_string($smtp['host'] ?? null) || !preg_match('/\A[a-zA-Z0-9][a-zA-Z0-9.-]{0,252}\z/', $smtp['host'])
        || !is_int($smtp['port'] ?? null) || !in_array($smtp['port'], [465, 587], true)
        || !in_array($smtp['encryption'] ?? '', ['tls', 'ssl'], true)) {
        throw new \RuntimeException('Invalid SMTP configuration');
    }
    foreach (['username', 'password'] as $key) {
        if (!is_string($smtp[$key] ?? null) || $smtp[$key] === '' || preg_match('/[\x00-\x1F\x7F]/', $smtp[$key])) {
            throw new \RuntimeException('Missing SMTP credentials');
        }
    }
    if ($seznamFrom && ($smtp['username'] !== $from || $smtp['host'] !== 'smtp.seznam.cz'
        || $smtp['port'] !== 465 || $smtp['encryption'] !== 'ssl')) {
        throw new \RuntimeException('Invalid Seznam sender configuration');
    }
    return $config;
}

function message(array $values, array $config, ?PHPMailer $mailer = null): PHPMailer
{
    $mailer ??= new PHPMailer(true);
    $mailer->CharSet = 'UTF-8';
    $mailer->setFrom($config['from'], 'Imbolg Harmony');
    $mailer->addAddress(RECIPIENT);
    $mailer->addReplyTo($values['email'], $values['name']);
    $mailer->Subject = 'Zpráva z kontaktního formuláře Imbolg Harmony';
    $mailer->isHTML(false);
    $mailer->Body = 'Jméno: ' . $values['name'] . "\nE-mail: " . $values['email'] . "\n\n" . $values['message'];
    return $mailer;
}

function deliver(PHPMailer $mailer, array $config, string $private): string
{
    if ($config['transport'] === 'capture') {
        // Also guard the delivery boundary; never substitute mail()/sendmail().
        if (getenv('IMBOLG_LOCAL_CAPTURE') !== '1') { throw new \RuntimeException('Capture disabled'); }
        if (!$mailer->preSend()) { throw new \RuntimeException('MIME failed'); }
        $dir = $private . '/var/capture';
        if (!is_dir($dir) && !mkdir($dir, 0700, true) && !is_dir($dir)) { throw new \RuntimeException('Capture unavailable'); }
        $path = $dir . '/' . bin2hex(random_bytes(16)) . '.eml';
        if (file_put_contents($path, $mailer->getSentMIMEMessage(), LOCK_EX) === false) {
            throw new \RuntimeException('Capture write failed');
        }
        return 'Lokální test: zpráva byla zachycena, žádný e-mail nebyl odeslán.';
    }
    if ($config['transport'] !== 'smtp') { throw new \RuntimeException('Transport disabled'); }
    $smtp = $config['smtp'];
    $mailer->isSMTP();
    $mailer->Host = $smtp['host'];
    $mailer->Port = $smtp['port'];
    $mailer->SMTPSecure = $smtp['encryption'];
    $mailer->SMTPAuth = true;
    $mailer->Username = $smtp['username'];
    $mailer->Password = $smtp['password'];
    $mailer->SMTPDebug = 0;
    $mailer->Timeout = 10;
    if (!$mailer->send()) { throw new \RuntimeException('SMTP rejected'); }
    return 'Zpráva byla předána k odeslání. Doručení do schránky zatím není potvrzené.';
}
