import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function Dashboard() {
  return (
    <div className="max-w-4xl mx-auto mt-10 space-y-6">
      <h2 className="text-2xl font-bold text-center">Dashboard</h2>

      <Card className="shadow-lg border border-gray-200 dark:border-gray-700">
        <CardHeader>
          <CardTitle>Analisis Sentimen Mobile Legends</CardTitle>
        </CardHeader>
        <CardContent>
          <p>
            Proyek ini bertujuan untuk menganalisis sentimen pengguna terhadap
            game Mobile Legends menggunakan algoritma **Support Vector Machine
            (SVM)**. Dengan memahami sentimen pengguna, kita dapat memberikan
            wawasan berharga bagi pengembang game dan komunitas pemain.
          </p>
        </CardContent>
      </Card>

      <Card className="shadow-lg border border-gray-200 dark:border-gray-700">
        <CardHeader>
          <CardTitle>Metode Pelatihan Model</CardTitle>
        </CardHeader>
        <CardContent>
          <p>
            Salah satu teknik yang digunakan adalah **Sequential Training**, yang
            lebih sederhana dan cepat dibandingkan dengan metode lain seperti
            **Quadratic Programming** dan **Sequential Minimal Optimization
            (SMO)**.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
