import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import { ModeToggle } from "@/components/ui/mode-toggle"; // Tombol dark mode

const navItems = [
  { name: "Dashboard", path: "/" },
  { name: "Data Training", path: "/datatraining" },
  { name: "Preprocessing", path: "/preprocessing" },
  { name: "TF IDF", path: "/tfidf" },
  { name: "SVM", path: "/svm" },
  { name: "Evaluate", path: "/evaluate" },
];

export default function Topbar() {
  const location = useLocation();

  return (
    <nav className="w-full bg-white dark:bg-gray-800 shadow-md p-4 flex justify-between items-center">
      <span className="text-xl font-semibold">SVM</span>
      <div className="flex gap-4">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={cn(
              "px-4 py-2 rounded-md text-sm font-medium",
              location.pathname === item.path
                ? "bg-gray-200 dark:bg-gray-700"
                : "hover:bg-gray-100 dark:hover:bg-gray-700"
            )}
          >
            {item.name}
          </Link>
        ))}
      </div>
      <ModeToggle />
    </nav>
  );
}
