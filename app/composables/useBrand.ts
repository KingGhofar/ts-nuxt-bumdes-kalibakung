type Brand = { nama: string, logo: string | null, alamat: string | null }

// Diisi sekali di app.vue; diperbarui setelah Profil BUMDes disimpan.
export const useBrand = () => useState<Brand>('brand', () => ({ nama: 'BUMDes', logo: null, alamat: null }))
