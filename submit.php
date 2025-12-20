<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>설문 제출 완료</title>
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
<body class="bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-500 min-h-screen py-8 px-4 md:px-8 font-sans flex items-center justify-center">
    <div class="max-w-2xl w-full bg-white rounded-2xl shadow-2xl overflow-hidden">
        <?php
        // POST 데이터 확인
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            echo '<div class="p-8 text-center">';
            echo '<div class="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg mb-6">';
            echo '<div class="flex items-center mb-3">';
            echo '<svg class="w-8 h-8 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
            echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>';
            echo '</svg>';
            echo '<h1 class="text-2xl font-bold text-red-700">오류</h1>';
            echo '</div>';
            echo '<p class="text-red-600">잘못된 접근입니다.</p>';
            echo '</div>';
            echo '<a href="index.php" class="inline-block bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200">설문지로 돌아가기</a>';
            echo '</div>';
            exit;
        }
        
        // 설문지 JSON 파일 읽기
        $jsonFile = 'survey.json';
        if (!file_exists($jsonFile)) {
            die('설문지 파일을 찾을 수 없습니다.');
        }
        
        $jsonData = file_get_contents($jsonFile);
        $survey = json_decode($jsonData, true);
        
        // 응답 데이터 수집
        $responses = [];
        $textResponses = [];
        $totalScore = 0;
        $answeredCount = 0;
        $categoryScores = [];
        
        foreach ($survey['questions'] as $question) {
            $questionId = $question['id'];
            $isTextQuestion = isset($question['type']) && $question['type'] === 'text';
            
            if ($isTextQuestion) {
                // 주관식 질문 처리
                $textFieldName = 'question_text_' . $questionId;
                if (isset($_POST[$textFieldName])) {
                    $textAnswer = trim($_POST[$textFieldName]);
                    if (!empty($textAnswer)) {
                        $textResponses[$questionId] = [
                            'question' => $question['question'],
                            'category' => $question['category'],
                            'answer' => mb_substr($textAnswer, 0, 500), // 최대 500자
                            'type' => 'text'
                        ];
                        $answeredCount++;
                    }
                }
            } else {
                // 객관식 질문 처리
                $fieldName = 'question_' . $questionId;
                
                if (isset($_POST[$fieldName])) {
                    $answer = intval($_POST[$fieldName]);
                    if ($answer >= 1 && $answer <= 5) {
                        $responses[$questionId] = [
                            'question' => $question['question'],
                            'category' => $question['category'],
                            'answer' => $answer,
                            'answer_label' => $survey['scale'][(string)$answer],
                            'type' => 'radio'
                        ];
                        
                        $totalScore += $answer;
                        $answeredCount++;
                        
                        // 카테고리별 점수 집계
                        $category = $question['category'];
                        if (!isset($categoryScores[$category])) {
                            $categoryScores[$category] = ['total' => 0, 'count' => 0];
                        }
                        $categoryScores[$category]['total'] += $answer;
                        $categoryScores[$category]['count']++;
                    }
                }
            }
        }
        
        // 모든 문항에 답변했는지 확인 (주관식은 선택사항으로 처리)
        $requiredQuestions = array_filter($survey['questions'], function($q) {
            return !isset($q['type']) || $q['type'] !== 'text';
        });
        $requiredCount = count($requiredQuestions);
        $answeredRequired = 0;
        foreach ($requiredQuestions as $q) {
            $fieldName = 'question_' . $q['id'];
            if (isset($_POST[$fieldName])) {
                $answeredRequired++;
            }
        }
        
        if ($answeredRequired < $requiredCount) {
            echo '<div class="p-8 text-center">';
            echo '<div class="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg mb-6">';
            echo '<div class="flex items-center mb-3">';
            echo '<svg class="w-8 h-8 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
            echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>';
            echo '</svg>';
            echo '<h1 class="text-2xl font-bold text-red-700">오류</h1>';
            echo '</div>';
            echo '<p class="text-red-600">모든 문항에 답변해주세요.</p>';
            echo '</div>';
            echo '<a href="index.php" class="inline-block bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200">설문지로 돌아가기</a>';
            echo '</div>';
            exit;
        }
        
        // 응답 데이터 저장
        $responseData = [
            'timestamp' => date('Y-m-d H:i:s'),
            'ip_address' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
            'total_questions' => $answeredCount,
            'total_score' => $totalScore,
            'average_score' => $answeredCount > 0 ? round($totalScore / $answeredCount, 2) : 0,
            'category_scores' => [],
            'responses' => $responses,
            'text_responses' => $textResponses
        ];
        
        // 카테고리별 평균 점수 계산
        foreach ($categoryScores as $category => $data) {
            $responseData['category_scores'][$category] = [
                'total' => $data['total'],
                'count' => $data['count'],
                'average' => round($data['total'] / $data['count'], 2)
            ];
        }
        
        // 결과 저장 디렉토리 생성 (result 폴더)
        $resultsDir = 'result';
        if (!is_dir($resultsDir)) {
            if (!mkdir($resultsDir, 0755, true)) {
                echo '<div class="p-8 text-center">';
                echo '<div class="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg mb-6">';
                echo '<div class="flex items-center mb-3">';
                echo '<svg class="w-8 h-8 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
                echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>';
                echo '</svg>';
                echo '<h1 class="text-2xl font-bold text-red-700">오류</h1>';
                echo '</div>';
                echo '<p class="text-red-600">result 폴더 생성에 실패했습니다. 폴더 권한을 확인해주세요.</p>';
                echo '</div>';
                echo '<a href="index.php" class="inline-block bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200">설문지로 돌아가기</a>';
                echo '</div>';
                exit;
            }
        }
        
        // 파일명 생성 (타임스탬프 기반)
        $filename = $resultsDir . '/response_' . date('Ymd_His') . '_' . uniqid() . '.json';
        
        // JSON 파일로 저장
        $jsonContent = json_encode($responseData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        $saved = file_put_contents($filename, $jsonContent);
        
        if ($saved === false) {
            echo '<div class="p-8 text-center">';
            echo '<div class="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg mb-6">';
            echo '<div class="flex items-center mb-3">';
            echo '<svg class="w-8 h-8 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
            echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>';
            echo '</svg>';
            echo '<h1 class="text-2xl font-bold text-red-700">오류</h1>';
            echo '</div>';
            echo '<p class="text-red-600">응답 저장 중 오류가 발생했습니다. 파일 쓰기 권한을 확인해주세요.</p>';
            echo '</div>';
            echo '<a href="index.php" class="inline-block bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200">설문지로 돌아가기</a>';
            echo '</div>';
            exit;
        }
        
        // 성공 메시지 표시
        echo '<div class="bg-gradient-to-r from-green-400 to-emerald-500 text-white px-8 py-10 text-center">';
        echo '<div class="w-20 h-20 mx-auto mb-4 bg-white rounded-full flex items-center justify-center shadow-lg">';
        echo '<svg class="w-12 h-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
        echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>';
        echo '</svg>';
        echo '</div>';
        echo '<h1 class="text-3xl md:text-4xl font-bold mb-3">설문 제출 완료</h1>';
        echo '<p class="text-green-50 text-base md:text-lg">소중한 의견 감사합니다!</p>';
        echo '<p class="text-green-50 text-sm md:text-base mt-1">설문 응답이 성공적으로 저장되었습니다.</p>';
        echo '<div class="mt-4 bg-white bg-opacity-20 rounded-lg p-3 text-sm">';
        echo '<p class="text-green-50">📁 저장 위치: <span class="font-semibold">result/' . htmlspecialchars(basename($filename)) . '</span></p>';
        echo '</div>';
        echo '</div>';
        
        echo '<div class="p-8">';
        
        // 요약 정보 표시
        echo '<div class="bg-gradient-to-br from-gray-50 to-primary-50 rounded-xl p-6 mb-6 shadow-md border border-gray-200">';
        echo '<h3 class="text-xl font-bold text-primary-600 mb-5 flex items-center">';
        echo '<svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
        echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>';
        echo '</svg>응답 요약</h3>';
        echo '<div class="space-y-3">';
        echo '<div class="flex justify-between items-center py-3 border-b border-gray-200 last:border-0">';
        echo '<span class="text-gray-600 font-medium">총 문항 수</span>';
        echo '<span class="text-gray-800 font-bold text-lg">' . $answeredCount . '개</span>';
        echo '</div>';
        echo '<div class="flex justify-between items-center py-3 border-b border-gray-200 last:border-0">';
        echo '<span class="text-gray-600 font-medium">총점</span>';
        echo '<span class="text-primary-600 font-bold text-lg">' . $totalScore . '점</span>';
        echo '</div>';
        echo '<div class="flex justify-between items-center py-3 border-b border-gray-200 last:border-0">';
        echo '<span class="text-gray-600 font-medium">평균 점수</span>';
        echo '<span class="bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent font-bold text-xl">' . round($totalScore / $answeredCount, 2) . '점</span>';
        echo '</div>';
        echo '<div class="flex justify-between items-center py-3 border-b border-gray-200 last:border-0">';
        echo '<span class="text-gray-600 font-medium">제출 시간</span>';
        echo '<span class="text-gray-800 font-semibold">' . date('Y-m-d H:i:s') . '</span>';
        echo '</div>';
        echo '<div class="flex justify-between items-center py-3 border-b border-gray-200 last:border-0">';
        echo '<span class="text-gray-600 font-medium">저장 파일</span>';
        echo '<span class="text-gray-800 font-semibold text-sm break-all">' . htmlspecialchars(basename($filename)) . '</span>';
        echo '</div>';
        echo '</div>';
        echo '</div>';
        
        // 카테고리별 평균 점수
        if (!empty($categoryScores)) {
            echo '<div class="bg-gradient-to-br from-gray-50 to-purple-50 rounded-xl p-6 mb-6 shadow-md border border-gray-200">';
            echo '<h3 class="text-xl font-bold text-primary-600 mb-5 flex items-center">';
            echo '<svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
            echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>';
            echo '</svg>카테고리별 평균 점수</h3>';
            echo '<div class="space-y-3">';
            foreach ($categoryScores as $category => $data) {
                $avg = round($data['total'] / $data['count'], 2);
                echo '<div class="flex justify-between items-center py-3 border-b border-gray-200 last:border-0">';
                echo '<span class="text-gray-700 font-medium">' . htmlspecialchars($category) . '</span>';
                echo '<span class="bg-gradient-to-r from-primary-500 to-secondary-500 text-white px-4 py-1 rounded-full font-bold text-sm">' . $avg . '점</span>';
                echo '</div>';
            }
            echo '</div>';
            echo '</div>';
        }
        
        // 버튼
        echo '<div class="flex flex-col sm:flex-row gap-4 justify-center pt-6 border-t border-gray-200">';
        echo '<a href="index.php" class="bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 text-center">';
        echo '<span class="flex items-center justify-center space-x-2">';
        echo '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
        echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>';
        echo '</svg>';
        echo '<span>다시 설문하기</span>';
        echo '</span>';
        echo '</a>';
        echo '<a href="view_results.php" class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 text-center">';
        echo '<span class="flex items-center justify-center space-x-2">';
        echo '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
        echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>';
        echo '</svg>';
        echo '<span>결과 보기</span>';
        echo '</span>';
        echo '</a>';
        echo '</div>';
        echo '</div>'; // p-8 닫기
        ?>
    </div>
</body>
</html>

