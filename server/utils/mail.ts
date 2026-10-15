// Pengiriman email verifikasi via Brevo SMTP.
// Bila kredensial belum diset di .env, link verifikasi di-log ke console server
// supaya alur tetap bisa diuji lokal tanpa kirim email sungguhan.
import nodemailer from 'nodemailer'

const cfg = () => {
  const config = useRuntimeConfig()
  return {
    user: (config.brevoUser as string) || process.env.BREVO_USER || '',
    pass: (config.brevoApiKey as string) || process.env.BREVO_API_KEY || '',
    fromEmail: (config.brevoFromEmail as string) || process.env.BREVO_FROM_EMAIL || 'no-reply@bumdeskalibakung.desa.id',
    fromName: (config.brevoFromName as string) || process.env.BREVO_FROM_NAME || 'BUMDes Desa Kalibakung',
    appUrl: (config.appUrl as string) || process.env.APP_URL || 'http://localhost:3000',
  }
}

export async function sendVerifyEmail(to: string, nama: string, token: string) {
  const { user, pass, fromEmail, fromName, appUrl } = cfg()
  const link = `${appUrl.replace(/\/$/, '')}/verify?token=${encodeURIComponent(token)}`
  const subjek = 'Verifikasi Email — Portal BUMDes Desa Kalibakung'
  const html = `
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;padding:24px;color:#0f172a">
      <h2 style="margin:0 0 12px">Verifikasi Email Anda</h2>
      <p>Halo <b>${nama}</b>,</p>
      <p>Anda mendaftar sebagai pengurus pada sistem BUMDes Desa Kalibakung. Klik tombol di bawah untuk memverifikasi alamat email Anda. Link berlaku <b>24 jam</b>.</p>
      <p style="text-align:center;margin:28px 0">
        <a href="${link}" style="background:#2563eb;color:#fff;text-decoration:none;padding:12px 24px;border-radius:999px;font-weight:600">Verifikasi Email</a>
      </p>
      <p style="font-size:12px;color:#64748b">Jika tombol tidak berfungsi, salin link ini:<br><a href="${link}">${link}</a></p>
    </div>`

  if (!user || !pass) {
    // Mode pengembangan: tampilkan link di console server.
    console.log('\n[DEV-MAIL] Verifikasi email untuk', to)
    console.log('[DEV-MAIL]', link, '\n')
    return { mode: 'console' as const }
  }

  const transporter = nodemailer.createTransport({
    host: 'smtp-relay.brevo.com',
    port: 587,
    secure: false, // TLS
    auth: { user, pass },
  })

  await transporter.sendMail({
    from: `${fromName} <${fromEmail}>`,
    to,
    subject: subjek,
    html,
  })
  return { mode: 'sent' as const }
}
