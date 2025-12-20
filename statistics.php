<?php
session_start();

// 로그인 확인
if (!isset($_SESSION['admin_logged_in']) || $_SESSION['admin_logged_in'] !== true) {
    header('Location: admin.php');
    exit;
}

// 설문지 데이터 읽기
$surveyFile = 'survey.json';
if (!file_exists($surveyFile)) {
    die('설문지 파일을 찾을 수 없습니다.');
}
$surveyData = json_decode(file_get_contents($surveyFile), true);

// result 폴더의 모든 응답 파일 읽기
$resultsDir = 'result';
$allResponses = [];
$totalResponses = 0;

if (is_dir($resultsDir)) {
    $files = glob($resultsDir . '/response_*.json');
    $totalResponses = count($files);
    
    foreach ($files as $file) {
        $data = json_decode(file_get_contents($file), true);
        if ($data) {
            $allResponses[] = $data;
        }
    }
}

// 통계 계산
$questionStats = [];
$categoryStats = [];
$totalScoreSum = 0;
$totalQuestionsAnswered = 0;

foreach ($allResponses as $response) {
    $totalScoreSum += $response['total_score'] ?? 0;
    $totalQuestionsAnswered += $response['total_questions'] ?? 0;
    
    // 카테고리별 통계
    if (isset($response['category_scores'])) {
        foreach ($response['category_scores'] as $category => $scores) {
            if (!isset($categoryStats[$category])) {
                $categoryStats[$category] = ['total' => 0, 'count' => 0];
            }
            $categoryStats[$category]['total'] += $scores['average'];
            $categoryStats[$category]['count']++;
        }
    }
    
    // 문항별 통계
    if (isset($response['responses'])) {
        foreach ($response['responses'] as $questionId => $answerData) {
            if (!isset($questionStats[$questionId])) {
                $questionStats[$questionId] = [
                    'question' => $answerData['question'],
                    'category' => $answerData['category'],
                    'answers' => [1 => 0, 2 => 0, 3 => 0, 4 => 0, 5 => 0],
                    'total' => 0,
                    'count' => 0
                ];
            }
            $answer = $answerData['answer'];
            $questionStats[$questionId]['answers'][$answer]++;
            $questionStats[$questionId]['total'] += $answer;
            $questionStats[$questionId]['count']++;
        }
    }
}

// 주관식 응답 수집
$textResponsesByQuestion = [];
foreach ($allResponses as $response) {
    if (isset($response['text_responses'])) {
        foreach ($response['text_responses'] as $questionId => $textData) {
            if (!isset($textResponsesByQuestion[$questionId])) {
                $textResponsesByQuestion[$questionId] = [
                    'question' => $textData['question'],
                    'category' => $textData['category'],
                    'responses' => []
                ];
            }
            $textResponsesByQuestion[$questionId]['responses'][] = [
                'answer' => $textData['answer'],
                'timestamp' => $response['timestamp'] ?? 'unknown'
            ];
        }
    }
}

