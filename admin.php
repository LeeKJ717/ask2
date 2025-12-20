<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>관리자 로그인</title>
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
<body class="bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-500 min-h-screen flex items-center justify-center py-8 px-4 font-sans">
    <div class="max-w-md w-full">
        <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <!-- 헤더 -->
            <div class="bg-gradient-to-r from-primary-500 to-secondary-500 text-white px-8 py-8 text-center">
                <div class="w-16 h-16 mx-auto mb-4 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                    <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                    </svg>
                </div>
                <h1 class="text-2xl md:text-3xl font-bold mb-2">관리자 로그인</h1>
                <p class="text-primary-100 text-sm">식물성 케톤식 영양강좌 관리 시스템</p>
            </div>
            
            <!-- 로그인 폼 -->
            <div class="p-8">
                <?php if (isset($_GET['error']) && $_GET['error'] == '1'): ?>
                <div class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                    <div class="flex items-center">
                        <svg class="w-5 h-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <p class="text-red-700 text-sm font-medium">아이디 또는 비밀번호가 올바르지 않습니다.</p>
                    </div>
                </div>
                <?php endif; ?>
                
                <form method="POST" action="admin_login.php" class="space-y-6">
                    <!-- 아이디 입력 -->
                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
                            <span class="flex items-center">
                                <svg class="w-4 h-4 mr-1 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                                </svg>
                                아이디
                            </span>
                        </label>
                        <input 
                            type="text" 
                            id="username" 
                            name="username" 
                            required
                            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition-all duration-200"
                            placeholder="관리자 아이디를 입력하세요"
                            autocomplete="username"
                        >
                    </div>
                    
                    <!-- 비밀번호 입력 -->
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                            <span class="flex items-center">
                                <svg class="w-4 h-4 mr-1 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                                </svg>
                                비밀번호
                            </span>
                        </label>
                        <input 
                            type="password" 
                            id="password" 
                            name="password" 
                            required
                            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-200 outline-none transition-all duration-200"
                            placeholder="비밀번호를 입력하세요"
                            autocomplete="current-password"
                        >
                    </div>
                    
                    <!-- 로그인 버튼 -->
                    <button 
                        type="submit"
                        class="w-full bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 text-white font-bold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-primary-300"
                    >
                        <span class="flex items-center justify-center space-x-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path>
                            </svg>
                            <span>로그인</span>
                        </span>
                    </button>
                </form>
                
                <!-- 뒤로가기 링크 -->
                <div class="mt-6 text-center">
                    <a href="index.php" class="text-sm text-gray-500 hover:text-primary-600 transition-colors duration-200 flex items-center justify-center space-x-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                        </svg>
                        <span>설문지로 돌아가기</span>
                    </a>
                </div>
            </div>
        </div>
        
        <!-- 푸터 -->
        <div class="mt-6 text-center">
            <p class="text-white text-xs opacity-75">© 2024 식물성 케톤식 영양강좌. All rights reserved.</p>
        </div>
    </div>
</body>
</html>

