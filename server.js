// server.js
const express = require('express');
const cors = require('cors');
const sgMail = require('@sendgrid/mail');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

if (!process.env.SENDGRID_API_KEY) {
  console.warn('⚠️  SENDGRID_API_KEY missing in .env');
}
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const otpStore = {}; // simple in-memory store

function generateOtp() {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

app.post('/api/send-otp', async (req, res) => {
  try {
    const { email } = req.body;
    if (!email) return res.status(400).json({ success: false, error: 'Email required' });

    const otp = generateOtp();
    otpStore[email] = { otp, expiresAt: Date.now() + 5 * 60 * 1000 };

    const msg = {
      to: email,
      from: process.env.SENDGRID_FROM_EMAIL,
      subject: 'Your SahaYOGI OTP',
      text: `Your OTP is ${otp}. Valid for 5 minutes.`,
    };

    await sgMail.send(msg);
    console.log(`✅ OTP ${otp} sent to ${email}`);
    res.json({ success: true });
  } catch (err) {
    console.error(err.response?.body || err);
    res.status(500).json({ success: false, error: 'SendGrid failed' });
  }
});

app.post('/api/verify-otp', (req, res) => {
  const { email, otp } = req.body;
  const entry = otpStore[email];
  if (!entry) return res.status(400).json({ success: false, error: 'No OTP for this email' });
  if (Date.now() > entry.expiresAt) return res.status(400).json({ success: false, error: 'Expired' });
  if (otp !== entry.otp) return res.status(400).json({ success: false, error: 'Invalid OTP' });

  delete otpStore[email];
  res.json({ success: true });
});

app.get('/', (req, res) => res.send('SahaYOGI OTP backend running'));
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
