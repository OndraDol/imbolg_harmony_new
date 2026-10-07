<?php
declare(strict_types=1);
// Copy only to private/config.php outside DocumentRoot. No usable credentials.
return [
    'transport' => 'disabled',
    'from' => '',
    'from_verified' => false,
    'rate_key' => '', // Random secret, at least 32 bytes. Never publish it.
    'rate_limit' => 5,
    'rate_window' => 600,
    'smtp' => [
        'enabled' => false,
        'host' => '',
        'port' => 587,
        'encryption' => 'tls', // tls (STARTTLS) or ssl; no plaintext SMTP.
        'username' => '',
        'password' => '',
    ],
];
