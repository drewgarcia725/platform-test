
import CaseTable from "./casetable";

const mockCases = [
  {
    id: "1",
    case_number: "C-001",
    client: "Client A",
    payer_name: "Aetna",
    denied_amount: 100,
    status: "new",
    priority: 3,
  },
  {
    id: "2",
    case_number: "C-002",
    client: "Client B",
    payer_name: "BCBS",
    denied_amount: 200,
    status: "approved",
    priority: 2,
  },
  {
    id: "3",
    case_number: "C-003",
    client: "Client A",
    payer_name: "Cigna",
    denied_amount: 150,
    status: "in_review",
    priority: 4,
  },
];

export default function App() {
  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Denial Cases</h1>
      <CaseTable cases={mockCases} />
    </div>
  );
}
