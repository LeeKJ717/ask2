<?php
// 간단한 로그인 처리 (실제 운영 시에는 보안 강화 필요)
session_start();

// 기본 관리자 계정 (실제 운영 시에는 데이터베이스 사용 권장)
$admin_username = 'admin';
$admin_password = '1234'; // 실제 운영 시에는 해시된 비밀번호 사용

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    if ($username === $admin_username && $password === $admin_password) {
        $_SESSION['admin_logged_in'] = true;
        $_SESSION['admin_username'] = $username;
        header('Location: statistics.php');
        exit;
    } else {
        header('Location: admin.php?error=1');
        exit;
    }
} else {
    header('Location: admin.php');
    exit;
}
?>

