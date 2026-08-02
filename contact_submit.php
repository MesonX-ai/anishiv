<?php
/*
 * Contact form handler for homepage submissions.
 *
 * Configure destination email with CONTACT_FORM_TO environment variable.
 */

declare(strict_types=1);

function respond_json(int $status, array $payload): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=UTF-8');
    echo json_encode($payload);
    exit;
}

function respond_html(int $status, string $message): void
{
    http_response_code($status);
    header('Content-Type: text/html; charset=UTF-8');
    echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Contact</title></head><body>';
    echo '<p>' . htmlspecialchars($message, ENT_QUOTES, 'UTF-8') . '</p>';
    echo '<p><a href="index.htm">Return to home page</a></p>';
    echo '</body></html>';
    exit;
}

function is_ajax_request(): bool
{
    $requestedWith = $_SERVER['HTTP_X_REQUESTED_WITH'] ?? '';
    if (strcasecmp($requestedWith, 'XMLHttpRequest') === 0) {
        return true;
    }

    $accept = $_SERVER['HTTP_ACCEPT'] ?? '';
    return strpos($accept, 'application/json') !== false;
}

function fail(int $status, string $message): void
{
    if (is_ajax_request()) {
        respond_json($status, ['ok' => false, 'message' => $message]);
    }
    respond_html($status, $message);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    fail(405, 'Method not allowed.');
}

$name = trim((string)($_POST['name'] ?? ''));
$email = trim((string)($_POST['email'] ?? ''));
$message = trim((string)($_POST['message'] ?? ($_POST['text'] ?? '')));
$honeypot = trim((string)($_POST['website'] ?? ''));

if ($honeypot !== '') {
    fail(400, 'Invalid submission.');
}

if ($name === '' || $email === '' || $message === '') {
    fail(422, 'Name, email, and message are required.');
}

if (strlen($name) > 120 || strlen($email) > 180 || strlen($message) > 5000) {
    fail(422, 'Submission is too long.');
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    fail(422, 'Please enter a valid email address.');
}

$recipient = getenv('CONTACT_FORM_TO');
if (!$recipient) {
    $recipient = 'shiva.dhanuskodi@mesonsoft.com';
}

$subject = 'New message from AniShiv homepage';
$bodyLines = [
    'You received a new homepage message.',
    '',
    'Name: ' . $name,
    'Email: ' . $email,
    '',
    'Message:',
    $message,
    '',
    'IP: ' . ($_SERVER['REMOTE_ADDR'] ?? 'unknown'),
    'User-Agent: ' . ($_SERVER['HTTP_USER_AGENT'] ?? 'unknown')
];
$body = implode("\n", $bodyLines);

$cleanEmail = str_replace(["\r", "\n"], '', $email);
$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'From: AniShiv Contact <no-reply@anishiv.com>',
    'Reply-To: ' . $cleanEmail,
    'X-Mailer: PHP/' . phpversion()
];

$mailSent = @mail($recipient, $subject, $body, implode("\r\n", $headers));

$logDir = __DIR__ . '/messages';
$logPath = $logDir . '/contact_messages.log';
$logged = false;

if (!is_dir($logDir)) {
    @mkdir($logDir, 0750, true);
}

$logRecord = [
    'timestamp' => gmdate('c'),
    'name' => $name,
    'email' => $email,
    'message' => $message,
    'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown',
    'mail_sent' => $mailSent
];

$encodedRecord = json_encode($logRecord, JSON_UNESCAPED_SLASHES);
if ($encodedRecord !== false) {
    $logged = @file_put_contents($logPath, $encodedRecord . PHP_EOL, FILE_APPEND | LOCK_EX) !== false;
}

if (!$mailSent && !$logged) {
    fail(500, 'Unable to deliver your message right now. Please try again later.');
}

$successMessage = 'Thanks for your message. We will get back to you soon.';
if (is_ajax_request()) {
    respond_json(200, ['ok' => true, 'message' => $successMessage]);
}
respond_html(200, $successMessage);