// 전체 평균 계산
$overallAverage = $totalResponses > 0 ? round($totalScoreSum / $totalResponses, 2) : 0;
$averagePerQuestion = $totalQuestionsAnswered > 0 ? round($totalScoreSum / $totalQuestionsAnswered, 2) : 0;
?>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>응답 통계 - 관리자</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: {
                            50: '#f0f4ff',
                            100: '#e0e9ff',
                            500: '#667eea',
                            600: '#5568d3',
                            700: '#4c5dbb',
                        },
                        secondary: {
                            500: '#764ba2',
                            600: '#6a3d8f',
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-500 min-h-screen py-8 px-4 md:px-8 font-sans">
    <div class="max-w-7xl mx-auto">
        <!-- 헤더 -->
        <div class="bg-white rounded-2xl shadow-2xl overflow-hidden mb-6">
            <div class="bg-gradient-to-r from-primary-500 to-secondary-500 text-white px-8 py-6">
                <div class="flex items-center justify-between">
                    <div>
                        <h1 class="text-3xl md:text-4xl font-bold mb-2">응답 통계</h1>
                        <p class="text-primary-100">식물성 케톤식 영양강좌 수요조사 분석</p>
                    </div>
                    <div class="text-right">
                        <p class="text-sm text-primary-100">관리자: <?php echo htmlspecialchars($_SESSION['admin_username']); ?></p>
                        <a href="admin_logout.php" class="text-sm text-white hover:text-primary-100 underline mt-1 inline-block">로그아웃</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- 전체 통계 카드 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-600 text-sm font-medium mb-1">총 응답 수</p>
                        <p class="text-3xl font-bold text-gray-800"><?php echo number_format($totalResponses); ?></p>
                    </div>
                    <div class="bg-blue-100 rounded-full p-4">
                        <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.196-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.196-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                        </svg>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-600 text-sm font-medium mb-1">전체 평균 점수</p>
                        <p class="text-3xl font-bold text-gray-800"><?php echo $overallAverage; ?></p>
                        <p class="text-xs text-gray-500 mt-1">응답당 평균</p>
                    </div>
                    <div class="bg-green-100 rounded-full p-4">
                        <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                        </svg>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-600 text-sm font-medium mb-1">문항당 평균</p>
                        <p class="text-3xl font-bold text-gray-800"><?php echo $averagePerQuestion; ?></p>
                        <p class="text-xs text-gray-500 mt-1">전체 문항 평균</p>
                    </div>
                    <div class="bg-purple-100 rounded-full p-4">
                        <svg class="w-8 h-8 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- 카테고리별 통계 -->
        <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                <svg class="w-6 h-6 mr-2 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
                카테고리별 평균 점수
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <?php
                ksort($categoryStats);
                foreach ($categoryStats as $category => $data) {
                    $avg = $data['count'] > 0 ? round($data['total'] / $data['count'], 2) : 0;
                    $percentage = ($avg / 5) * 100;
                ?>
                <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="font-semibold text-gray-700"><?php echo htmlspecialchars($category); ?></h3>
                        <span class="bg-gradient-to-r from-primary-500 to-secondary-500 text-white px-3 py-1 rounded-full text-sm font-bold"><?php echo $avg; ?>점</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full" style="width: <?php echo $percentage; ?>%"></div>
                    </div>
                    <p class="text-xs text-gray-500 mt-1">응답 수: <?php echo $data['count']; ?>개</p>
                </div>
                <?php } ?>
            </div>
        </div>

        <!-- 문항별 상세 통계 -->
        <div class="bg-white rounded-xl shadow-lg p-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                <svg class="w-6 h-6 mr-2 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
                문항별 상세 통계
            </h2>
            
            <div class="space-y-6">
                <?php
                ksort($questionStats);
                foreach ($questionStats as $questionId => $stats) {
                    $avg = $stats['count'] > 0 ? round($stats['total'] / $stats['count'], 2) : 0;
                    $maxCount = max($stats['answers']);
                ?>
                <div class="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
                    <div class="flex items-start justify-between mb-4">
                        <div class="flex-1">
                            <div class="flex items-center mb-2">
                                <span class="bg-primary-500 text-white text-xs font-bold px-2 py-1 rounded mr-2">Q<?php echo $questionId; ?></span>
                                <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded"><?php echo htmlspecialchars($stats['category']); ?></span>
                            </div>
                            <h3 class="text-base font-medium text-gray-800 mb-2"><?php echo htmlspecialchars($stats['question']); ?></h3>
                            <div class="flex items-center space-x-4 text-sm">
                                <span class="text-gray-600">평균: <span class="font-bold text-primary-600"><?php echo $avg; ?>점</span></span>
                                <span class="text-gray-600">응답: <span class="font-bold"><?php echo $stats['count']; ?>개</span></span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 답변 분포 -->
                    <div class="space-y-2">
                        <?php for ($i = 1; $i <= 5; $i++): 
                            $count = $stats['answers'][$i];
                            $percentage = $stats['count'] > 0 ? round(($count / $stats['count']) * 100, 1) : 0;
                            $barWidth = $stats['count'] > 0 ? ($count / $maxCount) * 100 : 0;
                        ?>
                        <div class="flex items-center space-x-3">
                            <div class="w-8 text-sm font-medium text-gray-600"><?php echo $i; ?>.</div>
                            <div class="flex-1">
                                <div class="flex items-center justify-between mb-1">
                                    <span class="text-xs text-gray-600"><?php echo htmlspecialchars($surveyData['scale'][(string)$i]); ?></span>
                                    <span class="text-xs font-semibold text-gray-700"><?php echo $count; ?> (<?php echo $percentage; ?>%)</span>
                                </div>
                                <div class="w-full bg-gray-200 rounded-full h-2">
                                    <div class="bg-gradient-to-r from-primary-400 to-primary-600 h-2 rounded-full transition-all duration-300" style="width: <?php echo $barWidth; ?>%"></div>
                                </div>
                            </div>
                        </div>
                        <?php endfor; ?>
                    </div>
                </div>
                <?php } ?>
            </div>
        </div>

        <!-- 주관식 응답 -->
        <?php if (!empty($textResponsesByQuestion)): ?>
        <div class="bg-white rounded-xl shadow-lg p-6 mt-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                <svg class="w-6 h-6 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
                주관식 응답
            </h2>
            
            <div class="space-y-6">
                <?php
                ksort($textResponsesByQuestion);
                foreach ($textResponsesByQuestion as $questionId => $textData):
                    $responseCount = count($textData['responses']);
                ?>
                <div class="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow bg-gradient-to-br from-green-50 to-emerald-50">
                    <div class="flex items-start justify-between mb-4">
                        <div class="flex-1">
                            <div class="flex items-center mb-2 flex-wrap gap-2">
                                <span class="bg-green-500 text-white text-xs font-bold px-2 py-1 rounded mr-2">Q<?php echo $questionId; ?></span>
                                <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded"><?php echo htmlspecialchars($textData['category']); ?></span>
                                <span class="text-xs text-gray-600 bg-white px-2 py-1 rounded border">응답 수: <?php echo $responseCount; ?>개</span>
                            </div>
                            <h3 class="text-base font-medium text-gray-800 mb-3"><?php echo htmlspecialchars($textData['question']); ?></h3>
                        </div>
                    </div>
                    
                    <!-- 주관식 응답 목록 -->
                    <div class="space-y-3">
                        <?php foreach ($textData['responses'] as $index => $textResponse): ?>
                        <div class="bg-white rounded-lg p-4 border-l-4 border-green-400 shadow-sm">
                            <div class="flex items-start justify-between mb-2">
                                <span class="text-xs text-gray-500 font-medium">응답 #<?php echo $index + 1; ?></span>
                                <span class="text-xs text-gray-400"><?php echo htmlspecialchars($textResponse['timestamp']); ?></span>
                            </div>
                            <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap"><?php echo nl2br(htmlspecialchars($textResponse['answer'])); ?></p>
                        </div>
                        <?php endforeach; ?>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endif; ?>

        <!-- 뒤로가기 버튼 -->
        <div class="mt-6 text-center">
            <a href="index.php" class="inline-block bg-white hover:bg-gray-100 text-gray-800 font-semibold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200">
                <span class="flex items-center justify-center space-x-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                    </svg>
                    <span>설문지로 돌아가기</span>
                </span>
            </a>
        </div>
    </div>
</body>
</html>

