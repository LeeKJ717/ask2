import Head from 'next/head';
import Link from 'next/link';

export default function SubmitSuccess() {
  return (
    <>
      <Head>
        <title>설문 제출 완료</title>
      </Head>
      
      <div className="min-h-screen bg-gradient-to-br from-[#667eea] via-[#5568d3] to-[#764ba2] flex items-center justify-center py-8 px-4">
        <div className="max-w-2xl w-full bg-white rounded-2xl shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-green-400 to-emerald-500 text-white px-8 py-10 text-center">
            <div className="w-20 h-20 mx-auto mb-4 bg-white rounded-full flex items-center justify-center shadow-lg">
              <svg className="w-12 h-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h1 className="text-3xl md:text-4xl font-bold mb-3">설문 제출 완료</h1>
            <p className="text-green-50 text-base md:text-lg">소중한 의견 감사합니다!</p>
            <p className="text-green-50 text-sm md:text-base mt-1">설문 응답이 성공적으로 저장되었습니다.</p>
          </div>

          <div className="p-8 text-center">
            <Link href="/" className="inline-block bg-gradient-to-r from-[#667eea] to-[#764ba2] hover:from-[#5568d3] hover:to-[#6a3d8f] text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200">
              <span className="flex items-center justify-center space-x-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                <span>다시 설문하기</span>
              </span>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}

