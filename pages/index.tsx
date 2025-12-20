import { useState, useEffect } from 'react';
import Head from 'next/head';

interface Question {
  id: number;
  category: string;
  question: string;
  type?: string;
}

interface SurveyData {
  title: string;
  description: string;
  scale: Record<string, string>;
  questions: Question[];
}

export default function Home() {
  const [surveyData, setSurveyData] = useState<SurveyData | null>(null);
  const [loading, setLoading] = useState(true);
  const [responses, setResponses] = useState<Record<number, number>>({});
  const [textResponses, setTextResponses] = useState<Record<number, string>>({});
  const [progress, setProgress] = useState(0);

  // 설문지 데이터 로드
  useEffect(() => {
    fetch('/survey.json')
      .then(res => res.json())
      .then(data => {
        setSurveyData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading survey data:', err);
        setLoading(false);
      });
  }, []);

  if (loading || !surveyData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#667eea] via-[#5568d3] to-[#764ba2] flex items-center justify-center">
        <div className="text-white text-xl">로딩 중...</div>
      </div>
    );
  }

  const questions = surveyData.questions;
  const objectiveQuestions = questions.filter(q => !q.type || q.type !== 'text');
  const totalQuestions = objectiveQuestions.length;

  // 카테고리별로 그룹화
  const questionsByCategory: Record<string, Question[]> = {};
  questions.forEach((question) => {
    const category = question.category;
    if (!questionsByCategory[category]) {
      questionsByCategory[category] = [];
    }
    questionsByCategory[category].push(question);
  });

  useEffect(() => {
    const answered = Object.keys(responses).length;
    setProgress((answered / totalQuestions) * 100);
  }, [responses, totalQuestions]);

  const handleRadioChange = (questionId: number, value: number) => {
    setResponses(prev => ({ ...prev, [questionId]: value }));
  };

  const handleTextChange = (questionId: number, value: string) => {
    setTextResponses(prev => ({ ...prev, [questionId]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const answered = Object.keys(responses).length;
    if (answered < totalQuestions) {
      if (!confirm('일부 문항에 답변하지 않았습니다. 그래도 제출하시겠습니까?')) {
        return;
      }
    }

    try {
      const response = await fetch('/api/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          responses,
          textResponses,
        }),
      });

      if (response.ok) {
        window.location.href = '/submit-success';
      } else {
        alert('제출 중 오류가 발생했습니다.');
      }
    } catch (error) {
      alert('제출 중 오류가 발생했습니다.');
    }
  };

  return (
    <>
      <Head>
        <title>{surveyData.title}</title>
        <meta name="description" content={surveyData.description} />
        <script src="https://cdn.tailwindcss.com"></script>
        <script dangerouslySetInnerHTML={{
          __html: `
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
          `
        }} />
      </Head>
      
      <div className="progress-bar" style={{ width: `${progress}%`, position: 'fixed', top: 0, left: 0, height: '4px', background: 'linear-gradient(to right, #667eea, #764ba2)', zIndex: 1000, transition: 'width 0.3s ease' }}></div>
      
      <div className="min-h-screen bg-gradient-to-br from-[#667eea] via-[#5568d3] to-[#764ba2] py-4 sm:py-8 px-3 sm:px-4 md:px-8">
        <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* 헤더 */}
          <div className="bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white px-4 sm:px-8 py-6 sm:py-10 text-center">
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-2 sm:mb-3 leading-tight">
              {surveyData.title}
            </h1>
            <p className="text-[#e0e9ff] text-xs sm:text-sm md:text-base leading-relaxed px-2">
              {surveyData.description}
            </p>
          </div>

          {/* 메인 컨텐츠 */}
          <div className="p-4 sm:p-6 md:p-10">
            {/* 척도 정보 */}
            <div className="bg-gradient-to-r from-[#f0f4ff] to-purple-50 border-l-4 border-[#667eea] rounded-lg p-4 sm:p-5 mb-6 sm:mb-8 shadow-sm">
              <h3 className="text-base sm:text-lg font-semibold text-gray-800 mb-3 sm:mb-4 flex items-center">
                <svg className="w-5 h-5 mr-2 text-[#667eea] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                평가 척도
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2 sm:gap-3 md:gap-4">
                {Object.entries(surveyData.scale).map(([num, label]) => (
                  <div key={num} className="flex items-center space-x-2 bg-white px-3 sm:px-4 py-2 rounded-full shadow-sm border border-[#e0e9ff] text-sm sm:text-base">
                    <span className="bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white w-6 h-6 sm:w-7 sm:h-7 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">
                      {num}
                    </span>
                    <span className="text-xs sm:text-sm text-gray-700 font-medium">{label}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* 설문 폼 */}
            <form onSubmit={handleSubmit}>
              {Object.entries(questionsByCategory).map(([category, categoryQuestions]) => (
                <div key={category} className="mb-6 sm:mb-10 bg-gradient-to-br from-gray-50 to-[#f0f4ff] rounded-xl p-4 sm:p-6 shadow-md border border-gray-100">
                  <div className="flex items-center mb-4 sm:mb-6 pb-3 sm:pb-4 border-b-2 border-[#667eea]">
                    <div className="bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg mr-2 sm:mr-3 flex-shrink-0">
                      <svg className="w-4 h-4 sm:w-5 sm:h-5 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                      </svg>
                    </div>
                    <h2 className="text-lg sm:text-xl md:text-2xl font-bold text-[#667eea] break-words">{category}</h2>
                  </div>

                  {categoryQuestions.map((question) => {
                    const isTextQuestion = question.type === 'text';
                    
                    return (
                      <div key={question.id} className="mb-4 sm:mb-6 p-4 sm:p-5 bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
                        <div className="mb-3 sm:mb-4">
                          <span className="inline-block bg-[#667eea] text-white text-xs sm:text-sm font-bold px-2 sm:px-3 py-1 rounded-full mr-2 flex-shrink-0">
                            Q{question.id}
                          </span>
                          {isTextQuestion && (
                            <span className="inline-block bg-green-500 text-white text-xs font-bold px-2 py-0.5 rounded mr-2">주관식</span>
                          )}
                          <span className="text-sm sm:text-base md:text-lg text-gray-800 font-medium leading-relaxed">
                            {question.question}
                          </span>
                        </div>

                        {isTextQuestion ? (
                          <div className="mt-4">
                            <textarea
                              name={`question_text_${question.id}`}
                              id={`question_text_${question.id}`}
                              rows={4}
                              maxLength={500}
                              placeholder="의견을 자유롭게 작성해주세요..."
                              value={textResponses[question.id] || ''}
                              onChange={(e) => handleTextChange(question.id, e.target.value)}
                              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-[#667eea] focus:ring-2 focus:ring-[#e0e9ff] outline-none transition-all duration-200 resize-y text-sm sm:text-base"
                            />
                            <div className="flex justify-between items-center mt-2">
                              <p className="text-xs text-gray-500">최대 500자까지 입력 가능합니다.</p>
                              <p className="text-xs text-gray-500">
                                {(textResponses[question.id] || '').length} / 500자
                              </p>
                            </div>
                          </div>
                        ) : (
                          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2 sm:gap-3">
                            {[1, 2, 3, 4, 5].map((num) => (
                              <label
                                key={num}
                                htmlFor={`q${question.id}_${num}`}
                                className="flex items-center space-x-2 sm:space-x-3 p-3 sm:p-4 rounded-lg border-2 border-gray-200 hover:border-[#667eea] hover:bg-[#f0f4ff] active:bg-[#e0e9ff] cursor-pointer transition-all duration-200 group"
                              >
                                <input
                                  type="radio"
                                  id={`q${question.id}_${num}`}
                                  name={`question_${question.id}`}
                                  value={num}
                                  required={!isTextQuestion}
                                  checked={responses[question.id] === num}
                                  onChange={() => handleRadioChange(question.id, num)}
                                  className="w-6 h-6 sm:w-5 sm:h-5 text-[#667eea] focus:ring-2 focus:ring-[#667eea] focus:ring-offset-2 cursor-pointer flex-shrink-0"
                                />
                                <span className="text-sm sm:text-base text-gray-700 group-hover:text-[#667eea] font-medium flex-1">
                                  <span className="font-bold text-[#667eea]">{num}.</span>{' '}
                                  <span className="hidden sm:inline">{surveyData.scale[num.toString()]}</span>
                                  <span className="sm:hidden text-xs">
                                    {surveyData.scale[num.toString()].substring(0, 8)}
                                  </span>
                                </span>
                              </label>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              ))}

              {/* 제출 버튼 */}
              <div className="mt-6 sm:mt-10 pt-6 sm:pt-8 border-t-2 border-gray-200 text-center">
                <div className="mb-3 sm:mb-4 text-sm text-gray-600">
                  {Object.keys(responses).length} / {totalQuestions} 문항 완료
                </div>
                <button
                  type="submit"
                  className="w-full sm:w-auto bg-gradient-to-r from-[#667eea] to-[#764ba2] hover:from-[#5568d3] hover:to-[#6a3d8f] text-white font-bold py-3 sm:py-4 px-8 sm:px-12 rounded-full text-base sm:text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-[#e0e9ff] active:scale-95"
                >
                  <span className="flex items-center justify-center space-x-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <span>설문 제출하기</span>
                  </span>
                </button>
              </div>
            </form>
          </div>

          {/* 관리자 링크 */}
          <div className="text-center py-3 sm:py-4 border-t border-gray-200 bg-gray-50">
            <a href="/admin" className="text-xs text-gray-400 hover:text-gray-600 transition-colors duration-200">
              관리자 페이지
            </a>
          </div>
        </div>
      </div>
    </>
  );
}

