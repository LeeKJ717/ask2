import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { username, password } = req.body;

  // 기본 관리자 계정
  if (username === 'admin' && password === '1234') {
    // 실제로는 JWT 토큰이나 세션 사용
    return res.status(200).json({ success: true });
  }

  return res.status(401).json({ success: false, error: 'Invalid credentials' });
}

