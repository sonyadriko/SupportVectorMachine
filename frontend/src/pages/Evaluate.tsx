import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectTrigger, SelectContent, SelectItem } from "@/components/ui/select";  // Using ShadCN imports
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import axios from 'axios';

const Evaluate = () => {
  const [gamma, setGamma] = useState('');
  const [lambda, setLambda] = useState('');
  const [complexity, setComplexity] = useState('');
  const [testSize, setTestSize] = useState('0.1');
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await axios.get('http://127.0.0.1:5000/api/svm', {
        params: {
          gamma,
          lambda,
          complexity,
          test_size: testSize,
        },
      });
      setResult(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="min-h-screen flex flex-col p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Pengujian</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="gamma" className="block text-sm font-medium">Gamma:</label>
              <Input
                id="gamma"
                type="text"
                value={gamma}
                onChange={(e) => setGamma(e.target.value)}
                required
                className="mt-2 block w-full border border-gray-300 rounded-md p-2"
              />
            </div>

            <div>
              <label htmlFor="lambda" className="block text-sm font-medium">Lambda (C):</label>
              <Input
                id="lambda"
                type="text"
                value={lambda}
                onChange={(e) => setLambda(e.target.value)}
                required
                className="mt-2 block w-full border border-gray-300 rounded-md p-2"
              />
            </div>

            <div>
              <label htmlFor="complexity" className="block text-sm font-medium">Complexity (coef0):</label>
              <Input
                id="complexity"
                type="text"
                value={complexity}
                onChange={(e) => setComplexity(e.target.value)}
                required
                className="mt-2 block w-full border border-gray-300 rounded-md p-2"
              />
            </div>

            <div>
              <label htmlFor="test_size" className="block text-sm font-medium">Data Testing:</label>
              <Select
                value={testSize}
                onValueChange={(value) => setTestSize(value)}
                className="mt-2 block w-full border border-gray-300 rounded-md p-2"
              >
                <SelectTrigger>
                  <span>Data Testing: {testSize * 100}%</span>
                </SelectTrigger>
                <SelectContent>
                  {[...Array(5).keys()].map(i => {
                    const value = (i + 1) / 10;
                    const dataTestingPercentage = value * 100;
                    const dataTrainingPercentage = (1 - value) * 100;
                    return (
                      <SelectItem key={i} value={value.toString()}>
                        Data Testing {dataTestingPercentage}% - Data Training {dataTrainingPercentage}%
                      </SelectItem>
                    );
                  })}
                </SelectContent>
              </Select>
            </div>

            <Button type="submit" className="w-full py-2 px-4 bg-blue-600 text-white rounded-md">
              Submit
            </Button>
          </form>
        </CardContent>
      </Card>

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>Hasil Pengujian</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p>Total data testing yang digunakan: {result.total_data}</p>
            <p>Accuracy: {result.accuracy ? (result.accuracy * 100).toFixed(2) + '%' : 'N/A'}</p>
            <p>TN: {result.tn}</p>
            <p>FP: {result.fp}</p>
            <p>FN: {result.fn}</p>
            <p>TP: {result.tp}</p>
            <p>Precision: {result.precision ? (result.precision * 100).toFixed(2) + '%' : 'N/A'}</p>
            <p>F1 Score: {result.f1_score ? (result.f1_score * 100).toFixed(2) + '%' : 'N/A'}</p>
            <p>Recall: {result.recall ? (result.recall * 100).toFixed(2) + '%' : 'N/A'}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Evaluate;
