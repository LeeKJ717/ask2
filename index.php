<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <meta name="description" content="식물성 케톤식 영양강좌 수요조사에 참여해주세요. 여러분의 소중한 의견을 기다립니다.">
    <title>식물성 케톤식 영양강좌 수요조사</title>
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
    <style>
        /* 모바일 터치 최적화 */
        @media (max-width: 768px) {
            input[type="radio"] {
                width: 24px !important;
                height: 24px !important;
                min-width: 24px;
                min-height: 24px;
            }
        }
        
        /* 스크롤 부드럽게 */
        html {
            scroll-behavior: smooth;
        }
        
        /* 진행률 표시 */
        .progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: linear-gradient(to right, #667eea, #764ba2);
            z-index: 1000;
            transition: width 0.3s ease;
        }
    </style>
</head>
<body class="bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-500 min-h-screen py-4 sm:py-8 px-3 sm:px-4 md:px-8 font-sans">
    <!-- 진행률 바 -->
    <div class="progress-bar" id="progressBar" style="width: 0%"></div>
    <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl overflow-hidden">
        <?php
        // JSON 파일 읽기
        $jsonFile = 'survey.json';
        if (!file_exists($jsonFile)) {
            die('설문지 파일을 찾을 수 없습니다.');
        }
        
        $jsonData = file_get_contents($jsonFile);
        $survey = json_decode($jsonData, true);
        
        if (!$survey) {
            die('설문지 파일을 읽을 수 없습니다.');
        }
        
        // 헤더 섹션
        echo '<div class="bg-gradient-to-r from-primary-500 to-secondary-500 text-white px-4 sm:px-8 py-6 sm:py-10 text-center">';
        echo '<h1 class="text-2xl sm:text-3xl md:text-4xl font-bold mb-2 sm:mb-3 leading-tight">' . htmlspecialchars($survey['title']) . '</h1>';
        echo '<p class="text-primary-100 text-xs sm:text-sm md:text-base leading-relaxed px-2">' . htmlspecialchars($survey['description']) . '</p>';
        echo '</div>';
        
        // 메인 컨텐츠 영역
        echo '<div class="p-4 sm:p-6 md:p-10">';
        
        // 척도 정보 출력
        echo '<div class="bg-gradient-to-r from-primary-50 to-purple-50 border-l-4 border-primary-500 rounded-lg p-4 sm:p-5 mb-6 sm:mb-8 shadow-sm">';
        echo '<h3 class="text-base sm:text-lg font-semibold text-gray-800 mb-3 sm:mb-4 flex items-center">';
        echo '<svg class="w-5 h-5 mr-2 text-primary-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
        echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>';
        echo '</svg>평가 척도</h3>';
        echo '<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2 sm:gap-3 md:gap-4">';
        foreach ($survey['scale'] as $num => $label) {
            echo '<div class="flex items-center space-x-2 bg-white px-3 sm:px-4 py-2 rounded-full shadow-sm border border-primary-100 text-sm sm:text-base">';
            echo '<span class="bg-gradient-to-r from-primary-500 to-secondary-500 text-white w-6 h-6 sm:w-7 sm:h-7 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">' . $num . '</span>';
            echo '<span class="text-xs sm:text-sm text-gray-700 font-medium">' . htmlspecialchars($label) . '</span>';
            echo '</div>';
        }
        echo '</div>';
        echo '</div>';
        
        // 카테고리별로 문항 그룹화
        $questionsByCategory = [];
        foreach ($survey['questions'] as $question) {
            $category = $question['category'];
            if (!isset($questionsByCategory[$category])) {
                $questionsByCategory[$category] = [];
            }
            $questionsByCategory[$category][] = $question;
        }
        
        // 폼 시작
        echo '<form method="POST" action="submit.php" id="surveyForm">';
        
        // 카테고리별로 출력
        foreach ($questionsByCategory as $category => $questions) {
            echo '<div class="mb-6 sm:mb-10 bg-gradient-to-br from-gray-50 to-primary-50 rounded-xl p-4 sm:p-6 shadow-md border border-gray-100">';
            echo '<div class="flex items-center mb-4 sm:mb-6 pb-3 sm:pb-4 border-b-2 border-primary-500">';
            echo '<div class="bg-gradient-to-r from-primary-500 to-secondary-500 text-white px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg mr-2 sm:mr-3 flex-shrink-0">';
            echo '<svg class="w-4 h-4 sm:w-5 sm:h-5 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
            echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>';
            echo '</svg>';
            echo '</div>';
            echo '<h2 class="text-lg sm:text-xl md:text-2xl font-bold text-primary-600 break-words">' . htmlspecialchars($category) . '</h2>';
            echo '</div>';
            
            foreach ($questions as $question) {
                $isTextQuestion = isset($question['type']) && $question['type'] === 'text';
                
                echo '<div class="mb-4 sm:mb-6 p-4 sm:p-5 bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">';
                echo '<div class="mb-3 sm:mb-4">';
                echo '<span class="inline-block bg-primary-500 text-white text-xs sm:text-sm font-bold px-2 sm:px-3 py-1 rounded-full mr-2 flex-shrink-0">Q' . $question['id'] . '</span>';
                if ($isTextQuestion) {
                    echo '<span class="inline-block bg-green-500 text-white text-xs font-bold px-2 py-0.5 rounded mr-2">주관식</span>';
                }
                echo '<span class="text-sm sm:text-base md:text-lg text-gray-800 font-medium leading-relaxed">' . htmlspecialchars($question['question']) . '</span>';
                echo '</div>';
                
                if ($isTextQuestion) {
                    // 주관식 질문 - 텍스트 입력 필드
                    echo '<div class="mt-4">';
                    echo '<textarea name="question_text_' . $question['id'] . '" id="question_text_' . $question['id'] . '" rows="4" maxlength="500" placeholder="의견을 자유롭게 작성해주세요..." class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition-all duration-200 resize-y text-sm sm:text-base" oninput="updateTextLength(this, \'text_count_' . $question['id'] . '\')"></textarea>';
                    echo '<div class="flex justify-between items-center mt-2">';
                    echo '<p class="text-xs text-gray-500">최대 500자까지 입력 가능합니다.</p>';
                    echo '<p class="text-xs text-gray-500"><span id="text_count_' . $question['id'] . '">0</span> / 500자</p>';
                    echo '</div>';
                    echo '</div>';
                } else {
                    // 객관식 질문 - 라디오 버튼
                    echo '<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2 sm:gap-3">';
                    for ($i = 1; $i <= 5; $i++) {
                        $scaleLabel = $survey['scale'][(string)$i];
                        $radioId = 'q' . $question['id'] . '_' . $i;
                        echo '<label for="' . $radioId . '" class="flex items-center space-x-2 sm:space-x-3 p-3 sm:p-4 rounded-lg border-2 border-gray-200 hover:border-primary-400 hover:bg-primary-50 active:bg-primary-100 cursor-pointer transition-all duration-200 group touch-manipulation">';
                        echo '<input type="radio" id="' . $radioId . '" name="question_' . $question['id'] . '" value="' . $i . '" required class="w-6 h-6 sm:w-5 sm:h-5 text-primary-500 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 cursor-pointer flex-shrink-0" onclick="updateProgress()">';
                        echo '<span class="text-sm sm:text-base text-gray-700 group-hover:text-primary-600 font-medium flex-1">';
                        echo '<span class="font-bold text-primary-500">' . $i . '.</span> <span class="hidden sm:inline">' . htmlspecialchars($scaleLabel) . '</span>';
                        echo '<span class="sm:hidden text-xs">' . htmlspecialchars(mb_substr($scaleLabel, 0, 8)) . '</span>';
                        echo '</span>';
                        echo '</label>';
                    }
                    echo '</div>';
                }
                echo '</div>';
            }
            
            echo '</div>';
        }
        
        // 제출 버튼
        echo '<div class="mt-6 sm:mt-10 pt-6 sm:pt-8 border-t-2 border-gray-200 text-center">';
        echo '<div class="mb-3 sm:mb-4 text-sm text-gray-600">';
        echo '<span id="progressText">0</span> / ' . count($survey['questions']) . ' 문항 완료';
        echo '</div>';
        echo '<button type="submit" class="w-full sm:w-auto bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white font-bold py-3 sm:py-4 px-8 sm:px-12 rounded-full text-base sm:text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-primary-300 active:scale-95 touch-manipulation">';
        echo '<span class="flex items-center justify-center space-x-2">';
        echo '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">';
        echo '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>';
        echo '</svg>';
        echo '<span>설문 제출하기</span>';
        echo '</span>';
        echo '</button>';
        echo '</div>';
        
        echo '</div>'; // 메인 컨텐츠 영역 닫기
        echo '</form>';
        ?>
        
        <!-- 관리자 페이지 링크 -->
        <div class="text-center py-3 sm:py-4 border-t border-gray-200 bg-gray-50">
            <a href="admin.php" class="text-xs text-gray-400 hover:text-gray-600 transition-colors duration-200">
                관리자 페이지
            </a>
        </div>
    </div>
    
    <script>
        // 총 문항 수 계산 (객관식만)
        const totalQuestions = <?php 
            $objectiveCount = 0;
            foreach ($survey['questions'] as $q) {
                if (!isset($q['type']) || $q['type'] !== 'text') {
                    $objectiveCount++;
                }
            }
            echo $objectiveCount;
        ?>;
        
        // 텍스트 길이 업데이트 함수
        function updateTextLength(textarea, countId) {
            const countElement = document.getElementById(countId);
            if (countElement) {
                countElement.textContent = textarea.value.length;
                if (textarea.value.length > 450) {
                    countElement.classList.add('text-orange-500', 'font-bold');
                } else {
                    countElement.classList.remove('text-orange-500', 'font-bold');
                }
            }
        }
        
        // 진행률 업데이트 함수
        function updateProgress() {
            const form = document.getElementById('surveyForm');
            const inputs = form.querySelectorAll('input[type="radio"]:checked');
            const answered = inputs.length;
            const progress = (answered / totalQuestions) * 100;
            
            // 진행률 바 업데이트
            document.getElementById('progressBar').style.width = progress + '%';
            
            // 진행률 텍스트 업데이트
            const progressText = document.getElementById('progressText');
            if (progressText) {
                progressText.textContent = answered;
            }
            
            // 제출 버튼 스타일 업데이트
            const submitBtn = form.querySelector('button[type="submit"]');
            if (answered === totalQuestions) {
                submitBtn.classList.remove('opacity-75');
                submitBtn.classList.add('ring-2', 'ring-green-300');
            } else {
                submitBtn.classList.add('opacity-75');
                submitBtn.classList.remove('ring-2', 'ring-green-300');
            }
        }
        
        // 페이지 로드 시 진행률 초기화
        document.addEventListener('DOMContentLoaded', function() {
            updateProgress();
            
            // 모든 라디오 버튼에 이벤트 리스너 추가
            const radios = document.querySelectorAll('input[type="radio"]');
            radios.forEach(radio => {
                radio.addEventListener('change', updateProgress);
            });
            
            // 모든 텍스트 영역의 길이 카운터 초기화
            const textareas = document.querySelectorAll('textarea');
            textareas.forEach(textarea => {
                const countId = textarea.id.replace('question_text_', 'text_count_');
                if (document.getElementById(countId)) {
                    updateTextLength(textarea, countId);
                }
            });
            
            // 폼 제출 전 확인
            document.getElementById('surveyForm').addEventListener('submit', function(e) {
                const checked = document.querySelectorAll('input[type="radio"]:checked').length;
                if (checked < totalQuestions) {
                    if (!confirm('일부 문항에 답변하지 않았습니다. 그래도 제출하시겠습니까?')) {
                        e.preventDefault();
                        return false;
                    }
                } else {
                    if (!confirm('설문을 제출하시겠습니까?')) {
                        e.preventDefault();
                        return false;
                    }
                }
            });
        });
        
        // 모바일에서 스크롤 최적화
        if (window.innerWidth <= 768) {
            document.body.style.overflowX = 'hidden';
        }
    </script>
</body>
</html>


