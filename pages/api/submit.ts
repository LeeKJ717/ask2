import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { responses, textResponses } = req.body;

  // Vercel은 서버리스 환경이므로 파일 저장이 제한적입니다
  // 실제 운영 시에는 데이터베이스나 Vercel KV 사용 권장
  
  // 임시로 메모리에 저장 (실제로는 데이터베이스 사용)
  const responseData = {
    timestamp: new Date().toISOString(),
    ip_address: req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'unknown',
    responses,
    textResponses,
  };

  // 성공 응답
  return res.status(200).json({ 
    success: true, 
    message: '설문이 성공적으로 제출되었습니다.',
    data: responseData
  });
}

