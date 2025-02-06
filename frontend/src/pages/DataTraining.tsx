"use client";

import { useEffect, useState, useMemo } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DataTable } from "@/components/ui/data-table"; // Import DataTable
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";

const MySwal = withReactContent(Swal);

interface DataItem {
  rawContent: string;
  status: string;
}

export default function DataTraining() {
  const [data, setData] = useState<DataItem[]>([]);
  const [positifCount, setPositifCount] = useState(0);
  const [negatifCount, setNegatifCount] = useState(0);
  const [searchTerm, setSearchTerm] = useState(""); // State untuk pencarian

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/data_training");
      if (!response.ok) throw new Error("Gagal mengambil data");

      const result = await response.json();
      setData(result.data);
      setPositifCount(result.positif_count);
      setNegatifCount(result.negatif_count);
    } catch (error) {
      MySwal.fire({
        icon: "error",
        title: "Gagal!",
        text: "Gagal mengambil data. Periksa koneksi internet Anda.",
      });
    }
  };

  const deleteExcelFile = async () => {
    MySwal.fire({
      title: "Apakah Anda yakin?",
      text: "File ini tidak dapat dikembalikan!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Ya, hapus!",
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          const response = await fetch("http://127.0.0.1:5000/delete-excel", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fileName: "data_tweet.csv" }),
          });

          const resJson = await response.json();
          if (resJson.success) {
            MySwal.fire("Terhapus!", "File Excel telah dihapus.", "success").then(() =>
              window.location.reload()
            );
          } else {
            throw new Error("Gagal menghapus file");
          }
        } catch (error) {
          MySwal.fire("Gagal!", "Gagal menghapus file.", "error");
        }
      }
    });
  };

  const columns = useMemo(
    () => [
      { accessorKey: "index", header: "No." },
      { accessorKey: "rawContent", header: "Data" },
      { accessorKey: "status", header: "Status" },
    ],
    []
  );

  return (
    <div className="max-w-6xl mx-auto mt-10 space-y-6">
      <h2 className="text-2xl font-bold text-center">Data Training</h2>

      <Card className="shadow-lg border border-gray-200 dark:border-gray-700">
        <CardHeader>
          <CardTitle>Ringkasan Data</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Positif: {positifCount} data</p>
          <p>Negatif: {negatifCount} data</p>
        </CardContent>
      </Card>

      <Card className="shadow-lg border border-gray-200 dark:border-gray-700">
        <CardHeader>
          <CardTitle>Data Training</CardTitle>
        </CardHeader>
        <CardContent>
          <Input
            placeholder="Cari data..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="mb-4"
          />
          <DataTable columns={columns} data={data} searchTerm={searchTerm} />
        </CardContent>
      </Card>

      <Button variant="destructive" onClick={deleteExcelFile}>
        Hapus File Excel
      </Button>
    </div>
  );
}
