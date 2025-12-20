import Head from 'next/head';
import Link from 'next/link';

export default function Statistics() {
  return (
    <>
      <Head>
        <title>응답 통계 - 관리자</title>
      </Head>
      
      <div className="min-h-screen bg-gradient-to-br from-[#667eea] via-[#5568d3] to-[#764ba2] py-8 px-4 md:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-2xl shadow-2xl overflow-hidden mb-6">
            <div className="bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white px-8 py-6">
              <h1 className="text-3xl md:text-4xl font-bold mb-2">응답 통계</h1>
              <p className="text-[#e0e9ff]">식물성 케톤식 영양강좌 수요조사 분석</p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <p className="text-gray-600 mb-4">통계 기능은 데이터베이스 연동 후 사용 가능합니다.</p>
            <p className="text-sm text-gray-500 mb-6">
              Vercel은 서버리스 환경이므로 파일 저장이 제한적입니다.<br/>
              데이터베이스(Supabase, MongoDB 등) 연동을 권장합니다.
            </p>
            <Link href="/" className="inline-block bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200">
              설문지로 돌아가기
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}

