<?php
declare(strict_types=1);
namespace Imbolg;

// One flock-protected state file; no visitor text, mail address or raw IP stored.
function rateAllowed(string $dir, string $ip, string $secret, int $limit, int $window, ?int $now = null): bool
{
    $now ??= time();
    if (!is_dir($dir) && !mkdir($dir, 0700, true) && !is_dir($dir)) {
        throw new \RuntimeException('Rate directory unavailable');
    }
    $handle = fopen($dir . '/rate.json', 'c+');
    if ($handle === false) { throw new \RuntimeException('Rate state unavailable'); }
    try {
        if (!flock($handle, LOCK_EX)) { throw new \RuntimeException('Rate lock unavailable'); }
        $raw = stream_get_contents($handle);
        $state = $raw === '' ? [] : json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
        if (!is_array($state)) { throw new \RuntimeException('Invalid rate state'); }
        foreach ($state as $key => $times) {
            if (!is_array($times)) { throw new \RuntimeException('Invalid rate bucket'); }
            $state[$key] = array_values(array_filter($times, static fn($t) => is_int($t) && $t > $now - $window));
            if ($state[$key] === []) { unset($state[$key]); }
        }
        $key = hash_hmac('sha256', $ip, $secret);
        $allowed = count($state[$key] ?? []) < $limit && (isset($state[$key]) || count($state) < 10000);
        if ($allowed) { $state[$key][] = $now; }
        $json = json_encode($state, JSON_THROW_ON_ERROR);
        rewind($handle);
        if (!ftruncate($handle, 0) || fwrite($handle, $json) !== strlen($json) || !fflush($handle)) {
            throw new \RuntimeException('Rate write failed');
        }
        return $allowed;
    } finally {
        flock($handle, LOCK_UN);
        fclose($handle);
    }
}
