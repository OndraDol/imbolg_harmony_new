<?php
declare(strict_types=1);
namespace Imbolg;

function validate(array $input): array
{
    $values = ['name' => '', 'email' => '', 'message' => '', 'website' => ''];
    $errors = [];
    foreach ($values as $field => $_) {
        $value = $input[$field] ?? '';
        if (!is_string($value)) {
            $errors[$field] = 'Pole musí obsahovat text.';
            continue;
        }
        $limit = ['name' => 800, 'email' => 254, 'message' => 40000, 'website' => 800][$field];
        if (strlen($value) > $limit || !preg_match('//u', $value)) {
            $errors[$field] = 'Text je příliš dlouhý nebo má neplatné kódování.';
            continue;
        }
        $controls = $field === 'message' ? '/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/' : '/[\x00-\x1F\x7F]/';
        if (preg_match($controls, $value)) {
            $errors[$field] = 'Pole obsahuje nepovolené řídicí znaky.';
            continue;
        }
        preg_match_all('/./us', $value, $chars);
        if (count($chars[0]) > ['name' => 200, 'email' => 254, 'message' => 10000, 'website' => 200][$field]) {
            $errors[$field] = 'Text je příliš dlouhý.';
            continue;
        }
        $values[$field] = trim($value);
    }
    foreach (['name', 'email'] as $field) {
        if (!isset($errors[$field]) && $values[$field] === '') {
            $errors[$field] = 'Vyplňte prosím toto pole.';
        }
    }
    if (!isset($errors['email']) && !filter_var($values['email'], FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'Zadejte platnou e-mailovou adresu.';
    }
    return [$values, $errors];
}

function render(int $status, string $summary, array $values = [], array $errors = [], bool $form = true): void
{
    http_response_code($status);
    $escape = static fn(string $s): string => htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    $html = '';
    if ($form) {
        $template = file_get_contents(__DIR__ . '/templates/contact-form.html');
        if ($template === false) { throw new \RuntimeException('Missing form template'); }
        $replacements = ['__SUMMARY__' => $escape($summary)];
        foreach (['name', 'email', 'message'] as $field) {
            $prefix = '__' . strtoupper($field);
            $replacements[$prefix . '__'] = $escape($values[$field] ?? '');
            $replacements[$prefix . '_ERROR__'] = $escape($errors[$field] ?? '');
            $replacements[$prefix . '_INVALID__'] = isset($errors[$field]) ? 'aria-invalid="true"' : '';
        }
        $html = strtr($template, $replacements);
    } else {
        $html = '<p role="status">' . $escape($summary) . '</p>';
    }
    echo '<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kontaktní formulář | Imbolg Harmony</title><link rel="stylesheet" href="/assets/css/site.css"></head><body><main class="site-main"><h1>Kontaktní formulář</h1>' . $html . '<p><a href="/">Zpět na úvod</a></p></main></body></html>';
}
